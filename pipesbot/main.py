import nest_asyncio
nest_asyncio.apply()
import discord
import random
import pickle
import time
import os
import pathlib
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# my packages
import Postables

# modules
import creds
import chatgpt_handler
import Pollen.pollen as pollen
import Gas.gas as gas
import Spotify.spotify_search as spotify_search
import messages
import uptime
import postables
import station_db_handler
import birthday_db_handler

# Set up the postables folder
postables_folders_only = postables.return_postables_folders()
# Create the variables using globals()
for folder in postables_folders_only:
    globals()[folder] = Postables.MemeFolder(folder.lower())

# Try to establish connection
print('attempting to establish connection...')
intents = discord.Intents.default()
intents.message_content = True
#client = discord.Client(intents=intents)
flag = False
while flag == False:
    try:
        client = discord.Client(intents=intents)
        flag = True
    except:
        flag = False
        print('   connection failed, trying again...')
        time.sleep(1)
print('connection established!')

# Confirmation that pipes-bot is ready to go
@client.event 
async def on_ready():
    print(f'We have logged in as {client}')

# Start the uptime count
uptime.new_start()

# Start the event loop
@client.event
async def on_message(message):
    
    # Say who and what the message sent was in server terminal
    if message.author == client.user:
        if str(message.content) == '':
            print('  '+str(message.author) + ' sent content')
        else:
            print('  '+str(message.author) + ' sent: "' + str(message.content) + '"')
    else:
        print(str(message.author) + ' sent: "' + str(message.content) + '"')

    # Need to ensure bot does not reply to itself
    if message.author == client.user:
        return
    
    if message.content.startswith('$info'):
        await message.channel.send(messages.msg_info)
        
    if message.content.startswith('$help'):
        await message.channel.send(messages.msg_info)
    
    if message.content.startswith('$update'):
        await message.channel.send(messages.msg_update)
        
    if message.content.startswith('$test'):
        await message.channel.send(message.author.id)
        await message.channel.send(message.channel.id)

    if message.content.startswith('$pipesbot,'):
        msg = message.content.replace('$pipesbot,','')
        await message.channel.send(chatgpt_handler.requestz(msg))
    
    # Uptime command
    if message.content.startswith('$uptime'):
        uptime.new_end()
        await message.channel.send(f'Pipes Bot has been online for {uptime.display_time_difference()}.')
    
    # Pollen count command
    if message.content.startswith('$pollen'):
        try:
            int(pollen.getPollenCount())
            await message.channel.send('The pollen count in Atlanta for the day is ' + str(pollen.getPollenCount()))
        except:
            await message.channel.send(str(pollen.getPollenCount()))
    
    # Birthday
    if '$birthday help' in str(message.content).lower():
        await message.channel.send(messages.msg_birthday)
    elif '$birthday' in str(message.content).lower():
        try:
            year, month, day = birthday_db_handler.return_birthday(str(message.author.id))
            await message.channel.send(f"Your birthday is {month}-{day}-{year}.")
        except:
            await message.channel.send("Your birthday is not in the system.")
    if '$add birthday' in str(message.content).lower():
        try:
            date_list = str(message.content).lower().replace('$add birthday ','').replace('/','-').split('-')
            month, day, year = int(date_list[0]), int(date_list[1]), int(date_list[2])
            if month > 12 or month < 1:
                raise Exception('Invalid Month')
            if day > 31 or day < 1:
                raise Exception('Invalid Day')
            if year > 2022 or year < 1922:
                raise Exception('Invalid Year')
            await message.channel.send(birthday_db_handler.record_birthday(str(message.author.id), str(message.author), year, month, day))
        except:
            await message.channel.send("Unexpected error occured. Format the date as MONTH-DAY-YEAR")
    if '$remove birthday' in str(message.content).lower():
        try:
            await message.channel.send(birthday_db_handler.remove_birthday(str(message.author.id)))
        except:
            await message.channel.send("Unexpected error occured.")
    

    # Gas Station DB commands
    if '$gas help' in str(message.content).lower():
        await message.channel.send(messages.msg_gas_help)
    if '$station add' in str(message.content).lower():
        try:
            station_num = int(str(message.content).lower().replace('$station add ',''))
            await message.channel.send(station_db_handler.record_station(str(message.author), station_num))
        except:
            await message.channel.send("Unexpected error occured")
    if '$station remove' in str(message.content).lower():
        try:
            station_num = int(str(message.content).lower().replace('$station remove ',''))
            await message.channel.send(station_db_handler.remove_station(str(message.author), station_num))
        except:
            await message.channel.send("Unexpected error occured")
    if '$gas stations' in str(message.content).lower():
        stations = station_db_handler.return_stations(str(message.author))
        if len(stations) == 0:
            await message.channel.send("You currently have no GasBuddy stations saved. Use '$gas help' to find out how.")
        else:
            msg = ''
            for code in stations:
                msg += (f"https://www.gasbuddy.com/station/{code}\n")
            await message.channel.send(msg)

    # Gas
    #TODO: add a way to add favorite gas stations per user
    #TODO: add a way to grab gas stations by zip code? 
    #TODO: add a way to grab historicals
    elif message.content.startswith('$gas'):
        if len(str(message.content)) != 4:
            if len(str(message.content).replace('$gas ','')) == 2:
                initials = str((message.content).replace('$gas ','')).upper()
                await message.channel.send(gas.get_gas_msg(initials))
            else:
                state_name = str((message.content).replace('$gas ','')).title()
                await message.channel.send(gas.get_gas_msg(state_name))
        # if these specific users call out $gas
        elif message.author.name == 'Guwop' or message.author.name == 'yamoe':
            await message.channel.send(gas.get_gas_msg('TX'))
        elif message.author.name == 'mal-bon':
            await message.channel.send(gas.get_gas_msg('NC'))
        else:
            await message.channel.send(gas.get_gas_msg('GA'))
        

    """
    if message.content.startswith('$hello'):
        if message.author == 'pipeeeeees#3187' or message.author.name == 'Guwop':
            await message.channel.send('Hello, King!')
        elif message.author.name == 'steebon':
            await message.channel.send('Hello, Loser!')
        else:
            await message.channel.send('Hello, {0.author.mention}').format(message)
    """
    # post from the postables folder
    for sub_folder in postables_folders_only:
        if sub_folder in str(message.content).lower():
            await message.channel.send(file=discord.File(globals()[sub_folder].return_path()))
    
    # Facts
    if 'FACTS' in str(message.content).upper():
        await message.channel.send('Factual statement detected^')
      
    # SHEEEEEESH
    if 'sheeee' in str(message.content).lower():
        await message.channel.send('Major sheesh detected^')
            
    # Spotify Search
    #TODO: Needs refactoring, also threaded API calling to reduce search time
    #TODO: Longer term, figure out how to make other searching tools...
    if message.content.startswith('$spotify '):
        keyword = str(message.content).replace('$spotify ','')
        
        #try:
        mystring = f"""You have requested to search Spotify for playlists containing the keyword '{keyword}'. I will return the top songs that appear the most in those playlists. Please wait while I retrieve that information...\n"""
        await message.channel.send(mystring)
        flag = False
        for i in range(10):
            try:
                await message.channel.send(spotify_search.popular_tracks_based_on_keyword(keyword,19))
                flag = True
            except:
                time.sleep(2)
            if flag == True:
                break
        if flag == False:
            await message.channel.send('An error occurred. Please try again.')
    elif message.content.startswith('$spotify-'):
        try:
            numtimes = int(str(message.content).replace("$spotify-","").split(" ")[0])
            if str(message.content)[9] == ' ':
                keyword = str(message.content)[10:]
            else:
                keyword = str(message.content)[11:]
            
            #try:
            mystring = f"""You have requested to search Spotify for playlists containing the keyword '{keyword}'. I will return the top songs that appear the most in those playlists. Please wait while I retrieve that information...\n"""
            await message.channel.send(mystring)
            flag = False
            for i in range(10):
                try:
                    await message.channel.send(spotify_search.popular_tracks_based_on_keyword(keyword,numtimes))
                    flag = True
                except:
                    time.sleep(2)
                if flag == True:
                    break
            if flag == False:
                await message.channel.send('An error occurred. Please try again.')
        except:
            await message.channel.send('An error occurred. Syntax is wrong.')

"""Happy Birthday Sender"""
scheduler = AsyncIOScheduler()
@scheduler.scheduled_job('cron', hour=21, minute=41)
async def send_message():
    global client
    user_id = 326676188057567232  # Replace this with the user's actual Discord ID
    await client.wait_until_ready()
    user = client.fetch_user(user_id)
    await client.wait_until_ready()
    await user.send("Hello, user!")


client.run(creds.pipesbot_key)

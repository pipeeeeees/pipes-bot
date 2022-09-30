"""
Discord Bot: main.py
Author: pipeeeeees@gmail.com
"""

# packages
import nest_asyncio
nest_asyncio.apply()
import discord
import random
import pickle
import time
import os
import pathlib

# my packages
import KanyeREST
import Postables

# modules
import creds
import Pollen.pollen as pollen
import Gas.gas as gas
import Spotify.spotify_search as spotify_search
import Messages.messages as messages

INTERVALS = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)

def display_time(seconds):
    result = []
    for name, count in INTERVALS:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(int(value), name))
    return ', '.join(result)

def mac_or_windows():
    main_directory = str(pathlib.Path(__file__).parent.resolve())
    if '/' in main_directory:
        return 'MAC'
    else:
        return 'WIN'

def postables_pathfinder():
    if mac_or_windows() == 'MAC':
        return os.listdir(str(pathlib.Path(__file__).parent.resolve()) + '/Postables')
    else:
        return os.listdir(str(pathlib.Path(__file__).parent.resolve()) + '\\Postables')


postables_folders_only = []
for file in postables_pathfinder():
    if '.' in str(file):
        pass
    else:
        postables_folders_only.append(file)
for folder in postables_folders_only:
    globals()[folder] = Postables.MemeFolder(folder.lower())

# check in the terminal if connection has been established
print('attempting to establish connection...')
flag = False
while flag == False:
    try:
        client = discord.Client()
        flag = True
    except:
        flag = False
        print('   connection failed, trying again...')
        time.sleep(1)
print('connection established!')
start = time.time()

# when the bot is ready
@client.event 
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global msg_update
    global msg_info
    global main_directory
    
    # need to ensure bot does not reply to itself
    if message.author == client.user:
        return
    
    # say who and what the message sent was
    print(str(message.author.name) + ' sent: "' + str(message.content) + '"')

    if message.content.startswith('$info'):
        await message.channel.send(messages.msg_info)
        
    if message.content.startswith('$help'):
        await message.channel.send(messages.msg_info)
    
    if message.content.startswith('$update'):
        await message.channel.send(messages.msg_update)
        
    if message.content.startswith('$test'):
        await message.channel.send(message.author)
        
    if message.content.startswith('$uptime'):
        end = time.time()
        uptime = display_time(end - start)
        await message.channel.send(f'Pipes Bot has been online for {uptime}.')
    
    if message.content.startswith('$hello'):
        if message.author.name == 'pipeeeeees' or message.author.name == 'Guwop':
            await message.channel.send('Hello, King!')
        elif message.author.name == 'steebon':
            await message.channel.send('Hello, Loser!')
        else:
            await message.channel.send('Hello, {0.author.mention}').format(message)
    
    for sub_folder in postables_folders_only:
        if sub_folder in str(message.content).lower():
            await message.channel.send(file=discord.File(globals()[sub_folder].return_path()))
            
    if 'FACTS' in str(message.content).upper():
        await message.channel.send('Factual statement detected^')
      
    if 'sheeeee' in str(message.content).lower():
        await message.channel.send('Major sheesh detected^')
            
    if '$kanye' in str(message.content).lower():
        await message.channel.send('"' + KanyeREST.yeezy_quote() + '" - Kanye West')
  
    if message.content.startswith('$spotify '):
        keyword = str(message.content).replace('$spotify ','')
        
        #try:
        mystring = f"""You have requested to search Spotify for playlists containing the keyword '{keyword}'. I will return the top songs that appear the most in those playlists. Please wait while I retrieve that information...\n"""
        await message.channel.send(mystring)
        flag = False
        for i in range(10):
            try:
                await message.channel.send(spotify_search.popular_tracks_based_on_keyword(keyword),19)
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
            keyword = str(message.content).split(" ")[2]
            
            #try:
            mystring = f"""You have requested to search Spotify for playlists containing the keyword '{keyword}'. I will return the top songs that appear the most in those playlists. Please wait while I retrieve that information...\n"""
            await message.channel.send(mystring)
            flag = False
            for i in range(10):
                try:
                    await message.channel.send(spotify_search.popular_tracks_based_on_keyword(keyword),numtimes)
                    flag = True
                except:
                    time.sleep(2)
                if flag == True:
                    break
            if flag == False:
                await message.channel.send('An error occurred. Please try again.')
        except:
            await message.channel.send('An error occurred. Syntax is wrong.')
  
    if message.content.startswith('$pollen'):
        try:
            int(pollen.getPollenCount())
            await message.channel.send('The pollen count in Atlanta for the day is ' + str(pollen.getPollenCount()))
        except:
            await message.channel.send(str(pollen.getPollenCount()))
      
    if message.content.startswith('$gas'):
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

    if message.content.startswith('Wordle '):
        ind = str(message.content).find('/') - 1
        if int(str(message.content)[ind]) == 1:
            await message.channel.send("Cheater Detected^ 🤡")
        elif int(str(message.content)[ind]) == 2:
            await message.channel.send("Nerd Detected^")
        elif str(message.content)[ind] == 'X':
            await message.channel.send("Fuckin dumbass")
            

client.run(creds.pipesbot_key)

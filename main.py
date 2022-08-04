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

# my packages
import KanyeREST
import Postables

# modules
import creds
import pollen
import gas
import spotify_search


msg_update = """
Updates (August 1st, 2022):
- fixed lebron, brady, biden, obama meme posts feature
- re-organized source code

TODO:
- add runtime reporter
- add feature request option
- revamp $info
- add gas plotting
- figure out running things on a schedule
- figure out how to post things to specific channels
"""
msg_info = """
Hello! I am Pipes Bot, a bot created by David H. Pipes as a means to implement useful commands and features on an online platform.

Here is a list of commands:
$update : find out what features have been added or taken away
$uptime : reports how long the bot has been up since last start
$pollen : find out the pollen count in the Atlanta area
Gas commands:
    - $gas : find out what the average gas prices are in the state of Georgia
    - $gas [state-abbreviation] : find average gas prices in any state
$kanye : get a random Kanye quote
$spotify [keyword] : does a spotify search of the top songs with that keyword
Meme commands:
    - $brady
    - $lebron
    - $obama
    - $biden

Pipes Bot also reacts to really great or very bad Wordle scores shared to it. Try it out!
"""

#current_working_directory = r'C:\Users\pipee\Documents\PyProjects\Discord-Bot'
current_working_directory = os.getcwd()

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

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)

def display_time(seconds):
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(int(value), name))
    return ', '.join(result)

# when the bot is ready
@client.event 
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global msg_update
    global msg_info
    global current_working_directory
    
    # say who and what the message sent was
    print(str(message.author.name) + ' sent: "' + str(message.content) + '"')
    # need to ensure bot does not reply to itself
    if message.author == client.user:
        return
    
    if message.content.startswith('$info'):
        await message.channel.send(msg_info)
        
    if message.content.startswith('$help'):
        await message.channel.send(msg_info)
    
    if message.content.startswith('$update'):
        await message.channel.send(msg_update)
        
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
            await message.channel.send('Hello {0.author.mention}').format(message)
                    
    if 'brady' in str(message.content).lower():
        await message.channel.send(file=discord.File(Postables.brady.return_path()))

    if 'biden' in str(message.content).lower():
        await message.channel.send(file=discord.File(Postables.biden.return_path()))
        
    if 'obama' in str(message.content).lower():
        await message.channel.send(file=discord.File(Postables.obama.return_path()))
        
    if 'lebron' in str(message.content).lower():
        await message.channel.send(file=discord.File(Postables.lebron.return_path()))
            
    if 'FACTS' in str(message.content).upper():
        await message.channel.send('Factual statement detected^')
      
    if 'sheeeee' in str(message.content).lower():
        await message.channel.send('Major sheesh detected^')
            
    if '$kanye' in str(message.content).lower():
        await message.channel.send('"' + KanyeREST.yeezyQuote() + '" - Kanye West')
  
    if message.content.startswith('$spotify '):
        keyword = str(message.content).replace('$spotify ','')
        try:
            mystring = f"""You have requested to search Spotify for playlists containing the keyword '{keyword}'. I will return the top songs that appear the most in those playlists. Please wait while I retrieve that information...\n"""
            await message.channel.send(mystring)
            await message.channel.send(spotify_search.popular_tracks_based_on_keyword(keyword))
        except:
            await message.channel.send('An error occurred. Please try again.')
  
    if message.content.startswith('$pollen'):
        try:
            int(pollen.getPollenCount())
            await message.channel.send('The pollen count in Atlanta for the day is ' + str(pollen.getPollenCount()))
        except:
            await message.channel.send(str(pollen.getPollenCount()))
      
    if message.content.startswith('$gas'):
        if len(str(message.content)) != 4:
            if len(str(message.content).replace('$gas','').replace(' ','')) == 2:
                try:
                    initials = str(message.content).replace('$gas','').replace(' ','').upper()
                    reg,mid,prem,die = gas.getGaGasANY(initials)
                    msg = f'Today in {initials}, the average gas prices are:\n\t\tRegular: {reg}\n\t\tMidgrade: {mid}\n\t\tPremium: {prem}\nSource: https://gasprices.aaa.com/?state={initials}'
                    await message.channel.send(msg)
                except:
                    pass
        elif message.author.name == 'Guwop' or message.author.name == 'yamoe':
            reg,mid,prem,die = gas.getGaGasTX()
            msg = 'Today in the state of Texas, the average gas prices are:\n\t\tRegular: {}\n\t\tMidgrade: {}\n\t\tPremium: {}\nSource: https://gasprices.aaa.com/?state=TX'.format(reg,mid,prem)
            await message.channel.send(msg)
        elif message.author.name == 'mal-bon':
            reg,mid,prem,die = gas.getGaGasNC()
            msg = 'Today in the state of North Carolina, the average gas prices are:\n\t\tRegular: {}\n\t\tMidgrade: {}\n\t\tPremium: {}\nSource: https://gasprices.aaa.com/?state=NC'.format(reg,mid,prem)
            await message.channel.send(msg)
        else:
            reg,mid,prem,die = gas.getGaGas()
            msg = 'Today in the state of Georgia, the average gas prices are:\n\t\tRegular: {}\n\t\tMidgrade: {}\n\t\tPremium: {}\nSource: https://gasprices.aaa.com/?state=GA'.format(reg,mid,prem)
            await message.channel.send(msg)

    if message.content.startswith('Wordle '):
        ind = str(message.content).find('/') - 1
        if int(str(message.content)[ind]) == 1:
            await message.channel.send("Cheater Detected^ 🤡")
        elif int(str(message.content)[ind]) == 2:
            await message.channel.send("Nerd Detected^")
        elif str(message.content)[ind] == 'X':
            await message.channel.send("Fuckin dumbass")
            

client.run(creds.pipesbot_key)

"""
Discord Bot: main.py
Desc: this file orchestrates and runs the discord bot
Author: pipeeeeees@gmail.com
"""

import nest_asyncio
nest_asyncio.apply()
import discord
import random
import pickle
import time
import os

from Modules.creds as creds
from Modules.pollen as pollen
from Modules.gas as gas
from Modules.APIs as APIs
from Modules.spotify_search as spotify_search

msg_update = """
Updates (July 25th, 2022):
- fixed lebron, brady, biden, obama meme posts feature
- re-organized source code

TODO:
- add runtime reporter
- add feature request option
- revamp $info
"""
msg_info = """
lol nothing here yet
"""
current_working_directory = os.getcwd()

biden_list = []
brady_list = []
obama_list = []
lebron_list = []

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

# when the bot is ready
@client.event 
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global biden_list
    global brady_list
    global obama_list
    global lebron_list
    global msg_update
    global msg_info
    global current_working_directory
    
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
    
    if message.content.startswith('$hello'):
        if message.author.name == 'pipeeeeees' or message.author.name == 'Guwop':
            await message.channel.send('Hello, King!')
        elif message.author.name == 'steebon':
            await message.channel.send('Hello, Loser!')
        else:
            await message.channel.send('Hello {0.author.mention}').format(message)
                    
    if 'brady' in str(message.content).lower():
        num_brady_pics = len(os.listdir(current_working_directory + '\brady'))
        if len(brady_list) == num_brady_pics:
            brady_list = []
        rand_int = str(random.randrange(0, num_brady_pics))
        while rand_int in brady_list:
            rand_int = str(random.randrange(0, num_brady_pics))
        brady_list.append(rand_int)
        print(brady_list)
        await message.channel.send(file=discord.File(current_working_directory + '\brady\brady' + str(rand_int) + '.jpg'))

    if 'biden' in str(message.content).lower():
        num_biden_pics = len(os.listdir(current_working_directory + '\biden'))
        if len(biden_list) == num_biden_pics:
            biden_list = []
        rand_int = str(random.randrange(0, num_biden_pics))
        while rand_int in biden_list:
            rand_int = str(random.randrange(0, num_biden_pics))
        biden_list.append(rand_int)
        print(biden_list)
        await message.channel.send(file=discord.File(current_working_directory + '\biden\biden' + str(rand_int) + '.jpg'))
        
    if 'obama' in str(message.content).lower():
        num_obama_pics = len(os.listdir(current_working_directory + '\obama'))
        if len(obama_list) == num_obama_pics:
            obama_list = []
        rand_int = str(random.randrange(0, num_obama_pics))
        while rand_int in obama_list:
            rand_int = str(random.randrange(0, num_obama_pics))
        obama_list.append(rand_int)
        print(obama_list)
        await message.channel.send(file=discord.File(current_working_directory + '\obama\obama' + str(rand_int) + '.jpg'))
        
    if 'lebron' in str(message.content).lower():
        num_lebron_pics = len(os.listdir(current_working_directory + '\lebron'))
        if len(lebron_list) == num_lebron_pics:
            await message.channel.send(file=discord.File(current_working_directory + '\lebron\lebron_gif_1.gif'))
            lebron_list = []
        else:
            rand_int = str(random.randrange(0, num_lebron_pics))
            while rand_int in lebron_list:
                rand_int = str(random.randrange(0, num_lebron_pics))
            lebron_list.append(rand_int)
            print(lebron_list)
            await message.channel.send(file=discord.File(current_working_directory + '\lebron\lebron' + str(rand_int) + '.jpg'))
            
    
    
    
    
    if 'FACTS' in str(message.content).upper():
        await message.channel.send('Factual statement detected^')
      
    if 'sheeeee' in str(message.content).lower():
        await message.channel.send('Major sheesh detected^')
            
    if '$kanye' in str(message.content).lower():
        await message.channel.send('"' + APIs.yeezyQuote() + '" - Kanye West')
  
    if message.content.startswith('$spotify '):
        keyword = str(message.content).replace('$spotify ','')
        try:
            mystring = f"""You have requested to search Spotify for the top 50 playlists containing the keyword '{keyword}'. I will return the top 25 songs that appear most in those top 50 playlists. Please wait while I retrieve that information...\n"""
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

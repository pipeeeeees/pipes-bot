import nest_asyncio
nest_asyncio.apply()
import discord
import random

import creds
import pollen
import gas
import APIs

biden_list = []
brady_list = []
obama_list = []
lebron_list = []

# client is our connection to Discord
print('attempting to establish connection...')
flag = False
while flag == False:
    try:
        client = discord.Client()
        flag = True
    except:
        flag = False
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
    
    # need to ensure bot does not reply to itself
    if message.author == client.user:
        return
    

    if message.content.startswith('$info'):
        msg = """
I am Pipes Bot. I am here to provide information and detect key phrases. You can use the following commands:
- $hello: to receive a greeting
- $gas: to return the current average gas price in Georgia
- $pollen: to return the daily pollen count in the Atlanta area
- $kanye: to receive a quote from Kanye West

All feature requests can be made to @pipeeeeees#3187     
        """
        await message.channel.send(msg)
    
    if message.content.startswith('$update'):
        msg = """
Updates:
- Randomized tom brady pics on command

Known bugs:
- $hello not working for some
        """
        await message.channel.send(msg)
    
    
    
    
    if message.content.startswith('$hello'):
        if message.author.name == 'pipeeeeees' or message.author.name == 'Guwop':
            await message.channel.send('Hello, King!')
        elif message.author.name == 'steebon':
            await message.channel.send('Hello, Loser!')
        else:
            await message.channel.send('Hello {0.author.mention}').format(message)
            
            
            
            
            
    if 'brady' in str(message.content).lower():
        num_brady_pics = 14
        if len(brady_list) == num_brady_pics:
            brady_list = []
        rand_int = str(random.randrange(0, num_brady_pics))
        while rand_int in brady_list:
            rand_int = str(random.randrange(0, num_brady_pics))
        brady_list.append(rand_int)
        print(brady_list)
        await message.channel.send(file=discord.File('brady/brady' + str(rand_int) + '.jpg'))

    if 'biden' in str(message.content).lower():
        num_biden_pics = 10
        if len(biden_list) == num_biden_pics:
            biden_list = []
        rand_int = str(random.randrange(0, num_biden_pics))
        while rand_int in biden_list:
            rand_int = str(random.randrange(0, num_biden_pics))
        biden_list.append(rand_int)
        print(biden_list)
        await message.channel.send(file=discord.File('biden/biden' + str(rand_int) + '.jpg'))
        
    if 'obama' in str(message.content).lower():
        num_obama_pics = 8
        if len(obama_list) == num_obama_pics:
            obama_list = []
        rand_int = str(random.randrange(0, num_obama_pics))
        while rand_int in obama_list:
            rand_int = str(random.randrange(0, num_obama_pics))
        obama_list.append(rand_int)
        print(obama_list)
        await message.channel.send(file=discord.File('obama/obama' + str(rand_int) + '.jpg'))
        
    if 'lebron' in str(message.content).lower():
        num_lebron_pics = 4
        if len(lebron_list) == num_lebron_pics:
            lebron_list = []
        rand_int = str(random.randrange(0, num_lebron_pics))
        while rand_int in lebron_list:
            rand_int = str(random.randrange(0, num_lebron_pics))
        lebron_list.append(rand_int)
        print(lebron_list)
        await message.channel.send(file=discord.File('lebron/lebron' + str(rand_int) + '.jpg'))
            
    
    
    if 'penis' in str(message.content).lower():
        await message.channel.send('P-word detected^')

    if 'val' in str(message.content).lower() and '?' in str(message.content).lower():
        await message.channel.send('Valorant loser detected^')
    
    if 'FACTS' in str(message.content).upper():
        await message.channel.send('Factual statement detected^')
      
    if 'sheeeee' in str(message.content).lower():
        await message.channel.send('Major sheesh detected^')
    
    if ' eagles' in str(message.content).lower():
        await message.channel.send('The Philadelphia Eagles. Worst team in the NFL.')
    
    if message.content.startswith('$test'):
        await message.channel.send(message.author)
    
    if message.author.name == 'steebon':
        if 'air fryer' in str(message.content).lower():
            await message.channel.send('Chef Steph back with another air fryer abomination')
            
            
            
            
            
    if 'kanye' in str(message.content).lower():
        await message.channel.send('"' + APIs.yeezyQuote() + '" - Kanye West')
  
  
    if message.content.startswith('$pollen'):
        try:
            int(pollen.getPollenCount())
            await message.channel.send('The pollen count in Atlanta for the day is ' + str(pollen.getPollenCount()))
        except:
            await message.channel.send(str(pollen.getPollenCount()))
        
      
    if message.content.startswith('$gas'):
        if message.author.name == 'Guwop' or message.author.name == 'yamoe':
            reg,mid,prem,die = gas.getGaGasTX()
            msg = 'Today in the state of Texas, the average gas prices are:\n\t\tRegular: {}\n\t\tMidgrade: {}\n\t\tPremium: {}\n\nSource: https://gasprices.aaa.com/?state=TX'.format(reg,mid,prem)
            await message.channel.send(msg)

        else:
            reg,mid,prem,die = gas.getGaGas()
            msg = 'Today in the state of Georgia, the average gas prices are:\n\t\tRegular: {}\n\t\tMidgrade: {}\n\t\tPremium: {}\n\nSource: https://gasprices.aaa.com/?state=GA'.format(reg,mid,prem)
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
import nest_asyncio
nest_asyncio.apply()
import discord
import random

import creds
import pollen
import gas
import APIs

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
        await message.channel.send(file=discord.File('brady/brady' + str(random.randrange(0, 9)) + '.jpg'))

            
    
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
        elif int(str(message.content)[ind]) == 6:
            await message.channel.send("Idiot detected^ ☠️")
            

client.run(creds.pipesbot_key)
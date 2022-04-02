# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 21:38:53 2021

@author: dpipes
"""

import discord
import time
import requests
import os
import pandas as pd
from datetime import date
from keep_alive import keep_alive
import schedule
import pollen

client = discord.Client()
my_secret = os.environ['gas_bot_key']


def historicals():
  writeCSVrow()

schedule.every().day.at("01:00").do(historicals)


# client
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    if message.author.name == 'pipeeeeees' or message.author.name == 'Dave-bon' or message.author.name == 'Guwop-bon':
      await message.channel.send('Hello, King!')
    elif message.author.name == 'steebon':
      await message.channel.send('Hello, Loser!')
    else:
      await message.channel.send('Hello!')

  if 'val?' in str(message.content).lower():
    await message.channel.send('Loser detected^')

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
  
  if message.content.startswith('$pollen'):
    await message.channel.send('The pollen count in Atlanta for the day is ' + str(pollen.getPollenCount()))

keep_alive()
client.run(os.getenv('gas_bot_key'))

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute

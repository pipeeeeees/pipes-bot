#!/usr/bin/env python3
import asyncio
import discord
import os
import signal
import socket
import time

from pipesbot import uptime
from pipesbot import creds
from pipesbot import commit_id_getter
from pipesbot import message_handler
from pipesbot import schedule_messages
from pipesbot import db_handler
from pipesbot import PIPEEEEEES_DISCORD_ID

# Establish a connection
print('attempting to establish connection...')
intents = discord.Intents.all()
hostname = socket.gethostname()
flag = True
# continue trying to establish a connection forever
while flag:
    try:
        client = discord.Client(intents=intents)
        flag = False
    except:
        print('connection failed, trying again...')
        time.sleep(2)
print('connection established!')


# Confirmation that pipes-bot is ready to go in terminal
@client.event 
async def on_ready():
    print(f'We have logged in as {client.user}')

    # Fetch the user object
    user = await client.fetch_user(PIPEEEEEES_DISCORD_ID)
    dm_channel = await user.create_dm()
    await dm_channel.send(f'{client.user} is now online on commit ID {commit_id_getter.get_git_commit_id(os.getcwd())}.\nCurrent hostname: {hostname}\nCurrent directory: {os.getcwd()}')
    
    # Start the MessageScheduler, load messages from the database
    await db_handler.add_reminders_to_scheduler()
    await schedule_messages.scheduler.start()

    # Register the signal handler   
    signal.signal(signal.SIGINT, lambda s, f: asyncio.ensure_future(handle_sigint(s, f)))

# Initialize the MessageScheduler
schedule_messages.scheduler_setup(client)
    
# Start the event loop to handle incoming message
@client.event
async def on_message(message):
    await message_handler.handler(client, message)

# Define a signal handler for when the script is cancelled
async def handle_sigint(signum, frame):
    print("Received SIGINT signal, shutting down...")
    # Fetch the user object
    user = await client.fetch_user(PIPEEEEEES_DISCORD_ID)

    # Send a final message to the user
    dm_channel = await user.create_dm()
    try:
        await dm_channel.send(f"Bot is shutting down. Online for {uptime.display_time_difference()}.")
    except discord.errors.HTTPException as e:
        print(f"Failed to send message: {e}")

    # Log out of Discord and exit the script
    await client.close()
    exit(0)

#client.loop.create_task(start_scheduler())
client.run(creds.pipesbot_key)
import discord
import time
import signal
import asyncio

from pipesbot import uptime
from pipesbot import creds
from pipesbot import message_handler
from pipesbot import schedule_messages
from pipesbot import db_handler
from pipesbot import PIPEEEEEES_DISCORD_ID


# Try to establish connection
print('attempting to establish connection...')
intents = discord.Intents.default()
#intents.message_content = True
flag = True
while flag:
    try:
        client = discord.Client(intents=intents)
        flag = False
    except:
        print('connection failed, trying again...')
        time.sleep(1)
print('connection established!')

# Confirmation that pipes-bot is ready to go in terminal
@client.event 
async def on_ready():
    print(f'We have logged in as {client.user}')

    # Fetch the user object
    user = await client.fetch_user(PIPEEEEEES_DISCORD_ID)

    # Send the initial message to the user
    dm_channel = await user.create_dm()
    await dm_channel.send(f'{client.user} is now online.')

    # Register the signal handler   
    signal.signal(signal.SIGINT, lambda s, f: asyncio.ensure_future(handle_sigint(s, f)))

# Start the uptime count
uptime.new_start()

# Initialize the MessageScheduler
schedule_messages.scheduler_setup(client)
    
# Start the event loop
@client.event
# Handle incoming message
async def on_message(message):
    await message_handler.handler(client, message, schedule_messages.scheduler)

# Start the MessageScheduler in a separate task
async def start_scheduler():
    await db_handler.add_reminders_to_scheduler()
    await schedule_messages.scheduler.start()

# Define a signal handler for when the script is cancelled
async def handle_sigint(signum, frame):
    print("Received SIGINT signal, shutting down...")
    # Fetch the user object
    user = await client.fetch_user(PIPEEEEEES_DISCORD_ID)

    # Send a final message to the user
    dm_channel = await user.create_dm()
    try:
        await dm_channel.send("Bot is shutting down. Goodbye!")
    except discord.errors.HTTPException as e:
        print(f"Failed to send message: {e}")

    # Log out of Discord and exit the script
    await client.close()
    exit(0)

client.loop.create_task(start_scheduler())
client.run(creds.pipesbot_key)
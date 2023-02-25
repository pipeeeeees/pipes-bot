import discord
import time
import creds
from pipesbot import uptime


# Try to establish connection
print('attempting to establish connection...')
intents = discord.Intents.default()
intents.message_content = True
flag = True
while flag:
    try:
        client = discord.Client(intents=intents)
        flag = False
    except:
        print('connection failed, trying again...')
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
    """
    # Access Pipes Bot as a Member object
    pbot = client.user

    # Access the content of the message
    content = message.content

    # Access the author of the message as a Member object
    author = message.author

    # Access the channel where the message was sent as a TextChannel object
    channel = message.channel

    # Access the guild where the message was sent as a Guild object
    guild = message.guild

    # Access the list of Member objects that were mentioned in the message
    mentions = message.mentions

    # Access the list of Attachment objects that were attached to the message
    attachments = message.attachments

    # Access the list of Embed objects that were included in the message
    embeds = message.embeds

    # Access the timestamp of when the message was created as a datetime.datetime object
    created_at = message.created_at

    # Access the timestamp of when the message was last edited as a datetime.datetime object, or None if it was never edited
    edited_at = message.edited_at
    """
    


client.run(creds.pipesbot_key)

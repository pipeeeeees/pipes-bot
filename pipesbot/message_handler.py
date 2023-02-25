from pipesbot import PIPEEEEEES_DISCORD_ID
from pipesbot import schedule_messages
import datetime

async def send_message(client, channel_id, message):
    channel = await client.fetch_channel(channel_id)
    await channel.send(message)

async def handler(client, message, scheduler):
    pbot = client.user
    content = message.content
    author = message.author
    channel = message.channel
    guild = message.guild
    mentions = message.mentions
    attachments = message.attachments
    embeds = message.embeds
    created_at = message.created_at
    edited_at = message.edited_at
    
    # Do not reply to yourself, Pipes Bot!
    if message.author == client.user:
        return
    
    #print(author)
    #print(channel)
    #print(attachments)
    #await send_message(client,channel.id, "yo")

    # "LOL,2023,2,25,1,8,word"
    if message.content.startswith('LOL,'):
        msg = message.content.replace('LOL,','')
        msg_list = msg.split(',')

        date = datetime.date(int(msg_list[0]), int(msg_list[1]), int(msg_list[2]))
        time = datetime.time(int(msg_list[3]), int(msg_list[4])) # 8:00 AM
        channel_id =  channel.id # Replace with the actual channel ID
        message = msg_list[5]
        await scheduler.schedule_message(channel_id, message, date, time)


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
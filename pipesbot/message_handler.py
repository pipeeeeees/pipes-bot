from pipesbot import PIPEEEEEES_DISCORD_ID
from pipesbot import schedule_messages
from pipesbot import db_handler
from pipesbot import gpt_api
from pipesbot import uptime
from pipesbot import pollen
from pipesbot import postables
from pipesbot import gas
from pipesbot import spotify_search
#from pipesbot import postable_content
from pipesbot.postable_content import meme_selector
import discord
import datetime

postables_folders_only = postables.return_postables_folders()
# Create the variables using globals()
for folder in postables_folders_only:
    globals()[folder] = meme_selector.MemeFolder(folder.lower())

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

    # Say who and what the message sent was in server terminal
    if message.author == client.user:
        if str(message.content) == '':
            print(f'  {message.author} sent content to {channel}')
        else:
            print(f'  {message.author} sent to {channel}: "{str(message.content)}"')
    else:
        print(f"{message.author} sent: \"{message.content}\"")
    
    # Do not reply to yourself, Pipes Bot!
    if message.author == client.user:
        return

    if message.content.startswith('$test'):
        await message.channel.send(message.author.id)
        await message.channel.send(message.channel.id)

    if message.content.startswith('$pipesbot,'):
        msg = message.content.replace('$pipesbot,','')
        await message.channel.send(gpt_api.requestz(msg))

    if message.content.startswith('$uptime'):
        await message.channel.send(f'Pipes Bot has been online for {uptime.display_time_difference()}.')
    
    if message.content.startswith('$pollen'):
        try:
            int(pollen.getPollenCount())
            await message.channel.send('The pollen count in Atlanta for the day is ' + str(pollen.getPollenCount()))
        except:
            await message.channel.send(str(pollen.get_atl_pollen_count()))

    # post from the postables folder
    for sub_folder in postables_folders_only:
        if sub_folder in str(message.content).lower():
            await message.channel.send(file=discord.File(globals()[sub_folder].return_path()))


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

    # Manual Schedule
    """
    Format: "$remindme, 9-23-1999, 14:20, get something for Stephen's birthday"
    it will:
       1. add this entry to the database (db_handler.py)
       2. add the request to the scheduler (schedule_messages.py)
    """
    if message.content.startswith('$remindme,'):
        # Parse the data
        msg = message.content.replace('$remindme,','')
        msg_list = msg.split(',')
        raw_date = msg_list[0].replace(' ','')
        raw_date_split = raw_date.split('-')
        raw_time = msg_list[1].replace(' ','')
        raw_time_split = raw_time.split(':')
        joined_string = ','.join(msg_list[2:])

        # Create the right DS's
        date = datetime.date(int(raw_date_split[2]), int(raw_date_split[0]), int(raw_date_split[1]))
        time = datetime.time(int(raw_time_split[0]), int(raw_time_split[1])) 
        channel_id =  channel.id 
        message = joined_string

        # Upload to the scheduler
        await scheduler.schedule_message(channel_id, message, date, time)

        # Upload to the database
        db = db_handler.DatabaseHandler(r'pipesbot/database/messages.db')
        db.add_message(author.id, channel_id, int(raw_date_split[2]), int(raw_date_split[0]), int(raw_date_split[1]), int(raw_time_split[0]), int(raw_time_split[1]), message)
        db.close()
        await send_message(client,channel.id, f"Ok. I will remind you on {date.strftime('%m-%d-%Y')} at {time.strftime('%H:%M')}.")
        return
    
    elif message.content.startswith('$db'):
        db = db_handler.DatabaseHandler(r'pipesbot/database/messages.db')
        if 'me' in str(message.content).lower():
            messages = db.get_all_by_user_id(author.id)
            if len(messages) != 0:
                for message in messages:
                    m_user = await client.fetch_user(message['user_id'])
                    m_channel = client.get_channel(message['channel_id'])
                    print(f"user_id:{m_user.name}, channel_id:{m_channel}, date:{message['month']}-{message['day']}-{message['year']}, time:{message['hour']}:{message['minute']}, message:{message['message']}")
            else:
                print("Nothing here, chief.")
        else:
            messages = db.get_all_instances()
            if len(messages) != 0:
                for message in messages:
                    m_user = await client.fetch_user(message['user_id'])
                    m_channel = client.get_channel(message['channel_id'])
                    print(f"user_id:{m_user.name}, channel_id:{m_channel}, date:{message['month']}-{message['day']}-{message['year']}, time:{message['hour']}:{message['minute']}, message:{message['message']}")
            else:
                print("Nothing here, chief.")
            db.close()
        db.close()
        return
    
    elif message.content.startswith('$sch'):
        messages = schedule_messages.scheduler.scheduled_messages
        if len(messages) != 0:
            for message in messages:
                channel_id = message[0]
                m_channel = client.get_channel(channel_id)
                content = message[1]
                scheduled_time = message[2].strftime('%m-%d-%Y, %H:%M')
                print(f'channel: {m_channel}, time: {scheduled_time}, content: {content}')
        else:
            print("Nothing here, chief.")
        return
    
    if 'FACTS' in str(message.content).upper():
        await message.channel.send('Factual statement detected^')
      
    if 'SHEEE' in str(message.content).upper():
        await message.channel.send('Major sheesh detected^')

    if message.content.startswith('$spotify '):
        keyword = str(message.content).replace('$spotify ','')
        
        #try:
        mystring = f"""You have requested to search Spotify for playlists containing the keyword '{keyword}'. I will return the top songs that appear the most in those playlists. Please wait while I retrieve that information...\n"""
        await message.channel.send(mystring)
        flag = False
        for i in range(10):
            try:
                await message.channel.send(spotify_search.popular_tracks_based_on_keyword(keyword,19))
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
            if str(message.content)[9] == ' ':
                keyword = str(message.content)[10:]
            else:
                keyword = str(message.content)[11:]
            
            #try:
            mystring = f"""You have requested to search Spotify for playlists containing the keyword '{keyword}'. I will return the top songs that appear the most in those playlists. Please wait while I retrieve that information...\n"""
            await message.channel.send(mystring)
            flag = False
            for i in range(10):
                try:
                    await message.channel.send(spotify_search.popular_tracks_based_on_keyword(keyword,numtimes))
                    flag = True
                except:
                    time.sleep(2)
                if flag == True:
                    break
            if flag == False:
                await message.channel.send('An error occurred. Please try again.')
        except:
            await message.channel.send('An error occurred. Syntax is wrong.')

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

"""
#print(author)
#print(channel)
#print(attachments)
#await send_message(client,channel.id, "yo")
"""
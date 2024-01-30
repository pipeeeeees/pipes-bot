from pipesbot import PIPEEEEEES_DISCORD_ID
from pipesbot import STEEBON_ATL_STATION_ID
from pipesbot import schedule_messages
from pipesbot import db_handler
from pipesbot import gpt_api
from pipesbot import uptime
from pipesbot import pollen
from pipesbot import postables
from pipesbot import gas
from pipesbot import spotify_search
from pipesbot import commit_id_getter
from pipesbot import weather
from pipesbot import urban_dict
from pipesbot.postable_content import meme_selector
import os
import discord
import datetime
import subprocess
import pandas as pd
import traceback
import asyncio

postables_folders_only = postables.return_postables_folders()
# Create the variables using globals()
for folder in postables_folders_only:
    globals()[folder] = meme_selector.MemeFolder(folder.lower())

shutup = False

async def send_message(client, channel_id, message):
    channel = await client.fetch_channel(channel_id)
    await channel.send(message)

async def handler(client, message):
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

    if message.author == pbot:
        if str(message.content) == '':
            print(f'  {str(message.author)} sent content to {channel}')
        else:
            print(f'  {str(message.author)} sent to {channel}: "{str(message.content)}"')
    else:
        print(f"{str(message.author)} sent: \"{str(message.content)}\"")
    
    # Do not reply to yourself, Pipes Bot!
    if message.author == pbot:
        return
    
    # `$shutup` command (only for pipeeeeees)
    if message.author.name == 'pipeeeeees' and message.content.startswith('$shutup'):
        global shutup
        if shutup == False:
            shutup = True
            await message.channel.send('Shutting up.')
        else:
            shutup = False
            await message.channel.send('I am no longer shutting up.')
        return
    if shutup == True:
        return
    
    # `$reboot` command
    if message.content.startswith('$reboot'):
        await message.channel.send(f'Rebooting server. Hold on...')
        restart_command = "cd /home/pipeeeeees/pipes-bot && python3 main.py"
        subprocess.run(restart_command, shell=True, check=True)
        exit(0)

    # `$test` command
    if message.content.startswith('$test') and message.author.name == 'pipeeeeees':
        user = await client.fetch_user(PIPEEEEEES_DISCORD_ID)
        dm_channel = await user.create_dm()
        try:
            # 1 print the computer name pipes-bot is running on
            await message.channel.send(f'Computer name: {os.uname()[1]}')


            # 2 check that the morning report message is working
            schedule_messages.morning_report_command()
            await asyncio.sleep(2) 


            # 3 check that the rain plot is working
            #weather.plot_rain()
            #await message.channel.send(file=discord.File(r'pipesbot\plots\forecasted_rain.png'))
            #schedule_messages.clear_rain_plot()
            #db = db_handler.DatabaseHandler(r'pipesbot/database/messages.db')


            # 4 check that the database is working, print all instances
            """
            instances = db.get_all_instances()
            if len(instances) != 0:
                for instance in instances:
                    m_user = await client.fetch_user(instance['user_id'])
                    m_channel = client.get_channel(instance['channel_id'])
                    await message.channel.send(f'user_id:{m_user.name}, channel_id:{m_channel}, date:{instance["month"]}-{instance["day"]}-{instance["year"]}, time:{instance["hour"]}:{instance["minute"]}, message:{instance["message"]}')
            else:
                await message.channel.send("Nothing here, chief.")
            """

            # 5 print the pickle files in pipesbot/pickles
            if schedule_messages.check_gas_prices_historical():
                await dm_channel.send(f'Found gas_prices_ga.pkl....')
                schedule_messages.daily_update_gas_prices()
                gas_prices = schedule_messages.get_gas_prices_historical()
                gas_prices = gas_prices.to_string()
                with open('gas_prices.txt', 'w') as f:
                    f.write(gas_prices)
                await dm_channel.send(file=discord.File(r'gas_prices.txt'))
                os.remove('gas_prices.txt')

            else:
                await dm_channel.send(f'No gas prices found.')
                schedule_messages.create_gas_prices_historical()
                await dm_channel.send(f'Created gas_prices_ga.pkl....')
                reg,mid,prem,die = gas.get_gas('GA')
                schedule_messages.append_gas_prices_historical(reg,mid,prem,die,datetime.datetime.now())
                await dm_channel.send(f'Updated gas_prices_ga.pkl....')
                gas_prices = schedule_messages.get_gas_prices_historical()
                gas_prices = gas_prices.to_string()
                with open('gas_prices.txt', 'w') as f:
                    f.write(gas_prices)
                await dm_channel.send(file=discord.File(r'gas_prices.txt'))
                os.remove('gas_prices.txt')

            # send plot for gas prices
            outcome = schedule_messages.plot_gas_prices_historical(number_of_days=9999, zero_out=True)
            if outcome:
                await dm_channel.send(file=discord.File(schedule_messages.ga_gas_historical_plot_path))
                schedule_messages.clear_gas_prices_historical_plot()
            else:
                await dm_channel.send(f'No gas prices found.')

            # send word of the day to dm
            await dm_channel.send(schedule_messages.word_of_the_day_message())
            

        except Exception as e:
            exception_traceback = traceback.format_exc()
            await dm_channel.send(f'```{e}```\n```{exception_traceback}```')
            #send cwd
            await dm_channel.send(f'```{os.getcwd()}```')
        return
    

    # `$report` command
    if message.content == '$report':
        schedule_messages.morning_report_command(channel_id=channel.id)
    
    if message.content == '$word':
        message_string = ''
        word, definition = urban_dict.random_popular_word()
        if word and definition:
            message_string = message_string + f'The Word is: ```{word}```Definition: ```{definition}```'
        else:
            message_string = message_string + f'Unable to retrieve a word. Please complain to @pipeeeeees'
        await message.channel.send(message_string)
        return

    # `pipesbot, blah blah blah` command
    if message.content.startswith('pipesbot,'): #GPT reply
        msg = message.content.replace('pipesbot,','')
        await message.channel.send(gpt_api.requestz(msg))
        return
    
    # `$pipesbot, blah blah blah` command
    elif message.content.startswith('$pipesbot,'):
        msg = message.content.replace('$pipesbot,','')
        await message.channel.send(gpt_api.requestz(msg))
        return
    
    if message.content.startswith('$gas plot'):
        try:
            num = int(message.content.replace('$gas plot ',''))
            if num > 0 and num < 100:
                outcome = schedule_messages.plot_gas_prices_historical(number_of_days=num, zero_out=False)
                if outcome:
                    await message.channel.send(file=discord.File(schedule_messages.ga_gas_historical_plot_path))
                    schedule_messages.clear_gas_prices_historical_plot()
                else:
                    await message.channel.send(f'Something went wrong... :(')
        except:
            outcome = schedule_messages.plot_gas_prices_historical(number_of_days=9999, zero_out=False)
            if outcome:
                await message.channel.send(file=discord.File(schedule_messages.ga_gas_historical_plot_path))
                schedule_messages.clear_gas_prices_historical_plot()
        return
    
    if message.content.startswith('$gas data'):
        schedule_messages.daily_update_gas_prices()
        gas_prices = schedule_messages.get_gas_prices_historical()
        gas_prices = gas_prices.to_string()
        with open('gas_prices.txt', 'w') as f:
            f.write(gas_prices)
        await message.channel.send(file=discord.File(r'gas_prices.txt'))
        os.remove('gas_prices.txt')
        return
    
    # `$commitid` command
    if message.content.startswith('$commitid'):
        await message.channel.send(f'The commit id I am running on is {commit_id_getter.get_git_commit_id(os.getcwd())}')
        return
    
    # `$uptime` command
    if message.content.startswith('$uptime'):
        await message.channel.send(f'Pipes Bot has been online for {uptime.display_time_difference()}.')
        return
    
    # `$pollen` command
    if message.content.startswith('$pollen'):
        await message.channel.send(pollen.result_handler())
        return
    
    # postables
    for sub_folder in postables_folders_only:
        if sub_folder in str(message.content).lower():
            await message.channel.send(file=discord.File(globals()[sub_folder].return_path()))
            #return

    # `$gas` command   
    if message.content.startswith('$gas'):
        if len(str(message.content)) != 4:
            if len(str(message.content).replace('$gas ','')) == 2:
                initials = str((message.content).replace('$gas ','')).upper()
                await message.channel.send(gas.get_gas_msg(initials))
            else:
                state_name = str((message.content).replace('$gas ','')).title()
                await message.channel.send(gas.get_gas_msg(state_name))
        elif message.author.name == 'yamoe':
            await message.channel.send(gas.get_gas_msg('TX'))
        elif message.author.name == 'Guwop':
            await message.channel.send(gas.get_gas_msg('FL'))
        elif message.author.name == 'mal-bon':
            await message.channel.send(gas.get_gas_msg('NC'))
        else:
            await message.channel.send(gas.get_gas_msg('GA'))
        return

    # Remindme Input (format: '$remindme, 9-23-1999, 14:20, get something for Stephen's birthday')
    if message.content == '$remindme':
        msg = 'To set a reminder, compose a message with the following format (24 hour time):\n\n$remindme, `mm-dd-yyyy`, `hh:mm`, `message` \n\nExample: `$remindme, 9-23-1999, 14:00, tell Steebon Happy Birthday`\n\nSend `$reminders` to see your currently scheduled reminders.'
        await message.channel.send(msg)
        return
    

    if message.content.startswith('$remindme,'):
        # Parse the data
        msg = message.content.replace('$remindme,','')
        msg_list = msg.split(',')
        raw_date = msg_list[0].replace(' ','')
        if '-' in raw_date:
            raw_date_split = raw_date.split('-')
        elif '/' in raw_date:
            raw_date_split = raw_date.split('/')
        raw_time = msg_list[1].replace(' ','')
        raw_time_split = raw_time.split(':')
        joined_string = ','.join(msg_list[2:])

        # Create the right DS's
        date = datetime.date(int(raw_date_split[2]), int(raw_date_split[0]), int(raw_date_split[1]))
        time = datetime.time(int(raw_time_split[0]), int(raw_time_split[1])) 
        channel_id =  channel.id 
        message = joined_string

        # Upload to the scheduler
        await schedule_messages.scheduler.schedule_message(channel_id, str(author.mention) + '' + message, date, time)

        # Upload to the database
        db = db_handler.DatabaseHandler(r'pipesbot/database/messages.db')
        db.add_message(author.id, channel_id, int(raw_date_split[2]), int(raw_date_split[0]), int(raw_date_split[1]), int(raw_time_split[0]), int(raw_time_split[1]), str(author.mention) + '' + message)
        db.close()
        await send_message(client,channel.id, f"Ok. I will remind you on {date.strftime('%m-%d-%Y')} at {time.strftime('%H:%M')}.")
        return
    
    # 
    if message.content.startswith('$birthday'):
        msg = message.content.replace('$birthday','')
        msg_split = msg.split('-')
        month = int(msg_split[0])
        day = int(msg_split[1])
        year = int(msg_split[2])

        # See if bday has passed yet
        now = datetime.datetime.now()
        r_year = now.year
        r_month = now.month
        r_day = now.day
        if r_month < month:
            scheduled = r_year
        elif r_month == month:
            if r_day < day:
                scheduled = r_year
            else:
                scheduled = r_year + 1
        else:
            scheduled = r_year + 1

        # Create the right DS's
        date = datetime.date(scheduled, month, day)
        time = datetime.time(8, 0) 
        channel_id =  channel.id 
        message = f"HAPPY BIRTHDAY, {author.mention}"

        # Upload to the scheduler
        await schedule_messages.scheduler.schedule_message(channel_id, message, date, time)

        # Upload to the database
        db = db_handler.DatabaseHandler(r'pipesbot/database/messages.db')
        db.delete_messages_with_string(author.id, f"HAPPY BIRTHDAY, {author.mention}")
        db.add_message(author.id, channel_id, scheduled, month, day, 8, 0, message)
        # add it for the same day every year for the next 99 years
        for i in range(1,99):
            db.add_message(author.id, channel_id, scheduled + i, month, day, 8, 0, message)
        db.close()
        await send_message(client,channel.id, f"I will wish you a happy birthday on {date.strftime('%m-%d-%Y')}.")
        return
    if message.content.startswith('$reminders'):
        db = db_handler.DatabaseHandler(r'pipesbot/database/messages.db')
        if 'delete' in message.content:
            num = int(message.content.replace('$reminders delete',''))
            await send_message(client,channel.id, db.delete_message_by_number(author.id, num))
        else:
            await send_message(client,channel.id, db.get_numbered_messages(author.id))
        db.close()
        return
    if message.content.startswith('$db'):
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
    if message.content.startswith('$sch'):
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
        msg = "make a robotic message in a few sentences that a robot would say if a factual statement was detected and confirmed. Start the message with 'Factual statement confirmed.'"
        await message.channel.send(gpt_api.requestz(msg).replace('"',''))
        #await message.channel.send('Factual statement detected^')
        return
    
    if message.content == 'false':
        msg = "make a robotic message in a few sentences that a robot would say if a false statement was detected and confirmed false. Start the message with 'False statement confirmed.'"
        await message.channel.send(gpt_api.requestz(msg).replace('"',''))
        #await message.channel.send('Factual statement detected^')
        return
    """
    if 'SHEEEEE' in str(message.content).upper() and 'EEEEESH' in str(message.content).upper():
        msg = "make a short robotic message that a robot would say if a MAJOR SHEEEEESH statement was detected and validated. Start the message with 'Major sheeeeesh detected.'. No emojies"
        await message.channel.send(gpt_api.requestz(msg).replace('"',''))
        #await message.channel.send('Major sheesh detected^')
        return
    
    if 'SHEE' in str(message.content).upper() and 'EESH' in str(message.content).upper():
        msg = "make a short robotic message that a robot would say if a Minor SHEESH statement was detected and to encourage having major sheeeshes only. Start the message with 'Minor sheesh detected.'. No emojies"
        await message.channel.send(gpt_api.requestz(msg).replace('"',''))
        #await message.channel.send('Major sheesh detected^')
        return
    """

    # Spotify keyword search
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
        return
    elif message.content.startswith('$spotify-'):
        try:
            numtimes = int(str(message.content).replace("$spotify-","").split(" ")[0])
            if str(message.content)[9] == ' ':
                keyword = str(message.content)[10:]
            else:
                keyword = str(message.content)[11:]
            
            #try:
            mystring = f"""You have requested to search Spotify for playlists containing the keyword '{keyword}'. I will return ranked list of the songs that appear the most in those playlists. Please wait while I retrieve that information...\n"""
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
        return
    
    if message.author.name == 'GitHub':
        for embed in embeds:
            # extract information from the embed
            embed_title = embed.title
            if 'new commit' in embed_title and os.uname()[1] == 'bytespeed':
                git_pull_command = ["git", "pull"]
                subprocess.run(git_pull_command, cwd="/home/pipeeeeees/pipes-bot", check=True)

                user = await client.fetch_user(PIPEEEEEES_DISCORD_ID)
                dm_channel = await user.create_dm()
                await dm_channel.send(f'New commit detected. Rebooting...')

                restart_command = "cd /home/pipeeeeees/pipes-bot && python3 main.py"
                subprocess.run(restart_command, shell=True, check=True)
                exit(0)
    return

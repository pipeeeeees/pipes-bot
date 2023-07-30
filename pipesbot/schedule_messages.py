import asyncio
import datetime
import time
from pipesbot import db_handler
from pipesbot import pollen
from pipesbot import gas
from pipesbot import PIPEEEEEES_DISCORD_ID
from pipesbot import PIPES_SERVER_GENERAL_ID
from pipesbot import STEEBON_ATL_STATION_ID

class MessageScheduler:
    def __init__(self, client):
        self.client = client
        self.scheduled_messages = []

    async def schedule_message(self, channel_id, message, date, time):
        scheduled_time = datetime.datetime.combine(date, time)
        self.scheduled_messages.append((channel_id, message, scheduled_time))
        
    async def unschedule_message(self, channel_id, message):
        self.scheduled_messages = [(c, m, t) for (c, m, t) in self.scheduled_messages if not (c == channel_id and m == message)]

    async def check_scheduled_messages(self):
        now = datetime.datetime.now()
        for (channel_id, message, scheduled_time) in self.scheduled_messages:
            if now >= scheduled_time:
                channel = await self.client.fetch_channel(channel_id)
                await channel.send(message)
                self.scheduled_messages.remove((channel_id, message, scheduled_time))

    async def morning_report(self):
        message_string = ''

        # Compose the message
        if datetime.date.today().weekday() < 7:#< 5: # 5 for weekdays
            message_string = message_string + f'Good morning! Time for an Atlanta morning report:\n'
            pollen_cnt = pollen.get_atl_pollen_count()
            if type(pollen_cnt) == int:
                message_string = message_string + f' - The pollen count in Atlanta for today is {pollen_cnt}\n'

            
            reg,mid,prem,die = gas.get_gas('GA')
            message_string = message_string + f' - In Georgia, the state-wide average gas prices are:\n\t\tRegular: {reg}\n\t\tMidgrade: {mid}\n\t\tPremium: {prem}'

        # Send checker
        if message_string != '':
            channel = await self.client.fetch_channel(STEEBON_ATL_STATION_ID)
            await channel.send(message_string)
            await asyncio.sleep(60) 


    async def start(self):
        counter = 0
        min_flag = False
        time.sleep(2)
        while True:
            now = datetime.datetime.now()

            # check for reminder messages
            await self.check_scheduled_messages()

            # every day at 9:00 AM
            if now.hour == 10 and now.minute == 0 and min_flag == False:
                min_flag = True
                await self.morning_report()

            # check every n seconds
            n = 30
            await asyncio.sleep(n) 
            counter += 1

            # 5 minute counter 
            if counter >= ((60*5/n) - 1):
                db_handler.clear_old_reminders()
                min_flag = False
                counter = 0

    async def stop(self):
        pass

scheduler = None

def scheduler_setup(client):
    global scheduler
    scheduler = MessageScheduler(client)
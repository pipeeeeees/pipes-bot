import asyncio
import datetime
import time
from pipesbot import db_handler

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

    async def start(self):
        counter = 0
        time.sleep(2)
        while True:
            await self.check_scheduled_messages()

            # Check every 5 seconds
            n = 5
            await asyncio.sleep(n) 
            counter += 1
            if counter >= ((60*5/n) - 1):
                db_handler.clear_old_reminders()

    async def stop(self):
        pass

scheduler = None

def scheduler_setup(client):
    global scheduler
    scheduler = MessageScheduler(client)
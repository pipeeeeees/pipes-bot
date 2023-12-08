import asyncio
import os
import datetime
import discord
import time
import pandas as pd
from pipesbot import db_handler
from pipesbot import pollen
from pipesbot import gas
from pipesbot import PIPEEEEEES_DISCORD_ID
#from pipesbot import PIPES_SERVER_GENERAL_ID
from pipesbot import STEEBON_ATL_STATION_ID
from pipesbot import weather

class MessageScheduler:
    def __init__(self, client):
        self.client = client
        self.scheduled_messages = []

    # Unschedule a message
    async def schedule_message(self, channel_id, message, date, time):
        scheduled_time = datetime.datetime.combine(date, time)
        self.scheduled_messages.append((channel_id, message, scheduled_time))
    
    # Schedule a message
    async def unschedule_message(self, channel_id, message):
        self.scheduled_messages = [(c, m, t) for (c, m, t) in self.scheduled_messages if not (c == channel_id and m == message)]

    # Check scheduled messages
    async def check_scheduled_messages(self):
        now = datetime.datetime.now()
        for (channel_id, message, scheduled_time) in self.scheduled_messages:
            if now >= scheduled_time:
                channel = await self.client.fetch_channel(channel_id)
                await channel.send(message)
                self.scheduled_messages.remove((channel_id, message, scheduled_time))

    # Compose and send the morning report to STEEBON_ATL_STATION_ID
    async def morning_report(self, channel_id=STEEBON_ATL_STATION_ID):
        message_string = ''


        if datetime.date.today().weekday() < 7:
            user = await self.client.fetch_user(PIPEEEEEES_DISCORD_ID)
            dm_channel = await user.create_dm()
            try:
                # ensure no leftover plots remain
                if os.path.exists(r'pipesbot\plots\forecasted_rain.png'):
                    os.remove(r'pipesbot\plots\forecasted_rain.png')
                
                # compose the message
                message_string = message_string + morning_report_message()

                # store gas prices in a pandas dataframe indexed by datetime and store in a pickle file
                if os.path.exists(r'pipesbot\pickles\gas_prices_ga.pkl'):
                    # if it does, load the dataframe
                    gas_prices = pd.read_pickle(r'pipesbot\pickles\gas_prices_ga.pkl')
                    # append the new data
                    reg,mid,prem,die = gas.get_gas('GA')
                    gas_prices.loc[datetime.datetime.now()] = [reg,mid,prem,die]
                    # save the dataframe
                    gas_prices.to_pickle(r'pipesbot\pickles\gas_prices_ga.pkl')
                    await dm_channel.send(f'successfully updated gas_prices_ga.pkl')
                else:
                    # if it doesn't, create a new dataframe and save it
                    reg,mid,prem,die = gas.get_gas('GA')
                    gas_prices = pd.DataFrame([[reg,mid,prem,die]],columns=['Regular','Midgrade','Premium','Diesel'],index=[datetime.datetime.now()])
                    gas_prices.to_pickle(r'pipesbot\pickles\gas_prices_ga.pkl')
                    await dm_channel.send(f'successfully created gas_prices_ga.pkl')
                await dm_channel.send(f'```{gas_prices}```')
            except Exception as e:
                await dm_channel.send(f'```{e}```')

        # Send checker
        if message_string != '':
            channel = await self.client.fetch_channel(channel_id)
            await channel.send(message_string)

            # send potential plot if 'plots\forecasted_rain.png' exists
            if os.path.exists(r'pipesbot\plots\forecasted_rain.png'):
                try:
                    await channel.send(file=discord.File(r'pipesbot\plots\forecasted_rain.png'))
                    time.sleep(15)
                    await channel.send(file=discord.File(r'pipesbot\images\its-gon-rain.jpg'))
                except:
                    pass
                # delete the plot
                os.remove(r'pipesbot\plots\forecasted_rain.png')
            await asyncio.sleep(60) 
        
    # Start the scheduler loop
    async def start(self):
        counter = 0
        min_flag = False
        time.sleep(1)
        while True:
            now = datetime.datetime.now()

            # check for reminder messages
            await self.check_scheduled_messages()

            # every day at 9:00 AM
            if now.hour == 9 and now.minute == 00 and min_flag == False:
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

    # Stop the scheudler loop
    async def stop(self):
        # No urge to implement this yet
        pass

scheduler = None

def scheduler_setup(client):
    global scheduler
    scheduler = MessageScheduler(client)

def morning_report_message(plot=False):
    message_string = ''
    message_string = message_string + f"Good morning! Here is your Atlanta Morning Report for {datetime.datetime.now().strftime('%B %d, %Y')}:"
    
    pollen_cnt = pollen.get_atl_pollen_count()
    if type(pollen_cnt) == int:
        message_string = message_string + f'\n- The pollen count for today is {pollen_cnt} ' + chr(0x1F333)

    # gas
    reg, mid, prem, die = gas.get_gas('GA')
    diff_reg = 0
    diff_mid = 0
    diff_prem = 0
    if os.path.exists(r'pipesbot\pickles\gas_prices_ga.pkl'):
        gas_prices = pd.read_pickle(r'pipesbot\pickles\gas_prices_ga.pkl')
        if len(gas_prices) > 1:
            diff_reg = reg - gas_prices['Regular'].iloc[-1]
            diff_mid = mid - gas_prices['Midgrade'].iloc[-1]
            diff_prem = prem - gas_prices['Premium'].iloc[-1]
            message_string = message_string + f'\n- In Georgia, the state-wide average gas prices are:'
            if diff_reg > 0:
                message_string = message_string + f'\n\t\tRegular: {reg}' + chr(0x2197)
            elif diff_reg < 0:
                message_string = message_string + f'\n\t\tRegular: {reg}' + chr(0x2198)
            else:
                message_string = message_string + f'\n\t\tRegular: {reg}' + chr(0x2192)
            if diff_mid > 0:
                message_string = message_string + f'\n\t\tMidgrade: {mid}' + chr(0x2197)
            elif diff_mid < 0:
                message_string = message_string + f'\n\t\tMidgrade: {mid}' + chr(0x2198)
            else:
                message_string = message_string + f'\n\t\tMidgrade: {mid}' + chr(0x2192)
            if diff_prem > 0:
                message_string = message_string + f'\n\t\tPremium: {prem}' + chr(0x2197)
            elif diff_prem < 0:
                message_string = message_string + f'\n\t\tPremium: {prem}' + chr(0x2198)
            else:
                message_string = message_string + f'\n\t\tPremium: {prem}' + chr(0x2192)
        else:
            message_string = message_string + f'\n- In Georgia, the state-wide average gas prices are:\n\t\tRegular: {reg}\n\t\tMidgrade: {mid}\n\t\tPremium: {prem}'
    else:
        message_string = message_string + f'\n- In Georgia, the state-wide average gas prices are:\n\t\tRegular: {reg}\n\t\tMidgrade: {mid}\n\t\tPremium: {prem}'

    message_string = message_string + weather.real_time_weather_report(plot=True)
    message_string = message_string + f'\n- NOTE: The weather feature is in beta and may not be accurate yet. Please report any issues.'

    return message_string

if __name__ == '__main__':
    print(morning_report_message())
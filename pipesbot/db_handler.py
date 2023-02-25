import sqlite3
import datetime
from pipesbot import schedule_messages
import os

class DatabaseHandler:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def close(self):
        self.conn.close()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                user_id INTEGER,
                channel_id INTEGER,
                year INTEGER,
                month INTEGER,
                day INTEGER,
                hour INTEGER,
                minute INTEGER,
                message TEXT,
                PRIMARY KEY (user_id, channel_id, year, month, day, hour, minute)
            )
        ''')
        self.conn.commit()

    def add_message(self, user_id, channel_id, year, month, day, hour, minute, message):
        self.cursor.execute('''
            INSERT INTO messages (user_id, channel_id, year, month, day, hour, minute, message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, channel_id, year, month, day, hour, minute, message))
        self.conn.commit()

    def remove_message(self, user_id, channel_id, year, month, day, hour, minute):
        self.cursor.execute('''
            DELETE FROM messages
            WHERE user_id = ? AND channel_id = ? AND year = ? AND month = ? AND day = ? AND hour = ? AND minute = ?
        ''', (user_id, channel_id, year, month, day, hour, minute))
        self.conn.commit()
        
    def get_messages(self, user_id, channel_id, year, month, day, hour, minute):
        self.cursor.execute('''
            SELECT message FROM messages
            WHERE user_id = ? AND channel_id = ? AND year = ? AND month = ? AND day = ? AND hour = ? AND minute = ?
        ''', (user_id, channel_id, year, month, day, hour, minute))
        messages = self.cursor.fetchall()
        return messages

    def get_all_instances(self):
        self.cursor.execute("SELECT * FROM messages")
        rows = self.cursor.fetchall()
        
        # Convert each row to a dictionary
        messages = []
        for row in rows:
            message = {
                "user_id": int(row[0]),
                "channel_id": int(row[1]),
                "year": int(row[2]),
                "month": int(row[3]),
                "day": int(row[4]),
                "hour": int(row[5]),
                "minute": int(row[6]),
                "message": row[7]
            }
            messages.append(message)
            
        return messages

    def get_all_by_user_id(self, user_id):
        # Select all rows with matching user_id
        query = "SELECT * FROM messages WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        rows = self.cursor.fetchall()

        # Convert rows to list of dictionaries
        messages = []
        for row in rows:
            message = {
                "user_id": int(row[0]),
                "channel_id": int(row[1]),
                "year": int(row[2]),
                "month": int(row[3]),
                "day": int(row[4]),
                "hour": int(row[5]),
                "minute": int(row[6]),
                "message": row[7]
            }
            messages.append(message)

        return messages

def clear_old_reminders():
    # Get database instance, table instance, and all messages
    db = DatabaseHandler(r'pipesbot/database/messages.db')
    messages = db.get_all_instances()

    # Grab current time
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

    # Remove old reminders
    for rmndr in messages:
        if rmndr["year"] < year:
            db.remove_message(rmndr['user_id'], rmndr['channel_id'], rmndr['year'], rmndr['month'], rmndr['day'], rmndr['hour'], rmndr['minute'])
        elif rmndr["year"] == year:
            if rmndr["month"] < month:
                db.remove_message(rmndr['user_id'], rmndr['channel_id'], rmndr['year'], rmndr['month'], rmndr['day'], rmndr['hour'], rmndr['minute'])
            elif rmndr["month"] == month:
                if rmndr["day"] < day:
                    db.remove_message(rmndr['user_id'], rmndr['channel_id'], rmndr['year'], rmndr['month'], rmndr['day'], rmndr['hour'], rmndr['minute'])
                elif rmndr["day"] == day:
                    if rmndr["hour"] < hour:
                        db.remove_message(rmndr['user_id'], rmndr['channel_id'], rmndr['year'], rmndr['month'], rmndr['day'], rmndr['hour'], rmndr['minute'])
                    elif rmndr["hour"] == hour:
                        if rmndr["minute"] < minute:
                            db.remove_message(rmndr['user_id'], rmndr['channel_id'], rmndr['year'], rmndr['month'], rmndr['day'], rmndr['hour'], rmndr['minute'])

    
    db.close()

async def add_reminders_to_scheduler():
    # Get database instance, table instance, and all messages
    db = DatabaseHandler(r'pipesbot/database/messages.db')
    messages = db.get_all_instances()

    # add to scheduler
    for rmndr in messages:
        date = datetime.date(int(rmndr['year']), int(rmndr['month']), int(rmndr['day']))
        time = datetime.time(int(rmndr['hour']), int(rmndr['minute']))
        channel_id = rmndr['channel_id']
        message = rmndr['message']
        await schedule_messages.scheduler.schedule_message(channel_id, message, date, time)


    db.close()

clear_old_reminders()


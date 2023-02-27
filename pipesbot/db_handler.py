import sqlite3
import datetime
from pipesbot import schedule_messages

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
    
    def delete_messages_with_string(self, user_id, string):
        self.cursor.execute('''
            DELETE FROM messages
            WHERE user_id = ? AND message LIKE ?
        ''', (user_id, f'%{string}%'))
        self.conn.commit()

    def get_numbered_messages(self, user_id):
        messages = self.get_all_by_user_id(user_id)
        numbered_messages = ''
        for i, message in enumerate(messages, 1):
            post_date = datetime.date(message['year'], message['month'], message['day'])
            numbered_messages += f'{i}. {post_date.strftime("%m-%d-%Y")}: {message["message"]}\n'
        return numbered_messages
    
    def delete_message_by_number(self, user_id, number):
        messages = self.get_all_by_user_id(user_id)
        try:
            message = messages[number-1]
        except IndexError:
            return f'No message found with number {number}'
        self.remove_message(user_id, message['channel_id'], message['year'], message['month'], message['day'], message['hour'], message['minute'])
        return f'Deleted message {number}: {message["message"]}'
    
    def message_contains_substring(self, user_id, substring):
        query = "SELECT message FROM messages WHERE user_id = ?"
        self.cursor.execute(query, (user_id))
        rows = self.cursor.fetchall()
        for row in rows:
            if substring in row[0]:
                return True
        return False
    

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
        #print('reminder successfully scheduled')


    db.close()

clear_old_reminders()
#add_reminders_to_scheduler()


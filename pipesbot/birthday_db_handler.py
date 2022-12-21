import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')

# Create a cursor
cursor = conn.cursor()

# Check if the "birthday" table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='birthday'")

# If the "birthday" table does not exist, create it
if not cursor.fetchone():
    cursor.execute('''CREATE TABLE birthday (
                      discord_id TEXT NOT NULL,
                      username TEXT NOT NULL,
                      year INTEGER NOT NULL,
                      month INTEGER NOT NULL,
                      day INTEGER NOT NULL,
                      PRIMARY KEY (username))''')
    print("New 'birthday' table successfully created in the database.db file")

# Commit the changes and close the connection
conn.commit()
conn.close()

def record_birthday(discord_id, username, year, month, day):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        query = "INSERT INTO birthday (discord_id, username, year, month, day) VALUES (?, ?, ?, ?, ?)"
        values = (discord_id, username, year, month, day)

        cursor.execute(query, values)
        conn.commit()
        conn.close()
        return f"Birthday {month}-{day}-{year} has been saved successfully."
    except:
        conn.rollback()
        year, month, day = return_birthday(username)
        return f"A birthday for you already exists: {month}-{day}-{year}. To change, say '$remove birthday' and add again."


def remove_birthday(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = "DELETE FROM birthday WHERE (username) = (?)"
    values = (username,)

    cursor.execute(query, values)
    if cursor.rowcount > 0:
        # If rows were deleted, commit the changes and return "Done"
        conn.commit()
        conn.close()
        return f"Done. Birthday was removed."
    else:
        # If no rows were deleted, roll back the changes and return "Does not exist"
        conn.rollback()
        return "Birthday record does not exist"

def return_birthday(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT year, month, day FROM birthday WHERE username=?', (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result
    #year, month, day = result

def drop_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = "DROP TABLE birthday"
    cursor.execute(query)
    conn.commit()
    conn.close()
    print("birthday table dropped")

if __name__ == '__main__':
    #drop_table()
    #print(record_birthday("pipeeeeees#3187", 1998, 3, 23))
    #print(return_birthdays("pipeeeeees#3187"))
    #print(remove_birthday("pipeeeeees#3187"))
    pass
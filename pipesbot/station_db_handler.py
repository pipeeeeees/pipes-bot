import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')

# Create a cursor
cursor = conn.cursor()

# Check if the "stations" table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stations'")

# If the "stations" table does not exist, create it
if not cursor.fetchone():
    cursor.execute('''CREATE TABLE stations (
                      username TEXT NOT NULL,
                      station_num INTEGER NOT NULL,
                      PRIMARY KEY (username, station_num))''')
    print("New 'station' table successfully created in the database.db file")

# Commit the changes and close the connection
conn.commit()
conn.close()

def record_station(username, station_num):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        query = "INSERT INTO stations (username, station_num) VALUES (?, ?)"
        values = (username, station_num)

        cursor.execute(query, values)
        conn.commit()
        conn.close()
        return f"GasBuddy station number {station_num} has been saved successfully to user {username}."
    except sqlite3.IntegrityError:
        conn.rollback()
        return f"A record for {username} and station number {station_num} already exists."
    except:
        conn.rollback()
        return "Unexpected error occured..."

def remove_station(username, station_num):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = "DELETE FROM stations WHERE (username, station_num) = (?, ?)"
    values = (username, station_num)

    cursor.execute(query, values)
    if cursor.rowcount > 0:
        # If rows were deleted, commit the changes and return "Done"
        conn.commit()
        conn.close()
        return f"Done. Station number {station_num} was removed."
    else:
        # If no rows were deleted, roll back the changes and return "Does not exist"
        conn.rollback()
        return "Record does not exist"

def return_stations(username):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = "SELECT station_num FROM stations WHERE username = ?"

    # Define the value for the WHERE clause
    value = username

    cursor.execute(query, (value,))
    rows = cursor.fetchall()
    stations = [row[0] for row in rows]
    conn.close()
    return stations

def drop_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = "DROP TABLE stations"
    cursor.execute(query)
    conn.commit()
    conn.close()
    print("Stations table dropped")

if __name__ == '__main__':
    #drop_table()
    print(record_station("pipeeeeees#3187", 25360))
    print(record_station("pipeeeeees#3187", 71747))
    #print(return_stations("pipeeeeees#3187"))
    #print(remove_station("pipeeeeees#3187", 25360))
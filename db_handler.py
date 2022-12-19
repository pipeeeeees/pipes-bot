import sqlite3

# Connect to the database
conn = sqlite3.connect("database.db")

# Create a cursor
cursor = conn.cursor()

# Execute an SQL statement
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")

# Commit the changes
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()
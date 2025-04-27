import sqlite3

# Connect to (or create) external_user.db in the same folder
conn = sqlite3.connect('external_user.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS external_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

print("external_user.db created and ready!")

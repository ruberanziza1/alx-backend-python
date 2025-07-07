# 0-databaseconnection.py

import sqlite3

DATABASE_NAME = 'users.db'

class DatabaseConnection:
    """
    Custom class-based context manager for handling SQLite database connections.
    Automatically opens the connection on __enter__ and closes it on __exit__.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # This will be assigned to the variable after 'as'

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

# --- Setup: Ensure table and data exist ---
conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
''')
cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com')")
conn.commit()
conn.close()

# --- Use the custom context manager to fetch data ---
with DatabaseConnection(DATABASE_NAME) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(user)


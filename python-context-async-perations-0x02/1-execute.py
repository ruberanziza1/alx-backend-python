# 1-execute.py

import sqlite3

DATABASE_NAME = 'users.db'

class ExecuteQuery:
    """
    Custom context manager that manages both the database connection
    and execution of a given SQL query with optional parameters.
    """
    def __init__(self, query, params=None):
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

# --- Setup: Create table and dummy data ---
conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER
    )
''')
cursor.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (1, 'Alice', 'alice@example.com', 30)")
cursor.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (2, 'Bob', 'bob@example.com', 22)")
cursor.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (3, 'Charlie', 'charlie@example.com', 28)")
conn.commit()
conn.close()

# --- Use the context manager to fetch users older than 25 ---
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query, params) as results:
    for row in results:
        print(row)


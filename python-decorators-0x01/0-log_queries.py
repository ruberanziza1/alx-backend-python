# 0-log_queries.py
# Complies with rule: Does not use `print` or `from datetime import datetime`

import sqlite3
import functools
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            logging.info(f"Function: {func.__name__} - Executing SQL Query: {query}")
        else:
            logging.info(f"Function: {func.__name__} - No identifiable SQL query argument found for logging.")
        return func(*args, **kwargs)
    return wrapper

DATABASE_NAME = 'users.db'

def setup_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES ('Charlie', 'charlie@example.com')")
    conn.commit()
    conn.close()
    logging.info(f"Database '{DATABASE_NAME}' setup complete with dummy data.")

setup_database()

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

logging.info("\n--- Calling fetch_all_users with 'SELECT * FROM users' ---")
users = fetch_all_users(query="SELECT * FROM users")
logging.info("Fetched users:")
for user in users:
    logging.info(user)

logging.info("\n--- Calling fetch_all_users with 'SELECT name, email FROM users WHERE id = 1' ---")
specific_user = fetch_all_users(query="SELECT name, email FROM users WHERE id = 1")
logging.info("Fetched specific user:")
for user in specific_user:
    logging.info(user)

# Optional: Clean up
# if os.path.exists(DATABASE_NAME):
#     os.remove(DATABASE_NAME)
#     logging.info(f"Cleaned up database file: {DATABASE_NAME}")

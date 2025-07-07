# 3-retry_on_failure.py

import time
import sqlite3
import functools

DATABASE_NAME = 'users.db'

def with_db_connection(func):
    """
    Decorator to manage a SQLite database connection.
    Passes the connection object to the wrapped function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DATABASE_NAME)
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries a function if it raises an exception.
    Retries the specified number of times, waiting 'delay' seconds between attempts.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt >= retries:
                        raise e  # Re-raise the last exception
                    time.sleep(delay)
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# --- Example usage and test setup ---
if __name__ == "__main__":
    # Ensure the database and table exist
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

    # Try fetching users with retry logic
    try:
        users = fetch_users_with_retry()
        print(users)
    except Exception as e:
        print("Failed to fetch users after retries:", e)


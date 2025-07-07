# 1-with_db_connection.py

import sqlite3
import functools

DATABASE_NAME = 'users.db'

def with_db_connection(func):
    """
    Decorator to handle opening and closing a SQLite database connection.
    It injects the connection object as the first argument to the decorated function.
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

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Example usage
if __name__ == "__main__":
    # Ensure the database and table exist for this example
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

    user = get_user_by_id(user_id=1)
    print(user)


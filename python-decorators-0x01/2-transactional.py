# 2-transactional.py

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

def transactional(func):
    """
    Decorator to manage database transactions.
    Commits the transaction if the function executes successfully,
    otherwise rolls back if an exception occurs.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Example usage and setup for testing
if __name__ == "__main__":
    # Ensure the users table exists and user with ID 1 exists
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

    # Run the transaction-protected update
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')

    # Confirm the update
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = 1")
    print(cursor.fetchone())
    conn.close()


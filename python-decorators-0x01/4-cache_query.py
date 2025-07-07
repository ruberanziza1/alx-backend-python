# 4-cache_query.py

import time
import sqlite3
import functools

DATABASE_NAME = 'users.db'
query_cache = {}

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

def cache_query(func):
    """
    Decorator that caches the result of a query using the SQL string as key.
    Avoids redundant DB calls for the same query.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Look for 'query' in kwargs, or assume it's the second argument
        query = kwargs.get("query")
        if not query and len(args) > 1:
            query = args[1]

        if query in query_cache:
            print("Returning cached result for query:", query)
            return query_cache[query]

        result = func(*args, **kwargs)
        query_cache[query] = result
        print("Query executed and cached:", query)
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Setup: Create table and seed data if needed
if __name__ == "__main__":
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

    # First call will execute and cache
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call will use cache
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)


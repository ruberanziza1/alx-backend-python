import sqlite3
import functools
import os # Import os for file cleanup
import logging # Import the logging module

# Configure basic logging to output to console with a timestamp
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#### decorator to log SQL queries
def log_queries(func):
    """
    Decorator to log the SQL query before executing the decorated function.
    This decorator assumes the SQL query is passed as the first positional
    argument or as a keyword argument named 'query'.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = None
        # Try to find the query in keyword arguments first
        if 'query' in kwargs:
            query = kwargs['query']
        # If not in kwargs, check positional arguments
        elif args:
            # Assuming the first positional argument is the query string
            query = args[0]

        if query:
            logging.info(f"Function: {func.__name__} - Executing SQL Query: {query}")
        else:
            logging.info(f"Function: {func.__name__} - No identifiable SQL query argument found for logging.")

        # Execute the original function with its arguments
        return func(*args, **kwargs)
    return wrapper

# --- Database Setup for Demonstration ---
DATABASE_NAME = 'users.db'

def setup_database():
    """
    Creates the users.db database and the users table if they don't exist.
    Inserts some dummy data for testing.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()

    # Insert dummy data if table is empty
    cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES ('Charlie', 'charlie@example.com')")
    conn.commit()
    conn.close()
    logging.info(f"Database '{DATABASE_NAME}' setup complete with dummy data.")

# Ensure the database is set up before running the decorated function
setup_database()

# --- Decorated Function ---
@log_queries
def fetch_all_users(query):
    """
    Connects to the database, executes the provided query, and returns results.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results] # Convert rows to dictionaries for easier viewing

#### fetch users while logging the query
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

# --- Clean up the database file after demonstration (optional) ---
# Uncomment the following lines if you want the database file to be removed
# after each run of this script.
# if os.path.exists(DATABASE_NAME):
#     os.remove(DATABASE_NAME)
#     logging.info(f"\nCleaned up database file: {DATABASE_NAME}")

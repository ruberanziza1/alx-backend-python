import mysql.connector
import sys

# Attempt to import database connection details from seed.py
try:
    from seed import DB_CONFIG, DATABASE_NAME, TABLE_NAME
except ImportError:
    print("Error: seed.py not found or database configuration not exported.")
    print("Please ensure seed.py exists and exports DB_CONFIG, DATABASE_NAME, TABLE_NAME.")
    sys.exit(1)

def stream_users():
    """
    A generator function that streams rows one by one from the user_data table.
    It connects to the ALX_prodev database and yields each row as a dictionary.
    """
    connection = None
    cursor = None
    try:
        # Establish connection to the specific database
        db_config_with_db = DB_CONFIG.copy()
        db_config_with_db['database'] = DATABASE_NAME
        connection = mysql.connector.connect(**db_config_with_db)

        # Use dictionary=True to fetch rows as dictionaries, which is more readable
        cursor = connection.cursor(dictionary=True)

        # Execute the query to select all users
        query = f"SELECT user_id, name, email, age FROM {TABLE_NAME}"
        cursor.execute(query)

        # Fetch one row at a time and yield it
        # This loop is the ONLY loop allowed as per instructions.
        while True:
            row = cursor.fetchone()
            if row is None:
                break  # No more rows to fetch
            yield row # Yield the current row
    except mysql.connector.Error as err:
        print(f"Error streaming users: {err}")
    finally:
        # Ensure the cursor and connection are closed even if an error occurs
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

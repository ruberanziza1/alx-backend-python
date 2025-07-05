import mysql.connector
import sys

# Attempt to import database connection details from seed.py
try:
    from seed import DB_CONFIG, DATABASE_NAME, TABLE_NAME
except ImportError:
    print("Error: seed.py not found or database configuration not exported.", file=sys.stderr)
    print("Please ensure seed.py exists and exports DB_CONFIG, DATABASE_NAME, TABLE_NAME.", file=sys.stderr)
    sys.exit(1)

def stream_users_in_batches(batch_size):
    """
    A generator function that fetches rows from the user_data table in batches.
    Each yielded item is a list of user dictionaries (a batch).
    """
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("batch_size must be a positive integer.")

    connection = None
    cursor = None
    try:
        # Establish connection to the specific database
        db_config_with_db = DB_CONFIG.copy()
        db_config_with_db['database'] = DATABASE_NAME
        connection = mysql.connector.connect(**db_config_with_db)

        # Use dictionary=True to fetch rows as dictionaries
        cursor = connection.cursor(dictionary=True)

        # Execute the query to select all users
        query = f"SELECT user_id, name, email, age FROM {TABLE_NAME}"
        cursor.execute(query)

        # Loop 1: This loop fetches batches of rows
        while True:
            # fetchmany(batch_size) retrieves the specified number of rows
            batch = cursor.fetchmany(batch_size)
            if not batch: # If batch is empty, no more rows
                break
            yield batch # Yield the entire batch (list of dictionaries)
    except mysql.connector.Error as err:
        print(f"Error streaming users in batches: {err}", file=sys.stderr)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def batch_processing(batch_size):
    """
    Processes each batch of users to filter those over the age of 25.
    This function acts as a consumer for the stream_users_in_batches generator.
    It prints each filtered user.
    """
    # Loop 2: This loop iterates over the batches yielded by stream_users_in_batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 3: This loop iterates over individual users within each batch
        for user in batch:
            if user.get('age') > 25:
                # print to stdout, as per the main script's piping to head
                print(user)

import mysql.connector
import sys

# Attempt to import database connection details from seed.py
try:
    from seed import DB_CONFIG, DATABASE_NAME, TABLE_NAME
except ImportError:
    print("Error: seed.py not found or database configuration not exported.", file=sys.stderr)
    print("Please ensure seed.py exists and exports DB_CONFIG, DATABASE_NAME, TABLE_NAME.", file=sys.stderr)
    sys.exit(1)

def stream_user_ages():
    """
    A generator function that yields user ages one by one from the user_data table.
    This is the first of the two allowed loops.
    """
    connection = None
    cursor = None
    try:
        db_config_with_db = DB_CONFIG.copy()
        db_config_with_db['database'] = DATABASE_NAME
        connection = mysql.connector.connect(**db_config_with_db)
        cursor = connection.cursor(dictionary=True) # Fetch as dictionary to easily access 'age'

        # Select only the 'age' column for efficiency
        query = f"SELECT age FROM {TABLE_NAME}"
        cursor.execute(query)

        # Loop 1: Fetches ages one by one
        while True:
            row = cursor.fetchone()
            if row is None:
                break # No more ages to fetch
            yield int(row['age']) # Yield the age as an integer
    except mysql.connector.Error as err:
        print(f"Error streaming user ages: {err}", file=sys.stderr)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def calculate_average_age_from_stream():
    """
    Calculates the average age of users by consuming the stream_user_ages generator.
    This function processes ages without loading the entire dataset into memory.
    This contains the second of the two allowed loops.
    """
    total_age = 0
    count = 0

    # Loop 2: Iterates over the ages yielded by the generator
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}") # Format to 2 decimal places
    else:
        print("No user data found to calculate average age.")

if __name__ == "__main__":
    calculate_average_age_from_stream()

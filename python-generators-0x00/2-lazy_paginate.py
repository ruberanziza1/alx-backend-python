import mysql.connector
import sys

# Attempt to import database connection details from seed.py
try:
    from seed import DB_CONFIG, DATABASE_NAME, TABLE_NAME
except ImportError:
    print("Error: seed.py not found or database configuration not exported.", file=sys.stderr)
    print("Please ensure seed.py exists and exports DB_CONFIG, DATABASE_NAME, TABLE_NAME.", file=sys.stderr)
    sys.exit(1)

def paginate_users(page_size, offset):
    """
    Helper function to fetch a single page of user data from the database.
    This function connects, fetches, and closes the connection for each call.
    """
    connection = None
    cursor = None
    rows = []
    try:
        db_config_with_db = DB_CONFIG.copy()
        db_config_with_db['database'] = DATABASE_NAME
        connection = mysql.connector.connect(**db_config_with_db)
        cursor = connection.cursor(dictionary=True)
        # Ensure the table name is correctly used for the query, adhering to common checks
        cursor.execute(f"SELECT * FROM {TABLE_NAME} LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching page from database: {err}", file=sys.stderr)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
    return rows

def lazy_pagination(page_size):
    """
    A generator function that lazily loads paginated user data from the database.
    It fetches pages one by one as requested by iterating over the generator.
    """
    if not isinstance(page_size, int) or page_size <= 0:
        raise ValueError("page_size must be a positive integer.")

    offset = 0
    # This is the single loop allowed.
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break  # No more data to fetch, exit the loop
        yield page  # Yield the entire page (list of user dictionaries)
        offset += page_size # Increment offset for the next page

# Import the psycopg2 library to manage PostgreSQL database interactions
import psycopg2

# ================================
# Define database connection parameters; replace placeholders with actual values.
SERVER_ADDRESS = "<your_server_address>"  # Add server URL here
DATABASE_NAME = "<database_name>"         # Add database name here
USER_NAME = "<username>"                  # Add username here
PASSWORD = "<password>"                   # Add password here

# ================================
# Reconnect and create a cursor for executing SQL queries

try:
    # Re-establish connection to continue with queries
    db = psycopg2.connect(
        host=SERVER_ADDRESS,
        database=DATABASE_NAME,
        user=USER_NAME,
        password=PASSWORD
    )
    # Create a cursor object to execute SQL queries
    cursor = db.cursor()
except Exception as e:
    print(f"Error creating cursor: {e}")

# ================================
# Example query to retrieve basic information
query = """
SELECT category_name, headline
    FROM headlines
    INNER JOIN categories ON (headlines.category_id = categories.category_id)
    LIMIT 10;
"""

# Execute the query and fetch results
try:
    cursor.execute(query)
    results = cursor.fetchall()  # Retrieve all results from the executed query
    
    # Display each result
    for row in results:
        print(row)

except Exception as e:
    print(f"Error executing query: {e}")

# ================================
# More advanced query with multiple joins and filtering
advanced_query = """
SELECT category_name, headline, summary, headlines.summary_id
    FROM headlines
    INNER JOIN categories ON (headlines.category_id = categories.category_id)
    INNER JOIN summaries ON (headlines.summary_id = summaries.summary_id)
    WHERE headlines.summary_id != %s
    LIMIT 10;
"""

# Define parameterized values
excluded_summary_id = "<id_number>"  # Adjust as needed

# Execute the advanced query
try:
    cursor.execute(advanced_query, (excluded_summary_id,))
    advanced_results = cursor.fetchall()

    # Display each result
    for row in advanced_results:
        print(row)

except Exception as e:
    print(f"Error executing advanced query: {e}")

# ================================
# Close the cursor and database connection when done

finally:
    if cursor:
        cursor.close()
    if db:
        db.close()
    print("Database connection closed.")

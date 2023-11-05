import psycopg2

def ping_postgres(host, port, user, password, database):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        # Create a cursor object
        cur = conn.cursor()

        # Execute a simple query (in this case, we'll use SELECT 1)
        cur.execute('SELECT 1')

        # Fetch the result
        result = cur.fetchone()

        # Check if the result is as expected
        if result[0] == 1:
            print("Ping successful!")
        else:
            print("Ping failed. Unexpected result.")

        # Close the cursor and connection
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

# Usage
ping_postgres(
    host='localhost',
    port='5432',
    user='postgres',
    password='anypass',
    database='data_cloud'
)
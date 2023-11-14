import psycopg2

def ping_postgres(pg_connection: psycopg2.connection) -> None:
    try:
        # Create a cursor object
        cur = pg_connection.cursor()

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
        pg_connection.close()

    except Exception as e:
        print(f"Error: {e}")


def main():
    from postgres_connector import pg_connection
    ping_postgres(pg_connection)

if __name__ == "__main__":
    main()
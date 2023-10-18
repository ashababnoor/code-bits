import mysql.connector
import psycopg2

# Connect to the MySQL source database
mysql_conn = mysql.connector.connect(
    host="source_host",
    user="source_user",
    password="source_password",
    database="source_database"
)

# Connect to the PostgreSQL destination database
postgres_conn = psycopg2.connect(
    host="destination_host",
    user="destination_user",
    password="destination_password",
    database="destination_database"
)

# Create a cursor for the MySQL source database
mysql_cursor = mysql_conn.cursor()

# Create a cursor for the PostgreSQL destination database
postgres_cursor = postgres_conn.cursor()

# Define the SQL query to extract data from the MySQL source
mysql_query = "SELECT * FROM source_table"

# Execute the SQL query on the MySQL source
mysql_cursor.execute(mysql_query)

# Fetch all the rows from the MySQL source
rows = mysql_cursor.fetchall()

# Define the SQL query to insert data into the PostgreSQL destination
postgres_query = "INSERT INTO destination_table (column1, column2, column3) VALUES (%s, %s, %s)"

# Iterate through the rows and insert them into the PostgreSQL destination
for row in rows:
    postgres_cursor.execute(postgres_query, row)

# Commit the changes to the PostgreSQL destination
postgres_conn.commit()

# Close the cursors and connections
mysql_cursor.close()
postgres_cursor.close()
mysql_conn.close()
postgres_conn.close()
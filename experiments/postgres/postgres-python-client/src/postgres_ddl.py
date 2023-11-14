from postgres_connector import pg_connection

def create_table(pg_connection, table_name: str, columns: list[str], data_types: dict[str]={}, properties: dict[str]={}):
        # Create a cursor object
        cursor = pg_connection.cursor()

        # Define the SQL statement to create the table
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} "
        
        create_table_query += "(\n"
        for column in columns:
            if column == columns[-1]:
                create_table_query += f"\t {column} {data_types.get(column, '')} {properties.get(column, '')} \n"
            else:
                create_table_query += f"\t {column} {data_types.get(column, '')} {properties.get(column, '')}, \n"
        create_table_query += ")"
        
        print("Query:")
        print(create_table_query)
        
        # Execute the SQL statement
        cursor.execute(create_table_query)

        # Commit the transaction
        pg_connection.commit()

        # Close the cursor and connection
        cursor.close()
        pg_connection.close()

        print("Table created successfully!")
        


def main():
    table_name = "demo_table"
    columns = ["id", "name", "age"]
    data_types = dict(
        id="int",
        name="varchar(50)",
        age="float", 
    )
    properties = dict(
        id="primary key"
    )

    create_table(pg_connection, table_name=table_name, columns=columns, data_types=data_types, properties=properties)

if __name__ == "__main__":
    main()
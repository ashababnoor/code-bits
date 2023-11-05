import psycopg2

pg_connection = conn = psycopg2.connect(
    host='localhost',
    port='5432',
    user='postgres',
    password='anypass',
    database='data_cloud'
)


def main():
    from ping_test import ping_postgres
    ping_postgres(pg_connection)
    
if __name__ == "__main__":
    main()
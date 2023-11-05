import psycopg2

pg_connection = conn = psycopg2.connect(
    host='localhost',
    port='5432',
    user='postgres',
    password='anypass',
    database='data_cloud'
)
from dependency_injector import bigquery_client
from comparer import compare_schemas
from helper import Table


config_key = "food_tables"
table1, table2 = Table.get_tables_from_config(config_key)
schema1 = bigquery_client.get_schema(table1)
schema2 = bigquery_client.get_schema(table2)

output = compare_schemas(schema1, schema2)
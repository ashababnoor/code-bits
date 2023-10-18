from connector import *
import os

root_dir = os.path.dirname(os.path.dirname(__file__))
query_dir = "sql/"
query_file_name = "popular_search_terms.sql"

data_dir = "data/"
query_output_file_name = "query_output.txt"


with open(os.path.join(root_dir, query_dir, query_file_name), "r") as file:
    query = file.read()
    print("Query reading successful.")

query_executed_successfully = True

with open(os.path.join(root_dir, data_dir, query_output_file_name), "w") as file:
    for row in bq.execute(query=query):
        if query_executed_successfully:
            print("Query execution successful.")
            query_executed_successfully = False
        
        file.write(str(row))
    
    print("Query output writing to successful.")
    print(f"Output: {os.path.join(root_dir, data_dir, query_output_file_name)}")

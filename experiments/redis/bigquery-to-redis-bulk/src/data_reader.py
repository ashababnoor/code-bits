from connector import *
import os

root_dir = os.path.dirname(os.path.dirname(__file__))
query_dir = "sql/"
query_file_name = "address_history" # "popular_search_terms"
query_file_extension = ".sql"

data_dir = "data/"
query_output_file_name = f"query_output_{query_file_name}"
query_output_file_extention = ".txt"

query_file = f"{query_file_name}{query_file_extension}"
query_output_file = f"{query_output_file_name}{query_output_file_extention}"


with open(os.path.join(root_dir, query_dir, query_file), "r") as file:
    query = file.read()
    print("Query reading successful.")

query_executed_successfully = True

with open(os.path.join(root_dir, data_dir, query_output_file), "w") as file:
    for row in bq.execute(query=query):
        if query_executed_successfully:
            print("Query execution successful.")
            print()
            # print(f"{vars(row) = }")
            print(f"{dir(row) = }")
            print(row['recipient_identifier'], type(row['recipient_identifier']))
            print(row['address_history'], type(row['address_history']))
            
            query_executed_successfully = False
        
        file.write(str(row))
        file.write("\n")
    
    print(row.keys())
    
    print("Query output writing to successful.")
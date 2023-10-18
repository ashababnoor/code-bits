from utilities import *
from connector import *
import os
import json


root_dir = os.path.dirname(os.path.dirname(__file__))
query_dir = "sql/"
data_dir = "data/"

query_file_name = "address_history" # "popular_search_terms"
query_file_ext = "sql"

query_output_text_file_name = f"query_output_{query_file_name}"
query_output_text_file_ext = "txt"

query_output_json_file_name = f"query_output_{query_file_name}"
query_output_json_file_ext = "json"


query_file_path = os.path.join(
    root_dir,
    query_dir, 
    f"{query_file_name}.{query_file_ext}"
)
query_output_text_file_path = os.path.join(
    root_dir,
    data_dir, 
    f"{query_output_text_file_name}.{query_output_text_file_ext}"
)
query_output_json_file_path = os.path.join(
    root_dir,
    data_dir, 
    f"{query_output_json_file_name}.{query_output_json_file_ext}"
)


with open(query_file_path, "r") as file:
    query = file.read()
    print("Query reading successful.")


query_result = dict()
query_executed_successfully = True
seeds = 1

with open(query_output_text_file_path, "w") as file:
    for row in bq.execute(query=query):
        if query_executed_successfully:
            print("Query execution successful.")
            query_executed_successfully = False
        
        file.write(str(row) + "\n")
        result_dict_key = ", ".join([str(row.values()[i]) for i in range(seeds)])
        query_result[result_dict_key] = dict(zip(row.keys(), row.values()))
        
    print("Query output writing to text file successful.")
    

with open(query_output_json_file_path, 'w') as json_file:
    json.dump(query_result, json_file, indent=4, default=str)
    print("Query output writing to json file successful.")
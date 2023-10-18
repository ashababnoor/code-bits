import os
import sys
import json
import time
from itertools import tee
from utilities import *
from connector import *
from models import Query


# Defining global variables
BENCHMARK_MODE = True

script_start = time.time()

# Defining root dir and data dir 
root_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = "data/"


# Defining query object configuration
address_history = dict(query_name="address_history", seeds=1)
popular_search_terms = dict(query_name="popular_search_terms", seeds=2)
query = Query(**address_history)


# Defining output files names and paths
query_output_text_file_name = f"query_output_{query.query_name}.txt"
query_output_json_file_name = f"query_output_{query.query_name}.json"

query_output_text_file_path = os.path.join(
    root_dir,
    data_dir, 
    query_output_text_file_name
)
query_output_json_file_path = os.path.join(
    root_dir,
    data_dir, 
    query_output_json_file_name
)

try:
    query_execution_start = time.time()
    rows = bq.execute(query=query.get_query_string())
    query_execution_end = time.time()
    print("Query execution successful.")
except:
    print("Query execution failed. Exiting")
    sys.exit()


rows_text, rows_json = tee(rows, 2)


# Saving query result to text file
text_file_write_start = time.time()
query_result_text_output = [str(dict(row))+"\n" for row in rows_text]
with open(query_output_text_file_path, "w") as file:
    file.writelines(query_result_text_output)

text_file_write_end = time.time()
print("Query output writing to text file successful.")


# Saving query file to json file
json_file_write_start = time.time()
query_result_json_output = {
    ", ".join([str(row.values()[i]) for i in range(query.seeds)]): dict(row)
    for row in rows_json
}
with open(query_output_json_file_path, 'w') as json_file:
    json.dump(query_result_json_output, json_file, indent=4, default=str)

json_file_write_end = time.time()
print("Query output writing to json file successful.")


script_end = time.time()


# Output of script benchmark
if BENCHMARK_MODE:
    print("\nExecution times:")
    print(f"\tFull Script = {(script_end - script_start) * 10**3 :.2f} ms")
    print(f"\tQuery execution = {(query_execution_end - query_execution_start) * 10**3 :.2f} ms")
    print(f"\tText file write = {(text_file_write_end - text_file_write_start) * 10**3 :.2f} ms")
    print(f"\tJSON file write = {(json_file_write_end - json_file_write_start) * 10**3 :.2f} ms")
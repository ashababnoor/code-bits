import os
import sys
import json
import time
from itertools import tee
from datetime import datetime
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
text_conversion_start = time.time()

print(f"\tList for text generation started: {datetime.now().strftime('%H:%M:%S')}")
text_list_create_start = time.time()
query_result_text_output = [
    str(dict(row))+"\n" 
    for row in rows_text
]
text_list_create_end = time.time()
print(f"\tList for text generation ended: {datetime.now().strftime('%H:%M:%S')}")


print(f"\tText write started: {datetime.now().strftime('%H:%M:%S')}")
text_file_write_start = time.time()
with open(query_output_text_file_path, "w") as file:
    file.writelines(query_result_text_output)

text_file_write_end = time.time()
print(f"\tText write ended: {datetime.now().strftime('%H:%M:%S')}")

text_conversion_end = time.time()
print("Query output writing to text file successful.")



# Saving query file to json file
json_conversion_start = time.time()

print(f"\tDict for JSON generation started: {datetime.now().strftime('%H:%M:%S')}")
json_dict_create_start = time.time()
query_result_json_output = {
    ", ".join([str(row.values()[i]) for i in range(query.seeds)]): dict(row)
    for row in rows_json
}
json_dict_create_end = time.time()
print(f"\tDict for JSON generation ended: {datetime.now().strftime('%H:%M:%S')}")


print(f"\tJSON dump started: {datetime.now().strftime('%H:%M:%S')}")
json_file_write_start = time.time()
with open(query_output_json_file_path, 'w') as json_file:
    json.dump(query_result_json_output, json_file, default=str)  

json_file_write_end = time.time()
print(f"\tJSON dump ended: {datetime.now().strftime('%H:%M:%S')}")

json_conversion_end = time.time()
print("Query output writing to json file successful.")



script_end = time.time()

# Output of script benchmark
if BENCHMARK_MODE:
    print("\nExecution times:")
    print(f"\tFull Script = {(script_end - script_start) :.2f} s")
    print(f"\tQuery execution = {(query_execution_end - query_execution_start) * 10**3 :.2f} ms")
    
    print(f"\tText conversion = {(text_conversion_end - text_conversion_start) :.2f} s")
    print(f"\t\tText list generation = {(text_list_create_end - text_list_create_start) :.2f} s")
    print(f"\t\tText write execution  = {(json_file_write_end - json_file_write_start) :.2f} s")
    
    print(f"\tJSON conversion = {(json_conversion_end - json_conversion_start) :.2f} s")
    print(f"\t\tJSON dict generation = {(json_dict_create_end - json_dict_create_start) :.2f} s")
    print(f"\t\tJSON dump execution  = {(json_file_write_end - json_file_write_start) :.2f} s")
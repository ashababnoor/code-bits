import os
import sys
import json
import time
from itertools import tee
from datetime import datetime
import timeit
from utilities import *
from connector import *
from models import Query


# Defining root dir and data dir 
root_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = "data/"


# Defining query object configuration
limit = 20_000
address_history = dict(query_name="address_history", seeds=1, limit=limit)
popular_search_terms = dict(query_name="popular_search_terms", seeds=2, limit=limit)
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


start_time = timeit.default_timer()
# bq.write_to_text_file_(
#     query=query
#     , save_path=query_output_text_file_path+"1.txt"
#     , verbose=True
# )

bq.write_to_text_file(
    query=query
    , save_path=query_output_text_file_path+"2.txt"
    , verbose=True
)

print(f"Time needed f1: {timeit.default_timer() - start_time}")

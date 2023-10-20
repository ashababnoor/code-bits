import os
import json
import timeit
from utilities import *
from connector import *
from models import Query


# Defining root dir and data dir 
root_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = "data/"


# Defining query object configuration
limit = 1_000
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


with TimerBlock("Bigquery.write_to_text_file()", pretty=False) as block:
    bq.write_to_text_file(
        query=query
        , save_path=query_output_text_file_path
        , verbose=True
    )

Print.bold("Execution Time Reocrds")
TimerBlock.timing_summary(declarative=False)
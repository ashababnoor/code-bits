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


with TimerBlock("Bigquery.write_to_text_file()") as block:
    bq.write_to_text_file(
        query=query
        , save_path=query_output_text_file_path
        , verbose=True
    )
    
with TimerBlock("Bigquery.write_to_json_file()") as block:
    bq.write_to_json_file(
        query=query
        , save_path=query_output_json_file_path
        , verbose=True
    )

from redis_utils.json_to_redis import json_to_redis_commands
from redis_utils.redis_to_resp import redis_commands_to_resp

# Defining Redis files names and paths
redis_commands_file_name = f"redis_commands_{query.query_name}.txt"
resp_file_name = f"resp_{query.query_name}.txt"

redis_commands_file_path = os.path.join(
    root_dir,
    data_dir, 
    redis_commands_file_name
)
resp_file_name = os.path.join(
    root_dir,
    data_dir, 
    resp_file_name
)


with TimerBlock("JSON to Redis commands") as block:
    json_to_redis_commands(query_output_json_file_path, redis_commands_file_path)
    
with TimerBlock("Redis to Resp commands") as block:
    redis_commands_to_resp(redis_commands_file_path, resp_file_name)


TimerBlock.timing_summary()
import os
from utilities.classes.color import Color
from utilities.classes.print import Print
from utilities.classes.codeblock import CodeBlock
from utilities.classes.timerblock import TimerBlock

from connector import bq
from helper import Query
from loader import BigqueryLoader
from ingestor import RedisIngestor


# Defining root dir and data dir 
root_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = "data/"


# Defining query object configuration
limit = None
address_history = dict(query_name="address_history", grain=1, limit=limit)
popular_search_terms = dict(query_name="popular_search_terms", grain=2, limit=limit)
latest_popular_search_terms = dict(query_name="latest_popular_search_terms", grain=1, limit=limit)

query = Query(**address_history)


run_this = False
if run_this:
    bigquery_loader = BigqueryLoader(bigquery_client=bq)
    
    # Defining files names and paths
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
        bigquery_loader.write_to_text_file(
            query=query.add_limit(10000)
            , save_path=query_output_text_file_path
            , verbose=True
            , show_progress=True
        )
    
    with TimerBlock("Bigquery.write_to_json_file()") as block:
        bigquery_loader.write_to_json_file(
            query=query.add_limit(10000)
            , save_path=query_output_json_file_path
            , verbose=True
            , show_progress=True
        )


run_this = False
if run_this:
    from redis_utils.json_to_redis import json_to_redis_commands
    from redis_utils.redis_to_resp import redis_commands_to_resp

    # Defining files names and paths
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


run_this = False
if run_this:
    from connector import redis_local_apt
    ri = RedisIngestor(redis_client=redis_local_apt, bigquery_client=bq)
    limit_ = 1000
    
    redis_local_apt.flushall()
    
    with TimerBlock("RedisIngestor ingest_data() -- Parallel_computation=True; worker=8"):
        ri.ingest_data(
            query=query.add_limit(limit_)
            , verbose=True
            , show_progress=True
            , parallel_computation=True
            , worker_count=8
        )
    
    redis_local_apt.flushall()
    
    with TimerBlock("RedisIngestor ingest_data() -- Parallel_computation=False"):
        ri.ingest_data(
            query=query.add_limit(limit_)
            , verbose=True
            , show_progress=True
            , parallel_computation=False
        )
    
    redis_local_apt.close()


run_this = False
if run_this:
    from connector import redis_local_apt
    ri = RedisIngestor(redis_client=redis_local_apt, bigquery_client=bq)
    
    limit_ = 10
    query_ah = Query(**address_history)
    query_st = Query(**latest_popular_search_terms)
    
    redis_local_apt.flushall()
    
    with TimerBlock("RedisIngestor ingest_data() -- type=JSON; Parallel_computation=True; worker=8"):
        ri.ingest_data(
            query=query_ah.add_limit(limit_)
            , verbose=True
            , show_progress=True
            , parallel_computation=True
            , worker_count=8
            , redis_data_type=RedisIngestor.JSON
        )
        
    with TimerBlock("RedisIngestor ingest_data() -- type=HSET; Parallel_computation=True; worker=8"):
        ri.ingest_data(
            query=query_st.add_limit(limit_)
            , verbose=True
            , show_progress=True
            , parallel_computation=True
            , redis_data_type=RedisIngestor.HSET
        )
    
    redis_local_apt.close()


run_this = True
if run_this:
    from connector import redis_local_apt
    ri = RedisIngestor(redis_client=redis_local_apt, bigquery_client=bq)
    
    limit_ = 1000
    
    redis_local_apt.flushall()
    
    with TimerBlock("RedisIngestor ingest_address_history() -- using special windowing method"):
        ri.ingest_address_history(
            limit=limit_
            , verbose=True
            , parallel_computation=True
        )


TimerBlock.timing_summary()
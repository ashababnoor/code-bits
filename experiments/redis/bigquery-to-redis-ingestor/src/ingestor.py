import redis
from helper import Query
from loader import Bigquery
from tqdm import tqdm
from typing import Union
from utilities.classes.print import Print


class RedisIngestor:
    def __init__(self, redis_client, bigquery_client):
        self.redis_client = redis_client
        self.bigquery_client = bigquery_client
    
    def __get_redis_key_from_grain(row, grain: int, separator: str=";;") -> str:
        columns = list(row.keys())[:grain]
        key = separator.join([f"{column}:{row[column]}" for column in columns])
        return key
    
    def __get_redis_key_from_list(row, redis_key_columns: list, separator: str=";;") -> str:
        columns = list(set(redis_key_columns) & set(row.keys()))
        key = separator.join([f"{column}:{row[column]}" for column in columns])
        return key
    
    def __get_redis_value_from_list_as_dict(row, redis_value_columns: list) -> dict:
        columns = list(set(redis_value_columns) & set(row.keys()))
        value = {column: row[column] for column in columns}
        return value
    
    def __get_redis_value_as_dict(row, columns_to_exclude: Union[list, None]=None):
        if columns_to_exclude is not None:
            columns = list(set(row.keys()) - set(columns_to_exclude))
            value = {column: row[column] for column in columns}
            return value
        value = dict(row)
        return value
    
    def store_in_redis(
        self,
        query: Query,
        redis_client: redis.Redis,
        bigquery_client: Bigquery,
        verbose: bool=False,
        show_progress: bool=False,
    ):
        '''
        Only works with simple data structures containing int, float, string, byte etc.
        For complex data structures, code needs to be re-written.
        RedisJSON is a possible solution for JSON objects or complex objects/dictionaries
        '''
        rows = bigquery_client.execute(query.get_query_string())
        if show_progress:
            row_count = query.get_row_count(bigquery_client=bigquery_client)
            rows = tqdm(rows, total=row_count)
        
        pipe = redis.pipeline()
        
        for row in rows:
            key = ", ".join([str(row.values()[i]) for i in range(query.grain)])
            pipe.hset(key, mapping=dict(row))
        
        output = len(pipe.execute())
        if verbose: Print.log(f"Replies received = {output:,}")
    
    def store_in_redis_stack_as_json(
        self,
        query: Query,
        redis_client: redis.Redis,
        bigquery_client: Bigquery,
        redis_key_columns: list[Union[str, int]]=None,
        redis_value_columns: list[Union[str, int]]=None,
        verbose: bool=False,
        show_progress: bool=False,
        parallel_computation: bool=False,
    ):
        from redis.commands.json.path import Path
        
        pipe = redis_client.pipeline()
        
        def add_to_pipe(row, grain):
            key = ", ".join([str(row.values()[i]) for i in range(grain)])
            pipe.json().set(key, "$", dict(row))  
        
        if parallel_computation:
            Print.warning("Parallel computation is not yet supported. Please run with parallel_computation=False")
            return
        
        rows = bigquery_client.execute(query.get_query_string())
        if show_progress:
            row_count = query.get_row_count(bigquery_client=bigquery_client)
            rows = tqdm(rows, total=row_count)
            
        for row in rows:
            key = ", ".join([str(row.values()[i]) for i in range(query.grain)])
            pipe.json().set(key, Path.root_path(), dict(row))
        
        if verbose: Print.log("Pipeline generation complete. Executing pipeline")
        output = len(pipe.execute())
        if verbose: Print.log(f"Pipeline executed. Replies received = {output:,}")
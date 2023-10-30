import redis
from helper import Query
from loader import Bigquery
from typing import Union
from logger import logger
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from utilities.classes.print import Print
from utilities.functions import check_iterable_datatype

class RedisIngestor:
    def __init__(
            self, 
            redis_client: redis.Redis,
            bigquery_client: Bigquery,
        ):
        self.redis_client = redis_client
        self.bigquery_client = bigquery_client
        logger.debug("RedisIngestor object created")
    
    def __get_redis_key_from_grain(self, row, grain: int=1, redis_key_columns: list=None, separator: str=";;") -> str:
        columns = list(row.keys())[:grain]
        key = separator.join([f"{column}:{row[column]}" for column in columns])
        return key
    
    def __get_redis_key_from_list(self, row, *, grain: int=1, redis_key_columns: list=None, separator: str=";;") -> str:
        columns = list(set(redis_key_columns) & set(row.keys()))
        key = separator.join([f"{column}:{row[column]}" for column in columns])
        return key
    
    def __get_redis_value_from_list_as_dict(self, row, *, redis_value_columns: list=None, columns_to_exclude: Union[list, None]=None) -> dict:
        columns = list(set(redis_value_columns) & set(row.keys()))
        value = {column: row[column] for column in columns}
        return value
    
    def __get_redis_value_as_dict(self, row, *, redis_value_columns: list=None, columns_to_exclude: Union[list, None]=None) -> dict:
        if columns_to_exclude is not None:
            columns = list(set(row.keys()) - set(columns_to_exclude))
            value = {column: row[column] for column in columns}
            return value
        value = dict(row)
        return value
    
    def __redis_set(pipe, key, value):
        pipe.set(key, value)
    
    def __redis_hset(pipe, key, value):
        pipe.hset(key, mapping=value)
    
    def __redis_json_set(pipe, key, value):
        from redis.commands.json.path import Path
        pipe.json().set(key, Path.root_path(), value)
    
    def store_in_redis_as_hash(
        self,
        query: Query,
        redis_client: redis.Redis=None,
        bigquery_client: Bigquery=None,
        redis_key_columns: list[str]=None,
        redis_value_columns: list[str]=None,
        redis_columns_to_exclude: list[str]=None,
        verbose: bool=False,
        show_progress: bool=False,
    ):
        '''
        Only works with simple data structures containing int, float, string, byte etc.
        For complex data structures, code needs to be re-written.
        RedisJSON is a possible solution for JSON objects or complex objects/dictionaries
        '''
        
        if redis_client is None: 
            redis_client = self.redis_client
        if bigquery_client is None:
            bigquery_client = self.bigquery_client
        
        get_redis_key = None
        get_redis_value = None
        
        if redis_key_columns is not None and check_iterable_datatype(redis_key_columns, int) and redis_key_columns:
            get_redis_key = self.__get_redis_key_from_list
        else:
            get_redis_key = self.__get_redis_key_from_grain
        
        if redis_value_columns is not None and check_iterable_datatype(redis_value_columns, str) and redis_value_columns:
            get_redis_value = self.__get_redis_value_from_list_as_dict
        else:
            get_redis_value = self.__get_redis_value_as_dict
        
        logger.debug(f"Using {get_redis_key.__name__}() for generating redis key")
        logger.debug(f"Using {get_redis_value.__name__}() for generating redis value")
        
        rows = bigquery_client.execute(query.get_query_string())
        if show_progress:
            row_count = query.get_row_count(bigquery_client=bigquery_client)
            rows = tqdm(rows, total=row_count)
        
        pipe = redis_client.pipeline()
        
        for row in rows:
            key = get_redis_key(
                row=row,
                redis_key_columns=redis_key_columns,
                grain=query.grain, 
            )
            value = get_redis_value(
                row=row,
                redis_value_columns=redis_value_columns,
                columns_to_exclude=redis_columns_to_exclude
            )
            pipe.hset(key, mapping=value)
        
        if verbose: Print.log("Pipeline generation complete. Executing pipeline")
        output = len(pipe.execute())
        if verbose: Print.log(f"Pipeline executed. Replies received = {output:,}")
    
    
    def ingest_data(
        self,
        query: Query,
        redis_key_columns: list[str]=None,
        redis_value_columns: list[str]=None,
        redis_columns_to_exclude: list[str]=None,
        verbose: bool=False,
        show_progress: bool=False,
        parallel_computation: bool=False,
        worker_count: int=10,
    ):
        from redis.commands.json.path import Path
        
        redis_client = self.redis_client
        bigquery_client = self.bigquery_client
        
        get_redis_key = None
        get_redis_value = None
        
        if redis_key_columns is not None and check_iterable_datatype(redis_key_columns, int) and redis_key_columns:
            get_redis_key = self.__get_redis_key_from_list
        else:
            get_redis_key = self.__get_redis_key_from_grain
        
        if redis_value_columns is not None and check_iterable_datatype(redis_value_columns, str) and redis_value_columns:
            get_redis_value = self.__get_redis_value_from_list_as_dict
        else:
            get_redis_value = self.__get_redis_value_as_dict
        
        logger.debug(f"Using {get_redis_key.__name__}() for generating redis key")
        logger.debug(f"Using {get_redis_value.__name__}() for generating redis value")
        
        
        def _ingest_data_core(worker_number, query_string, show_progress=False):
            if verbose: Print.info(f"{worker_number = }, Query window = {query_string.splitlines()[-1]}")

            pipe = redis_client.pipeline()
            
            rows = bigquery_client.execute(query_string)                
            
            for row in rows:
                key = get_redis_key(
                    row=row,
                    redis_key_columns=redis_key_columns,
                    grain=query.grain, 
                )
                value = get_redis_value(
                    row=row,
                    redis_value_columns=redis_value_columns,
                    columns_to_exclude=redis_columns_to_exclude
                )
                pipe.json().set(key, Path.root_path(), value)
            
            if verbose: Print.info(f"{worker_number = }: Redis pipeline generation complete. Executing pipeline")
            output = len(pipe.execute())
            if verbose: Print.success(f"{worker_number = }: Redis pipeline executed. Replies received = {output:,}")
            
            return output
        
        
        if not parallel_computation:
            result = _ingest_data_core(
                worker_number=0, 
                query_string=query.get_query_string(),
                show_progress=show_progress
            )
            results = [result]
        else:
            from concurrent.futures import ThreadPoolExecutor
            
            worker_numbers = list(range(worker_count))
            query_strings = query.get_windowed_query_strings(
                bigquery_client=bigquery_client
                , window_number=worker_count
            )
            arguments = list(zip(worker_numbers, query_strings))
            
            with ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(_ingest_data_core, *argument)
                    for argument in arguments
                ]
                
                results = [
                    future.result()
                    for future in futures
                ]
                
        if verbose: Print.success(f"Data ingestion complete. Total {sum(results):,} rows ingested.")
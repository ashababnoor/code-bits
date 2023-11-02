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
    JSON: str = "JSON"
    HSET: str = "HSET"
    
    DEFAULT_DATA_TYPE: str = JSON
    SUPPORTED_DATA_TYPES: list[str] = [JSON, HSET]
    
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
    
    
    def __redis_hset(self, pipe, key, value):
        pipe.hset(key, mapping=value)
    
    def __redis_json_set(self, pipe, key, value):
        from redis.commands.json.path import Path
        pipe.json().set(key, Path.root_path(), value)
    
    
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
        redis_data_type: str=JSON
    ):        
        redis_client = self.redis_client
        bigquery_client = self.bigquery_client
        
        get_redis_key = None
        get_redis_value = None
        redis_setter_function = None
        
        if redis_key_columns is not None and check_iterable_datatype(redis_key_columns, int) and redis_key_columns:
            get_redis_key = self.__get_redis_key_from_list
        else:
            get_redis_key = self.__get_redis_key_from_grain
        
        if redis_value_columns is not None and check_iterable_datatype(redis_value_columns, str) and redis_value_columns:
            get_redis_value = self.__get_redis_value_from_list_as_dict
        else:
            get_redis_value = self.__get_redis_value_as_dict
        
        if redis_data_type not in RedisIngestor.SUPPORTED_DATA_TYPES:
            if verbose: Print.warning(f"Provided redis data type {redis_data_type} is currently not supported. Using default data type {RedisIngestor.DEFAULT_DATA_TYPE}")
            redis_setter_function = self.__redis_json_set
        elif redis_data_type == RedisIngestor.JSON:
            redis_setter_function = self.__redis_json_set
        elif redis_data_type == RedisIngestor.HSET:
            redis_setter_function = self.__redis_hset
        
        logger.debug(f"Using {get_redis_key.__name__}() for generating redis key")
        logger.debug(f"Using {get_redis_value.__name__}() for generating redis value")
        logger.debug(f"Using {redis_setter_function.__name__}() as redis setter function")
        
        
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
                redis_setter_function(pipe, key, value)
            
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
    
    
    def ingest_address_history(
            self,
            limit: list[Union[int, str, None]]=None,
            verbose: bool=False,
            show_progress: bool=False,
            parallel_computation: bool=True,
            worker_count: int=10,
        ):
        query = Query(
            query_name="address_history",
            grain=1,
            limit=limit
        )
        redis_key_columns = ["recipient_identifier"]
        redis_value_columns = ["address_history"]
        redis_data_type = RedisIngestor.JSON
        
        self.ingest_data(
            query=query,
            redis_key_columns=redis_key_columns,
            redis_value_columns=redis_value_columns,
            verbose=verbose,
            show_progress=show_progress,
            parallel_computation=parallel_computation,
            worker_count=worker_count,
            redis_data_type=redis_data_type
        )
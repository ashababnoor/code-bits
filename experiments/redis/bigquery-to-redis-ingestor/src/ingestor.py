import redis
from models import Query
from loader import Bigquery
from utilities import Print
from tqdm import tqdm


class RedisIngestor:
    def __init__(self):
        pass
    
    def store_in_redis_stack_as_json(
        self,
        query: Query,
        redis_client: redis.Redis,
        bigquery_client: Bigquery,
        verbose: bool=False,
        show_progress: bool=False,
        parallel_computation: bool=False,
        parallel_job_count: int=2,
    ):
        from redis.commands.json.path import Path
        from joblib import Parallel, delayed
        
        rows = bigquery_client.execute(query.get_query_string())
        if show_progress:
            row_count = query.get_row_count(bigquery_client=self)
            rows = tqdm(rows, total=row_count)
        
        pipe = redis_client.pipeline()
        
        def add_to_pipe(row, grain):
            key = ", ".join([str(row.values()[i]) for i in range(grain)])
            pipe.json().set(key, "$", dict(row))  
        
        if parallel_computation:
            Parallel(n_jobs=parallel_job_count)(
                    delayed(add_to_pipe)(row, query.grain) for row in rows
            )
        else:
            for row in rows:
                key = ", ".join([str(row.values()[i]) for i in range(query.grain)])
                pipe.json().set(key, "$", dict(row))
        
        if verbose: Print.log("Pipeline generation complete. Executing pipeline")
        output = len(pipe.execute())
        if verbose: Print.log(f"Replies received = {output:,}")
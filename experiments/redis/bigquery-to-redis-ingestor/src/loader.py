from google.cloud import bigquery
import redis
from models import Query
from tqdm import tqdm
from utilities.classes.print import Print


class Bigquery:
    def __init__(self, google_cred):
        self.__cnn = Bigquery._get_connection(google_cred)

    def execute(self, query):
        for row in self.__cnn.query(query):
            yield row

    @staticmethod
    def _get_connection(cred):
        if cred is not None:
            import os

            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred
        return bigquery.Client()
    
    def test_connection(self):
        import os

        datasets = self.__cnn.list_datasets(
            project=os.environ.get("BIGQUERY_PROJECT_ID")
        )
        return True if datasets else False


class BigqueryLoader:
    def __init__(self, bigquery_client) -> None:
        self.client = bigquery_client
    
    def write_to_text_file(
            self, 
            query: Query, 
            save_path: str, 
            verbose: bool=False,
            show_progress: bool=False,
            parallel_computation: bool=False,
            parallel_job_count: int=2,
        ):
        from joblib import Parallel, delayed
        
        rows = self.client.execute(query.get_query_string())
        if show_progress:
            row_count = query.get_row_count(bigquery_client=self.client)
            rows = tqdm(rows, total=row_count)
        
        with open(save_path, "w") as file:
            if parallel_computation:
                Parallel(n_jobs=parallel_job_count)(
                    delayed(file.write)(str(dict(row))+"\n") for row in rows
                )
            else:
                for row in rows:
                    file.write(str(dict(row))+"\n")

        if verbose: Print.success("Writing to text file completed!")
    
    def write_to_json_file(
            self, 
            query: Query, 
            save_path: str, 
            verbose: bool=False,
            use_indent: bool=True,
            show_progress: bool=False,
            parallel_computation: bool=False,
        ):
        import json
        from joblib import Parallel, delayed
        
        rows = self.client.execute(query.get_query_string())
        if show_progress:
            row_count = query.get_row_count(bigquery_client=self.client)
            rows = tqdm(rows, total=row_count)
        
        query_output_dict = {
            ", ".join([str(row.values()[i]) for i in range(query.grain)]): dict(row)
            for row in rows
        }

        with open(save_path, 'w') as json_file:
            if use_indent:
                json.dump(query_output_dict, json_file, indent=4, default=str)
            else:
                json.dump(query_output_dict, json_file, default=str)

        if verbose: Print.success("Writing to json file completed!")
    

class Redis:
    pass
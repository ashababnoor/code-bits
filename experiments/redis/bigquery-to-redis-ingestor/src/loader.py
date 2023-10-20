from google.cloud import bigquery
from models import Query
from utilities import Color, now


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
        
    def write_to_text_file(
            self, 
            query: Query, 
            save_path: str, 
            benchmark: bool=False, 
            verbose: bool=False
        ):
        import timeit
        
        if verbose: print(f"{Color.light_blue}Log:{Color.reset} Writing to file started: {now()}")
        
        with open(save_path, "w") as file:
            for row in self.execute(query.get_query_string()):
                file.write(str(dict(row))+"\n")
        
        if verbose: print(f"{Color.light_blue}Log:{Color.reset} Writing to file ended: {now()}")
        print("Writing to file successful!")
        if verbose: print("")
from google.cloud import bigquery


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

import os


class Query:
    __slots__ = (
        "__query_path",
        "__query_string",
        "query_name",
        "seeds",
    )

    __root_dir = os.path.dirname(os.path.dirname(__file__))
    __query_dir = "sql"

    def __init__(self, query_name, seeds=1) -> None:
        self.query_name = query_name
        self.seeds = seeds
        self.__query_path = os.path.join(
            Query.__root_dir, Query.__query_dir, f"{self.query_name}.sql"
        )
        self.__set_query_string()

    def __set_query_string(self) -> str:
        with open(self.__query_path, "r") as query_file:
            self.__query_string = query_file.read()

    def get_query_string(self):
        return self.__query_string


if __name__ == "__main__":
    query = Query("popular_search_terms")

    print(f"{query.query_name = }")
    print(query.get_query_string())

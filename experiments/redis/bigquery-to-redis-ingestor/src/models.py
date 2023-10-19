import os
from copy import copy 


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
            
    def __update_query_string(self, query_string) -> str:
        self.__query_string = query_string

    def get_query_string(self):
        return self.__query_string
    
    def add_limit(self, limit: int, inplace=False) -> 'Query':
        if type(limit) != int:
            raise Exception("Limit must be an integer.")
        limit_added_query_string = f"select * from ({self.get_query_string()}) limit {limit}"
        
        if inplace:
            self.__update_query_string(limit_added_query_string)
            return self

        query = copy(self)
        query.__update_query_string(limit_added_query_string)
        return query


if __name__ == "__main__":
    query = Query("popular_search_terms")

    print(f"{query.query_name = }")
    
    print("\nOriginal query:")
    print(query.get_query_string())
    
    print("\nQuery after adding limit:")
    print(query.add_limit(10).get_query_string())

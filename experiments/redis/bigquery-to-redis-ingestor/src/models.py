import os
from copy import copy
from typing import Union
from utilities import *

class Query:
    __slots__ = (
        "__query_path",
        "__query_string",
        "query_name",
        "seeds",
        "limit",
    )

    __root_dir: str = os.path.dirname(os.path.dirname(__file__))
    __query_dir: str = "sql"

    def __init__(self, query_name, seeds: int=1, limit: Union[int, str, None] = None) -> None:
        self.query_name = query_name
        self.seeds = seeds
        self.__query_path = os.path.join(
            Query.__root_dir, Query.__query_dir, f"{self.query_name}.sql"
        )
        self.__set_query_string()
        
        self.limit = limit
        if type(limit) == int or type(limit) == str:
            self.add_limit(limit, inplace=True)

    def __repr__(self) -> str:
        return f"Query(query_name='{self.query_name}', seeds={self.seeds}, limit={self.limit})"

    def __set_query_string(self) -> None:
        with open(self.__query_path, "r") as query_file:
            self.__query_string = query_file.read()
        return

    def __update_query_string(self, query_string: str) -> None:
        self.__query_string = query_string
        return

    def get_query_string(self) -> str:
        return self.__query_string

    def add_limit(self, limit: int, inplace: bool = False) -> Union["Query", None]:
        if type(limit) != int and type(limit) != str:
            raise Exception("Limit must be an integer or string.")
        limit_added_query_string = (
            f"select * from ({self.get_query_string()}) limit {limit}"
        )

        if inplace:
            self.limit = limit
            self.__update_query_string(limit_added_query_string)
            return

        query = copy(self)
        query.add_limit(limit, inplace=True)
        return query


if __name__ == "__main__":
    print(f"{green_bold}Query class regular constructor:{reset}")
    query = Query("popular_search_terms")
    print(query)
    print(f"{light_blue}Original query string:{reset}")
    print(query.get_query_string())
    
    print("\n")

    print(f"{green_bold}'add_limit()' with inplace=False:{reset}")
    print(query.add_limit(10))
    print(f"{light_blue}Modified query string:{reset}")
    print(query.add_limit(10).get_query_string())

    print("\n")

    print(f"{green_bold}Query class constructor with limit:{reset}")
    query = Query("address_history", limit=25)
    print(query)
    print(f"{light_blue}Original query:{reset}")
    print(query.get_query_string())

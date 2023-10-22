import os
from copy import copy
from typing import Union
from utilities import *


class Query:
    __slots__ = (
        "__query_path",
        "__query_string",
        "query_name",
        "grain",
        "limit",
    )

    __root_dir: str = os.path.dirname(os.path.dirname(__file__))
    __query_dir: str = "sql"

    def __init__(self, query_name, grain: int=1, limit: Union[int, str, None] = None) -> None:
        self.query_name = query_name
        self.grain = grain
        self.__query_path = os.path.join(
            Query.__root_dir, Query.__query_dir, f"{self.query_name}.sql"
        )
        self.__set_query_string()
        
        self.limit = limit
        if type(limit) == int or type(limit) == str:
            self.add_limit(limit, inplace=True)

    def __repr__(self) -> str:
        return f"Query(query_name='{self.query_name}', grain={self.grain}, limit={self.limit})"

    def __set_query_string(self) -> None:
        try:
            with open(self.__query_path, "r") as query_file:
                self.__query_string = query_file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Query file not found in path: {self.__query_path}")
        return

    def __update_query_string(self, query_string: str) -> None:
        self.__query_string = query_string
        return

    def get_query_string(self) -> str:
        return self.__query_string

    def add_limit(self, limit: int, inplace: bool = False) -> Union["Query", None]:
        if type(limit) != int and type(limit) != str:
            raise Exception("Limit must be an integer or string.")
        
        # New lines must be added to avoid the limit clause falling into a comment.
        limit_added_query_string = f"select * \nfrom (\n{self.get_query_string()}\n) \nlimit {limit}"

        if inplace:
            self.limit = limit
            self.__update_query_string(limit_added_query_string)
            return

        query = copy(self)
        query.add_limit(limit, inplace=True)
        return query

    def get_row_count_query(self) -> str:
        if self.limit is not None:
            return self.limit
        row_count_query_string = f"select count(*) \nfrom (\n{self.get_query_string()}\n)"
        return row_count_query_string

if __name__ == "__main__":
    print(f"{Color.green_bold}Query class regular constructor:{Color.reset}")
    query = Query("popular_search_terms")
    print(query)
    print(f"{Color.light_blue}Original query string:{Color.reset}")
    print(query.get_query_string())
    
    print("\n")

    print(f"{Color.green_bold}'add_limit()' with inplace=False:{Color.reset}")
    print(query.add_limit(10))
    print(f"{Color.light_blue}Modified query string:{Color.reset}")
    print(query.add_limit(10).get_query_string())

    print("\n")

    print(f"{Color.green_bold}Query class constructor with limit:{Color.reset}")
    query = Query("address_history", limit=25)
    print(query)
    print(f"{Color.light_blue}Original query:{Color.reset}")
    print(query.get_query_string())
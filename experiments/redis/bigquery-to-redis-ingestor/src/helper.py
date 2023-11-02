import os
from copy import copy
from typing import Union


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
        limit_added_query_string = f"SELECT * \nFROM (\n{self.get_query_string()}\n) \nLIMIT {limit}"

        if inplace:
            self.limit = limit
            self.__update_query_string(limit_added_query_string)
            return

        query = copy(self)
        query.add_limit(limit, inplace=True)
        return query

    def get_row_count(self, bigquery_client, use_limit=True) -> str:
        if use_limit and self.limit is not None:
            return self.limit
        
        row_count_query_string = f"SELECT COUNT(*) \nFROM (\n{self.get_query_string()}\n)"
        
        rows = bigquery_client.execute(row_count_query_string)
        results = [row for row in rows]
        return results[0].values()[0]
    
    def get_windowed_query_strings(self, bigquery_client, use_limit=True, window_number: int=10) -> list[str]:
        row_count = self.get_row_count(bigquery_client=bigquery_client, use_limit=use_limit)
        
        limit = (row_count // window_number) + 1
        offset = 0
        query_strings = []
        
        for _ in range(window_number):
            query_strings.append(
                f"SELECT * \nFROM (\n{self.get_query_string()}\n) \nLIMIT {limit} OFFSET {offset}"
            )
            offset += limit
        return query_strings
    
    def get_windowed_query_strings_for_address_history_using_string_prefix(self, bigquery_client) -> list[str]:
        string_prefix_query = Query(
            "address_history_windowing_template"
        ).get_query_string().format(base_query=self.get_query_string())

        string_prefixes_generator = bigquery_client.get_client().query(string_prefix_query).result()
        string_prefixes = [string_prefix.values()[0] for string_prefix in string_prefixes_generator]
        
        query_strings = []
        for string_prefix in string_prefixes:
            query_strings.append(
                f"SELECT * \nFROM (\n{self.get_query_string()}\n) \nWHERE recipient_identifier LIKE '{string_prefix}%'"
            )
        return query_strings


if __name__ == "__main__":
    from utilities.classes.color import Color
    from utilities.classes.print import Print
    from utilities.classes.codeblock import CodeBlock
    from utilities.classes.timerblock import TimerBlock


    with CodeBlock("Query class regular constructor", Color.light_sea_green_bold) as _:
        query = Query("popular_search_terms")
        print(query)
        Print.keyword("Query string", "original")
        print(query.get_query_string())

    
    with CodeBlock("add_limit() with inplace=False", Color.light_sea_green_bold) as _:
        print(query.add_limit(10))
        Print.keyword("Query string", "modified using add_limit()")
        print(query.add_limit(10).get_query_string())


    with CodeBlock("Query class constructor with limit", Color.light_sea_green_bold) as _:
        query = Query("address_history", limit=25)
        print(query)
        Print.keyword("Query string", "original")
        print(query.get_query_string())
    
    
    with CodeBlock("Query object get_row_count_query()", Color.light_sea_green_bold) as _:
        from connector import bq
        print(query.get_row_count(bigquery_client=bq, use_limit=True))
        
    with CodeBlock("Query object get_windowed_query_strings_for_address_history_using_string_prefix()", Color.light_sea_green_bold) as _:
        from connector import bq
        
        query = Query("address_history", limit=10)
        with TimerBlock():
            query_strings = query.get_windowed_query_strings_for_address_history_using_string_prefix(bigquery_client=bq)
            print(query_strings[0])
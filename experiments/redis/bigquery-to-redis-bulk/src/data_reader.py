from connector import *
import os

root_dir = os.path.dirname(os.path.dirname(__file__))
query_dir = "sql/"
query_file_name = "popular_search_terms.sql"

data_dir = "data/"
query_output_file_name = "query_output.txt"


with open(os.path.join(root_dir, query_dir, query_file_name), "r") as file:
    query = file.read()


with open(os.path.join(root_dir, data_dir, query_output_file_name), "w") as file:
    pass

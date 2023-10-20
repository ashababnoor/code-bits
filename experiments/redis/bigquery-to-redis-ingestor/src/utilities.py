from datetime import datetime
from dataclasses import dataclass


# Utility classes
@dataclass
class Color:
    # Define bold text and reset color and formatting
    bold: str = '\033[1m'               # bold text
    reset: str = '\033[0m'              # reset color and formatting

    # Define non-bold color codes
    blue: str = '\033[0;34m'            # Blue
    light_blue: str = '\033[0;36m'      # Light Blue
    green: str = '\033[0;32m'           # Green
    red: str = '\033[0;31m'             # Red
    yellow: str = '\033[0;33m'          # Yellow
    purple: str = '\033[0;35m'          # Purple

    # Define bold color codes
    blue_bold: str = '\033[1;34m'       # Bold Blue
    light_blue_bold: str = '\033[1;36m' # Bold Light Blue
    green_bold: str = '\033[1;32m'      # Bold Green
    red_bold: str = '\033[1;31m'        # Bold Red
    yellow_bold: str = '\033[1;33m'     # Bold Yellow
    purple_bold: str = '\033[1;35m'     # Bold Purple


# Utility lambdas
now: str = lambda: datetime.now().strftime('%H:%M:%S')


# Utility functions
def get_attributes(object: any) -> list:
    return [
        attr 
        for attr in dir(object) 
        if not callable(getattr(object, attr)) and not attr.startswith('__')
    ]

def get_regular_methods(object: any) -> list:
    return [
        method 
        for method in dir(object) 
        if callable(getattr(object, method)) and not method.startswith('__')
    ]

def get_dunder_methods(object: any) -> list:
    return [
        method 
        for method in dir(object) 
        if callable(getattr(object, method)) and method.startswith('__')
    ]    


# Driver code
if __name__ == "__main__":
    from connector import bq
    from models import Query
    
    query = Query("popular_search_terms", seeds=2, limit=1)
    query_string = query.get_query_string()
    
    for row in bq.execute(query_string):
        attributes = get_attributes(row)
        regular_methods = get_regular_methods(row)
        dunder_methods = get_dunder_methods(row)
        
        print(f"{attributes = }")       
        print(f"{regular_methods = }") 
        print(f"{dunder_methods = }")
        break
    
    print()
    print(f"{now() = }")
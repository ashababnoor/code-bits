def get_attributes(object: any) -> list:
    return [
        attr 
        for attr in dir(object) 
        if not callable(getattr(object, attr)) 
        and not attr.startswith('__')
    ]

def get_regular_methods(object: any) -> list:
    return [
        method 
        for method in dir(object) 
        if callable(getattr(object, method)) 
        and not method.startswith('__')
    ]
    
def get_dunder_methods(object: any) -> list:
    return [
        method 
        for method in dir(object) 
        if callable(getattr(object, method)) 
        and method.startswith('__')
    ]

if __name__ == "__main__":
    from connector import bq
    import os
    
    root_dir = os.path.dirname(os.path.dirname(__file__))
    query_dir = "sql/"
    query_file_name = "address_history" # "popular_search_terms"
    query_file_ext = "sql"

    query_file_path = os.path.join(
        root_dir,
        query_dir, 
        f"{query_file_name}.{query_file_ext}"
    )
    with open(query_file_path, "r") as file:
        query = file.read()

    for row in bq.query(query):
        attributes = get_attributes(row)
        regular_methods = get_regular_methods(row)
        dunder_methods = get_dunder_methods(row)
        
        print(f"{attributes = }")       
        print(f"{regular_methods = }") 

        print(f"{row.items() = }")
        print(f"{row.keys() = }")
        print(f"{row.values() = }")
        break
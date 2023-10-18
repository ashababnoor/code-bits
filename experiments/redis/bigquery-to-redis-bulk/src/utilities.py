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
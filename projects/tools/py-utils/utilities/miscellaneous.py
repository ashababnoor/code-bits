from datetime import datetime


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


def check_iterable_datatype(iterable, datatype):
    return all(isinstance(item, datatype) for item in iterable)


def now():
    return datetime.now().strftime('%H:%M:%S')


def to_human_readable_time(seconds: int, max_depth: int=2, use_short_names=True) -> str:
    import humanize
    from datetime import timedelta
    short_names = {
        " days": "d", " day": "d",
        " hours": "h", " hour": "h",
        " minutes": "min", " minute": "min",
        " seconds": "s", " second": "s",
        " milliseconds": "ms", " millisecond": "ms",
        " microseconds": "μs", " microsecond": "μs"
    }

    delta = timedelta(seconds=seconds)
    human_readable_time = humanize.precisedelta(delta, minimum_unit="microseconds")
    human_readable_time = human_readable_time.replace(" and ", ", ")
    
    if len(human_readable_time.split(", ")) > max_depth:
        units = human_readable_time.split(", ")
        units = units[:max_depth]
        human_readable_time = ", ".join(units)
    
    if use_short_names:
        for name, short_name in short_names.items(): human_readable_time = human_readable_time.replace(name, short_name)
    return human_readable_time


def to_human_readable_time_(seconds: int, max_depth: int=2, use_short_names=True) -> str:
    time_unit_to_seconds_mapping = dict(
        microsecond=0.000001,
        millisecond=0.001,
        second=1,
        minute=60,
        hour=3600,
        day=86400,
        month=2592000,
        year=31536000,
    )
    pass
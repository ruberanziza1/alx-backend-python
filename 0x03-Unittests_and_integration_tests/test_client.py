# utils.py
import requests
import functools

def get_json(url: str) -> dict:
    """Fetches JSON data from a given URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def access_nested_map(nested_map: dict, path: list):
    """Accesses a value in a nested dictionary using a list of keys."""
    # This is a common implementation for access_nested_map
    for key in path:
        nested_map = nested_map[key]
    return nested_map

def memoize(func):
    """Decorator to cache the results of a method call."""
    cache = {}
    @functools.wraps(func)
    def memoized_func(*args, **kwargs):
        if args in cache:
            return cache[args]
        result = func(*args, **kwargs)
        cache[args] = result
        return result
    return memoized_func

# For a simpler memoize that just works for methods without args beyond self:
# def memoize(func):
#     attr_name = '_memoized_' + func.__name__
#     @functools.wraps(func)
#     def memoized_wrapper(self, *args, **kwargs):
#         if not hasattr(self, attr_name):
#             setattr(self, attr_name, func(self, *args, **kwargs))
#         return getattr(self, attr_name)
#     return memoized_wrapper

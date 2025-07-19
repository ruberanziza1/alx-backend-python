#!/usr/bin/env python3
"""Utility functions for tests."""

def access_nested_map(nested_map: dict, path: list):
    """
    Accesses a nested map using a list of keys as the path.
    """
    current_map = nested_map
    try:
        for key in path:
            current_map = current_map[key]
        return current_map
    except (KeyError, TypeError) as e:
        raise ValueError(f"Path '{path}' not found in map: {e}")

# If your project uses get_json from utils, keep this.
# Otherwise, it might not be strictly necessary for THIS specific error,
# but it's common in these types of projects.
def get_json(url: str):
    """
    Fetches JSON data from a given URL.
    """
    import requests # Import requests here if not imported globally in utils
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# If your project uses memoize, keep this.
def memoize(fn):
    """
    Decorator to memoize a method's results.
    """
    attr_name = '_memoized_results_' + fn.__name__

    def wrapper(self, *args):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, {})
        
        key = args 
        if key not in getattr(self, attr_name):
            getattr(self, attr_name)[key] = fn(self, *args)
        return getattr(self, attr_name)[key]
    return wrapper

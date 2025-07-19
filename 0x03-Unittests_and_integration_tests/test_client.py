# utils.py
import requests
import functools # Needed for memoize

def get_json(url: str) -> dict:
    """Fetches JSON data from a given URL."""
    # In a real scenario, this would make an actual HTTP request.
    # For testing, it's often mocked, but it must be a valid function.
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        # You might want to log this or handle it differently in production code
        print(f"Error fetching URL {url}: {e}")
        raise # Re-raise to ensure tests catch unexpected network issues

def access_nested_map(nested_map: dict, path: list):
    """Accesses a value in a nested dictionary using a list of keys."""
    # This is a common implementation for access_nested_map
    current_map = nested_map
    for key in path:
        current_map = current_map[key]
    return current_map

def memoize(func):
    """Decorator to cache the results of a method call."""
    # A simple memoize decorator for methods that don't take extra arguments beyond 'self'
    # For more complex memoization, you'd need to consider args/kwargs for the cache key.
    attr_name = '_memoized_' + func.__name__

    @functools.wraps(func)
    def memoized_wrapper(self, *args, **kwargs):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self, *args, **kwargs))
        return getattr(self, attr_name)
    return memoized_wrapper

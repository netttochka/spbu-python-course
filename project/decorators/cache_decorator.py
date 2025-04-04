from collections import OrderedDict
from functools import wraps


def cache_results(max_cache_size=0):
    """Decorator to cache function results.

    Args:
        max_cache_size (int): The maximum number of results to cache.
                               Default is 0, which means no caching.

    Returns:
        function: The wrapped function with caching behavior.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a cache key based on the function arguments
            key = (args, frozenset(kwargs.items()))

            # Initialize cache if it doesn't exist
            if not hasattr(wrapper, "cache"):
                wrapper.cache = (
                    OrderedDict()
                )  # Using OrderedDict to maintain insertion order

            if not hasattr(wrapper, "calls"):
                wrapper.calls = 0  # Initialize call counter on the wrapper

            # Check if the result is already in the cache
            if key in wrapper.cache:
                return wrapper.cache[key]

            # Call the function and cache the result
            result = func(*args, **kwargs)
            wrapper.cache[key] = result
            wrapper.calls += 1  # Increment the call counter on the wrapper

            # Remove the oldest item if the cache exceeds the max size
            if max_cache_size > 0 and len(wrapper.cache) > max_cache_size:
                wrapper.cache.popitem(last=False)  # Remove the oldest item

            return result

        return wrapper

    return decorator

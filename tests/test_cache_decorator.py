from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from project.decorators.cache_decorator import cache_results
from collections import OrderedDict

# Example usage of the decorator
@cache_results(max_cache_size=3)
def expensive_computation(x, y=0):
    """Simulates an expensive computation.

    Args:
        x (int): First parameter.
        y (int, optional): Second parameter. Defaults to 0.

    Returns:
        int: The sum of x and y.
    """
    print(f"Computing result for ({x}, {y})")
    return x + y


# Example usage of the decorator on built-in functions
@cache_results(max_cache_size=3)
def cached_sum(*args):
    """Calculates the sum of the provided arguments."""
    return sum(args)


@cache_results(max_cache_size=3)
def cached_max(*args):
    """Returns the maximum of the provided arguments."""
    return max(args)


# Tests
def test_cache_no_caching():
    """Test the function without caching."""
    expensive_computation.calls = 0  # Call counter
    expensive_computation.cache = OrderedDict()

    result1 = expensive_computation(1)
    assert result1 == 1
    assert expensive_computation.calls == 1  # Should be called once

    result2 = expensive_computation(1)
    assert result2 == result1  # Result should be from cache
    assert expensive_computation.calls == 1  # No additional call

    assert expensive_computation(2) == 2  # New arguments, should compute again
    assert expensive_computation.calls == 2  # Should be called a second time


def test_cache_with_size_limit():
    """Test the function with caching and a size limit."""
    expensive_computation.calls = 0  # Call counter
    expensive_computation.cache = OrderedDict()

    assert expensive_computation(1) == 1  # Compute and cache (1, 0)
    assert expensive_computation.calls == 1  # Should be called once

    assert expensive_computation(2) == 2  # Compute and cache (2, 0)
    assert expensive_computation.calls == 2  # Should be called twice

    assert expensive_computation(1) == 1  # Use cache for (1, 0)
    assert expensive_computation.calls == 2  # No additional call

    # Cache contains (1, 0) and (2, 0)
    assert expensive_computation(3) == 3  # Compute and cache (3, 0)
    assert expensive_computation.calls == 3  # Should be called three times

    # Cache contains (1, 0), (2, 0), and (3, 0)
    assert expensive_computation(4) == 4  # Compute and cache (4, 0)
    assert expensive_computation.calls == 4  # Should be called four times

    # Cache now contains (2, 0), (3, 0), and (4, 0); (1, 0) should be evicted
    assert expensive_computation(2) == 2  # Use cache for (2, 0)
    assert expensive_computation(3) == 3  # Use cache for (3, 0)
    assert expensive_computation.calls == 4  # No additional calls

    # Since (1, 0) was evicted, this call should compute again
    assert expensive_computation(1) == 1
    assert expensive_computation.calls == 5  # Should be called five times


def test_cache_varied_arguments():
    """Test the function with varied arguments."""
    expensive_computation.calls = 0  # Call counter
    expensive_computation.cache = OrderedDict()

    assert expensive_computation(5, y=10) == 15  # Compute and cache (5, 10)
    assert expensive_computation.calls == 1  # Should be called once

    assert expensive_computation(5, y=10) == 15  # Use cache for (5, 10)
    assert expensive_computation.calls == 1  # No additional call

    assert expensive_computation(5, y=20) == 25  # Compute and cache (5, 20)
    assert expensive_computation.calls == 2  # Should be called twice

    # Cache contains (5, 10) and (5, 20)
    assert expensive_computation(10) == 10  # Compute and cache (10, 0)
    assert expensive_computation.calls == 3  # Should be called three times

    # Cache contains (5, 10), (5, 20), and (10, 0)
    assert expensive_computation(15, y=5) == 20  # Compute and cache (15, 5)
    assert expensive_computation.calls == 4  # Should be called four times

    # (5, 10) should be evicted as the cache reached its limit
    assert expensive_computation(5, y=10) == 15  # Should compute again (5, 10)
    assert expensive_computation.calls == 5  # Should be called five times


# Tests for cached_sum
def test_cached_sum_no_caching():
    """Test the cached_sum function without caching."""
    cached_sum.calls = 0  # Call counter
    cached_sum.cache = OrderedDict()

    result1 = cached_sum(1, 2)
    assert result1 == 3
    assert cached_sum.calls == 1  # Should be called once

    result2 = cached_sum(1, 2)
    assert result2 == result1  # Result should be from cache
    assert cached_sum.calls == 1  # No additional call

    assert cached_sum(3, 4) == 7  # New arguments, should compute again
    assert cached_sum.calls == 2  # Should be called a second time


def test_cached_sum_with_size_limit():
    """Test the cached_sum function with caching and a size limit."""
    cached_sum.calls = 0  # Call counter
    cached_sum.cache = OrderedDict()

    assert cached_sum(1, 2) == 3  # Compute and cache (1, 2)
    assert cached_sum.calls == 1  # Should be called once

    assert cached_sum(2, 3) == 5  # Compute and cache (2, 3)
    assert cached_sum.calls == 2  # Should be called twice

    assert cached_sum(1, 2) == 3  # Use cache for (1, 2)
    assert cached_sum.calls == 2  # No additional call

    # Cache contains (1, 2) and (2, 3)
    assert cached_sum(3, 4) == 7  # Compute and cache (3, 4)
    assert cached_sum.calls == 3  # Should be called three times

    # Cache contains (1, 2), (2, 3), and (3, 4)
    assert cached_sum(4, 5) == 9  # Compute and cache (4, 5)
    assert cached_sum.calls == 4  # Should be called four times

    # Cache now contains (2, 3), (3, 4), and (4, 5); (1, 2) should be evicted
    assert cached_sum(2, 3) == 5  # Use cache for (2, 3)
    assert cached_sum(3, 4) == 7  # Use cache for (3, 4)
    assert cached_sum.calls == 4  # No additional calls

    # Since (1, 2) was evicted, this call should compute again
    assert cached_sum(1, 2) == 3
    assert cached_sum.calls == 5  # Should be called five times


# Tests for cached_max
def test_cached_max_no_caching():
    """Test the cached_max function without caching."""
    cached_max.calls = 0  # Call counter
    cached_max.cache = OrderedDict()

    result1 = cached_max(1, 2)
    assert result1 == 2
    assert cached_max.calls == 1  # Should be called once

    result2 = cached_max(1, 2)
    assert result2 == result1  # Result should be from cache
    assert cached_max.calls == 1  # No additional call

    assert cached_max(3, 4) == 4  # New arguments, should compute again
    assert cached_max.calls == 2  # Should be called a second time


def test_cached_max_with_size_limit():
    """Test the cached_max function with caching and a size limit."""
    cached_max.calls = 0  # Call counter
    cached_max.cache = OrderedDict()

    assert cached_max(1, 2) == 2  # Compute and cache (1, 2)
    assert cached_max.calls == 1  # Should be called once

    assert cached_max(2, 3) == 3  # Compute and cache (2, 3)
    assert cached_max.calls == 2  # Should be called twice

    assert cached_max(1, 2) == 2  # Use cache for (1, 2)
    assert cached_max.calls == 2  # No additional call

    # Cache contains (1, 2) and (2, 3)
    assert cached_max(3, 4) == 4  # Compute and cache (3, 4)
    assert cached_max.calls == 3  # Should be called three times

    # Cache contains (1, 2), (2, 3), and (3, 4)
    assert cached_max(4, 5) == 5  # Compute and cache (4, 5)
    assert cached_max.calls == 4  # Should be called four times

    # Cache now contains (2, 3), (3, 4), and (4, 5); (1, 2) should be evicted
    assert cached_max(2, 3) == 3  # Use cache for (2, 3)
    assert cached_max(3, 4) == 4  # Use cache for (3, 4)
    assert cached_max.calls == 4  # No additional calls

    # Since (1, 2) was evicted, this call should compute again
    assert cached_max(1, 2) == 2
    assert cached_max.calls == 5  # Should be called five times

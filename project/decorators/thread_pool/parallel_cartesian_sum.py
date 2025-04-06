from concurrent.futures import ProcessPoolExecutor
import itertools
from typing import List


def product_sum(pair: tuple) -> int:
    """
    Calculate the sum of elements in a single pair of Cartesian product.

    Args:
        pair (tuple): A tuple representing a single element in the Cartesian product.

    Returns:
        int: The sum of elements in the tuple.
    """
    return sum(pair)


def parallel_cartesian_sum(sets: List[List[int]]) -> int:
    """
    Calculate the sum of the Cartesian product of multiple sets using parallel processing.

    Args:
        sets (List[List[int]]): A list of sets (each set is represented as a list of integers).

    Returns:
        int: The sum of all elements in the Cartesian product.
    """
    # Compute the full Cartesian product of all sets
    product = list(itertools.product(*sets))

    # Use ProcessPoolExecutor for parallel processing
    with ProcessPoolExecutor() as executor:
        # Map the product_sum function to each element in the Cartesian product
        partial_sum = list(executor.map(product_sum, product))

    # Sum all the partial sums
    return sum(partial_sum)

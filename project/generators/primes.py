from typing import Callable, Generator


def prime_generator() -> Generator[int, None, None]:
    """
    A generator that yields prime numbers indefinitely.
    """
    num = 2
    while True:
        is_prime = True
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            yield num
        num += 1


# Initialize the global prime generator once
prime_gen = prime_generator()


def prime_decorator(func: Callable[[int], int]) -> Callable[[int], int]:
    """
    A decorator that wraps a function to return the k-th prime number.

    Args:
        func (Callable[[int], int]): A function that takes an integer (prime)
                                      and returns an integer (the prime).

    Returns:
        Callable[[int], int]: A wrapped function that returns the k-th prime number.

    Raises:
        ValueError: If k is less than 1.
    """
    current_prime_index = 0  # Track the index of the next prime to be generated

    def wrapper(k: int) -> int:
        nonlocal current_prime_index

        if k < 1:
            raise ValueError("k must be greater than or equal to 1")

        # If the requested prime is greater than the last generated, continue
        # where we left off
        if k > current_prime_index:
            # Skip to the correct prime number
            for _ in range(k - current_prime_index):
                prime = next(prime_gen)
            current_prime_index = k  # Update the current prime index

        return func(prime)

    return wrapper


@prime_decorator
def get_kth_prime(prime: int) -> int:
    """
    Function to return the k-th prime number.

    Args:
        prime (int): The k-th prime number, provided by the decorator.

    Returns:
        int: The k-th prime number.
    """
    return prime

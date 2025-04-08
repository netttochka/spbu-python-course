from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from project.generators.primes import get_kth_prime, prime_generator

# Prime Number Test
@pytest.mark.parametrize(
    "k, expected",
    [
        (1, 2),
        (2, 3),
        (3, 5),
        (4, 7),
        (5, 11),
    ],
)
def test_get_kth_prime(k, expected):
    assert get_kth_prime(k) == expected


# Exclusion test for k < 1
@pytest.mark.parametrize("k", [-1, 0])
def test_get_kth_prime_invalid_k(k):
    with pytest.raises(ValueError, match="k must be greater than or equal to 1"):
        get_kth_prime(k)


def test_prime_generator_first_primes():
    """Test if the first few prime numbers are generated correctly."""
    prime_gen = prime_generator()
    assert next(prime_gen) == 2
    assert next(prime_gen) == 3
    assert next(prime_gen) == 5
    assert next(prime_gen) == 7
    assert next(prime_gen) == 11
    assert next(prime_gen) == 13

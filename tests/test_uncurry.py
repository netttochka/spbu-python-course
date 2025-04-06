from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from project.decorators.curry import curry_explicit
from project.decorators.uncurry import uncurry_explicit

# uncurry tests
def test_uncurry_basic():
    f2 = curry_explicit(lambda x, y, z: f"<{x},{y}, {z}>", 3)
    g2 = uncurry_explicit(f2, 3)
    assert g2(1, 2, 3) == "<1,2, 3>"


def test_uncurry_arity_mismatch():
    f = curry_explicit(lambda x, y: x + y, 2)
    g = uncurry_explicit(f, 2)
    with pytest.raises(TypeError):
        g(1)  # Not enough arguments


def test_uncurry_single_argument():
    f = curry_explicit(lambda x: x * 2, 1)
    g = uncurry_explicit(f, 1)
    assert g(5) == 10


def test_uncurry_multiple_arguments():
    f = curry_explicit(lambda a, b, c: a * b + c, 3)
    g = uncurry_explicit(f, 3)
    assert g(2, 3, 4) == 10  # 2 * 3 + 4 = 10


def test_uncurry_with_string():
    f = curry_explicit(lambda x, y: f"Hello {x}, {y}!", 2)
    g = uncurry_explicit(f, 2)
    assert g("Alice", "Bob") == "Hello Alice, Bob!"


def test_uncurry_negative_arity():
    with pytest.raises(ValueError):
        uncurry_explicit(lambda x: x, -1)


def test_uncurry_too_many_arguments():
    f = curry_explicit(lambda x, y: x * y, 2)
    g = uncurry_explicit(f, 2)
    with pytest.raises(TypeError):
        g(2, 3, 4)  # Too many arguments


def test_uncurry_mixed_types():
    f = curry_explicit(lambda x, y, z: f"{x} + {y} = {z}", 3)
    g = uncurry_explicit(f, 3)
    assert g("1", "1", "2") == "1 + 1 = 2"


def test_uncurry_large_number_of_arguments():
    f = curry_explicit(lambda *args: sum(args), 5)
    g = uncurry_explicit(f, 5)
    assert g(1, 2, 3, 4, 5) == 15  # 1 + 2 + 3 + 4 + 5 = 15

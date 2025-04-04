from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from project.decorators.curry import curry_explicit

# curry tests
def test_curry_basic():
    f2 = curry_explicit(lambda x, y, z: f"<{x},{y}, {z}>", 3)
    assert f2(1)(2)(3) == "<1,2, 3>"


def test_curry_arity_1():
    f = curry_explicit(lambda x: x * 2, 1)
    assert f(5) == 10


def test_curry_arity_0():
    f = curry_explicit(lambda: "Hello, World!", 0)
    assert f() == "Hello, World!"


def test_curry_type_error():
    f = curry_explicit(lambda x, y: x + y, 2)
    with pytest.raises(TypeError):
        f(1)(2)(3)  # Extra argument


def test_negative_arity():
    with pytest.raises(ValueError):
        curry_explicit(lambda x: x, -1)


def test_curry_proper_usage():
    f = curry_explicit(lambda x, y, z: f"{x} {y} {z}", 3)
    assert f(1)(2)(3) == "1 2 3"
    assert f(1)(2)(0) == "1 2 0"


def test_curry_preserve_arity():
    # Define a function with multiple arguments
    original_function = lambda a, b, c, d: a + b + c + d
    curried_function = curry_explicit(original_function, 4)

    with pytest.raises(TypeError):
        curried_function(1)(2)(3)(4)(5)

    # Ensure the curried function works as expected
    assert curried_function(1)(2)(3)(4) == 10  # Full application
    assert curried_function(1)(1)(1)(1) == 4  # All arguments are 1
    assert curried_function(1)(2)(3)(-1) == 5  # Mix of positive and negative

    # Test partial applications with remaining arguments
    assert curried_function(1)(2)(3)(0) == 6  # Full application with last arg as 0
    assert curried_function(1)(2)(-1)(0) == 2  # Full application with mixed args

    # Additional test for partial application
    partial_application = curried_function(1)(2)
    assert partial_application(3)(4) == 10  # Checking for correct subsequent calls
    assert partial_application(-1)(-1) == 1  # Mix of positive and negative


def test_curry_with_builtin_functions():
    # Test with the built-in max function
    curried_max = curry_explicit(max, 3)
    assert curried_max(1)(2)(3) == 3
    assert curried_max(10)(20)(5) == 20

    # Test with the built-in sum function
    curried_sum = curry_explicit(sum, 2)
    assert curried_sum([1, 2])(3) == 6
    assert curried_sum([10, 20])(30) == 60

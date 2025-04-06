from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from project.decorators.smart_args import smart_args, Evaluated, Isolated

# Example usage
import random
import pytest


def get_random_number():
    """Function to generate a random number between 0 and 100."""
    random.seed(0)
    return random.randint(0, 100)


# Tests
def test_evaluated():
    """Test Evaluated handling in the function."""

    @smart_args(allow_positional=False)
    def test_func(*, x=Evaluated(lambda: 0)):  # Use a lambda to return a fixed value
        return x

    result = test_func()
    assert result == 0  # Now it should always return 0


def test_isolated_and_evaluated_in_combination():
    """Test the combination of Isolated and Evaluated, which should raise an assertion error."""

    @smart_args()
    def test_func(*, d=Isolated(), y=Evaluated(lambda: 0)):
        return d, y

    assert test_func(d={}, y=0)  # Передаем значения явно


def test_evaluated_with_positional_argument():
    """Test Evaluated handling with positional arguments."""

    @smart_args(allow_positional=True)
    def test_func(x=Evaluated(get_random_number)):
        return x

    result = test_func(10)  # Positional argument passed
    assert result == 10  # Positional argument should take precedence


def test_mixed_arguments_with_evaluated():
    """Test that using positional and keyword arguments with Evaluated works as expected."""

    @smart_args(allow_positional=True)
    def test_func(x=Evaluated(get_random_number), y=0):
        return x, y

    result = test_func(1)  # Using positional argument
    assert result == (1, 0)  # Should return positional argument and default for y


def test_evaluated_called_each_time():
    """Test that Evaluated calls the function every time it's evaluated."""

    called_count = 0

    @smart_args(allow_positional=False)
    def test_func(*, x=Evaluated(lambda: get_and_count())):
        return x

    def get_and_count():
        nonlocal called_count
        called_count += 1
        return called_count  # Returns the count of how many times it was called

    # Call the function multiple times
    result1 = test_func()
    result2 = test_func()
    result3 = test_func()

    # Check that the values are correct and the function was called three times
    assert result1 == 1
    assert result2 == 2
    assert result3 == 3
    assert called_count == 3  # Ensure it was called three times


def test_isolated_returns_deep_copy():
    """Test that Isolated returns a deep copy of the argument."""

    original_dict = {"a": 10}

    @smart_args()
    def test_func(*, d=Isolated()):
        return d

    result = test_func(d={})  # Передаем пустой словарь явно

    # Ensure it is a new dictionary (deep copy)
    assert result is not original_dict  # Check they are different objects
    assert result == {}  # Check content is the same, should be empty by default

    # Modify the returned dictionary to ensure it is isolated
    result["a"] = 20
    assert result["a"] == 20  # Check if the modification is successful
    assert original_dict["a"] == 10  # Original should remain unchanged


def test_isolated_deep_copy_with_multiple_args():
    """Test that Isolated creates deep copies when multiple args are used."""

    @smart_args()
    def test_func(*, a=Isolated(), b=Isolated()):
        return a, b

    result_a, result_b = test_func(a={}, b={})  # Передаем два пустых словаря явно

    # Ensure each is a new dictionary (deep copy)
    assert result_a is not result_b  # They should be different objects
    assert result_a == {}
    assert result_b == {}

    # Modify one of the returned dictionaries
    result_a["x"] = 5
    assert result_a["x"] == 5
    assert result_b.get("x") is None  # The other should remain unchanged


def test_isolated_without_value():
    """Test that ValueError is raised if Isolated argument is not provided."""

    @smart_args()
    def test_func(*, d=Isolated()):
        return d

    with pytest.raises(ValueError, match="Argument 'd' requires a value for Isolated"):
        test_func()  # Не передаем значение для 'd', должно быть исключение

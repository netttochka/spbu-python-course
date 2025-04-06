from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from project.generators.rgba import get_rgba_element, rgba_generator

# Тест для RGBA
@pytest.mark.parametrize(
    "i, expected",
    [
        (0, (0, 0, 0, 0)),
        (1, (0, 0, 0, 2)),
        (1020, (0, 0, 20, 0)),
    ],
)
def test_get_rgba_element(i, expected):
    assert get_rgba_element(i) == expected


def test_rgba_generator_first_colors():
    gen = rgba_generator()
    assert next(gen) == (0, 0, 0, 0)
    assert next(gen) == (0, 0, 0, 2)
    assert next(gen) == (0, 0, 0, 4)
    assert next(gen) == (0, 0, 0, 6)
    assert next(gen) == (0, 0, 0, 8)

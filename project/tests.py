from . import main

def test_1_vector_multiplication():
    assert main.vector_multiplication((1, 1), (1, 1)) == 2

def test_2_vector_multiplication():
    assert main.vector_multiplication((1, 1), (1, 1, 1)) is None


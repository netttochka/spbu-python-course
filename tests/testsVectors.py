from project import vectorOperations


def test_1_vector_multiplication():
    assert vectorOperations.vector_multiplication((1, 1), (1, 1)) == 2


def test_2_vector_multiplication():
    assert vectorOperations.vector_multiplication((1, 1), (1, 1, 1)) is None


def test_3_vector_multiplication():
    assert vectorOperations.vector_multiplication((3, 4), (4, 3)) == 24


def test_1_vector_length():
    assert vectorOperations.vector_length((1, 1, 1)) == 1


def test_2_vector_length():
    assert vectorOperations.vector_length((2, 2)) == 2


def test_3_vector_length():
    assert vectorOperations.vector_length((3, 4)) == 5


def test_1_vector_angle():
    assert vectorOperations.vector_angle((3, 4), (4, 3)) == 16


def test_2_vector_angle():
    assert vectorOperations.vector_angle((7, 1), (5, 5)) == 35


def test_3_vector_angle():
    assert vectorOperations.vector_angle((7, 1, 2), (5, 5)) is None


def test_4_vector_angle():
    assert vectorOperations.vector_angle((), ()) is None

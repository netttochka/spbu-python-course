from project import matrix_operations


def test_1_matrix_sum():
    assert matrix_operations.matrix_sum(
        [[1, 2, 3], [2, 3, 5]], [[0, 1, 2], [5, 6, 8]]
    ) == [[1, 3, 5], [7, 9, 13]]


def test_2_matrix_sum():
    assert (
        matrix_operations.matrix_sum([[1, 2], [2, 3, 5]], [[0, 1, 2], [5, 6, 8]])
        is None
    )


def test_1_matrix_multi():
    assert matrix_operations.matrix_mult([[1, 2], [2, 1]], [[0, 3], [5, -1]]) == [
        [10, 1],
        [5, 5],
    ]


def test_2_matrix_multi():
    assert matrix_operations.matrix_mult(
        [[-1, 31], [0, -5], [3, 0]], [[0, 3, 0], [5, -1, 0]]
    ) == [[155, -34, 0], [-25, 5, 0], [0, 9, 0]]


def test_3_matrix_multi():
    assert matrix_operations.matrix_mult([[-1], [0], [3]], [[0], [5]]) is None


def test_1_matrix_transposition():
    assert matrix_operations.matrix_transposition([[-1, 0, 3]]) == [[-1], [0], [3]]


def test_2_matrix_transposition():
    assert matrix_operations.matrix_transposition([[2, 0], [1, 2], [3, 5]]) == [
        [2, 1, 3],
        [0, 2, 5],
    ]

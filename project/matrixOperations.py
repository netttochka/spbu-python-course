from math import sqrt, acos, pi


def matrix_sum(matrix_1: list[list], matrix_2: list[list]):
    """Calculates the sum of two matrices.

    Args:
    -----
      matrix_1: The first matrix, represented as a list of lists.
      matrix_2: The second matrix, represented as a list of lists.

    Returns:
    --------
      The sum of the two matrices, represented as a list of lists.
      Returns None if the matrices have different dimensions.
    """
    if len(matrix_1) != len(matrix_2) or len(matrix_1[0]) != len(matrix_2[0]):
        return None
    else:
        sum_matrix = [
            [matrix_1[i][j] + matrix_2[i][j] for j in range(len(matrix_1[0]))]
            for i in range(len(matrix_1))
        ]
        return sum_matrix


def matrix_multi(matrix_1: list[list], matrix_2: list[list]):
    """Calculates the product of two matrices.

    Args:
    -----
      matrix_1: The first matrix, represented as a list of lists.
      matrix_2: The second matrix, represented as a list of lists.

    Returns:
    --------
      The product of the two matrices, represented as a list of lists.
      Returns None if the number of columns in the first matrix does not equal the number of rows in the second matrix.
    """

    if len(matrix_1[0]) != len(matrix_2):
        return None
    else:
        product_matrix = [
            [
                sum(matrix_1[i][k] * matrix_2[k][j] for k in range(len(matrix_1[0])))
                for j in range(len(matrix_2[0]))
            ]
            for i in range(len(matrix_1))
        ]
        return product_matrix


def matrix_transposition(matrix_1: list[list]):
    """Calculates the transpose of a matrix.

    Args:
    -----
      matrix_1: The input matrix, represented as a list of lists.

    Returns:
    --------
      The transpose of the input matrix, represented as a list of lists.
    """
    transpose = [
        [matrix_1[j][i] for j in range(len(matrix_1))] for i in range(len(matrix_1[0]))
    ]
    return transpose

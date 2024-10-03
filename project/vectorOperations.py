from math import sqrt, acos, pi


def vector_multiplication(vector_1: list[int], vector_2: list[int]):
    """Calculates the dot product of two vectors.

    Args:
    -----
      vector_1: The first vector, represented as a list of integers.
      vector_2: The second vector, represented as a list of integers.

    Returns:
    --------
      The dot product of the two vectors, or None if the vectors have different lengths.
    """
    if len(vector_1) != len(vector_2):
        return None
    s = 0
    for i in range(len(vector_1)):
        s += vector_1[i] * vector_2[i]
    return s


def vector_length(vector_1: list[int]):
    """Calculates the Euclidean length (magnitude) of a vector.

    Args:
    -----
      vector_1: The input vector, represented as a list of integers.

    Returns:
    --------
      The Euclidean length of the vector, rounded down to the nearest integer.
    """
    s = 0
    for i in range(len(vector_1)):
        s += pow(vector_1[i], 2)
    return int(sqrt(s))


def vector_angle(vector_1: list[int], vector_2: list[int]):
    """Calculates the angle between two vectors in degrees.

    Args:
    -----
      vector_1: The first vector, represented as a list of integers.
      vector_2: The second vector, represented as a list of integers.

    Returns:
    --------
      The angle between the two vectors in degrees, rounded to the nearest integer.
      Returns None if the vectors have different lengths or are both empty.
    """
    if len(vector_1) != len(vector_2):
        return None
    elif len(vector_1) == 0 and len(vector_2) == 0:
        return None
    else:
        cos_a_b = vector_multiplication(vector_1, vector_2) / (
            vector_length(vector_1) * vector_length(vector_2)
        )
        ac_a_b = acos(cos_a_b) * 180 / pi
        return round(ac_a_b)


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

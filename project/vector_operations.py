from math import sqrt, acos, pi


def vector_multiplication(vector_1: list[int], vector_2: list[int]) -> int | None:
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


def vector_length(vector_1: list[int]) -> int:
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


def vector_angle(vector_1: list[int], vector_2: list[int]) -> float | None:
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
        vec_mult = vector_multiplication(vector_1, vector_2)
        if vec_mult != None:
            cos_a_b = vec_mult / (vector_length(vector_1) * vector_length(vector_2))
            ac_a_b = acos(cos_a_b) * 180 / pi
            return round(ac_a_b)
        else:
            return None

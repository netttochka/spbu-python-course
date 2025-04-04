def uncurry_explicit(function, arity):
    """
    Uncurries a curried function to accept multiple arguments at once.

    Arguments:
    function -- The curried function to be uncurried.
    arity -- The number of arguments the function expects.

    Returns:
    A function that accepts all arguments at once.

    Raises:
    ValueError -- If arity is negative.
    TypeError -- If the wrong number of arguments is provided.
    """
    if arity < 0:
        raise ValueError("Arity cannot be negative")

    def uncurried(*args):
        if len(args) != arity:
            raise TypeError(f"Expected {arity} arguments, but got {len(args)}")
        result = function
        for arg in args:
            result = result(arg)
        return result

    return uncurried

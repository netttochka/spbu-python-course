def curry_explicit(function, arity):
    """
    Curries the given function to the specified arity.

    Arguments:
    function -- The original function to be curried.
    arity -- The number of arguments the function takes.

    Returns:
    A curried version of the function.

    Raises:
    ValueError -- If arity is negative.
    """
    if arity < 0:
        raise ValueError("Arity cannot be negative")
    if arity == 0:
        return lambda: function()

    def curried(arg):
        if curried.remaining_arity == 1:
            return function(arg)
        return curry_explicit(
            lambda *args: function(arg, *args), curried.remaining_arity - 1
        )

    curried.remaining_arity = arity
    return curried

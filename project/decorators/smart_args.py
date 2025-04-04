import copy
import inspect


class Evaluated:
    """Wrapper for evaluated default values. Expects a callable function."""

    def __init__(self, func):
        assert callable(func), "Evaluated expects a callable"
        self.func = func


class Isolated:
    """Placeholder for isolated default values that should be deeply copied."""

    pass


def smart_args(allow_positional=False):
    """
    Decorator to handle 'Evaluated' and 'Isolated' argument defaults.

    Args:
    allow_positional (bool): If True, positional arguments are allowed.
                             Otherwise, only keyword arguments are supported.

    Raises:
    - ValueError: If an Isolated argument is not provided with a value.
    """

    def decorator(func):
        """
        Decorator function that wraps the original function to handle
        'Evaluated' and 'Isolated' argument defaults.

        Args:
            func (callable): The function to be wrapped.

        Returns:
            callable: A wrapper function that processes the arguments before
                    calling the original function.
        """

        # Fetch full argument specification
        full_argspec = inspect.getfullargspec(func)
        defaults = full_argspec.defaults or []
        kwonly_defaults = full_argspec.kwonlydefaults or {}
        positional_args = full_argspec.args or []
        pos_defaults_offset = len(positional_args) - len(defaults)

        def wrapper(*args, **kwargs):
            """
            Wrapper function that processes arguments for the decorated function,
            handling special cases for 'Evaluated' and 'Isolated' argument defaults.

            Args:
                *args: Positional arguments passed to the original function.
                **kwargs: Keyword arguments passed to the original function.

            Returns:
                The result of the original function after processing the arguments.
            """

            # Check if positional arguments are allowed
            if not allow_positional:
                assert len(args) == 0, "Only keyword arguments are allowed"

            # Process named arguments
            bound_args = kwargs.copy()

            # Apply positional arguments (if allowed)
            for i, arg_value in enumerate(args):
                arg_name = positional_args[i]
                bound_args[arg_name] = arg_value

            # Handle default values for positional arguments
            for i, arg_name in enumerate(positional_args[pos_defaults_offset:]):
                if arg_name not in bound_args:
                    bound_args[arg_name] = defaults[i] if i < len(defaults) else None

            # Handle keyword-only arguments and apply defaults if necessary
            for kwarg_name, default_value in kwonly_defaults.items():
                if kwarg_name not in bound_args:
                    bound_args[kwarg_name] = default_value

            # Process Evaluated and Isolated
            for name, value in bound_args.items():
                if isinstance(value, Evaluated):
                    bound_args[name] = value.func()  # Evaluate function
                elif isinstance(value, Isolated):
                    # Ensure the value is provided in kwargs (not in bound_args)
                    if name not in kwargs:
                        raise ValueError(
                            f"Argument '{name}' requires a value for Isolated"
                        )
                    # Deep copy the value if it was provided
                    bound_args[name] = copy.deepcopy(kwargs[name])

            # Check for incorrect combination of Evaluated and Isolated
            for name in bound_args:
                if isinstance(bound_args[name], Evaluated) and isinstance(
                    bound_args[name], Isolated
                ):
                    raise ValueError(
                        f"Cannot combine Evaluated and Isolated for argument '{name}'"
                    )

            return func(**bound_args)

        return wrapper

    return decorator

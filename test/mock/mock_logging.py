# Variables keeping track of call arguments
debug_called_args = []
info_called_args = []
warning_called_args = []
error_called_args = []
critical_called_args = []


def reset_calls():
    """
    Resets all the call arguments.
    """
    # Reset all the called_args.
    global debug_called_args, info_called_args, warning_called_args, error_called_args, critical_called_args
    debug_called_args = []
    info_called_args = []
    warning_called_args = []
    error_called_args = []
    critical_called_args = []


class DebugMethod:
    """
    Simulates a debug method for the logging module.
    """


    def __init__(self, *args):
        """
        Simulates a debug method for the logging module.
        """
        # Append to the called_args.
        debug_called_args.append(args)


    @classmethod
    def assert_called_once(cls, *args):
        """
        Make sure that the debug_called_args has a length of exactly one.

        Raises:
            AssertionError : The method wasn't called with the arguments.
        """
        # Check the calls.
        if len(debug_called_args) < 1:
            raise AssertionError(f'debug was never called')
        elif len(debug_called_args) > 1:
            raise AssertionError(f'debug was called {len(debug_called_args)} times, not 1')


    @classmethod
    def assert_called_with(cls, *args):
        """
        Iterate through the debug_called_args and see if any calls line up.

        Raises:
            AssertionError : The method wasn't called with the arguments.
        """
        # Check the calls.
        if args not in debug_called_args:
            raise AssertionError(f'debug was never called with arguments {args}')


    @classmethod
    def assert_called_once_with(cls, *args):
        """
        Make sure that there was only one call and that it was called with the given arguments.

        Raises:
            AssertionError : The method wasn't called with the arguments.
        """
        # Assert that there is only one call.
        cls.assert_called_once()

        # Check the calls.
        if args not in debug_called_args:
            raise AssertionError(f'debug was never called with arguments {args}')


class InfoMethod:
    """
    Simulates a info method for the logging module.
    """


    def __init__(self, *args):
        """
        Simulates a info method for the logging module.
        """
        # Append to the called_args.
        info_called_args.append(args)


    @classmethod
    def assert_called_once(cls, *args):
        """
        Make sure that the info_called_args has a length of exactly one.

        Raises:
            AssertionError : The method wasn't called with the arguments.
        """
        # Check the calls.
        if len(info_called_args) < 1:
            raise AssertionError(f'info was never called')
        elif len(info_called_args) > 1:
            raise AssertionError(f'info was called {len(info_called_args)} times, not 1')


    @classmethod
    def assert_called_with(cls, *args):
        """
        Iterate through the info_called_args and see if any calls line up.

        Raises:
            AssertionError : The method wasn't called with the arguments.
        """
        # Check the calls.
        if args not in info_called_args:
            raise AssertionError(f'info was never called with arguments {args}')


    @classmethod
    def assert_called_once_with(cls, *args):
        """
        Make sure that there was only one call and that it was called with the given arguments.

        Raises:
            AssertionError : The method wasn't called with the arguments.
        """
        # Assert that there is only one call.
        cls.assert_called_once()

        # Check the calls.
        if args not in info_called_args:
            raise AssertionError(f'info was never called with arguments {args}')


class WarningMethod:
    """
    Simulates a warning method for the logging module.
    """


    def __init__(self, *args):
        """
        Simulates a warning method for the logging module.
        """
        # Append to the called_args.
        warning_called_args.append(args)


    @classmethod
    def assert_called_once(cls, *args):
        """
        Make sure that the warning_called_args has a length of exactly one.

        Raises:
            AssertionError : The method wasn't called with the arguments.
        """
        # Check the calls.
        if len(warning_called_args) < 1:
            raise AssertionError(f'warning was never called')
        elif len(warning_called_args) > 1:
            raise AssertionError(f'warning was called {len(warning_called_args)} times, not 1')


    @classmethod
    def assert_called_with(cls, *args):
        """
        Iterate through the warning_called_args and see if any calls line up.

        Raises:
            AssertionError : The method wasn't called with the arguments.
        """
        # Check the calls.
        if args not in warning_called_args:
            raise AssertionError(f'warning was never called with arguments {args}')


    @classmethod
    def assert_called_once_with(cls, *args):
        """
        Make sure that there was only one call and that it was called with the given arguments.

        Raises:
            AssertionError : The method wasn't called with the arguments.
        """
        # Assert that there is only one call.
        cls.assert_called_once()

        # Check the calls.
        if args not in warning_called_args:
            raise AssertionError(f'warning was never called with arguments {args}')


class ErrorMethod:
    """
    Simulates a error method for the logging module.
    """


    def __init__(self, *args):
        """
        Simulates a error method for the logging module.
        """
        # Append to the called_args.
        error_called_args.append(args)


    @classmethod
    def assert_called_once(cls, *args):
        """
        Make sure that the error_called_args has a length of exactly one.

        Raises:
            AssertionError : The method wasn't called with the arguments.
        """
        # Check the calls.
        if len(error_called_args) < 1:
            raise AssertionError(f'error was never called')
        elif len(error_called_args) > 1:
            raise AssertionError(f'error was called {len(error_called_args)} times, not 1')


    @classmethod
    def assert_called_with(cls, *args):
        """
        Iterate through the error_called_args and see if any calls line up.

        Raises:
            AssertionError : The method wasn't called with the arguments.
        """
        # Check the calls.
        if args not in error_called_args:
            raise AssertionError(f'error was never called with arguments {args}')


    @classmethod
    def assert_called_once_with(cls, *args):
        """
        Make sure that there was only one call and that it was called with the given arguments.

        Raises:
            AssertionError : The method wasn't called with the arguments.
        """
        # Assert that there is only one call.
        cls.assert_called_once()

        # Check the calls.
        if args not in error_called_args:
            raise AssertionError(f'error was never called with arguments {args}')


class CriticalMethod:
    """
    Simulates a critical method for the logging module.
    """


    def __init__(self, *args):
        """
        Simulates a critical method for the logging module.
        """
        # Append to the called_args.
        critical_called_args.append(args)


    @classmethod
    def assert_called_once(cls, *args):
        """
        Make sure that the critical_called_args has a length of exactly one.

        Raises:
            AssertionError : The method wasn't called with the arguments.
        """
        # Check the calls.
        if len(critical_called_args) < 1:
            raise AssertionError(f'critical was never called')
        elif len(critical_called_args) > 1:
            raise AssertionError(f'critical was called {len(critical_called_args)} times, not 1')


    @classmethod
    def assert_called_with(cls, *args):
        """
        Iterate through the critical_called_args and see if any calls line up.

        Raises:
            AssertionError : The method wasn't called with the arguments.
        """
        # Check the calls.
        if args not in critical_called_args:
            raise AssertionError(f'critical was never called with arguments {args}')


    @classmethod
    def assert_called_once_with(cls, *args):
        """
        Make sure that there was only one call and that it was called with the given arguments.

        Raises:
            AssertionError : The method wasn't called with the arguments.
        """
        # Assert that there is only one call.
        cls.assert_called_once()

        # Check the calls.
        if args not in critical_called_args:
            raise AssertionError(f'critical was never called with arguments {args}')


# Set local variables
debug = DebugMethod
info = InfoMethod
warning = WarningMethod
error = ErrorMethod
critical = CriticalMethod

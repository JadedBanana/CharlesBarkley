"""
Environment file. Helps with managing dozens of environment variables.
"""
# Imports
from lib.util.exceptions import UndefinedVariableError
import os

# List of variables we should expect to see in every .env file.
EXPECTED_DOTENV_VARS = [
    'DEPLOYMENT_CLIENT', 'VERSION_NUMBER', 'LAUNCH_RUN_CRONCHECK', 'DEVELOPER_DISCORD_IDS',
    'LOGGING_LEVEL', 'LOG_TO_CONSOLE', 'LOG_TO_FILE', 'DO_LEVEL_HEADERS', 'DO_TIMESTAMPS', 'LOGS_DIR',
    'BOT_TOKEN', 'GLOBAL_PREFIX',
    'YOUTUBE_API_KEY', 'YOUTUBE_SEARCH_COUNT', 'YOUTUBE_RICKROLL_CHANCE'
]
# List of expected .env types. Used in both load_dotenv and get.
EXPECTED_DOTENV_TYPES = {
    'DEPLOYMENT_CLIENT': bool,
    'LAUNCH_RUN_CRONCHECK': bool,
    'DEVELOPER_DISCORD_IDS': list,
    'LOGGING_LEVEL': int,
    'LOG_TO_CONSOLE': bool,
    'LOG_TO_FILE': bool,
    'DO_LEVEL_HEADERS': bool,
    'DO_TIMESTAMPS': bool,
    'YOUTUBE_SEARCH_COUNT': int,
    'YOUTUBE_RICKROLL_CHANCE': int
}


def load_dotenv():
    """
    Loads the .env file. Also checks to make sure that the file exists, and that all required
    variables are accounted for.

    Raises:
        InvalidDotenvFileError : .env file is either missing or is lacking a required variable.
    """
    # Required imports
    from lib.util.exceptions import InvalidDotenvFileError

    # First, check that the .env file does exist.
    if not os.path.exists('.env'):
        raise InvalidDotenvFileError('.env file missing from working directory')

    # Then, load .env.
    from dotenv import load_dotenv as dotenv_load
    dotenv_load()

    # Detect if any dotenv_vars are missing.
    for dotenv_var in EXPECTED_DOTENV_VARS:
        if dotenv_var not in os.environ.keys():
            raise InvalidDotenvFileError(f'Missing variable {dotenv_var}')

    # Detect any non-str data types.
    # List is excluded from this check, as the only way to derive lists in .env is to split them by comma.
    for var_name in EXPECTED_DOTENV_TYPES:
        # Bool detection (written as 0 or 1 in .env file, for simplicity) and integer protection are packaged together.
        if EXPECTED_DOTENV_TYPES[var_name] is bool or EXPECTED_DOTENV_TYPES[var_name] is int:
            try:
                int(os.environ[var_name])
            except ValueError:
                raise InvalidDotenvFileError(f'Variable {var_name} is not of type {EXPECTED_DOTENV_TYPES[var_name]}')


def get(variable_name):
    """
    Returns a variable declared in the .env file.
    Acts as a semi-wrapper for os.environ, with minor differences.
    Will only return values declared in the .env file.

    Arguments:
        variable_name (str) : The name of the desired variable.

    Returns:
        bool | int | str | list : Either a boolean, integer, string, or list value, depending on the variable.

    Raises:
        UndefinedVariableError: The variable name provided is not one that is provided in the .env file.
    """
    # Check to make sure the variable name is a valid one.
    if variable_name not in EXPECTED_DOTENV_VARS:
        raise UndefinedVariableError(f'{variable_name} is not a valid .env variable')

    # If variable type is str, simply return it.
    if variable_name not in EXPECTED_DOTENV_TYPES:
        return os.environ[variable_name]

    # If variable type is list, return the string value split by ','.
    if EXPECTED_DOTENV_TYPES[variable_name] is list:
        return os.environ[variable_name].split(',')

    # If variable type is other (integer or boolean), first get the integer value.
    var_int = int(os.environ[variable_name])
    # Return it straight if int, otherwise typecast it to bool.
    return var_int if EXPECTED_DOTENV_TYPES[variable_name] is int else bool(var_int)
"""
Parsing class helps with understanding commands more easily.
There are multiple methods that help with picking out pieces and piecing things together.
"""
# Imports
from lib.util import environment


def normalize_string(input_str, remove_double_spaces=True):
    """
    Removes spaces at the start and end of strings, as well as double spaces, newlines, and tabs in strings.
    """
    # Newlines, tabs
    input_str = input_str.replace('\t', ' ').replace('\n', ' ')

    # Start spaces
    while input_str.startswith(' '):
        input_str = input_str[1:]

    # End spaces
    while input_str.endswith(' '):
        input_str = input_str[:len(input_str) - 1]

    # Double spaces
    if remove_double_spaces:
        while '  ' in input_str:
            input_str = input_str.replace('  ', ' ')

    # Return
    return input_str


def get_command_from_message(message):
    """
    Gets a command from a message, with one argument after
    """
    # Immediately returns if command prefix is missing
    if not message.content.lower().startswith(environment.get("GLOBAL_PREFIX")):
        return None, None

    # Removes global prefix from message
    message = message.content[len(environment.get("GLOBAL_PREFIX")):]

    # Finds space or end of line -- whichever comes first, and returns
    end_index = message.find(' ')
    if not end_index + 1:
        return message, None
    return message[:end_index].lower(), message[end_index + 1:]
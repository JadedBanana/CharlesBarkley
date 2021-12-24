"""
Parsing class helps with understanding commands more easily.
There are multiple methods that help with picking out pieces and piecing things together.
"""


def normalize_string(input_str):
    """
    Removes spaces at the start and end of strings, as well as double spaces, newlines, and tabs in strings.

    Arguments:
        input_str (str) : The string to be normalized.

    Returns:
        str : The normalized string.
    """
    # If it's not a string, then just return it.
    if not isinstance(input_str, str):
        return input_str

    # Newlines, tabs
    input_str = input_str.replace('\t', ' ').replace('\n', ' ')

    # Remove spaces on the ends
    input_str = input_str.strip(' ')

    # Double spaces
    while '  ' in input_str:
        input_str = input_str.replace('  ', ' ')

    # Return
    return input_str


def get_command_from_message(global_prefix, message):
    """
    Splits a message's contents into command and argument.
    If either one can't be found, then None is returned in its stead.

    Arguments:
        global_prefix (str) : The global prefix.
        message (discord.message.Message) : The discord message object that triggered this command.

    Returns:
        str, str : The command, then the argument in that order.
    """
    # Immediately returns if command prefix is missing
    if not message.content.lower().startswith(global_prefix):
        return None, None

    # Removes global prefix from message
    message = message.content[len(global_prefix):]

    # Finds space or end of line -- whichever comes first, and returns
    end_index = message.find(' ')
    if not end_index + 1:
        return message.lower(), None
    return message[:end_index].lower(), message[end_index + 1:]

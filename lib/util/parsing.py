"""
Parsing class helps with understanding commands more easily.
There are multiple methods that help with picking out pieces and piecing things together.
"""
# One constant.
EMOJI_MIN_ORD = 8805


def normalize_string(input_str, remove_emojis=False):
    """
    Removes spaces at the start and end of strings, as well as double spaces, newlines, and tabs in strings.

    Arguments:
        input_str (str) : The string to be normalized.
        remove_emojis (bool) : Whether to remove emojis.

    Returns:
        str : The normalized string.
    """
    # If it's not a string, then just return it.
    if not isinstance(input_str, str):
        return input_str

    # Emojis
    if remove_emojis:
        # Iterate through each character in the name and pull out any characters with ord's greater than the max.
        i = 0
        while i < len(input_str):
            if ord(input_str[i]) > EMOJI_MIN_ORD:
                input_str = input_str.replace(input_str[i], '')
            else:
                i += 1

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

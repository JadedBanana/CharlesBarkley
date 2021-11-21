"""
Parsing class helps with understanding commands more easily.
There are multiple methods that help with picking out pieces and piecing things together.
"""

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
"""
Arguments file helps with managing differently formatted arguments.
"""
# Imports
from lib.util import parsing


# Variable statements.
CONVERT_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+_'
MAX_CONVERT_DEPTH = -16
NONDECIMAL_BASES = {
    '0x': [16, 'hexadecimal'],
    '0d': [12, 'duodecimal'],
    '0o': [8, 'octal'],
    '0b': [2, 'binary']
}


def convert_num_to_decimal(n, base):
    """
    Converts a number to decimal from another base.

    Arguments:
        n (str) : The string version of the number.
        base (int) : The base.

    Raises:
        ValueError : There's more than one decimal place in the number, or the base is a negative number,
                     or n uses an unexpected character.

    Returns:
        int | float : The converted number, in decimal.
    """
    # Error handling; make sure the base > 1 and that there's only one decimal point.
    if base < 2:
        raise ValueError("Base less than 2")
    if n.count('.') > 1:
        raise ValueError('More than one decimal point in n')

    # If there is no decimal point, we take the easy way out.
    if '.' not in n:
        return int(n, base=base)

    # Get the index of the decimal point and take the easy way out for the numbers BEFORE the decimal point.
    per_index = n.find('.')
    decimal_num = int(n[:per_index], base=base)

    # We add a little leniency for those below base 36 in terms of capitalization for the next part.
    if base <= 36:
        n = n.upper()

    # Iterate through the remaining numbers' decimal points.
    for index in range(per_index + 1, len(n)):
        # This math works by multiplying the converted numbers by their exponents then adding them onto final_num.
        exp = per_index - index
        # Get the decimal number of the current character
        num_of_char = CONVERT_CHARS.find(n[index])
        # A little error handling for characters that aren't in the list or are more than this base can handle
        if num_of_char == -1 or num_of_char >= base:
            raise ValueError('Unexpected character')
        # Then add it to the decimal number.
        else:
            decimal_num += base ** exp * num_of_char

    # Return the decimal number.
    return decimal_num


def convert_num_from_decimal(n, base):
    """
    Converts a number from decimal to another base.

    Arguments:
        n (float) : The number, represented as a float.
        base (int) : The base.

    Returns:
        str : The converted number represented as a string.
    """
    # Gets maximum exponent that will be necessary to dissect this number.
    exp = 0
    while base**(exp  + 1) <= n:
        exp+= 1

    # Adds all the numbers that aren't a multiple of base to the string.
    num_str = ''
    while n != 0 and exp >= MAX_CONVERT_DEPTH:
        # Adds a decimal point if we're below 0 exp.
        if exp == -1:
            num_str+= '.'
        # Grab the correct num character and add it to the string.
        num_str += CONVERT_CHARS[int(n / base ** exp)]
        # Subtract our remaining number and exponent.
        n -= (int(n / base**exp) * base**exp)
        exp-= 1

    # Adds all the zeros between exp and 0 if exp is not below 0.
    while exp >= 0:
        num_str+= '0'
        exp-= 1

    # Return the converted number.
    return num_str


def get_multibased_num_from_argument(argument):
    """
    Gets the number from an argument.
    Numbers can be in base 2, 8, 10, 12, or 16, but non-10 bases must be preceded
    by their respective prefixes.

    Returns:
        int : The integer version of the parsed number.

    Raises:
        ValueError : Incorrectly formatted number.

    Returns:
        int | float : The specified number, in decimal.
    """
    # Gets usages for arguments
    argument = parsing.normalize_string(argument)
    argument2 = argument.lower()

    # Go through nondecimal bases.
    for base in NONDECIMAL_BASES:
        if argument2.startswith(base):
            # Attempt to convert.
            return convert_num_to_decimal(argument[2:], NONDECIMAL_BASES[base][0])

    # If we've made it this far, then it means that the number is a decimal base.
    return float(argument)
"""
Misc util methods module.
Has a lot of very different methods.
"""
# Package Imports
import colorsys


# Constants.
CONVERT_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+_'
MAX_CONVERT_DEPTH = -16


def format_time_delta_str(time_delta):
    """
    Creates the time delta string.

    Arguments:
        time_delta (datetime.time_delta) : The time delta (change in time).

    Returns:
        str : The time passage string (formatted like {days}d {hours}h {mins}m {seconds}s).
    """
    # Starts out with empty time string.
    time_str = ''

    # Add on the days.
    if time_delta.days:
        time_str += str(time_delta.days) + 'd '

    # Add on the hours.
    if int(time_delta.seconds / 3600):
        time_str += str(int(time_delta.seconds / 3600)) + 'h '

    # Add on the minutes.
    if int(time_delta.seconds / 60):
        time_str += str(int(time_delta.seconds % 3600 / 60)) + 'm '

    # Add on the seconds.
    time_str += str(time_delta.seconds % 60) + 's'

    # Return the final string.
    return time_str


def get_multi_index(source, arg):
    """
    Gets multiple indexes for the argument in the source.
    For example, in the string 'aessdeeae', the letter 'e' appears at indexes 1, 5, 6, and 8.
    Therefore, calling this method with that string with 'e' as the arg will return [1, 5, 6, 8].

    Arguments:
        source (list | str) : An iterable object, such as a list or a str.
        arg (object) : An object that we may find in the source.

    Returns:
        int[] : A list of indexes.
                The arg appears in source at these indexes.
    """
    # List of all indexes, as well as the length we've removed.
    all_indexes = []
    len_removed = 0

    # Iterates through all the appearances of arg in the source.
    while arg in source:
        next_index = source.index(arg)

        # Updates outer variables.
        all_indexes.append(len_removed + next_index)
        len_removed += next_index + 1
        source = source[next_index + 1:]

    # Returns.
    return all_indexes


def upper_per_word(input_str):
    """
    Makes the beginning of every word an uppercase letter, and all others lowercase.

    Arguments:
        input_str (str) : The input string.

    Returns:
        str : The fully formatted string.
    """
    # Iterate through each letter.
    for i in range(len(input_str)):

        # If this is the first letter or there was a space before this one, make it uppercase.
        if i == 0 or input_str[i - 1] == ' ':
            input_str = input_str[:i] + input_str[i].upper() + input_str[i + 1:]

        # Otherwise, make it lowercase.
        else:
            input_str = input_str[:i] + input_str[i].lower() + input_str[i + 1:]

    # Return the updated string.
    return input_str


def find_color_tuple_midpoint_hsv(color1, color2, factor=0.5):
    """
    Finds the midpoint between the two RGB colors using HSV midpoints.

    Arguments:
        color1 (int, int, int) : The first color, in RGB.
        color2 (int, int, int) : The second color, in RGB.
        factor (float) : The factor of how much to blend them.
                         Lower factor = closer to color 1.
                         Higher factor = closer to color 2.
    """
    # Gets HSV versions of both colors.
    color1 = colorsys.rgb_to_hsv(color1[0] / 255, color1[1] / 255, color1[2] / 255)
    color2 = colorsys.rgb_to_hsv(color2[0] / 255, color2[1] / 255, color2[2] / 255)

    # Gets the average of both colors.
    color3 = colorsys.hsv_to_rgb(color1[0] * (1 - factor) + color2[0] * factor,
                                 color1[1] * (1 - factor) + color2[1] * factor,
                                 color1[2] * (1 - factor) + color2[2] * factor)

    # Return the color in the same format as before.
    return int(color3[0] * 255), int(color3[1] * 255), int(color3[2] * 255)


def multiply_int_tuple(int_tuple, factor=0.5):
    """
    Multiplies the values in the tuple by the factor.

    Arguments:
        int_tuple (tuple) : A tuple of any length, with just ints as its values.
        factor (float) : The factor by which to multiply them.
    """
    # Create a list for copying the tuple over.
    int_tuple2 = []

    # Add the original values to the new tuple.
    for i in range(len(int_tuple)):
        int_tuple2.append(int(int_tuple[i] * factor + 0.5))

    # Return the new tuple.
    return tuple(int_tuple2)


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


def get_string_closeness(source, arg):
    """
    Gets the string closeness for the argument in the given string.
    This is measured by the amount of the string is the argument divided by the length of the string.

    Returns:
        float : The amount of the string that is the argument.
    """
    # Simple replace and divide.
    return 1 - (len(source.replace(arg, '')) / len(source))

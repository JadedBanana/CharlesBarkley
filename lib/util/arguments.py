"""
Arguments module helps with managing differently formatted arguments.
"""
# Imports
from lib.util.exceptions import NoUserSpecifiedError, UnableToFindUserError
from lib.util import parsing, misc


# Variable statements.
CONVERT_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+_'
MAX_CONVERT_DEPTH = -16
NONDECIMAL_BASES = {
    '0x': 16,
    '0d': 12,
    '0o': 8,
    '0b': 2
}


def get_closest_users(message, argument, exclude_bots=False, exclude_users=None, limit=None):
    """
    Gets the closest users to the given argument. Returns a list of users.
    The closest user is the one that matches the closest as prioritized:
        1. nick
        2. username
        3. id
    In the form of COUNT, INDEX(ES), and NON-ARGUMENT CHARACTER COUNT.
    If two users match in one, the next best values are compared.
    If two users match for all three, the preexisting one is prioritized.
    Users can be chosen more than once, but priority will be given to ones that also match once it has been put into the list.
    Duplicate users will be removed at the end.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
        argument (str) : The command's argument, if any.
        exclude_bots (bool) : Whether or not to exclude bots from the list. Defaults to False.
        exclude_users (list) : Which users to exclude from the list. Defaults to None.
        limit (int) : The maximum amount of users in the list. Defaults to None.
    """
    # Checks to see if this message specifically mentions anyone.
    # If so, immediately return that.
    if message.mentions:
        return message.mentions

    # Normalize the argument, split it by its spaces.
    try:
        approx_user = parsing.normalize_string(argument).lower()

    # If the argument isn't a string, raise a NoUserSpecifiedError.
    except AttributeError:
        raise NoUserSpecifiedError()

    # If there is no argument left to parse, we raise NoUserSpecifiedError.
    if not approx_user or len(approx_user) < 3:
        raise NoUserSpecifiedError()

    # Otherwise, we search through the users and try to find matching strings.
    # First, we get a list of all users.
    all_users = misc.get_applicable_users(message, exclude_bots, exclude_users)

    # Then, we find the closest user.
    # This is prioritized as:
    #   1. nick
    #   2. username
    #   3. id
    # In the form of COUNT, INDEX(ES), and NON-ARGUMENT CHARACTER COUNT.
    # If two users match in one, the next best values are compared.
    # If two users match for all three, the preexisting one is prioritized.
    # Users can be chosen more than once, but priority will be given to ones that also match once it has been put into the list.
    # Duplicate users will be removed at the end.
    pointed_users = []

    # This list will store the following:
    #   1. The user object
    #   2. Whether or not the user is already in pointed_users
    #   3. The COUNTS for argument appearance in nick and username
    #   4. The INDEXES for argument appearance in nick and username
    #   5. The NON-ARGUMENT CHARACTER COUNT for argument appearance in nick and username
    #   6. The COUNTS, INDEXES, and NON-ARGUMENT CHARACTER COUNT for argument appearance in id
    current_user_priority = []

    # Iterate through all users
    for usr in all_users:

        # Test to see if argument is in the user's attributes described above
        if any([approx_user in str(attr).lower() for attr in [usr.name, usr.nick if usr.nick else '', usr.id]]):

            # Gathering the values for the attributes
            in_pointed_users = usr in pointed_users
            counts = [attr.lower().count(approx_user) for attr in [usr.name, usr.nick if usr.nick else '']]
            indexes = [misc.get_multi_index(attr.lower(), approx_user) for attr in [usr.name + '#' + usr.discriminator, usr.nick if usr.nick else '']]
            non_argument_char_count = [len(attr) - len(approx_user) * attr.lower().count(approx_user) for attr in [usr.name + '#' + usr.discriminator, usr.nick if usr.nick else '']]
            id_stuffs = [str(usr.id).count(approx_user), misc.get_multi_index(str(usr.id), approx_user), len(str(usr.id)) - len(approx_user) * str(usr.id).count(approx_user)]

            # Seeing if there is already a user in current_user_priority. If so, we do comparison.
            if current_user_priority:
                # If this user is the same as the one in current_user_priority, we continue.
                if usr == current_user_priority[0]:
                    continue

                # Otherwise, we prioritize the one that isn't already in_pointed_users.
                # If both, we let the first one stay.
                if in_pointed_users:
                    continue
                if current_user_priority[1]:
                    current_user_priority = [usr, in_pointed_users, counts, indexes, non_argument_char_count, id_stuffs]
                    continue

                # Gottem says whether or not we got one out in the previous check,
                gottem = False

                # Next, we check and see which has the highest count in username and nick.
                for i in range(2):
                    if current_user_priority[2][i] < counts[i]:
                        current_user_priority = [usr, in_pointed_users, counts, indexes, non_argument_char_count, id_stuffs]
                        gottem = True
                    elif current_user_priority[2][i] > counts[i]:
                        gottem = True

                # Do gottem check.
                if gottem:
                    continue

                # Next, we check and see whose occurrences happen FIRST.
                for i in range(2):
                    for j in range(len(current_user_priority[3][i])):
                        if current_user_priority[3][i][j] < indexes[i][j]:
                            current_user_priority = [usr, in_pointed_users, counts, indexes, non_argument_char_count, id_stuffs]
                            gottem = True
                        elif current_user_priority[3][i][j] > indexes[i][j]:
                            gottem = True

                # Do gottem check.
                if gottem:
                    continue

                # Next, we check and see which has the lowest non-argument character count in username and nick.
                for i in range(2):
                    if current_user_priority[4][i] > non_argument_char_count[i]:
                        current_user_priority = [usr, in_pointed_users, counts, indexes, non_argument_char_count, id_stuffs]
                        gottem = True
                    elif current_user_priority[4][i] < non_argument_char_count[i]:
                        gottem = True

                # Do gottem check.
                if gottem:
                    continue

                # Finally, we do the same for the id's.
                # First, the count.
                if current_user_priority[5][0] < id_stuffs[0]:
                    current_user_priority = [usr, in_pointed_users, counts, indexes, non_argument_char_count, id_stuffs]
                    continue
                elif current_user_priority[5][0] > id_stuffs[0]:
                    continue

                # Then, the indexes.
                for j in range(len(current_user_priority[5][1])):
                    if current_user_priority[5][1][j] < id_stuffs[1][j]:
                        current_user_priority = [usr, in_pointed_users, counts, indexes, non_argument_char_count, id_stuffs]
                        gottem = True
                    elif current_user_priority[5][1][j] > id_stuffs[1][j]:
                        gottem = True

                # Do gottem check.
                if gottem:
                    continue

                # Finally, the lowest non-argument character count.
                if current_user_priority[5][2] > id_stuffs[2]:
                    current_user_priority = [usr, in_pointed_users, counts, indexes, non_argument_char_count, id_stuffs]
                    continue
                elif current_user_priority[5][2] < id_stuffs[2]:
                    continue

            # If there isn't a user in the current_user_priority, we set it to the current one.
            else:
                current_user_priority = [usr, in_pointed_users, counts, indexes, non_argument_char_count, id_stuffs]

    # Now that that's out of the way, we test and see if the current_user_priority has a thing in it.
    if current_user_priority:
        # If it's already in pointed_users, we ignore it.
        if current_user_priority[0] not in pointed_users:
            pointed_users.append(current_user_priority[0])

    # If there is no current_user_priority, we throw an UnableToFindUserError.
    else:
        raise UnableToFindUserError(pointed_users, approx_user)

    # If we're operating under a limit, we return the second the limit matches.
    if limit:
        if len(pointed_users) == limit:
            return pointed_users

    # Return.
    return pointed_users


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
            return convert_num_to_decimal(argument[2:], NONDECIMAL_BASES[base])

    # If we've made it this far, then it means that the number is a decimal base.
    return float(argument)
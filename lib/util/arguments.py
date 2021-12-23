"""
Arguments module helps with managing differently formatted arguments.
"""
# Package Imports
from functools import cmp_to_key

# Local Imports
from lib.util.exceptions import NoUserSpecifiedError, UnableToFindUserError
from lib.util import discord_info, misc, parsing


# Variable statements.
NON_DECIMAL_BASES = {
    '0x': 16,
    '0d': 12,
    '0o': 8,
    '0b': 2
}


def get_closest_users(message, argument, exclude_bots=False, exclude_users=None, limit=None):
    """
    Gets the closest users to the given argument. Returns a list of users.
    The closest user is the one that matches the closest as prioritized:
        1. display name + username combined percentage
        2. display name index
        3. username index
        4. role count (relevance?)
    If two users match in one, the next best values are compared.
    If two users match for all, the preceding one is prioritized.
    Users can be chosen more than once,
    but priority will be given to ones that also match once it has been put into the list.
    Duplicate users will be removed at the end.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
        argument (str) : The command's argument, if any.
        exclude_bots (bool) : Whether or not to exclude bots from the list. Defaults to False.
        exclude_users (list) : Which users to exclude from the list. Defaults to None.
        limit (int) : The maximum amount of users in the list. Defaults to None.

    Returns:
        discord.User[] : A list of users.
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
    all_users = discord_info.get_applicable_users(message, exclude_bots, exclude_users)

    # Then, we find the closest user.
    # This list contains tuples such that:
    #   0 = user object
    #   1 = nick percentage
    #   2 = username percentage
    #   3 = nick index
    #   4 = username index
    #   5 = role count
    pointed_users = []

    # For each user, gather the required variables and put them into the pointed_users.
    for user in all_users:

        # Get display name and username.
        display_name = user.display_name.lower()
        username = user.name.lower()

        # If the argument is in either the display name or the username, then add them to the list.
        if approx_user in display_name or approx_user in username:
            pointed_users.append((
                user,
                misc.get_string_closeness(display_name, approx_user),
                misc.get_string_closeness(username, approx_user),
                display_name.find(approx_user),
                username.find(approx_user),
                len(user.roles) if hasattr(user, 'roles') else 0
            ))

    # If there are no pointed_users, then raise the error.
    if not pointed_users:
        raise UnableToFindUserError(pointed_users, approx_user)

    # Sort.
    pointed_users = sorted(pointed_users, key=cmp_to_key(sort_closest_user_list))

    # If we're operating under a limit, we return only limit amount.
    if limit:
        return [pointed_tuple[0] for pointed_tuple in pointed_users[:limit]]

    # Return.
    return [pointed_tuple[0] for pointed_tuple in pointed_users]


def sort_closest_user_list(item1, item2):
    """
    Sorts the closest user list.
    Used exclusively in get_closest_users. Separated for sorting reasons.

    Arguments:
        item1 (discord.User, float, float, int, int, int) : A tuple representing an entry in the pointed_users list.
                                                            It should be formatted such that index:
                                                                0 = user object
                                                                1 = nick percentage
                                                                2 = username percentage
                                                                3 = nick index
                                                                4 = username index
                                                                5 = role count
        item2 (discord.User, float, float, int, int, int) : Same format as item1, but different user.

    Returns:
        int : < 0 if item1 goes first, > 0 if item2 goes first.
    """
    # First, compare the sum of the nick percentage and username percentage.
    if item1[1] + item1[2] != item2[1] + item2[2]:
        return item2[1] + item2[2] - item1[1] - item1[2]

    # Then, compare the nick index.
    if item1[3] != item2[3]:
        return item1[3] - item2[3]

    # Next, compare the username index.
    if item1[4] != item2[4]:
        return item1[4] - item2[4]

    # Finally, compare the role count.
    return item2[5] - item1[5]


def get_multi_based_num_from_argument(argument):
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
    argument = parsing.normalize_string(argument).lower()

    # Go through non-decimal bases.
    for base in NON_DECIMAL_BASES:
        if argument.startswith(base):
            # Attempt to convert.
            return misc.convert_num_to_decimal(argument[2:], NON_DECIMAL_BASES[base])

    # If we've made it this far, then it means that the number is a decimal base.
    return float(argument)

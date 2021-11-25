# ===============================================================
#                 UTILITY METHODS (NOT COMMANDS)
# ===============================================================
from math import factorial
from lib.util.exceptions import *
from PIL import Image
import constants
import colorsys
import requests
import discord
import os

def prod(iterable,*, start=1):
    """
    Returns product of all values in iterable, starting at start
    """
    for i in iterable:
        start*= i
    return start

def perm(n, r=None):
    """
    nPr function.
    """
    # Setting r to n for bad values
    if r is None:
        r = n
        
    # Return for non-ints
    if not isinstance(n, int):
        raise TypeError('must be a nonzero integer value, not ' + str(type(n)))
    if not isinstance(r, int):
        raise TypeError('must be a nonzero integer value, not ' + str(type(r)))
        
    # Return for negatives
    if n < 0 or r < 0:
        raise ValueError('must be a nonzero integer value')
    
    # Return if r > n
    if r > n:
        return 0
    
    # Returns
    return factorial(n) / factorial(n - r)

def comb(n, r=None):
    """
    nCr function.
    Simple modification of perm function.
    """
    if r is None:
        r = n
    return perm(n, r) / factorial(r)


def get_photogenic_username(user):
    """
    Gets a more photogenic username based on the user's username and nickname.

    Arguments:
        user (discord.user.User) : The user.

    Returns:
        str : The photogenic username.
    """
    # Return.
    return user.nick if user.nick else user.name


def get_applicable_users(message, exclude_bots=True, exclude_users=None):
    """
    Returns a list of applicable users that fit the criteria provided.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
        exclude_bots (bool) : Whether or not to exclude bots from the list.
        exclude_users (list) : Which users, if any, to exclude from the list.

    Returns:
        discord.user.User[] : A list of users that fit the criteria.

    Raises:
        CannotAccessUserlistError : Can't access the userlist.
                                    This error is common when working from Windows.
    """
    # First, we get a list of all users.
    # If this is a guild, grab the users in the guild.
    if isinstance(message.channel, discord.TextChannel):
        all_users = message.guild.members

    # If this is a DM, grab the recipient.
    elif isinstance(message.channel, discord.DMChannel):
        all_users = [message.channel.recipient]

    # Otherwise (group channel), pull the recipients.
    else:
        all_users = message.channel.recipients

    # If there isn't an all_users, raise a CannotAccessUserlistError.
    if len(all_users) < 2:
        raise CannotAccessUserlistError()

    # If we were told to not include bots, we get rid of them.
    if exclude_bots:
        for i in range(len(all_users) - 1, -1, -1):
            if all_users[i].bot:
                all_users.remove(all_users[i])

    # We remove all the users in exclude_users, if any.
    if exclude_users:
        for usr in exclude_users:
            if usr in all_users:
                all_users.remove(usr)

    # Returns.
    return all_users



async def get_secondmost_recent_message(message):
    """
    Gets the second-most recent message in a channel, given a message.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.

    Returns:
        discord.message.Message : The previous message in the channel.

    Raises:
        FirstMessageInChannelError : The message this method was called with is the first message in the channel.
    """
    # Simple get statement.
    try:
        return (await message.channel.history(limit=2).flatten())[1].content

    # If there's an index error, raise the FirstMessageInChannelError.
    except IndexError:
        raise FirstMessageInChannelError()


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
        len_removed+= next_index + len(arg)
        source = source[next_index + len(arg):]

    # Returns.
    return all_indexes


def calculate_time_passage(time_delta):
    """
    Creates the time delta string and reports to channel, then returns time delta string.

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
    time_str += str(time_delta.seconds % 60) + 's '

    # Return the final string.
    return time_str


def multiply_color_tuple(color, factor):
    """
    Multiplies the values in the tuple by the factor.
    """
    color2 = []
    for i in range(len(color)):
        color2.append(int(color[i] * factor + 0.5))
    return tuple(color2)


def find_color_tuple_midpoint_hsv(color1, color2, factor=0.5):
    """
    Finds the midpoint between the two RGB colors using HSV midpoints.
    """
    color1 = colorsys.rgb_to_hsv(color1[0] / 255, color1[1] / 255, color1[2] / 255)
    color2 = colorsys.rgb_to_hsv(color2[0] / 255, color2[1] / 255, color2[2] / 255)
    color3 = colorsys.hsv_to_rgb(color1[0] * (1 - factor) + color2[0] * factor, color1[1] * (1 - factor) + color2[1] * factor, color1[2] * (1 - factor) + color2[2] * factor)
    return int(color3[0] * 255), int(color3[1] * 255), int(color3[2] * 255)


def upper_per_word(input_str):
    """
    Makes the beginning of every word an uppercase letter, and all others lowercase.
    """
    for i in range(len(input_str)):
        if i == 0 or input_str[i - 1] == ' ':
            input_str = input_str[:i] + input_str[i].upper() + input_str[i + 1:]
        else:
            input_str = input_str[:i] + input_str[i].lower() + input_str[i + 1:]
    return input_str
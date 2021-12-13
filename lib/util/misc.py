"""
Misc util methods module.
Has a lot of very different methods.
"""
# Local Imports
from lib.util.arguments import MAX_CONVERT_DEPTH, CONVERT_CHARS
from lib.util.exceptions import *

# Package Imports
from datetime import datetime
import colorsys
import discord
import logging
import pytz


# Timezone names for different discord VoiceRegions.
DISCORD_REGION_TIMEZONE_NAMES = {
    'us-west': 'America/Los_Angeles',
    'us-east': 'America/New_York',
    'us-south': 'America/Chicago',
    'us-central': 'America/Chicago',
    'eu_west': 'Europe/London',
    'eu_central': 'Europe/Berlin',
    'singapore': 'Singapore',
    'london': 'Europe/London',
    'sydney': 'Australia/Sydney',
    'amsterdam': 'Europe/Amsterdam',
    'frankfurt': 'Europe/Berlin',
    'brazil': 'Brazil/East',
    'hongkong': 'Hongkong',
    'russia': 'Europe/Moscow',
    'japan': 'Asia/Tokyo',
    'southafrica': 'Egypt',
    'south-korea': 'Asia/Seoul',
    'india': 'Asia/Kolkata',
    'europe': 'Europe/Berlin',
    'dubai': 'Asia/Dubai',
    'vip-us-east': 'America/New_York',
    'vip-us-west': 'America/Los_Angeles',
    'vip-amsterdam': 'Europe/Amsterdam'
}


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
    time_str += str(time_delta.seconds % 60) + 's'

    # Return the final string.
    return time_str


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



def get_guild_regions_weighted(message):
    """
    Gets the supposed region for a guild.
    This depends on the region overrides for each voice channel.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.

    Returns:
        dict : A list of voice regions and how often they appear in each voice channel.
    """
    # First, make sure this is a guild. If it isn't, just return an empty dict.
    if not isinstance(message.channel, discord.TextChannel):
        return {}

    # Now, we keep a tally (score).
    region_count = {}

    # Iterate through voice channels.
    for voice_channel in message.guild.voice_channels:

        # Get rtc region.
        region = voice_channel.rtc_region

        # If it's None, then continue.
        if not region:
            continue

        # Add it to the region_count.
        if region in region_count:
            region_count[region] += 1
        else:
            region_count[region] = 1

    # Return the region_count.
    return region_count


def get_guild_time(message):
    """
    Gets a guild's average local time.
    This is basicaly guessed by using the weighted guild regions.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.

    Returns:
        datetime.datetime : The average datetime across all the guild's channels.
    """
    # First, get the weighted guild regions.
    guild_regions = get_guild_regions_weighted(message)

    # List for keeping track of time weights.
    time_weights = []

    # Iterate through each guild region.
    for region, weight in guild_regions.items():

        # If the region is NOT In the discord region timezone names list, log an error and continue.
        if region.value not in DISCORD_REGION_TIMEZONE_NAMES:
            logging.error(f'VoiceRegion {region.value} completely unexpected')
            continue

        # Otherwise, add the timezone's current time to the list.
        time_weights.append((datetime.now(pytz.timezone(DISCORD_REGION_TIMEZONE_NAMES[region.value])), weight))

    # If there are no time_weights, just send the local time.
    if not time_weights:
        return datetime.now()

    # Now that all the time weights are acquired, start adding.
    time_total = 0

    # Iterate through time and weights.
    for time, weight in time_weights:

        # Add up the times.
        time_total += (time.timestamp() + time.tzinfo.utcoffset(time).total_seconds()) * weight

    # Now, average it.
    time_average = time_total / sum([weight for time, weight in time_weights])

    # Create a datetime object from that average time and return.
    return datetime.fromtimestamp(time_average)


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
        return (await message.channel.history(limit=2).flatten())[1]

    # If there's an index error, raise the FirstMessageInChannelError.
    except IndexError:
        raise FirstMessageInChannelError()


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
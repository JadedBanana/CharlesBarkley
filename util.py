# ===============================================================
#                 UTILITY METHODS (NOT COMMANDS)
# ===============================================================
from math import factorial
from exceptions import *
from PIL import Image
from pg import DB
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

def normalize_string(input_str, remove_discord_formatting=True, remove_double_spaces=True):
    """
    Removes spaces at the start and end as well as double spaces in a string.
    """
    # Start spaces
    while input_str.startswith(' '):
        input_str = input_str[1:]
    # End spaces
    while input_str.endswith(' '):
        input_str = input_str[:len(input_str) - 1]
    # Newlines, tabs
    input_str = input_str.replace('\t', ' ').replace('\n', ' ')
    # Double spaces
    if remove_double_spaces:
        while '  ' in input_str:
            input_str = input_str.replace('  ', ' ')
    # Code segments, spoilers, italics/bold
    if remove_discord_formatting:
        input_str = input_str.strip('`').strip('*').strip('_')
    # Return
    return input_str

def calculate_time_passage(time_delta):
    """
    Creates the time delta string and reports to channel, then returns time delta string.
    """
    bot_str = ''
    if time_delta.days:
        bot_str+= str(time_delta.days) + 'd '
    if int(time_delta.seconds / 3600):
        bot_str+= str(int(time_delta.seconds / 3600)) + 'h '
    if int(time_delta.seconds / 60):
        bot_str+= str(int(time_delta.seconds % 3600 / 60)) + 'm '
    bot_str+= str(time_delta.seconds % 60) + 's '

    return bot_str

def get_applicable_users(message, is_in_guild, exclude_bots=True, exclude_users=None):
    """
    Returns a list of applicable users that fit the criteria provided.
    """
    # First, we get a list of all users.
    all_users = message.guild.members if is_in_guild else ([message.channel.recipient] if isinstance(message.channel, discord.DMChannel) else message.channel.recipients)

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

def get_comm_start(message, is_in_guild):
    """
    Gets the command prefix. Just used to cut down space.
    """
    if is_in_guild:
        return constants.COMM_LOG_PREFIX_GUILD.format(message.author, message.channel, message.guild)
    elif isinstance(message.channel, discord.DMChannel):
        return constants.COMM_LOG_PREFIX.format(message.author, message.channel)
    else:
        return constants.COMM_LOG_PREFIX.format(message.author, message.channel)

def get_command_from_message(message):
    """
    Gets a command from a message, with one argument after
    """
    # Immediately returns if command prefix is missing
    if not message.content.lower().startswith(constants.GLOBAL_PREFIX):
        return None, None

    # Removes global prefix from message
    message = message.content[len(constants.GLOBAL_PREFIX):]

    # Finds space or end of line -- whichever comes first, and returns
    end_index = message.find(' ')
    if not end_index + 1:
        return message, None
    return message[:end_index].lower(), message[end_index + 1:]

def get_multi_index(source, arg):
    """
    Gets multiple indexes for the argument in the source.
    """
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

def get_closest_users(message, argument, is_in_guild, exclude_bots=False, exclude_users=None, limit=None):
    """
    Gets the closest user to the given argument. Returns list of users.
    """
    # Checks to see if this message specifically mentions anyone.
    # If so, immediately return that.
    if message.mentions:
        return message.mentions

    # If there is no argument left to parse, we raise NoUserSpecifiedError.
    if not argument:
        raise NoUserSpecifiedError()

    # Normalize the argument, split it by its spaces.
    arguments = normalize_string(argument, remove_discord_formatting=False).lower().split(' ')

    # Same as above, but now on the normalized and split str.
    if not arguments:
        raise NoUserSpecifiedError()

    # Otherwise, we search through the users and try to find matching strings.
    # First, we get a list of all users.
    all_users = get_applicable_users(message, is_in_guild, exclude_bots, exclude_users)

    # Then, we iterate through each argument and find the closest user.
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
    for arg in arguments:

        # Return ArgumentTooShortError when an argument is too short.
        if len(arg) < 2:
            raise ArgumentTooShortError(arg)

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
            if any([str(attr).lower().find(arg) + 1 for attr in [usr.name, usr.nick if usr.nick else '', usr.id]]):

                # Gathering the values for the attributes
                in_pointed_users = usr in pointed_users
                counts = [attr.lower().count(arg) for attr in [usr.name, usr.nick if usr.nick else '']]
                indexes = [get_multi_index(attr.lower(), arg) for attr in [usr.name + '#' + usr.discriminator, usr.nick if usr.nick else '']]
                non_argument_char_count = [len(attr) - len(arg) * attr.lower().count(arg) for attr in [usr.name + '#' + usr.discriminator, usr.nick if usr.nick else '']]
                id_stuffs = [str(usr.id).count(arg), get_multi_index(str(usr.id), arg), len(str(usr.id)) - len(arg) * str(usr.id).count(arg)]

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
            raise UnableToFindUserError(pointed_users, arg)

        # If we're operating under a limit, we return the second the limit matches.
        if limit:
            if len(pointed_users) == limit:
                return pointed_users

    return pointed_users

def get_profile_picture(user, already_id=False):
    """
    Gets the profile picture for a user.
    """
    # The path for the image.
    if already_id:
        image_locale = os.path.join(constants.TEMP_DIR, str(user) + constants.PFP_FILETYPE)
    else:
        image_locale = os.path.join(constants.TEMP_DIR, str(user.id) + constants.PFP_FILETYPE)
    # If the image exists, we just open that.
    if os.path.isfile(image_locale):
        return Image.open(image_locale), image_locale
    # Gets the url.
    pfp_url = user.avatar_url
    # Downloads image in bytes
    image_bytes = requests.get(pfp_url).content
    # Writes image to disk
    with open(image_locale, 'wb') as w:
        w.write(image_bytes)
    # Opens as image
    img_return = Image.open(image_locale)
    # Returns image.
    return img_return, image_locale


async def get_secondmost_recent_message(channel):
    """
    Gets the second-most recent message in a channel, given a channel.
    """
    try:
        return (await channel.history(limit=2).flatten())[1].content
    except IndexError:
        raise FirstMessageInChannelError()


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
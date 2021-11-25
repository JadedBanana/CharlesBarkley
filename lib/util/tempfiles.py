"""
Tempfiles helps with creating, maintaining, and deleting files in the temp/ directory.
Mainly deals with profile pictures (hence, that's what most of the methods are for).
"""
# Imports
from PIL import Image
import requests
import random
import os


# Active profile pictures dict keeps track of what modules are using what profile pictures.
# These are keyed using the command key and the channel id appended to the end.
ACTIVE_PROFILE_PICTURES = {}

# Image saving.
TEMP_DIR = 'temp'
PFP_DIR = 'pfps'
PFP_FILETYPE = '.webp'
TEMP_FILE_LENGTH = 16
TEMP_FILE_FILETYPE = '.png'
TEMP_FILE_CHAR_POSSIBILITIES = '1234567890-=_+qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'


def initialize():
    """
    Initializes the tempfiles module.
    Pretty much just used to make sure all the directories exist.
    """
    # Make temp dir
    if not os.path.isdir(TEMP_DIR):
        os.mkdir(TEMP_DIR)

    # Make profile picture dir
    if not os.path.isdir(os.path.join(TEMP_DIR, PFP_DIR)):
        os.mkdir(os.path.join(TEMP_DIR, PFP_DIR))


def checkout_profile_picture_by_user(user, message, command_key, size=None):
    """
    Checks out a profile picture for temporary use.
    Will download the profile picture if it doesn't yet exist in the files.

    Args:
        user (discord.user.User) : The desired user.
        message (discord.message.Message) : The discord message object that triggered the command.
        command_key (str) : The key that will be used to keep track of which command is using the image.
                            Should be a wholly unique key for each command.
        size ((int, int)) : The size, represented by a 2-entry tuple of ints.
                            Width first, then height.
    """
    # First, see if the user's profile picture is already in the dict. If it isn't, then download it.
    if user.id not in ACTIVE_PROFILE_PICTURES:
        load_profile_picture(user)

    # Then, modify the user profile picture data.
    ACTIVE_PROFILE_PICTURES[user.id][1].append(command_key + str(message.channel.id))

    # Then, get the image.
    image = ACTIVE_PROFILE_PICTURES[user.id][0].copy()

    # If it should be resized, then resize it.
    if size and size > (0, 0):
        image = image.resize((size[0], size[1]),
                             Image.NEAREST if image.width < size[0] or image.height < size[1] else Image.LANCZOS)

    # And return the image.
    return image


def retire_profile_picture_by_user(user, message, command_key):
    """
    Retires the use of a profile picture.

    Args:
        user (discord.user.User) : The desired user.
        message (discord.message.Message) : The discord message object that triggered the command.
        command_key (str) : The key that will be used to keep track of which command is no longer using the image.
                            Should be a wholly unique key for each command.
    """
    # If the user ID is in the dict, then clear the usage key.
    if user.id in ACTIVE_PROFILE_PICTURES:
        ACTIVE_PROFILE_PICTURES[user.id][1].remove(command_key + str(message.channel.id))

    # Run the script that clears empty profile pictures.
    # TODO


def load_profile_picture(user):
    """
    Gets the profile picture for a user and slots it into the dict.

    Args:
        user (discord.user.User) : The desired profile picture's user.
    """
    # Gets the user's avatar URL.
    pfp_url = user.avatar_url

    # Downloads image in bytes
    image_bytes = requests.get(pfp_url).content

    # Writes image to disk
    image_locale = os.path.join(TEMP_DIR, PFP_DIR, str(user.id) + PFP_FILETYPE)
    with open(image_locale, 'wb') as w:
        w.write(image_bytes)

    # Opens as image
    image = Image.open(image_locale)

    # Slots it all into the dict.
    ACTIVE_PROFILE_PICTURES[user.id] = (image, [])


def save_temporary_image(image):
    """
    Saves a temporary image to a temp file that will be deleted later.

    Arguments:
        image (PIL.Image) : The Image object to be sent as the embed's image.

    Returns:
        str : The image's path.
    """
    # Get the filename.
    image_path = os.path.join(TEMP_DIR,
                              ''.join(random.choice(TEMP_FILE_CHAR_POSSIBILITIES) for i in range(TEMP_FILE_LENGTH))
                              + TEMP_FILE_FILETYPE)

    # Save.
    image.save(image_path)

    # Return the filename.
    return image_path

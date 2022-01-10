"""
Tempfiles helps with creating, maintaining, and deleting files in the temp/ directory.
Mainly deals with profile pictures (hence, that's what most of the methods are for).
"""
# Package Imports
import datetime

from PIL import Image
import threading
import requests
import logging
import random
import time
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

# Image deletion.
TEMP_FILES_DELETION_INTERVAL = 60
TEMP_FILES_MINIMUM_AGE = 20


def initialize():
    """
    Initializes the temp_files module.
    Pretty much just used to make sure all the directories exist.
    """
    # Make temp dir
    if not os.path.isdir(TEMP_DIR):
        os.mkdir(TEMP_DIR)

    # Make profile picture dir
    if not os.path.isdir(os.path.join(TEMP_DIR, PFP_DIR)):
        os.mkdir(os.path.join(TEMP_DIR, PFP_DIR))

    # Clear profile pictures not in use, as well as leftover temp images.
    clear_profile_pictures_not_in_use()
    clear_all_temporary_files()


def get_profile_picture_by_user(user, size=None):
    """
    Gets a profile picture for one-time use.

    Args:
        user (discord.user.User) : The desired user.
        size ((int, int)) : The size, represented by a 2-entry tuple of ints.
                            Width first, then height.

    Returns:
        PIL.Image.Image : The profile picture as an image, if return_image is True.
    """
    # Get the image.
    # If the user is in the ACTIVE_PROFILE_PICTURES dict, then use that.
    if user.id in ACTIVE_PROFILE_PICTURES:
        image = Image.open(ACTIVE_PROFILE_PICTURES[user.id][0])

    # Otherwise, download it.
    else:
        image_locale = download_profile_picture(user)
        image = Image.open(image_locale)

    # If it should be resized, then resize it.
    if size and size > (0, 0):
        image = image.resize((size[0], size[1]),
                             Image.NEAREST if image.width < size[0] or image.height < size[1] else Image.LANCZOS)

    # And return the image.
    return image


async def get_profile_picture_by_user_with_typing(user, message, size=None):
    """
    Gets a profile picture for one-time use.

    Args:
        user (discord.user.User) : The desired user.
        message (discord.message.Message) : The discord message object that triggered the command.
        size ((int, int)) : The size, represented by a 2-entry tuple of ints.
                            Width first, then height.

    Returns:
        PIL.Image.Image : The profile picture as an image, if return_image is True.
    """
    # If the user isn't downloaded yet, then run the get_profile_picture_by_user method with typing.
    if user not in ACTIVE_PROFILE_PICTURES:
        async with message.channel.typing():
            return get_profile_picture_by_user(user, size=size)

    # Otherwise, don't type.
    return get_profile_picture_by_user(user, size=size)


def checkout_profile_picture_by_user(user, message, command_key, return_image=False, size=None):
    """
    Checks out a profile picture for long-term use.
    Will download the profile picture if it doesn't yet exist in the files.

    Args:
        user (discord.user.User) : The desired user.
        message (discord.message.Message) : The discord message object that triggered the command.
        command_key (str) : The key that will be used to keep track of which command is using the image.
                            Should be a wholly unique key for each command.
        return_image (bool) : Whether to return the image. Defaults to False.
        size ((int, int)) : The size, represented by a 2-entry tuple of ints.
                            Width first, then height.

    Returns:
        PIL.Image.Image : The profile picture as an image, if return_image is True.
    """
    # First, see if the user's profile picture is already in the dict. If it isn't, then download it and slot it into
    # the dict.
    if user.id not in ACTIVE_PROFILE_PICTURES:
        image_locale = download_profile_picture(user)
        ACTIVE_PROFILE_PICTURES[user.id] = (image_locale, [command_key + str(message.channel.id)])

    # Otherwise, just put this command key in the dict.
    else:
        ACTIVE_PROFILE_PICTURES[user.id][1].append(command_key + str(message.channel.id))

    # Then, if told to do so, get the image.
    if return_image:
        return get_profile_picture_by_user(user, size=size)


async def checkout_profile_picture_by_user_with_typing(user, message, command_key, return_image=False, size=None):
    """
    Checks out a profile picture for long-term use.
    Will download the profile picture if it doesn't yet exist in the files.
    Will type in the discord channel if it has to download anything.

    Args:
        user (discord.user.User) : The desired user.
        message (discord.message.Message) : The discord message object that triggered the command.
        command_key (str) : The key that will be used to keep track of which command is using the image.
                            Should be a wholly unique key for each command.
        return_image (bool) : Whether to return the image. Defaults to False.
        size ((int, int)) : The size, represented by a 2-entry tuple of ints.
                            Width first, then height.

    Returns:
        PIL.Image.Image : The profile picture as an image, if return_image is True.
    """
    # If the user isn't downloaded yet, then run the checkout_profile_picture_by_user method with typing.
    if user.id not in ACTIVE_PROFILE_PICTURES:
        async with message.channel.typing():
            return checkout_profile_picture_by_user(user, message, command_key, return_image=return_image, size=size)

    # Otherwise, don't type.
    return checkout_profile_picture_by_user(user, message, command_key, return_image=return_image, size=size)


def checkout_profile_picture_by_user_bulk(users, message, command_key, return_image=False, size=None):
    """
    Checks out a profile picture for temporary use.
    Will download the profile picture if it doesn't yet exist in the files.

    Args:
        users (discord.user.User[]) : A list of users.
        message (discord.message.Message) : The discord message object that triggered the command.
        command_key (str) : The key that will be used to keep track of which command is using the image.
                            Should be a wholly unique key for each command.
        return_image (bool) : Whether to return the image. Defaults to False.
        size ((int, int)) : The size, represented by a 2-entry tuple of ints.
                            Width first, then height.
    """
    # Run the standard version for every user.
    return [checkout_profile_picture_by_user(user, message, command_key, return_image=return_image, size=size)
            for user in users]


async def checkout_profile_picture_by_user_bulk_with_typing(users, message, command_key, return_image=False, size=None):
    """
    Checks out a profile picture for temporary use.
    Will download the profile picture if it doesn't yet exist in the files.
    Will type in the discord channel if it has to download anything.

    Args:
        users (discord.user.User[]) : A list of users.
        message (discord.message.Message) : The discord message object that triggered the command.
        command_key (str) : The key that will be used to keep track of which command is using the image.
                            Should be a wholly unique key for each command.
        return_image (bool) : Whether to return the image. Defaults to False.
        size ((int, int)) : The size, represented by a 2-entry tuple of ints.
                            Width first, then height.
    """
    # If there are any users not downloaded yet, then run the checkout_profile_picture_by_user_bulk method with typing.
    if any(user.id not in ACTIVE_PROFILE_PICTURES for user in users):
        async with message.channel.typing():
            return checkout_profile_picture_by_user_bulk(users, message, command_key, return_image=return_image,
                                                         size=size)

    # Otherwise, don't type.
    return checkout_profile_picture_by_user_bulk(users, message, command_key, return_image=return_image, size=size)


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
    if user.id in ACTIVE_PROFILE_PICTURES and \
            command_key + str(message.channel.id) in ACTIVE_PROFILE_PICTURES[user.id][1]:
        ACTIVE_PROFILE_PICTURES[user.id][1].remove(command_key + str(message.channel.id))


def retire_profile_picture_by_user_bulk(users, message, command_key):
    """
    Retires the use of a profile picture.

    Args:
        users (discord.user.User[]) : A list of users.
        message (discord.message.Message) : The discord message object that triggered the command.
        command_key (str) : The key that will be used to keep track of which command is no longer using the image.
                            Should be a wholly unique key for each command.
    """
    # Run the user id version.
    [retire_profile_picture_by_user(user, message, command_key) for user in users]


def download_profile_picture(user):
    """
    Gets the profile picture for a user and slots it into the dict.

    Args:
        user (discord.user.User) : The desired profile picture's user.

    Returns:
        str : Where the image was saved.
    """
    # Log that we're downloading it.
    logging.debug(f'Tempfile management downloading profile picture for user id {user.id}')

    # Downloads image in bytes.
    image_bytes = requests.get(user.avatar).content

    # Writes image to disk.
    image_locale = os.path.join(TEMP_DIR, PFP_DIR, str(user.id) + PFP_FILETYPE)
    with open(image_locale, 'wb') as w:
        w.write(image_bytes)

    # Return.
    return image_locale


def save_temporary_image(image):
    """
    Saves a temporary image to a temp file that will be deleted later.

    Arguments:
        image (PIL.Image.Image) : The Image object to be sent as the embed's image.

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


def save_temporary_text_file(text_str):
    """
    Saves the text message to a text file that will be deleted later.

    Arguments:
        text_str (str) : The string to be saved to the file.

    Returns:
        str : The text file's path.
    """
    # Get the filename.
    text_file_path = os.path.join(
        TEMP_DIR,
        ''.join(random.choice(TEMP_FILE_CHAR_POSSIBILITIES) for i in range(TEMP_FILE_LENGTH)) + TEMP_FILE_FILETYPE
    )

    # Save.
    with open(text_file_path, 'w') as file:
        file.write(text_str)

    # Return the filename.
    return text_file_path


def clear_profile_pictures_not_in_use():
    """
    Clears (deletes) profile pictures that are not in use.
    """
    # Iterate through all the images in the directory.
    for profile_image in os.listdir(os.path.join(TEMP_DIR, PFP_DIR)):

        # Look for instances of images not being in the ACTIVE_PROFILE_PICTURES.
        if int(profile_image[:-len(PFP_FILETYPE)]) not in ACTIVE_PROFILE_PICTURES:
            logging.debug(f'Tempfile management removing profile picture for '
                          f'user id {profile_image[:-len(PFP_FILETYPE)]}')
            os.remove(os.path.join(TEMP_DIR, PFP_DIR, profile_image))
            continue

        # Look for instances of images in the ACTIVE_PROFILE_PICTURES not having any active users.
        if not ACTIVE_PROFILE_PICTURES[int(profile_image[:-len(PFP_FILETYPE)])][1]:
            logging.debug(f'Tempfile management removing profile picture for '
                          f'user id {profile_image[:-len(PFP_FILETYPE)]}')
            del ACTIVE_PROFILE_PICTURES[int(profile_image[:-len(PFP_FILETYPE)])]
            os.remove(os.path.join(TEMP_DIR, PFP_DIR, profile_image))


def clear_all_temporary_files():
    """
    Clears (deletes) all the temporary images saved in the temp directory.
    """
    # Iterate through all the images in the directory.
    for temp_image in os.listdir(TEMP_DIR):

        # Ignore directories.
        if os.path.isdir(os.path.join(TEMP_DIR, temp_image)):
            continue

        # Delete the remaining files.
        os.remove(os.path.join(TEMP_DIR, temp_image))


def clear_old_temporary_files():
    """
    Clears (deletes) old temporary files (that are past TEMP_FILES_MINIMUM_AGE seconds old).
    """
    # Iterate through all the images in the directory.
    for temp_image in os.listdir(TEMP_DIR):

        # Ignore directories.
        if os.path.isdir(os.path.join(TEMP_DIR, temp_image)):
            continue

        # If the seconds are less than TEMP_FILES_MINIMUM_AGE, then ignore; otherwise delete.
        if time.time() - os.path.getmtime(os.path.join(TEMP_DIR, temp_image)) >= TEMP_FILES_MINIMUM_AGE:
            os.remove(os.path.join(TEMP_DIR, temp_image))


class TempFilesThread(threading.Thread):
    """
    Thread designed to constantly delete the old temp_files.
    This prevents them from being all built up and whatever.
    """

    def run(self):
        """
        Loop infinitely, deleting old temporary files.
        """
        # Import time
        import time

        # Infinite loop.
        while True:

            # Delete old temporary files.
            clear_old_temporary_files()

            # Delete old profile pictures.
            clear_profile_pictures_not_in_use()

            # Wait until next time to delete.
            time.sleep(TEMP_FILES_DELETION_INTERVAL)

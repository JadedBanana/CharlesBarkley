"""
Random Manga
Uses the Jikan (MAL) API to pull a random manga from the given user's manga list.
Has a default user that is set in .env.
"""
# Local Imports
from lib.util import environment, messaging, misc, parsing
from lib.util.logger import BotLogger as logging

# Package Imports
import requests
import discord
import random


# A lot of constants important for the Youtube API.
DEFAULT_USER = None  # Initialized in initialize method
DEFAULT_PAGE_NUMBERS = None  # Initialized in initialize method
DEFAULT_PAGE_WEIGHTS = None  # Initialized in initialize method
MANGA_PER_PAGE = 300
PTR_API_URL = 'https://api.jikan.moe/v3/user/{0}/mangalist/ptr'
ALL_API_URL = 'https://api.jikan.moe/v3/user/{0}/mangalist/all/{1}'
PRELOADED_MANGA_URLS = {}
PRELOADED_MANGA_FROM_USERS = []
PRELOADED_DEFAULT_PAGES = []
ALL_DEFAULT_PAGES_PRELOADED = False
EMBED_COLOR = (46 << 16) + (81 << 8) + 162


async def random_manga_master(bot, message, argument):
    """
    Generates a random manga page from MyAnimeList and sends it to the user.
    If a valid MAL username is passed, it will pull a random manga from that user's plan to watch list.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # First, see if the argument exists.
    if argument := parsing.normalize_string(argument):
        await random_manga_custom_user(message, argument)

    # If not, use the default values.
    else:
        await random_manga_default(message)


async def random_manga_custom_user(message, user):
    """
    Generates a random manga page from the given user's plan to watch section.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        user (str) : The username of the user to pull manga from.
    """
    # Try / catch just in case username doesn't exist.
    try:

        # Fetch the manga.
        async with message.channel.typing():
            manga_id, manga_url = get_random_manga_from_user_ptr(user)

        # Log and send.
        logging.info(message, f'requested random manga from user {user}, responded with MAL id {manga_id}')
        await messaging.send_text_message(message, manga_url)

    # On KeyError, invalid user.
    except KeyError:

        # Log and send.
        logging.info(message, f'requested random manga from user {user}, invalid')
        await messaging.send_text_message(message, f"Invalid user '{user}'.")

    # On IndexError, user has NO ptr.
    except IndexError:

        # Log and send.
        logging.info(message, f'requested random manga from user {user}, no ptr')
        await messaging.send_text_message(message, 'That user either has no manga tagged as plan-to-watch, or the '
                                                   'MyAnimeList API had a bad day. Try again later.')


async def random_manga_default(message):
    """
    Generates a random manga page from the default user OR the preloaded manga, if that exists.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Get the random manga.
    try:
        manga_id, manga_url = await get_random_manga_from_default_user(message)

        # Log and send.
        logging.info(message, f'requested random manga from default, responded with MAL id {manga_id}')
        await messaging.send_text_message(message, manga_url)

    # On IndexError, MAL API had a bad day.
    except IndexError:

        # Log and send.
        logging.info(message, f'requested random manga from default, MAL API error')
        await messaging.send_text_message(message, 'MyAnimeList API had an error, try again later.')


def get_random_manga_from_user_ptr(user):
    """
    Gets a random manga from the given user's plan-to-watch section.

    Arguments:
        user (str) : The username of the user to pull manga from.

    Returns:
        int, str : The MAL id of the manga, followed by its URL.
    """
    # Make the API call.
    response = requests.get(PTR_API_URL.format(user), timeout=10)
    manga_list_json = response.json()['manga']

    # Add this user's list to the preloaded manga, if we are doing that.
    add_user_list_to_preloaded_if_not_already(user, manga_list_json)

    # Pick a random one.
    chosen_manga = random.choice(manga_list_json)

    # Return the chosen manga's id and url.
    return chosen_manga['mal_id'], chosen_manga['url']


async def get_random_manga_from_default_user(message):
    """
    Gets a random manga from the default user.
    Basically, just picks a random manga from their list.
    Ideally, the default user has a LOT of manga in their list.
    Will act differently depending on whether or not everything is preloaded.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.

    Returns:
        int, str : The MAL id of the manga, followed by its URL.
    """
    # If we have preloaded all the pages, then just pick a random one from the preloaded list.
    if ALL_DEFAULT_PAGES_PRELOADED:
        return random.choice(list(PRELOADED_MANGA_URLS.items()))

    # Otherwise, make a request... and GET it.
    async with message.channel.typing():
        return get_random_manga_from_default_user_download()


def get_random_manga_from_default_user_download():
    """
    Gets a random manga from the default user by downloading from MyAnimeList.
    Only downloads pages that haven't been downloaded before.

    Returns:
        int, str : The MAL id of the manga, followed by its URL.
    """
    # Instantiates global variable.
    global DEFAULT_PAGE_WEIGHTS, ALL_DEFAULT_PAGES_PRELOADED

    # Picks which page to pull from.
    page_num = random.choices(
        [page_num for page_num in DEFAULT_PAGE_NUMBERS if page_num not in PRELOADED_DEFAULT_PAGES],
        DEFAULT_PAGE_WEIGHTS
    )[0]

    # Appends that page to PRELOADED_DEFAULT_PAGES.
    PRELOADED_DEFAULT_PAGES.append(page_num)

    # Modifies the DEFAULT_PAGE_WEIGHTS depending on if the page_num is the last page.
    if page_num == DEFAULT_PAGE_NUMBERS[-1]:
        DEFAULT_PAGE_WEIGHTS = DEFAULT_PAGE_WEIGHTS[:-1]
    else:
        DEFAULT_PAGE_WEIGHTS = DEFAULT_PAGE_WEIGHTS[1:]

    # Set the value of ALL_DEFAULT_PAGES_PRELOADED.
    ALL_DEFAULT_PAGES_PRELOADED = \
        not [page_num for page_num in DEFAULT_PAGE_NUMBERS if page_num not in PRELOADED_DEFAULT_PAGES]

    # Make the API call.
    response = requests.get(ALL_API_URL.format(DEFAULT_USER, page_num), timeout=10)
    manga_list_json = response.json()['manga']

    # Add the manga list to the preloaded.
    add_user_list_to_preloaded(manga_list_json)

    # Pick a random one.
    chosen_manga = random.choice(manga_list_json)

    # Return the chosen manga's id and url.
    return chosen_manga['mal_id'], chosen_manga['url']


def add_user_list_to_preloaded_if_not_already(user, manga_list_json):
    """
    Adds all the manga from the manga list that are missing from the preloaded manga list to the preloaded manga list.
    Only works if this user hasn't had their stuff preloaded yet.

    Arguments:
        user (str) : The username of the user this list came from.
        manga_list_json: The complete manga list JSON for this user.
    """
    # Initial check.
    if not PRELOADED_MANGA_URLS or user in PRELOADED_MANGA_FROM_USERS:
        return

    # Run the other method.
    add_user_list_to_preloaded(manga_list_json)


def add_user_list_to_preloaded(manga_list_json):
    """
    Adds all the manga from the manga list that are missing from the preloaded manga list to the preloaded manga list.

    Arguments:
        manga_list_json: The complete manga list JSON for this user.
    """
    # Iterate through each manga entry and put it in if it isn't yet there.
    for manga in manga_list_json:
        if manga['mal_id'] not in PRELOADED_MANGA_URLS:
            PRELOADED_MANGA_URLS[manga['mal_id']] = manga['url']


def initialize():
    """
    Initializes the command.
    In this case, uses environment variables to set default values.
    """
    # Log.
    import logging
    logging.info('Initializing fun_simple.random_manga...')

    # Global variable establishments.
    global DEFAULT_USER, DEFAULT_PAGE_NUMBERS, DEFAULT_PAGE_WEIGHTS

    # Default user is a straight copy.
    DEFAULT_USER = environment.get('MAL_DEFAULT_MANGA_USER')

    # DEFAULT_PAGE_NUMBERS and DEFAULT_PAGE_WEIGHTS are generated using the MAL_MANGA_COUNT and MANGA_PER_PAGE.
    manga_count = environment.get('MAL_MANGA_COUNT')
    page_count = int(manga_count / MANGA_PER_PAGE) if manga_count % MANGA_PER_PAGE == 0 else \
        int(manga_count / MANGA_PER_PAGE) + 1

    # Set the variables.
    DEFAULT_PAGE_NUMBERS = [i + 1 for i in range(page_count)]
    DEFAULT_PAGE_WEIGHTS = [300 for i in range(page_count - 1)] + [manga_count % MANGA_PER_PAGE]


# Command values
PUBLIC_COMMAND_DICT = {
    'randommanga': random_manga_master
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'randommanga',
        'category': 'fun_simple',
        'description': 'Generates a random Manga using MyAnimeList. Can be used to pick ANY manga, or one from a '
                       "specific user's plan-to-watch section."
                       'Because of how finnicky the MAL API is, spamming the command is not recommended.',
        'examples': [('randommanga', 'Generates a random manga.'),
                     ('randommanga ManWild', "Picks a random manga from MAL user 'ManWild's plan-to-read list.")],
        'usages': ['randommanga', 'randommanga < user >']
    }
]

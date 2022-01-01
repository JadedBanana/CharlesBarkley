"""
Random Anime
Uses the Jikan (MAL) API to pull a random anime from the given user's anime list.
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
ANIME_PER_PAGE = 300
PTW_API_URL = 'https://api.jikan.moe/v3/user/{0}/animelist/ptw'
ALL_API_URL = 'https://api.jikan.moe/v3/user/{0}/animelist/all/{1}'
PRELOADED_ANIME_URLS = {}
PRELOADED_ANIME_FROM_USERS = []
PRELOADED_DEFAULT_PAGES = []
ALL_DEFAULT_PAGES_PRELOADED = False


async def random_anime_master(bot, message, argument):
    """
    Generates a random anime page from MyAnimeList and sends it to the user.
    If a valid MAL username is passed, it will pull a random anime from that user's plan to watch list.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # First, see if the argument exists.
    argument = parsing.normalize_string(argument)
    if argument:
        await random_anime_custom_user(message, argument)

    # If not, use the default values.
    else:
        await random_anime_default(message)


async def random_anime_custom_user(message, user):
    """
    Generates a random anime page from the given user's plan to watch section.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        user (str) : The username of the user to pull anime from.
    """
    # Try / catch just in case username doesn't exist.
    try:

        # Fetch the anime.
        async with message.channel.typing():
            anime_id, anime_url = get_random_anime_from_user_ptw(user)

        # Log and send.
        logging.debug(message, f'requested random anime from user {user}, responded with MAL id {anime_id}')
        await messaging.send_text_message(message, anime_url)

    # On KeyError, invalid user.
    except KeyError:

        # Log and send.
        logging.debug(message, f'requested random anime from user {user}, invalid')
        await messaging.send_text_message(message, f"Invalid user '{user}'.")

    # On IndexError, user has NO ptw.
    except IndexError:

        # Log and send.
        logging.debug(message, f'requested random anime from user {user}, no ptw')
        await messaging.send_text_message(message, 'That user either has no anime tagged as plan-to-watch, or the '
                                                   'MyAnimeList API had a bad day. Try again later.')


async def random_anime_default(message):
    """
    Generates a random anime page from the default user OR the preloaded anime, if that exists.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Get the random anime.
    try:
        anime_id, anime_url = await get_random_anime_from_default_user(message)

        # Log and send.
        logging.debug(message, f'requested random anime from default, responded with MAL id {anime_id}')
        await messaging.send_text_message(message, anime_url)

    # On IndexError, MAL API had a bad day.
    except IndexError:

        # Log and send.
        logging.debug(message, f'requested random anime from default, MAL API error')
        await messaging.send_text_message(message, 'MyAnimeList API had an error, try again later.')


def get_random_anime_from_user_ptw(user):
    """
    Gets a random anime from the given user's plan-to-watch section.

    Arguments:
        user (str) : The username of the user to pull anime from.

    Returns:
        int, str : The MAL id of the anime, followed by its URL.
    """
    # Make the API call.
    response = requests.get(PTW_API_URL.format(user), timeout=10)
    anime_list_json = response.json()['anime']

    # Add this user's list to the preloaded anime, if we are doing that.
    add_user_list_to_preloaded_if_not_already(user, anime_list_json)

    # Pick a random one.
    chosen_anime = random.choice(anime_list_json)

    # Return the chosen anime's id and url.
    return chosen_anime['mal_id'], chosen_anime['url']


async def get_random_anime_from_default_user(message):
    """
    Gets a random anime from the default user.
    Basically, just picks a random anime from their list.
    Ideally, the default user has a LOT of anime in their list.
    Will act differently depending on whether or not everything is preloaded.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.

    Returns:
        int, str : The MAL id of the anime, followed by its URL.
    """
    # If we have preloaded all the pages, then just pick a random one from the preloaded list.
    if ALL_DEFAULT_PAGES_PRELOADED:
        return random.choice(list(PRELOADED_ANIME_URLS.items()))

    # Otherwise, make a request... and GET it.
    async with message.channel.typing():
        return get_random_anime_from_default_user_download()


def get_random_anime_from_default_user_download():
    """
    Gets a random anime from the default user by downloading from MyAnimeList.
    Only downloads pages that haven't been downloaded before.

    Returns:
        int, str : The MAL id of the anime, followed by its URL.
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
    anime_list_json = response.json()['anime']

    # Add the anime list to the preloaded.
    add_user_list_to_preloaded(anime_list_json)

    # Pick a random one.
    chosen_anime = random.choice(anime_list_json)

    # Return the chosen anime's id and url.
    return chosen_anime['mal_id'], chosen_anime['url']


def add_user_list_to_preloaded_if_not_already(user, anime_list_json):
    """
    Adds all the anime from the anime list that are missing from the preloaded anime list to the preloaded anime list.
    Only works if this user hasn't had their stuff preloaded yet.

    Arguments:
        user (str) : The username of the user this list came from.
        anime_list_json: The complete anime list JSON for this user.
    """
    # Initial check.
    if not PRELOADED_ANIME_URLS or user in PRELOADED_ANIME_FROM_USERS:
        return

    # Run the other method.
    add_user_list_to_preloaded(anime_list_json)


def add_user_list_to_preloaded(anime_list_json):
    """
    Adds all the anime from the anime list that are missing from the preloaded anime list to the preloaded anime list.

    Arguments:
        anime_list_json: The complete anime list JSON for this user.
    """
    # Iterate through each anime entry and put it in if it isn't yet there.
    for anime in anime_list_json:
        if anime['mal_id'] not in PRELOADED_ANIME_URLS:
            PRELOADED_ANIME_URLS[anime['mal_id']] = anime['url']


def initialize():
    """
    Initializes the command.
    In this case, uses environment variables to set default values.
    """
    # Log.
    import logging
    logging.debug('Initializing fun_simple.random_anime...')

    # Global variable establishments.
    global DEFAULT_USER, DEFAULT_PAGE_NUMBERS, DEFAULT_PAGE_WEIGHTS

    # Default user is a straight copy.
    DEFAULT_USER = environment.get('MAL_DEFAULT_ANIME_USER')

    # DEFAULT_PAGE_NUMBERS and DEFAULT_PAGE_WEIGHTS are generated using the MAL_ANIME_COUNT and ANIME_PER_PAGE.
    anime_count = environment.get('MAL_ANIME_COUNT')
    page_count = int(anime_count / ANIME_PER_PAGE) if anime_count % ANIME_PER_PAGE == 0 else \
        int(anime_count / ANIME_PER_PAGE) + 1

    # Set the variables.
    DEFAULT_PAGE_NUMBERS = [i + 1 for i in range(page_count)]
    DEFAULT_PAGE_WEIGHTS = [300 for i in range(page_count - 1)] + [anime_count % ANIME_PER_PAGE]


# Command values
PUBLIC_COMMAND_DICT = {
    'randomanime': random_anime_master,
    'randommal': random_anime_master,
    'randomani': random_anime_master
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'randomanime',
        'category': 'fun_simple',
        'description': 'Generates a random Anime using MyAnimeList. Can be used to pick ANY anime, or one from a '
                       "specific user's plan-to-watch section."
                       'Because of how finnicky the MAL API is, spamming the command is not recommended.',
        'examples': [('randomanime', 'Generates a random anime.'),
                     ('randomanime ManWild', "Picks a random anime from MAL user 'ManWild's plan-to-watch list.")],
        'aliases': ['randommal', 'randomani'],
        'usages': ['randomanime', 'randomanime < user >']
    }
]

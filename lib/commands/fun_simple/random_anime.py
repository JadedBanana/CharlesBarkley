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
EMBED_COLOR = (46 << 16) + (81 << 8) + 162


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
    if argument := parsing.normalize_string(argument):
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
        logging.info(message, f'requested random anime from user {user}, responded with MAL id {anime_id}')
        await messaging.send_text_message(message, anime_url)

    # On KeyError, invalid user.
    except KeyError:

        # Log and send.
        logging.info(message, f'requested random anime from user {user}, invalid')
        await messaging.send_text_message(message, f"Invalid user '{user}'.")


async def random_anime_default(message):
    """
    Generates a random anime page from the default user OR the preloaded anime, if that exists.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # If the preloaded anime exist, then pull from that.
    if PRELOADED_ANIME_URLS:
        anime_id = random.choice(PRELOADED_ANIME_URLS)
        anime_url = PRELOADED_ANIME_URLS[anime_id]

    # Otherwise, get it from the request.
    else:
        async with message.channel.typing():
            anime_id, anime_url = get_random_anime_from_default_user()

    # Log and send.
    logging.info(message, f'requested random anime from default, responded with MAL id {anime_id}')
    await messaging.send_text_message(message, anime_url)


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


def get_random_anime_from_default_user():
    """
    Gets a random anime from the default user.
    Basically, just picks a random anime from their list.
    Ideally, the default user has a LOT of anime in their list.

    Returns:
        int, str : The MAL id of the anime, followed by its URL.
    """
    # Picks which page to pull from.
    page_num = random.choices(DEFAULT_PAGE_NUMBERS, DEFAULT_PAGE_WEIGHTS)[0]

    # Make the API call.
    response = requests.get(ALL_API_URL.format(DEFAULT_USER, page_num), timeout=10)
    anime_list_json = response.json()['anime']

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
        'description': 'Generates a random Anime using MyAnimeList. Can be used to pick ANY anime, or one from a'
                       "specific user's plan-to-watch section.",
        'examples': [('randomanime', 'Generates a random anime.'),
                     ('randomanime ManWild', "Picks a random anime from MAL user 'ManWild's plan-to-watch list.")],
        'aliases': ['randommal', 'randomani'],
        'usages': ['randomanime', 'randomanime < user >']
    }
]

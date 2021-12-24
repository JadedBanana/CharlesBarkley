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
PRELOADED_ANIME = []
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
        anime = get_random_anime_from_user_ptw(argument)

    # If not, use the default values.
    else:
        anime = get_random_anime_from_default_user()

    # Log and send.
    logging.info(message, f"requested random anime, responded with MAL id {anime['mal_id']}")
    await messaging.send_text_message(message, anime['url'])


def get_random_anime_from_user_ptw(user):
    """
    Gets a random anime from the given user's plan-to-watch section.

    Arguments:
        user (str) : The username of the user to pull anime from.

    Returns:
        dict : Dict representing anime data.
    """
    # Make the API call.
    response = requests.get(PTW_API_URL.format(user))
    anime_list_json = response.json()['anime']

    # Pick a random one.
    chosen_anime = random.choice(anime_list_json)

    # If this isn't in the preloaded anime and we are preloading anime, add it.
    if PRELOADED_ANIME and chosen_anime['mal_id'] not in PRELOADED_ANIME:
        PRELOADED_ANIME[chosen_anime['mal_id']] = chosen_anime['url']

    # Return the chosen anime.
    return chosen_anime


def get_random_anime_from_default_user():
    """
    Gets a random anime from the default user.
    Basically, just picks a random anime from their list.
    Ideally, the default user has a LOT of anime in their list.

    Returns:
        dict : Dict representing anime data.
    """
    # Picks which page to pull from.
    page_num = random.choices(DEFAULT_PAGE_NUMBERS, DEFAULT_PAGE_WEIGHTS)[0]

    # Make the API call.
    response = requests.get(ALL_API_URL.format(DEFAULT_USER, page_num))
    anime_list_json = response.json()['anime']

    # Return a random one.
    return random.choice(anime_list_json)


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
    'randommal': random_anime_master
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'randomanime',
        'category': 'fun_simple',
        'description': 'Generates a random Anime using MyAnimeList. Can be used to pick ANY anime, or one from a'
                       "specific user's plan-to-watch section.",
        'examples': [('randomanime', 'Generates a random anime.'),
                     ('randomanime ManWild', "Picks a random anime from MAL user 'ManWild's plan-to-watch list.")],
        'aliases': ['randommal'],
        'usages': ['randomanime', 'randomanime < user >']
    }
]
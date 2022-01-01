"""
Random Wikipedia command.
Uses the public, free Wikipedia API to pull a random Wikipedia article.
Unlike the random YouTube command, has no quota.
"""
# Local Imports
from lib.util.logger import BotLogger as logging
from lib.util import messaging

# Package Imports
import wikipedia


async def random_wikipedia(bot, message, argument):
    """
    Generates a random wikipedia link and sends it.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Set wiki_page to None.
    wiki_page = None

    # As long as we don't have a wiki page, try to get one.
    while not wiki_page:
        try:
            wiki_page = wikipedia.page(wikipedia.random(1))
        except wikipedia.PageError or wikipedia.RedirectError or wikipedia.DisambiguationError:
            pass

    # Log and send the message back.
    logging.debug(message, f'requested random wikipedia page, returned {wiki_page}')
    await messaging.send_text_message(message, wiki_page.url)


# Command values
PUBLIC_COMMAND_DICT = {
    'randomwiki': random_wikipedia,
    'randomwikipedia': random_wikipedia
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'randomwiki',
        'category': 'fun_simple',
        'description': 'Generates a random Wikipedia page.',
        'examples': [('randomwiki', 'Generates a random Wikipedia page.')],
        'aliases': ['randomwikipedia'],
        'usages': ['randomwiki']
    }
]
"""
Random Wikipedia command.
Uses the public, free Wikipedia API to pull a random Wikipedia article.
Unlike the random YouTube command, has no quota.
"""
from lib.util.logger import BotLogger as logging
from lib.util import messaging
import wikipedia


async def random_wikipedia(bot, message, argument):
    """
    Generates a random youtube link.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # A simple and easy call.
    wiki_page = wikipedia.page(wikipedia.random(1))

    # Log and send the message back.
    logging.info(message, f'requested random wikipedia page, returned {wiki_page}')
    await messaging.send_text_message(message, wiki_page.url)


# Command values
PUBLIC_COMMAND_DICT = {
    'randomwiki': random_wikipedia,
    'randomwikipedia': random_wikipedia
}
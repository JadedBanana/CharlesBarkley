"""
Runtime command.
Gets the bot's running time.
"""
# Local Imports
from lib.util.logger import BotLogger as logging
from lib.util.misc import format_time_delta_str
from lib.util import messaging

# Package Imports
from datetime import datetime


# Stores the bot object.
BOT = None  # Initialized in initialize method


async def runtime(message, argument):
    """
    Prints out the runtime of the bot.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Immediately returns if bot start time was not established
    if not BOT.bot_start_time:
        logging.error(message, 'requested runtime, could not find runtime variable on bot')
        return await messaging.send_text_message(message, 'An error occurred while getting runtime, sorry! :P')

    # Gets the time passage string.
    time_delta = datetime.today() - BOT.bot_start_time
    time_str = format_time_delta_str(time_delta)

    # Sends report, logs message
    logging.debug(message, f'requested runtime, responded with {time_str}')
    await messaging.send_text_message(message, f'Jadi3Pi has been running for {time_str}.')


def initialize(bot):
    """
    Initializes the command.
    In this case, uses environment variables to set default values.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
    """
    # Log.
    import logging
    logging.debug('Initializing info.runtime...')

    # Set global variables.
    global BOT
    BOT = bot


# Command values
PUBLIC_COMMAND_DICT = {
    'runtime': runtime
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'runtime',
        'category': 'info',
        'description': 'Displays the time the bot has been running for.',
        'examples': [('runtime', 'Displays the time the bot has been running for.')],
        'usages': ['runtime']
    }
]
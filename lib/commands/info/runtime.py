"""
Runtime command.
Gets the bot's running time.
"""
# Imports
from lib.util.logger import BotLogger as logging
from lib.util.misc import calculate_time_passage
from lib.util import messaging
from datetime import datetime


async def runtime(bot, message, argument):
    """
    Prints out the runtime of the bot.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Immediately returns if bot start time was not established
    if not bot.bot_start_time:
        logging.error(message, 'requested runtime, could not find runtime variable on bot')
        return await messaging.send_text_message(message, 'An error occurred while getting runtime, sorry! :P')

    # Gets the time passage string.
    time_delta = datetime.today() - bot.bot_start_time
    time_str = calculate_time_passage(time_delta)

    # Sends report, logs message
    logging.info(message, f'requested runtime, responded with {time_str}')
    await messaging.send_text_message(message, f'Jadi3Pi has been running for {time_str}.')


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
"""
Uptime command.
Gets how long the bot has been up for.
"""
# Local Imports
from lib.util.logger import BotLogger as logging
from lib.util.misc import format_time_delta_str
from lib.util import messaging

# Package Imports
from datetime import datetime


async def uptime(bot, message, argument):
    """
    Prints out the uptime of the bot.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Immediately returns if bot start time was not established
    if not bot.bot_uptime:
        logging.error(message, 'requested uptime, could not find uptime variable on bot')
        return await messaging.send_text_message(message, 'An error occurred while getting uptime, sorry! :P')

    # Gets the time passage string.
    time_delta = datetime.today() - bot.bot_uptime
    time_str = format_time_delta_str(time_delta)

    # Sends report, logs message
    logging.debug(message, f'requested uptime, responded with {time_str}')
    await messaging.send_text_message(message, f'Jadi3Pi has been connected for {time_str}.')


# Command values
PUBLIC_COMMAND_DICT = {
    'uptime': uptime
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'uptime',
        'category': 'info',
        'description': 'Displays the time the bot has been up for.',
        'examples': [('uptime', 'Displays the time the bot has been up for.')],
        'usages': ['uptime']
    }
]
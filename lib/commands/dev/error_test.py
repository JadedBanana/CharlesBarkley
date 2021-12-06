"""
Get PID command.
Gets the PID this bot is running from and sends it back as a text message.
"""
# Imports
from lib.util.logger import BotLogger as logging
from lib.util import messaging
import os


async def error_test(bot, message, argument):
    """
    Raises an exception.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Raise the exception.
    raise ValueError(255)


# Command values
DEVELOPER_COMMAND_DICT = {
    'errortest': error_test
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'errortest',
        'category': 'dev_only',
        'description': 'Raise an exception.',
        'examples': [('errortest', 'Raises an exception.')],
        'usages': ['errortest']
    }
]
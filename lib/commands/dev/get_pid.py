"""
Get PID command.
Gets the PID this bot is running from and sends it back as a text message.
"""
# Local Imports
from lib.util.logger import BotLogger as logging
from lib.util import messaging

# Package Imports
import os


async def get_pid(message, argument):
    """
    Gets the local PID this bot is running on.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Gets PID
    pid = os.getpid()

    # Logs and returns PID
    logging.debug(message, f'ordered local PID, returned {pid}')
    await messaging.send_text_message(message, f'Current running PID is {pid}')


# Command values
DEVELOPER_COMMAND_DICT = {
    'getpid': get_pid
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'getpid',
        'category': 'dev_only',
        'description': 'Get the PID that the bot is running under. Can only be used by developers.',
        'examples': [('getpid', 'Gets the PID.')],
        'usages': ['getpid']
    }
]
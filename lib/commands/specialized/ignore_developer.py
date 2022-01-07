"""
toggle_ignore_developer command.
Specialized command in that it can be called even when the developer is being ignored.
"""
# Local Imports
from lib.util.logger import BotLogger as logging
from lib.util import messaging


# Stores the bot object.
BOT = None  # Initialized in initialize method


async def toggle_ignore_dev(message, argument=None):
    """
    Toggles whether to ignore the developer.
    The response varies depending on whether this is the deployment version.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # For deployment client, toggle the ignoring developer status.
    if BOT.deployment_client:
        BOT.ignore_developer = not BOT.ignore_developer
        logging.debug(message, f'Requested ignore developer, now'
                               f'{" " if BOT.ignore_developer else " no longer "}ignoring developers')
        await messaging.send_text_message(message, f'Deployment version speaking, now'
                                                   f'{" " if BOT.ignore_developer else " no longer "}'
                                                   f'ignoring developers')

    # For development client, ignore this message.
    else:
        logging.debug(message, f'Requested ignore developer, ignoring ignore request')
        await messaging.send_text_message(message, f'Development version speaking, ignoring ignore request')


def initialize(bot):
    """
    Initializes the command.
    In this case, uses environment variables to set default values.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
    """
    # Log.
    import logging
    logging.debug('Initializing specialized.ignore_developer...')

    # Set global variables.
    global BOT
    BOT = bot


# Command values
DEVELOPER_COMMAND_DICT = {
    'toggleignoredev': toggle_ignore_dev,
    'toggleignoredevs': toggle_ignore_dev,
    'toggleignoredeveloper': toggle_ignore_dev,
    'toggleignoredevelopers': toggle_ignore_dev
}
SPECIALIZED_COMMAND_DICT = {
    'toggleignoredev': toggle_ignore_dev
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'toggleignoredev',
        'category': 'dev_only',
        'description': 'Toggles whether to ignore developers. Can only be used by developers, and only works on deployment verions.',
        'examples': [('toggleignoredev', 'Toggles whether to ignore the developer.')],
        'aliases': ['toggleignoredevs', 'toggleignoredeveloper', 'toggleignoredevelopers'],
        'usages': ['toggleignoredev']
    }
]

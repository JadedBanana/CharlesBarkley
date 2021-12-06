"""
Swooce command.
Watch me SWOOCE right in! Swooce... swooce!
"""
# Local Imports
from lib.util.logger import BotLogger as logging
from lib.util import messaging


# Swooce YouTube url.
SWOOCE = 'https://www.youtube.com/watch?v=gghBcjgOdd0'


async def swooce(bot, message, argument):
    """
    Sends the swooce video.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Log and send.
    logging.info(message, 'swooced right in')
    await messaging.send_text_message(message, SWOOCE)


# Command values
PUBLIC_COMMAND_DICT = {
    'swooce': swooce
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'swooce',
        'description': 'Watch me swooce right in!',
        'examples': [('swooce', 'Swooce swooce!')],
        'usages': ['swooce']
    }
]
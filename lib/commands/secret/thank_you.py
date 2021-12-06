"""
Thank you command.
Thanks the bot.
"""
# Local Imports
from lib.util.logger import BotLogger as logging
from lib.util import messaging

# Package Imports
import random


# Stored responses.
THANK_YOU_RESPONSES = [
    ':)',
    ':D',
    'You\'re welcome!',
    'It\'s my pleasure.',
    'I aim to please!',
    'Hehe, I\'m just doing my job!',
    ':blush:'
]


async def thank_you(bot, message, argument):
    """
    Thanks the bot!
    :D

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    logging.info(message, 'thanked the bot')
    await messaging.send_text_message(message, random.choice(THANK_YOU_RESPONSES))


# Command values
PUBLIC_COMMAND_DICT = {
    'thankyou': thank_you,
    'thanks': thank_you,
    'thank': thank_you,
    'thanku': thank_you
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'thankyou',
        'description': 'Thanks the bot.',
        'examples': [('thankyou', 'Thanks the bot.')],
        'usages': ['thankyou'],
        'aliases': ['thanks', 'thank', 'thanku']
    }
]
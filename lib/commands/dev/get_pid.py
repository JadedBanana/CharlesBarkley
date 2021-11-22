"""
Get PID command.
Gets the PID this bot is running from and sends it back as a text message.
"""
# Imports
from lib.util.logger import BotLogger as logging
from lib.util import messaging
import os


async def get_pid(bot, message, argument):
    """
    Gets the local PID this bot is running on.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Gets PID
    pid = os.getpid()

    # Logs and returns PID
    logging.info(message, f'Ordered local PID, returned {pid}')
    await messaging.send_text_message(message, f'Current running PID is {pid}')


# Command values
DEVELOPER_COMMAND_DICT = {
    'getpid': get_pid
}
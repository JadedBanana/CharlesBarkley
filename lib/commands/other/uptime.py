"""
Binary command.
Converts numbers from other bases into binary.
"""
# Imports
from lib.util.logger import BotLogger as logging
from lib.util.misc import calculate_time_passage
from lib.util import messaging
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
    time_str = calculate_time_passage(time_delta)

    # Sends report, logs message
    logging.info(message, f'requested uptime, responded with {time_str}')
    await messaging.send_text_message(message, f'Bot has been connected for {time_str}')


# Command values
COMMAND_NAMES = ['uptime']
CALL_METHOD = uptime
"""
Send log command.
Sends the log file for a specific date.
"""
# Imports
from lib.util import environment, messaging, parsing
from lib.util.logger import BotLogger as logging
from lib.util import logger
import discord
import os


# Log file variables
LOG_FILE_CHARS = '1234567890-'


async def send_log(bot, message, argument):
    """
    Sends a log file through discord.
    Argument should be formatted in YYYY-MM-DD.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # If there is no argument, we simply grab today's log file.
    if not argument:
        target_log = logger.LOG_FILE
        # If there is no log file today, then we send an error message.
        if not target_log:
            logging.info(message, 'Requested log file for today, currently not logging to file')
            return await messaging.send_text_message(message, 'Not logging to file right now. '
                                                              'Try to pull a log file from the past.')

    # Attempt to grab something from the argument.
    if not target_log:
        # Now, get the target_log from the argument.
        target_log = os.path.join(environment.get('LOGS_DIR'), parsing.normalize_string(argument).lower().strip(' ').replace('/', '-') + '.log')

    # We see if that log file exists.
    if os.path.isfile(target_log):

        # Log then send file.
        logging.info(message, f'Ordered log file {target_log}, sending')
        await messaging.send_file(message, target_log)

    # If the log file doesn't exist, we tell the user that.
    else:
        logging.info(message, f'Ordered log file, file {target_log} does not exist')
        await message.channel.send(f'Log file {target_log} does not exist.')


# Command values
DEVELOPER_COMMAND_DICT = {
    'sendlog': send_log
}

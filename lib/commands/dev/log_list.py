"""
Log list command.
Lists the available log files in the logs dir.
"""
# Imports
from lib.util.logger import BotLogger as logging
from lib.util import environment, messaging
import os


async def log_list(bot, message, argument):
    """
    Sends a list of all the log files in the log folder.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Get the log folder.
    log_folder = environment.get('LOGS_DIR')

    # Check to make sure that the log folder exists.
    if not os.path.exists(log_folder):
        # If not, send an appropriate message back.
        logging.info(message, "Ordered log list, but log folder doesn't exist")
        return await messaging.send_text_message(message, 'Log folder does not exist.')

    # Log the order.
    logging.info(message, 'Ordered log list, sent.')

    # Gets the file list and file sizes
    log_files = sorted(os.listdir(log_folder))
    file_sizes = [os.path.getsize(os.path.join(log_folder, log_file)) for log_file in log_files]

    # If the log file list is empty, we send a message saying so.
    if not log_files:
        return await messaging.send_text_message(message, 'Log folder is empty.')

    # Create the message string.
    log_str = '\n'.join(f'{log_files[i]}\t({file_sizes[i]} bytes)' for i in range(len(log_files)))

    # Send the log message.
    await messaging.send_codeblock_message(message, log_str)


# Command values
DEVELOPER_COMMAND_DICT = {
    'loglist': log_list
}

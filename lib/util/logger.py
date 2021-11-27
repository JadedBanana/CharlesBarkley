"""
Logging file.
Sets up the Python logging module as well as hosting the BotLogger class.
"""
# Imports
from lib.util import environment
import discord
import logging
import os


# Storage of logging levels based on numbers.
LOGGING_LEVELS = [
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL
]
# Log file name.
LOG_FILE = None


def basic_setup():
    """
    Performs basic setup for the logging module.
    Sets the logging format and level, as well as making the logging directory if we are set to log to a file.
    """
    # Check if we are supposed to log to a file.
    if environment.get('LOG_TO_FILE'):

        # Create the logging directory, if it doesn't exist.
        logging_dir = environment.get('LOGS_DIR')
        if not os.path.isdir(logging_dir):
            os.mkdir(logging_dir)

        # Create the log file.
        from datetime import datetime
        global LOG_FILE
        LOG_FILE = os.path.join(logging_dir, datetime.today().strftime('%Y-%m-%d') + '.log')

        # Set the config.
        logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s',
                            level=LOGGING_LEVELS[environment.get('LOGGING_LEVEL')],
                            handlers=[logging.FileHandler(LOG_FILE, encoding='utf-8'), logging.StreamHandler()])

        # Log a basic line showing where the thread's logs begin.
        log_message = 'NEW INSTANCE'
        logging.critical('=' * len(log_message) * 3)
        logging.critical(' ' * len(log_message) + log_message)
        logging.critical('=' * len(log_message) * 3)

    # No logging file, just log to console.
    else:
        logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=LOGGING_LEVELS[environment.get('LOGGING_LEVEL')])


class BotLogger:
    """
    A Logging module designed specifically for use in Jadi3Pi commands.
    Logging methods require Discord message objects in their calls for this reason.
    """

    @staticmethod
    def get_message_info_str(message):
        """
        Gets message information from the message object and returns it as a str.

        Arguments:
            message (discord.message.Message) : The discord message object that triggered the command.

        Returns:
            str : The message's information data, represented in a readable format.
        """
        # Message in a guild
        if isinstance(message.channel, discord.TextChannel):
            return f'{message.author} ({message.guild}, {message.channel}): '

        # Message in DM's
        elif isinstance(message.channel, discord.DMChannel):
            return f'{message.author} (DM): '

        # Other (idk how this would work)
        return f'{message.author} (Mystery Channel: {message.channel}): '


    @staticmethod
    def log(level, message, logging_text):
        """
        Logs a message to the specified level.

        Arguments:
            level (int) : The level the message should be logged to.
                              0 = debug
                              1 = info
                              2 = warning
                              3 = error
                              4 = critical
            message (discord.message.Message) : The discord message object that triggered the command.
            logging_text (str) : The log's text.
        """
        # Log.
        logging.log(LOGGING_LEVELS[level], BotLogger.get_message_info_str(message) + logging_text)


    @staticmethod
    def debug(message, logging_text):
        """
        Logs a DEBUG message.

        Arguments:
            message (discord.message.Message) : The discord message object that triggered the command.
            logging_text (str) : The log's text.
        """
        # Call the central logging message.
        BotLogger.log(0, message, logging_text)


    @staticmethod
    def info(message, logging_text):
        """
        Logs an INFO message.

        Arguments:
            message (discord.message.Message) : The discord message object that triggered the command.
            logging_text (str) : The log's text.
        """
        # Call the central logging message.
        BotLogger.log(1, message, logging_text)


    @staticmethod
    def warning(message, logging_text):
        """
        Logs a WARNING message.

        Arguments:
            message (discord.message.Message) : The discord message object that triggered the command.
            logging_text (str) : The log's text.
        """
        # Call the central logging message.
        BotLogger.log(2, message, logging_text)


    @staticmethod
    def error(message, logging_text):
        """
        Logs an ERROR message.

        Arguments:
            message (discord.message.Message) : The discord message object that triggered the command.
            logging_text (str) : The log's text.
        """
        # Call the central logging message.
        BotLogger.log(3, message, logging_text)


    @staticmethod
    def critical(message, logging_text):
        """
        Logs a CRITICAL message.

        Arguments:
            message (discord.message.Message) : The discord message object that triggered the command.
            logging_text (str) : The log's text.
        """
        # Call the central logging message.
        BotLogger.log(4, message, logging_text)
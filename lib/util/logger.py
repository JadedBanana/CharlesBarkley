"""
Environment file. Helps with managing dozens of environment variables.
"""
# Imports
from lib.util import environment
import logging
import discord


# Storage of logging levels based on numbers.
LOGGING_LEVELS = [
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL
]

def basic_setup():
    """
    Performs basic setup for the logging module.
    Sets the logging format and level.
    """
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=LOGGING_LEVELS[environment.get('LOGGING_LEVEL')])


def debug_setup():
    """
    Performs debug setup for the logging module.
    Sets the logging format and level.
    """
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.DEBUG)


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
            return f'{message.author} (Guild {message.guild}, Channel {message.channel}): '

        # Message in DM's
        elif isinstance(message.channel, discord.DMChannel):
            return f'{message.author} (DM): '

        # Other (idk how this would work)
        return f'{message.author} (Unknown Channel {message.channel}): '


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
"""
Binary command.
Converts numbers from other bases into binary.
"""
# Imports
from lib.util.logger import BotLogger as logging
from lib.util import arguments, messaging


async def binary(bot, message, argument):
    """
    Converts a number to binary.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    try:
        # Get the decimal version of the number.
        num = arguments.get_multibased_num_from_argument(argument)
        # Convert the decimal number into a binary one.
        num = arguments.convert_num_from_decimal(num, 2)

        logging.info(message, f'requested binary conversion for {argument}, responded with 0b{num}')
        await messaging.send_text_message(message, '0b' + str(num))

    # Something went wrong, log and send message.
    except (ValueError, AttributeError):
        logging.info(message, f'requested binary conversion for {argument}, invalid')
        return await messaging.send_text_message(message, 'Invalid number.')


# Command values
COMMAND_NAMES = ['bin', 'binary']
CALL_METHOD = binary
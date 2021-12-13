"""
Binary command.
Converts numbers from other bases into binary.
"""
# Imports
from lib.util.logger import BotLogger as logging
from lib.util import arguments, messaging, misc


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
        num = misc.convert_num_from_decimal(num, 2)

        logging.info(message, f'requested binary conversion for {argument}, responded with 0b{num}')
        await messaging.send_text_message(message, '0b' + str(num))

    # Something went wrong, log and send message.
    except (ValueError, AttributeError):
        logging.info(message, f'requested binary conversion for {argument}, invalid')
        return await messaging.send_text_message(message, 'Invalid number.')


# Command values
PUBLIC_COMMAND_DICT = {
    'bin': binary,
    'binary': binary
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'binary',
        'category': 'math',
        'description': 'Converts a given number to binary.',
        'examples': [('binary 10', 'Converts the number 10 from decimal to binary.'),
                     ('binary 0x1A', 'Converts the number 1A from hexadecimal to binary.'),
                     ('binary 2.5', 'Converts the number 2.5 from decimal to binary.')],
        'aliases': ['bin'],
        'usages': ['binary < number >']
    }
]
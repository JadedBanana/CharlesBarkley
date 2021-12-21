"""
Octal command.
Converts numbers from other bases into octal.
"""
# Imports
from lib.util.logger import BotLogger as logging
from lib.util import arguments, messaging, misc


async def octal(bot, message, argument):
    """
    Converts a number to octal.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    try:
        # Get the decimal version of the number.
        num = arguments.get_multibased_num_from_argument(argument)
        # Convert the decimal number into an octal one.
        num = misc.convert_num_from_decimal(num, 8)

        logging.info(message, f'requested octal conversion for {argument}, responded with 0o{num}')
        return await messaging.send_text_message(message, '0o' + str(num))

    # Something went wrong, log and send message.
    except (ValueError, AttributeError):
        logging.info(message, f'requested octal conversion for {argument}, invalid')
        return await messaging.send_text_message(message, 'Invalid number.')


# Command values
PUBLIC_COMMAND_DICT = {
    'oct': octal,
    'octal': octal
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'octal',
        'category': 'math',
        'description': 'Converts a given number to octal.',
        'examples': [('octal 45', 'Converts the number 45 from decimal to octal.'),
                     ('octal 0b110101', 'Converts the number 110101 from binary to octal.'),
                     ('octal 0x1A', 'Converts the number 1A from hexadecimal to octal.')],
        'aliases': ['oct'],
        'usages': ['octal < number >']
    }
]
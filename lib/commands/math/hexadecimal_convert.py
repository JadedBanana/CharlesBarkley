"""
Hexadecimal command.
Converts numbers from other bases into hexadecimal.
"""
# Imports
from lib.util.logger import BotLogger as logging
from lib.util import arguments, messaging, misc


async def hexadecimal(bot, message, argument):
    """
    Converts a number to hexadecimal.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    try:
        # Get the decimal version of the number.
        num = arguments.get_multi_based_num_from_argument(argument)
        # Convert the decimal number into a hexadecimal one.
        num = misc.convert_num_from_decimal(num, 16)

        logging.info(message, f'requested hexadecimal conversion for {argument}, responded with 0x{num}')
        return await messaging.send_text_message(message, '0x' + str(num))

    # Something went wrong, log and send message.
    except (ValueError, AttributeError):
        logging.info(message, f'requested hexadecimal conversion for {argument}, invalid')
        return await messaging.send_text_message(message, 'Invalid number.')


# Command values
PUBLIC_COMMAND_DICT = {
    'hex': hexadecimal,
    'hexadec': hexadecimal,
    'hexadecimal': hexadecimal
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'hexadecimal',
        'category': 'math',
        'description': 'Converts a given number to hexadecimal.',
        'examples': [('hexadecimal 45', 'Converts the number 45 from decimal to hexadecimal.'),
                     ('hexadecimal 0b110101', 'Converts the number 110101 from binary to hexadecimal.'),
                     ('hexadecimal 0o71', 'Converts the number 71 from octal to hexadecimal.')],
        'aliases': ['hex', 'hexadec'],
        'usages': ['hexadecimal < number >']
    }
]
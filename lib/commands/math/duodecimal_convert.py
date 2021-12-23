"""
Duodecimal command.
Converts numbers from other bases into duodecimal.
"""
# Imports
from lib.util.logger import BotLogger as logging
from lib.util import arguments, messaging, misc


async def duodecimal(bot, message, argument):
    """
    Converts a number to duodecimal.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    try:
        # Get the decimal version of the number.
        num = arguments.get_multi_based_num_from_argument(argument)
        # Convert the decimal number into a duodecimal one.
        num = misc.convert_num_from_decimal(num, 12)

        logging.info(message, f'requested duodecimal conversion for {argument}, responded with 0d{num}')
        return await messaging.send_text_message(message, '0d' + str(num))

    # Something went wrong, log and send message.
    except (ValueError, AttributeError):
        logging.info(message, f'requested duodecimal conversion for {argument}, invalid')
        return await messaging.send_text_message(message, 'Invalid number.')


# Command values
PUBLIC_COMMAND_DICT = {
    'duo': duodecimal,
    'duoadec': duodecimal,
    'duodecimal': duodecimal
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'duodecimal',
        'category': 'math',
        'description': 'Converts a given number to duodecimal.',
        'examples': [('duodecimal 45', 'Converts the number 45 from decimal to duodecimal.'),
                     ('duodecimal 0b110101', 'Converts the number 110101 from binary to duodecimal.'),
                     ('duodecimal 0x1A', 'Converts the number 1A from hexadecimal to duodecimal.')],
        'aliases': ['duo', 'duodec'],
        'usages': ['duodecimal < number >']
    }
]
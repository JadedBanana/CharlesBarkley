"""
Decimal command.
Converts numbers from other bases into decimal.
"""
# Imports
from lib.util.logger import BotLogger as logging
from lib.util import arguments, messaging


async def decimal(bot, message, argument):
    """
    Converts a number to decimal.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    try:
        # Get the decimal version of the number.
        num = arguments.get_multibased_num_from_argument(argument)

        logging.info(message, f'requested decimal conversion for {argument}, responded with 0d{num}')
        await messaging.send_text_message(message, int(num) if num % 1 == 0 else num)

    # Something went wrong, log and send message.
    except (ValueError, AttributeError):
        logging.info(message, f'requested decimal conversion for {argument}, invalid')
        return await messaging.send_text_message(message, 'Invalid number.')


# Command values
PUBLIC_COMMAND_DICT = {
    'dec': decimal,
    'decimal': decimal
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'decimal',
        'category': 'math',
        'description': 'Converts a given number to decimal.',
        'examples': [('decimal 0b110101', 'Converts the number 110101 from binary to decimal.'),
                     ('decimal 0x1A', 'Converts the number 1A from hexadecimal to decimal.'),
                     ('decimal 0d34.B', 'Converts the number 34.B from duodecimal to decimal.')],
        'aliases': ['dec'],
        'usages': ['decimal < number >']
    }
]
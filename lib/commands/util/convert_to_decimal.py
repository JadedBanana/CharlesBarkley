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
    except ValueError:
        logging.info(message, f'requested decimal conversion for {argument}, invalid')
        return await messaging.send_text_message(message, 'Invalid number.')


# Command values
COMMAND_NAMES = ['dec', 'decimal']
CALL_METHOD = decimal
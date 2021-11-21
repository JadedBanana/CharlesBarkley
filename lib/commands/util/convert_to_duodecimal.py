"""
Duodecimal command.
Converts numbers from other bases into duodecimal.
"""
# Imports
from lib.util.logger import BotLogger as logging
from lib.util import arguments, messaging


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
        num = arguments.get_multibased_num_from_argument(argument)
        # Convert the decimal number into a duodecimal one.
        num = arguments.convert_num_from_decimal(num, 12)

        logging.info(message, f'requested duodecimal conversion for {argument}, responded with 0d{num}')
        await messaging.send_text_message(message, '0d' + str(num))

    # Something went wrong, log and send message.
    except (ValueError, AttributeError):
        logging.info(message, f'requested duodecimal conversion for {argument}, invalid')
        return await messaging.send_text_message(message, 'Invalid number.')


# Command values
COMMAND_NAMES = ['duo', 'duodec', 'duodecimal']
CALL_METHOD = duodecimal
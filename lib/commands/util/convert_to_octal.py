"""
Octal command.
Converts numbers from other bases into octal.
"""
# Imports
from lib.util.logger import BotLogger as logging
from lib.util import arguments, messaging

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
        num = arguments.convert_num_from_decimal(num, 8)

        logging.info(message, f'requested octal conversion for {argument}, responded with 0o{num}')
        await messaging.send_text_message(message, '0o' + str(num))

    # Something went wrong, log and send message.
    except ValueError:
        logging.info(message, f'requested octal conversion for {argument}, invalid')
        return await messaging.send_text_message(message, 'Invalid number.')


# Command values
COMMAND_NAMES = ['oct', 'octal']
CALL_METHOD = octal
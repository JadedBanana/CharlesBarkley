"""
Binary command.
Converts numbers from other bases into binary.
"""
# Imports
from lib.util import arguments

async def binary(bot, message, argument):
    """
    Converts a number to binary.
    """
    # Getting the number
    num = await arguments.get_multibased_num_from_argument(message, argument)

    # Error handling for not numbers
    if isinstance(num, str):
        log.info(util.get_comm_start(message, is_in_guild) + 'requested binary conversion for {}, invalid'.format(argument))
        return

    num = convert_num_from_decimal(num, 2)

    log.info(util.get_comm_start(message, is_in_guild) + 'requested binary conversion for {}, responded with 0b{}'.format(argument, num))
    await message.channel.send('0b' + str(num))
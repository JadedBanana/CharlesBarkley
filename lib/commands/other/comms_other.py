# =================================================================
#                        OTHER COMMANDS
# =================================================================
from datetime import datetime
import constants
from lib.util import misc

# Logging
log = None

async def help_command(self, message, argument, is_in_guild):
    """
    Prints out the help response.
    """
    log.debug(misc.get_comm_start(message, is_in_guild) + 'requested help message')
    await message.channel.send(constants.HELP_MSG.format(constants.VERSION) + (constants.HELP_MSG_DEV_ADDENDUM if message.author.id in constants.DEVELOPER_DISCORD_IDS else '```'))




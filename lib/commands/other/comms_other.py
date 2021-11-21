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


async def runtime(self, message, argument, is_in_guild):
    """
    Prints out the runtime of the bot.
    """
    # Immediately returns if bot start time was not established
    if not self.bot_start_time:
        log.warning(misc.get_comm_start(message, is_in_guild) + 'requested runtime, could not find start time')
        await message.channel.send('An error occurred while getting runtime, sorry! :P')
        return

    # Time delta
    time_delta = datetime.today() - self.bot_start_time

    # Does the thing
    bot_str = misc.calculate_time_passage(time_delta)

    # Sends report, logs message
    log.debug(misc.get_comm_start(message, is_in_guild) + 'requested runtime, responded with ' + bot_str)
    await message.channel.send(constants.RUNTIME_PREFIX + bot_str)



"""
Remote reboot command.
Reboots the bot.
In actuality, just terminates the bot. The deployment version should have a cronjob that restarts the bot in just a minute.
"""
# Local Imports
from lib.util.logger import BotLogger as logging
from lib.util import messaging

# Package Imports
from datetime import datetime, timedelta
import sys


# Reboot confirmation variables
REBOOT_CONFIRMATION = False
REBOOT_USER = None
REBOOT_CHANNEL = None


async def confirm_reboot(message):
    """
    Confirms or denies the reboot.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Make sure that the variables are set.
    global REBOOT_CONFIRMATION, REBOOT_USER, REBOOT_CHANNEL
    if not (REBOOT_CONFIRMATION and message.author.id == REBOOT_USER and message.channel.id == REBOOT_CHANNEL):
        return

    # Create response str.
    response = message.content.lower()

    # Only take the first character. Assuming the response was yes, continue on to the next part.
    if response.startswith('y'):

        # Gets time until bot should be back.
        current_time = datetime.today()
        # If the minute is even, our time delta will be 3 minutes 15 seconds instead of 2 minutes 15 seconds.
        time_delta_seconds = 185 if current_time.minute % 2 == 0 else 135
        # Creating next bot start time.
        next_bot_start_time = datetime(current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute) + timedelta(seconds=time_delta_seconds)

        # Notify user.
        logging.info(message, 'Confirmed remote restart, restarting')
        await messaging.send_text_message(message, 'Confirmed. Performing remote reboot...')
        await messaging.send_text_message(message, f'Bot is estimated to be back up in approximately {(next_bot_start_time - current_time).seconds} seconds.')

        # Exit.
        from lib.util import watchdog
        watchdog.stop_all_threads()

    # If the response was to abort, then abort.
    elif response.startswith('n'):

        # Set reboot confirmation to False, log, and send message back.
        REBOOT_CONFIRMATION = False
        logging.info(message, 'Aborted remote restart')
        await messaging.send_text_message(message, 'Remote reboot aborted.')

    # Invalid response.
    else:
        logging.debug(message, f'Invalid response to confirmation message ({response})')
        await messaging.send_text_message(message, 'Invalid response. Confirm? (y/n)')


async def remote_reboot(message, argument):
    """
    Since this bot runs on automatic crontabs, we can just exit and assume the scheduling will do the rest.
    However, we don't want to reboot all willy-nilly.
    So we have a contingency!
    This just sets the flag for a reboot.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Set the values for reboot confirmation.
    global REBOOT_CONFIRMATION, REBOOT_USER, REBOOT_CHANNEL
    REBOOT_CONFIRMATION = True
    REBOOT_USER = message.author.id
    REBOOT_CHANNEL = message.channel.id

    # Log and send the message.
    logging.info(message, 'Ordered remote reboot, confirming...')
    await messaging.send_text_message(message, 'Confirm remote reboot? (y/n)')


# Command values
DEVELOPER_COMMAND_DICT = {
    'reboot': remote_reboot
}
REACTIVE_COMMAND_LIST = [
    confirm_reboot
]
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'reboot',
        'category': 'dev_only',
        'description': 'Reboots (terminates) the bot. Requires a secondary confirmation afterwards. Can only be used by developers.',
        'examples': [('reboot', 'Reboots the bot.')],
        'usages': ['reboot'],
        'reactive commands': [('y', 'Confirm reboot.'),
                              ('n', 'Abort reboot.')]
    }
]
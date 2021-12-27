"""
Remote update command.
Uses a subprocess to perform 'git pull' on the working directory.
"""
# Local Imports
from lib.util.logger import BotLogger as logging
from lib.util import messaging

# Package Imports
import subprocess


async def remote_update(bot, message, argument):
    """
    Uses git to pull the most recent commit down.
    Reboot will need to be done to apply the changes.
    """
    # Perform the subprocess call
    process = subprocess.Popen(['git', 'pull'], stdout=subprocess.PIPE)

    # Get decoded version of the output.
    decoded_output = process.communicate()[0].decode('utf-8')

    # Log, then send report.
    logging.debug(message, 'Ordered remote update.')
    await messaging.send_text_message(message, 'Git output: ```' + decoded_output + '```')
    await messaging.send_text_message(message,
                                      'If update completed successfully, feel free to manually reboot using j!reboot')


# Command values
DEVELOPER_COMMAND_DICT = {
    'update': remote_update
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'update',
        'category': 'dev_only',
        'description': 'Calls git pull to update the bot. Can only be used by developers.',
        'examples': [('update', 'Opens a subprocess to call git pull.')],
        'usages': ['update']
    }
]
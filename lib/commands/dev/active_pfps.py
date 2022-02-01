"""
Active profile pictures command.
Sends the active profile picture dict, formatted as a codeblock.
"""
# Local Imports
from lib.util.logger import BotLogger as logging
from lib.util import messaging, temp_files


async def active_pfps(message, argument):
    """
    Gets all the active profile pictures.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # If there are no active profile pictures, then just say that there's no active profile pictures.
    if not temp_files.ACTIVE_PROFILE_PICTURES:
        logging.debug(message, 'requested active profile pictures, but there are none')
        return await messaging.send_text_message(message, 'No active profile pictures.')

    # Active profile pictures found, send the codeblock.
    logging.debug(message, f'requested active profile pictures, sent back '
                          f'{len(temp_files.ACTIVE_PROFILE_PICTURES)} entries')
    await messaging.send_codeblock_message(message, '\n'.join(
        [f'{pfp_id}: {", ".join(key for key in pfp_tuple[1])}'
         for pfp_id, pfp_tuple in temp_files.ACTIVE_PROFILE_PICTURES.items()]))


# Command values
DEVELOPER_COMMAND_DICT = {
    'activepfps': active_pfps
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'activepfps',
        'category': 'dev_only',
        'description': 'Get the active profile picture dict.',
        'examples': [('activepfps', 'Gets the active profile pictures.')],
        'usages': ['activepfps']
    }
]

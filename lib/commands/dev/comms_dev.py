# ===============================================================
#                     DEV-ONLY COMMANDS
# ===============================================================
from datetime import datetime, timedelta
import constants
import discord
import socket
import string
from lib.util import misc
import os

# Logging
log = None


async def update_remote(self, message, argument, is_in_guild):
    """
    Uses git to pull the most recent commit down.
    Reboot will need to be done to apply the changes.
    """
    # Import subprocess so we can do the call
    import subprocess;
    process = subprocess.Popen(['git', 'pull'], stdout=subprocess.PIPE)

    # Get decoded version of the output.
    decoded_output = process.communicate()[0].decode('utf-8')

    # Send report and log.
    log.info(misc.get_comm_start(message, is_in_guild) + 'Ordered remote update.')
    await message.channel.send('Git output: ```' + decoded_output + '```')
    await message.channel.send('If update completed successfully, feel free to manually reboot using j!reboot')


async def send_log(self, message, argument, is_in_guild):
    """
    Sends a log file through discord.
    Argument should be formatted in YYYY-MM-DD.
    """
    # If there is no argument, we simply grab today's log file.
    is_today = not argument
    if is_today:
        target_log = datetime.today().strftime('%Y-%m-%d') + '.txt'

    # Otherwise, we grab the argument and try to work it into a good target log.
    else:
        # Normalizing the string
        argument_slim = misc.normalize_string(argument)
        for i in range(len(argument_slim) - 1, -1, -1):
            if argument_slim[i] not in string.digits:
                argument_slim = argument_slim[:i] + argument_slim[i + 1:]

        # If the length of our argument isn't now 8, we tell the user that and return.
        if len(argument_slim) != 8:
            log.debug(misc.get_comm_start(message, is_in_guild) + 'Ordered log file, invalid date')
            await message.channel.send('Invalid date format. Should be YYYY-MM-DD')
            return

        # Now, we form a date.
        target_log = '{}-{}-{}.txt'.format(argument_slim[:4], argument_slim[4:6], argument_slim[6:8])
        is_today = target_log == datetime.today().strftime('%Y-%m-%d') + '.txt'

    # We see if that log file exists.
    if os.path.isfile(os.path.join(constants.LOGS_DIR, target_log)) or is_today:
        # Log then send file.
        log.info(misc.get_comm_start(message, is_in_guild) + 'Ordered log file {}, sending'.format(target_log))
        await message.channel.send(file=discord.File(os.path.join(constants.LOGS_DIR, target_log)))

    # If the log file doesn't exist, we tell the user that.
    else:
        log.debug(misc.get_comm_start(message, is_in_guild) + 'Ordered log file, file {} does not exist'.format(target_log))
        await message.channel.send('Log file {} does not exist.'.format(target_log))


async def log_list(self, message, argument, is_in_guild):
    """
    Sends a list of all the log files in the log folder.
    """
    # Logs debug
    log.debug(misc.get_comm_start(message, is_in_guild) + 'Ordered log list.')

    # Gets the file list and file sizes
    dir_files = sorted(os.listdir(constants.LOGS_DIR))
    file_sizes = [os.path.getsize(os.path.join(constants.LOGS_DIR, f)) for f in dir_files]

    # While there's dir files, we need to put them into their own sections (so that we don't overdo the 2000 character limit).
    messages = []
    current_message = '```'
    while dir_files:
        # Adds lines to the output.
        next_line = dir_files[0] + '\t({} bytes)\n'.format(file_sizes[0])
        if len(current_message) + len(next_line) + 3 <= 2000:
            current_message += next_line
        else:
            messages.append(current_message + '```')
            current_message = '```' + next_line

        # Removing the files from the list.
        dir_files.remove(dir_files[0])
        file_sizes.remove(file_sizes[0])

    # Finally, we add the final message to the end.
    messages.append(current_message + '```')

    # If the file list isn't empty, we send it.
    # Otherwise,
    if messages:
        for msg in messages:
            await message.channel.send(msg)
    else:
        await message.channel.send('Could not find any log files.')
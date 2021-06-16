# ===============================================================
#                     DEV-ONLY COMMANDS
# ===============================================================
from datetime import datetime, timedelta
import constants
import discord
import socket
import string
import util
import os

# Logging
log = None

async def get_local_ip(self, message, argument, is_in_guild):
    """
    Gets the local ip address this bot is running on.
    """
    # Windows part
    if self.on_windows:
        # Gets the local ip using socket.
        local_ip = socket.gethostbyname('Windows: ' + socket.gethostname())

        # Sends msg and logs.
        log.debug(util.get_comm_start(message, is_in_guild) + 'Ordered local ip, returned ' + str(local_ip))
        await message.channel.send(local_ip)

    # Linux Part
    else:
        # Imports netifaces and gets the local ip's.
        import netifaces;
        local_ips = [pre + ': ' + netifaces.ifaddresses(pre)[netifaces.AF_INET][0]['addr'] for pre in constants.LINUX_IP_PREFIXES]

        # Sends msg and logs.
        log.debug(util.get_comm_start(message, is_in_guild) + 'Ordered local ip, returned ' + str(local_ips))
        for local_ip in local_ips:
            await message.channel.send(local_ip)


async def toggle_ignore_dev(self, message, argument, is_in_guild):
    """
    Toggles whether or not to ignore the developer.
    If constants.IGNORE_DEVELOPER_ONLY_WORKS_ON_LINUX is set to True, this command only works on Linux.
    """
    if constants.IGNORE_DEVELOPER_ONLY_WORKS_ON_LINUX and self.on_windows:
        log.info(util.get_comm_start(message, is_in_guild) + 'Ordered ignore dev, but this is Windows')
        await message.channel.send('Windows: ignored ignore request')
    else:
        self.ignore_developer = not self.ignore_developer
        log.info(util.get_comm_start(message, is_in_guild) + 'Ordered ignore dev, set to ' + str(self.ignore_developer))
        await message.channel.send(('Windows: ' if self.on_windows else 'Linux: ') + 'set to ' + str(self.ignore_developer))


async def get_pid(self, message, argument, is_in_guild):
    """
    Gets the local PID this bot is running on.
    """
    # Gets PID
    pid = os.getpid()

    # Logs and returns PID
    log.info(util.get_comm_start(message, is_in_guild) + 'Ordered local PID, returned ' + str(pid))
    await message.channel.send(pid)


async def remote_reboot(self, message, argument, is_in_guild):
    """
    Since this bot runs on automatic crontabs, we can just exit and assume the scheduling will do the rest.
    However, we don't wanna reboot all willy-nilly.
    So we have a contingency!
    """
    self.reboot_confirmation = True
    log.info(util.get_comm_start(message, is_in_guild) + 'Ordered remote reboot, confirming...')
    await message.channel.send('Confirm remote reboot? (y/n)')


async def confirm_reboot(self, message, is_in_guild):
    """
    Confirms the reboot.
    """
    # Create response str.
    response = util.normalize_string(message.content).lower()

    # Yes
    if response.startswith('y'):
        # Gets time until bot should be back.
        current_time = datetime.today()
        # If the minute is even, our time delta will be 3 minutes 15 seconds instead of 2 minutes 15 seconds.
        time_delta_seconds = 135
        if current_time.minute % 2 == 0:
            time_delta_seconds = 185
        # Creating next bot start time.
        next_bot_start_time = datetime(current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute) + timedelta(seconds=time_delta_seconds)

        # Notify user.
        log.info(util.get_comm_start(message, is_in_guild) + 'Confirmed remote restart, restarting')
        await message.channel.send('Confirmed. Performing remote reboot...')
        await message.channel.send('Bot is estimated to be back up in approximately {} seconds.'.format((next_bot_start_time - current_time).seconds))

        # Exit.
        os._exit(0)

    # No
    elif response.startswith('n'):
        self.reboot_confirmation = False
        log.info(util.get_comm_start(message, is_in_guild) + 'Aborted remote restart')
        await message.channel.send('Remote reboot aborted.')

    # Invalid response
    else:
        log.debug(util.get_comm_start(message, is_in_guild) + 'Invalid response to confirmation message ({})'.format(response))
        await message.channel.send('Invalid response. Confirm? (y/n)')


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
    log.info(util.get_comm_start(message, is_in_guild) + 'Ordered remote update.')
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
        argument_slim = util.normalize_string(argument)
        for i in range(len(argument_slim) - 1, -1, -1):
            if argument_slim[i] not in string.digits:
                argument_slim = argument_slim[:i] + argument_slim[i + 1:]

        # If the length of our argument isn't now 8, we tell the user that and return.
        if len(argument_slim) != 8:
            log.debug(util.get_comm_start(message, is_in_guild) + 'Ordered log file, invalid date')
            await message.channel.send('Invalid date format. Should be YYYY-MM-DD')
            return

        # Now, we form a date.
        target_log = '{}-{}-{}.txt'.format(argument_slim[:4], argument_slim[4:6], argument_slim[6:8])
        is_today = target_log == datetime.today().strftime('%Y-%m-%d') + '.txt'

    # We see if that log file exists.
    if os.path.isfile(os.path.join(constants.LOGS_DIR, target_log)) or is_today:
        # Log then send file.
        log.info(util.get_comm_start(message, is_in_guild) + 'Ordered log file {}, sending'.format(target_log))
        await message.channel.send(file=discord.File(os.path.join(constants.LOGS_DIR, target_log)))

    # If the log file doesn't exist, we tell the user that.
    else:
        log.debug(util.get_comm_start(message, is_in_guild) + 'Ordered log file, file {} does not exist'.format(target_log))
        await message.channel.send('Log file {} does not exist.'.format(target_log))


async def log_list(self, message, argument, is_in_guild):
    """
    Sends a list of all the log files in the log folder.
    """
    # Logs debug
    log.debug(util.get_comm_start(message, is_in_guild) + 'Ordered log list.')

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


async def bash(self, message, argument, is_in_guild):
    """
    Runs bash using the arguments presented in the argument.
    """
    # Import subprocess so we can do the call
    import subprocess
    process = subprocess.Popen(argument.split(' '), stdout=subprocess.PIPE)

    # Get decoded version of the output.
    decoded_output = process.communicate()[0].decode('utf-8')

    # Send report and log.
    log.info(util.get_comm_start(message, is_in_guild) + 'Ordered bash execution of command ' + argument)
    if len(decoded_output) > 2000:
        await message.channel.send('Bash output greater than 2000 characters')
    elif not decoded_output:
        await message.channel.send('No output')
    else:
        await message.channel.send('Bash output: ```' + decoded_output + '```')


async def query(self, message, argument, is_in_guild):
    """
    Runs an SQL query using the arguments presented in the argument.
    """
    query_response = repr(util.query(argument))

    # Send report and log.
    log.info(util.get_comm_start(message, is_in_guild) + 'Ordered query execution of command ' + argument)
    if len(query_response) > 2000:
        await message.channel.send('Query output greater than 2000 characters')
    elif not query_response:
        await message.channel.send('No output')
    else:
        await message.channel.send('Query output: ```' + query_response + '```')
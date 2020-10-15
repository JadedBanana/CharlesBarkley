# Jadi3Pi bot file

# Imports
from src.commands import fun_commands, utility_commands, other_commands, dev_commands
from aiohttp.client_exceptions import ClientConnectorError
from datetime import datetime, timedelta
from src import constants, cron, logger, util
import platform
import discord
import socket
import os

# Outer-level crap
# Establishes logger
log = logger.JLogger()
fun_commands.log = log
utility_commands.log = log

# Gets start time
bot_start_time = datetime.today()

class JadieClient(discord.Client):

    # Keeps track of who we're copying by server and then id (hehehe)
    copied_users = {}

    # Keeps track of Hunger Games.
    curr_hg = {}

    # Keeps track of if the last attempt at randomyt was quota blocked.
    quota_blocked_last_time = False

    # Dict of commands gives easy automation so no switch statement required
    public_command_dict = {}
    developer_command_dict = {}

    # Time since last disconnect.
    bot_uptime = None

    # Keeps track of if this is the first time we've connected or not
    connected_before = False
    reconnected_since = False

    # Keep track of whether or not we should ignore the developer.
    ignore_developer = False

    # Whether or not
    reboot_confirmation = False


    # ===============================================================
    #                     GLOBAL BOT COMMANDS
    # ===============================================================
    def __init__(self, on_windows):
        """
        Sets up the commands.
        """
        # Discord client init
        discord.Client.__init__(self)

        self.on_windows = on_windows

        # Sets the public_command_dict!
        self.public_command_dict = {
            'help': self.help_command,
            'runtime': self.runtime,
            'copy': fun_commands.copy_user,
            'stopcopying': fun_commands.stop_copying,
            'uptime': self.uptime,
            'hex': utility_commands.hexadecimal, 'hexadecimal': utility_commands.hexadecimal,
            'duo': utility_commands.duodecimal, 'duodec': utility_commands.duodecimal, 'duodecimal': utility_commands.duodecimal,
            'dec': utility_commands.decimal, 'decimal': utility_commands.decimal,
            'oct': utility_commands.octal, 'octal': utility_commands.octal,
            'bin': utility_commands.binary, 'binary': utility_commands.binary,
            'randomyt': fun_commands.randomyt, 'randomyoutube': fun_commands.randomyt, 'ytroulette': fun_commands.randomyt, 'youtuberoulette': fun_commands.randomyt,
            'calc': utility_commands.evaluate, 'eval': utility_commands.evaluate, 'calculate': utility_commands.evaluate, 'evaluate': utility_commands.evaluate,
            'randomwiki': fun_commands.randomwiki, 'randomwikipedia': fun_commands.randomwiki, 'wikiroulette': fun_commands.randomwiki, 'wikipediaroulette': fun_commands.randomwiki,
            'ship': fun_commands.ship,
            'weather': utility_commands.weather,
            'uwu': fun_commands.uwuify, 'uwuify': fun_commands.uwuify,
            'owo': fun_commands.owoify, 'owoify': fun_commands.owoify,
            'business': fun_commands.business_only, 'businessonly': fun_commands.business_only,
            'ultimate': fun_commands.ultimate, 'talent': fun_commands.ultimate,
            'shsl': fun_commands.shsl,
            'hungergames': fun_commands.hunger_games, 'hg': fun_commands.hunger_games, 'hunger': fun_commands.hunger_games
        }

        # Sets the developer command_dict
        self.developer_command_dict = {
            'localip': self.get_local_ip,
            'toggleignoredev': self.toggle_ignore_dev,
            'getpid': self.get_pid, 'localpid': self.get_pid, 'pid': self.get_pid,
            'reboot': self.remote_reboot, 'restart': self.remote_reboot,
            'update': self.update_remote,
            'sendlog': self.send_log,
            'loglist': self.log_list, 'logs': self.log_list,
            'bash': self.bash
        }

    async def on_ready(self):
        """
        Activates when client is ready for use on Discord (connected and ready)
        """
        # Logs username and connection to discord
        log.info(f'{self.user} is ready')

        # Logs list of servers the bot is in
        if not self.guilds:
            log.info(f'No active guilds')
        else:
            for guild in self.guilds:
                log.info(f'Active in guild "{guild.name}" with id {guild.id}')

        # Bot uptime
        self.bot_uptime = datetime.today()

    async def on_connect(self):
        """
        Whenever the bot connects to discord.
        """
        # Connected_before ensures that we don't log the first time we go through.
        if self.connected_before:
            log.info(f'{self.user} has reconnected to Discord')
        else:
            self.connected_before = True
        # Reconnected_since makes sure we're not putting 2 disconnect messages in a row 
        # Marks ONLY when a reconnect has happened since the last disconnect
        self.reconnected_since = True

    async def on_disconnect(self):
        """
        Whenever the bot disconnects from discord.
        """
        # Reconnected_since makes sure we're not putting 2 disconnect messages in a row 
        # Marks ONLY when a reconnect has happened since the last disconnect
        if self.reconnected_since:
            log.info(f'{self.user} has disconnected from Discord')
            self.reconnected_since = False

    async def on_message(self, message):
        """
        Reacts to messages.
        """
        # Checks to make sure the message, channel, and author exist.
        if not message or not message.content or not message.channel or not message.author or message.author == self.user:
            return

        # Checks to see if the author was developer.
        author_is_developer = message.author.id in constants.DEVELOPER_DISCORD_IDS

        # If we're on Windows and the author was not developer and we're ignoring everyone but the author, we return
        if self.on_windows and not author_is_developer and constants.ON_WINDOWS_ONLY_RESPOND_TO_DEV:
            return
        # If the author was developer and we're ignoring the developer, we return (unless the command was to toggle ignore developer)
        elif author_is_developer and self.ignore_developer:
            if not message.content.startswith('j!toggleignoredev'):
                return

        # If the channel is a TextChannel, we check to make sure the guild exists and is good.
        is_in_guild = isinstance(message.channel, discord.TextChannel)
        if is_in_guild and not message.guild:
            return

        # Reactive commands (will return True if method should return now)
        # =================================================================
        if await fun_commands.copy_msg(self, message, is_in_guild): # Copy will copy a user's message if they're in the copy dict
            return
        if author_is_developer and self.reboot_confirmation:
            await self.confirm_reboot(message, is_in_guild)

        # Prompted commands
        # ==================
        command, argument = util.get_command_from_message(message)

        # Immediately returns if no command
        if not command:
            return

        # Grabs specific method from dict and runs command
        if command in self.public_command_dict.keys():
            await self.public_command_dict[command](self, message, argument, is_in_guild)

        # If the user is dev, we cycle through the developer dict as well.
        if author_is_developer:
            if command in self.developer_command_dict.keys():
                await self.developer_command_dict[command](self, message, argument, is_in_guild)


    # ===============================================================
    #                       OTHER COMMANDS
    # ===============================================================
    async def help_command(self, message, argument, is_in_guild):
        """
        Prints out the help response.
        """
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested help message')
        await message.channel.send(constants.HELP_MSG.format(constants.VERSION) + (constants.HELP_MSG_DEV_ADDENDUM if message.author.id in constants.DEVELOPER_DISCORD_IDS else '```'))

    async def runtime(self, message, argument, is_in_guild):
        """
        Prints out the runtime of the bot.
        """
        # Immediately returns if bot start time was not established
        if not bot_start_time:
            log.warning(util.get_comm_start(message, is_in_guild) + 'requested runtime, could not find start time')
            await message.channel.send('An error occurred while getting runtime, sorry! :P')
            return

        # Time delta
        time_delta = datetime.today() - bot_start_time

        # Does the thing
        bot_str = util.calculate_time_passage(time_delta)

        # Sends report, logs message
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested runtime, responded with ' + bot_str)
        await message.channel.send(constants.RUNTIME_PREFIX + bot_str)

    async def uptime(self, message, argument, is_in_guild):
        """
        Prints out the uptime of the bot.
        """
        # Immediately returns if bot start time was not established
        if not self.bot_uptime:
            log.warning(util.get_comm_start(message, is_in_guild) + 'requested runtime, could not find start time')
            await message.channel.send('An error occurred while getting uptime, sorry! :P')
            return

        # Time delta
        time_delta = datetime.today() - self.bot_uptime

        # Does the thing
        bot_str = util.calculate_time_passage(time_delta)

        # Sends report, logs message
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested uptime, responded with ' + bot_str)
        await message.channel.send(constants.UPTIME_PREFIX + bot_str)


    # ===============================================================
    #                     DEV-ONLY COMMANDS
    # ===============================================================
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
            import netifaces; local_ips = [pre + ': ' + netifaces.ifaddresses(pre)[netifaces.AF_INET][0]['addr'] for pre in constants.LINUX_IP_PREFIXES]

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
        import subprocess; process = subprocess.Popen(['git', 'pull'], stdout=subprocess.PIPE)

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
        import subprocess;
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


# Client is the thing that is basically the connection between us and Discord -- time to run.
def launch(on_windows):
    client = JadieClient(on_windows)

    # Next, start the cron loop so we don't end up running more than one of these at once.
    cron.start_cron_loop()

    # Logging new instance
    start_str = 'Starting new instance of JadieClient'
    run_str = 'Running on {} ({})'.format(socket.gethostname(), 'Windows' if on_windows else 'Linux')
    log.info('')
    log.info('=' * (max(len(start_str), len(run_str)) + 1))
    log.info(start_str)
    log.info(run_str)
    log.info('=' * (max(len(start_str), len(run_str)) + 1))

    # Making the temp dir if it doesn't exist already.
    if not os.path.isdir(constants.TEMP_DIR):
        os.mkdir(constants.TEMP_DIR)

    # All this crap around client.run occurs only if we can't connect initially.
    try:
        client.run(constants.BOT_TOKEN)
        os._exit(0)
    except ClientConnectorError:
        log.info('Cannot connect to Discord.')
        os._exit(-1)

# __main__, just in case.
if __name__ == '__main__':
    # Set the working directory to what we want so our imports work correctly
    # Also checks the OS to make sure we load into the correct working directory
    running_on_windows = platform.system() == 'Windows'
    if running_on_windows:
        os.chdir('C:/Users/popki/Projects/Python/Jadi3Pi')
    else:
        os.chdir('/home/pi/Jadi3Pi')

    # Then we launch.
    launch(running_on_windows)

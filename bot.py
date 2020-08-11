# Jadi3Pi bot file

# Imports
from aiohttp.client_exceptions import ClientConnectorError
from datetime import datetime, timedelta
import constants
import wikipedia
import platform
import discord
import logger
import random
import socket
import string
import urllib
import json
import time
import os

# Outer-level crap
# Establishes logger
log = logger.JLogger()

# Gets start time
bot_start_time = datetime.today()

class JadieClient(discord.Client):

    # Dict of commands gives easy automation so no switch statement required
    public_command_dict = {}
    developer_command_dict = {}

    # Keeps track of who we're copying by server and then id (hehehe)
    copied_users = {}

    # Time since last disconnect.
    bot_uptime = None

    # Keeps track of if this is the first time we've connected or not
    connected_before = False
    reconnected_since = False

    # Keeps track of if the last attempt at randomyt was quota blocked.
    quota_blocked_last_time = False

    # Keep track of whether or not we should ignore the developer.
    ignore_developer = False

    # Prefixes for bases that aren't decimal
    nondecimal_bases = {'0x': [16, 'hexadecimal'], '0d': [12, 'duodecimal'], '0o': [8, 'octal'], '0b': [2, 'binary']}

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
            'copy': self.copy_user,
            'stopcopying': self.stop_copying,
            'uptime': self.uptime,
            'hex': self.hexadecimal,
            'hexadecimal': self.hexadecimal, 'duo': self.duodecimal,
            'duodec': self.duodecimal, 'duodecimal': self.duodecimal,
            'dec': self.decimal, 'decimal': self.decimal,
            'oct': self.octal, 'octal': self.octal,
            'bin': self.binary, 'binary': self.binary,
            'randomyt': self.randomyt, 'randomyoutube': self.randomyt, 'ytroulette': self.randomyt, 'youtuberoulette': self.randomyt,
            'calc': self.evaluate, 'eval': self.evaluate, 'calculate': self.evaluate, 'evaluate': self.evaluate,
            'randomwiki': self.randomwiki, 'randomwikipedia': self.randomwiki, 'wikiroulette': self.randomwiki, 'wikipediaroulette': self.randomwiki
        }

        # Sets the developer command_dict
        self.developer_command_dict = {
            'localip': self.get_local_ip,
            'toggleignoredev': self.toggle_ignore_dev,
            'getpid': self.get_pid, 'localpid': self.get_pid, 'pid': self.get_pid,
            'reboot': self.remote_reboot, 'restart': self.remote_reboot,
            'update': self.update_remote,
            'sendlog': self.send_log,
            'loglist': self.log_list, 'logs': self.log_list
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
        if await self.copy_msg(message, is_in_guild): # Copy will copy a user's message if they're in the copy dict
            return
        if author_is_developer and self.reboot_confirmation:
            await self.confirm_reboot(message, is_in_guild)

        # Prompted commands
        # ==================
        command, argument = self.__get_command_from_message(message)

        # Immediately returns if no command
        if not command:
            return

        # Grabs specific method from dict and runs command
        if command in self.public_command_dict.keys():
            await self.public_command_dict[command](message, argument, is_in_guild)

        # If the user is dev, we cycle through the developer dict as well.
        if author_is_developer:
            if command in self.developer_command_dict.keys():
                await self.developer_command_dict[command](message, argument, is_in_guild)


    # ===============================================================
    #                        FUN COMMANDS
    # ===============================================================
    async def copy_msg(self, message, is_in_guild):
        """
        Copies a user's message if they have been deemed COPIABLE by someone. 
        That is, unless the message is to stop copying.
        """
        if message.content.startswith('j!stopcopying') and (len(message.content) == 13 or message.content[13] == ' '):
            return
        # Inside guilds
        if is_in_guild:
            if str(message.guild.id) in self.copied_users.keys() and message.author in self.copied_users[str(message.guild.id)]:
                await message.channel.send(message.content)
        # Inside DM's and Group Chats
        else:
            if str(message.channel.id) in self.copied_users.keys() and message.author in self.copied_users[str(message.channel.id)]:
                await message.channel.send(message.content)

    async def copy_user(self, message, argument, is_in_guild):
        """
        Marks a user down as copiable.
        Copiable users will be copied in every message they send.
        """
        # Tries to get a valid user out of the argument.
        users = self.__get_closest_users(message, argument)
        if not users:
            log.info(self.__get_comm_start(message, is_in_guild) + 'requested copy for user ' + argument + ', invalid')
            await message.channel.send('Invalid user.')
            return

        # Gets the key we'll be using for the copied_users dict.
        if is_in_guild:
            copied_key = str(message.guild.id)
        else:
            copied_key = str(message.channel.id)
        if copied_key not in self.copied_users.keys():
            self.copied_users.update({copied_key: []})

        # Adds the users to the copy dict.
        for user in users:

            # Checks to make sure it isn't self.
            if user == self.user:
                if not len(users) - 1:
                    log.debug(self.__get_comm_start(message, is_in_guild) + 'requested copy for this bot')
                    await message.channel.send('Yeah, no, I\'m not gonna copy myself.')
                continue

            # Other.
            await message.channel.send('Now copying user ' + (user.nick if user.nick else str(user)))
            if user not in self.copied_users[copied_key]:
                self.copied_users[copied_key].append(user)
                log.info(self.__get_comm_start(message, is_in_guild) + 'requested copy for user ' + str(user) + ', now copying')
            else:
                log.info(self.__get_comm_start(message, is_in_guild) + 'requested copy for user ' + str(user) + ', already copying')

    async def stop_copying(self, message, argument, is_in_guild):
        """
        Stops copying everyone in a server.
        """
        # Gets copy key
        if is_in_guild:
            copied_key = str(message.guild.id)
        else:
            copied_key = str(message.channel.id)

        # If the thing exists in the dict
        if copied_key in self.copied_users.keys():
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested to stop copying, {} users deleted from copied_users'.format(len(self.copied_users[copied_key])))
            self.copied_users.pop(copied_key)
            await message.channel.send('No longer copying people in this server.')
        else:
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested to stop copying, already done')
            await message.channel.send('Wasn\'t copying anyone here to begin with, but ok.')

    async def randomyt(self, message, argument, is_in_guild):
        """
        Generates a random youtube link.
        """
        # Rolls the random chance for a rick roll...
        if random.random() < constants.YOUTUBE_RICKROLL_CHANCE:
            log.info(self.__get_comm_start(message, is_in_guild) + 'requested random video, rickrolled them')
            await message.channel.send(constants.YOUTUBE_RICKROLL_URL)
            return

        # Otherwise...
        search_results = {'items': []}
        while not search_results['items']:
            # Gets random search term and searches
            random_search = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(random.choices(constants.YOUTUBE_SEARCH_LENGTHS, weights=constants.YOUTUBE_SEARCH_WEIGHTS)[0]))
            url_data = constants.YOUTUBE_SEARCH_URL.format(constants.YOUTUBE_API_KEY, constants.YOUTUBE_SEARCH_COUNT, random_search)

            # Opens url
            try:
                url_data = urllib.request.urlopen(url_data)
                data = url_data.read()

            # The only reason we would have an error is if quota has been reached. We tell the user that here.
            except urllib.error.HTTPError:
                # First, we get the time delta between now and when the quota should be reset.
                current_time = datetime.today()
                target_time = datetime.today()

                # If we are beyond the quota reset time, we add 1 to the target date.
                if current_time.hour >= constants.YOUTUBE_QUOTA_RESET_HOUR:
                    target_time = target_time + timedelta(days=1)

                # Then we create a new date from the target_time.
                target_time = datetime(year=target_time.year, month=target_time.month, day=target_time.day, hour=constants.YOUTUBE_QUOTA_RESET_HOUR)

                # Get time until quota and return that.
                quota_str = self.__calculate_time_passage(target_time - current_time)
                await message.channel.send('Youtube quota of 100 videos reached. Try again in {}'.format(quota_str))
                # We only put out the quota if it's the first time doing so today.
                if not self.quota_blocked_last_time:
                    log.warning(self.__get_comm_start(message, is_in_guild) + 'requested random video, quota reached')
                    self.quota_blocked_last_time = True
                return

            # Decodes data and makes it into a dict
            encoding = url_data.info().get_content_charset('utf-8')
            search_results = json.loads(data.decode(encoding))

        # Create list of video id's
        video_ids = [video['id']['videoId'] for video in search_results['items']]

        # Pick one
        choice = random.randint(0, len(video_ids) - 1)

        # Return selected video.
        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested random video, returned video id ' + video_ids[choice] + ' which was result ' + str(choice) + ' in results for ' + random_search)
        await message.channel.send(constants.YOUTUBE_VIDEO_URL_FORMAT.format(video_ids[choice]))
        self.quota_blocked_last_time = False

    async def randomwiki(self, message, argument, is_in_guild):
        """
        Generates a random youtube link.
        """
        # Simple call.
        wiki_page = wikipedia.page(wikipedia.random(1))

        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested random wikipedia page, returned {}'.format(wiki_page))
        await message.channel.send(wiki_page.url)


    # ===============================================================
    #                      UTILITY COMMANDS
    # ===============================================================
    async def evaluate(self, message, argument, is_in_guild):
        """
        Does math and shit.
        It's very basic, if your command needs 2 lines or a semicolon you're better off doing it yourself.
        """
        # Replace all the ^ with **.
        argument = argument.replace('^', '**').strip('`')

        # Print statements list for when we sub print() for our own thing.
        print_statements = []
        def add_to_print(m = None):
            print_statements.append(m)

        # Copies global vars to create local vars.
        local_globals = constants.EVAL_GLOBALS.copy()
        local_globals.update({'print': add_to_print, 'printf': add_to_print})

        # We surround our eval in a try statement so we can catch some errors.
        try:
            evaluated = eval(argument, local_globals)
        # For a syntax error, we actually SEND THE ERROR back to the user.
        except SyntaxError as e:
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested eval for expression {}, got a syntax error'.format(argument))
            await message.channel.send('Syntax Error on line {}:```{}\n'.format(e.args[1][1], e.args[1][3].split('\n')[0]) + ' ' * (e.args[1][2] - 1) + '^```')
            return
        # For a type error or value error, we send that shit back too.
        except (TypeError, ValueError) as e:
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested eval for expression {}, got a type error'.format(argument))
            await message.channel.send(repr(e))
            return

        # Prints out the print statements.
        for ps in print_statements:
            await message.channel.send(repr(ps))

        # Sends the evaluated value.
        if evaluated:
            await message.channel.send(repr(evaluated))

        # Logs evaluated value.
        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested eval for expression {}'.format(argument))

    async def hexadecimal(self, message, argument, is_in_guild):
        """
        Converts a number to hexadecimal.
        """
        # Getting the number
        num = await self.__get_num_from_argument(message, argument)

        # Error handling for not numbers
        if isinstance(num, str):
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested hex conversion for {}, invalid'.format(argument))
            return

        num = self.__convert_num_from_decimal(num, 16)

        await message.channel.send('0x' + str(num))
        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested hex conversion for {}, responded 0x{}'.format(argument, num))

    async def duodecimal(self, message, argument, is_in_guild):
        """
        Converts a number to duodecimal.
        """
        # Getting the number
        num = await self.__get_num_from_argument(message, argument)

        # Error handling for not numbers
        if isinstance(num, str):
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested duodec conversion for {}, invalid'.format(argument))
            return

        num = self.__convert_num_from_decimal(num, 12)

        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested duodec conversion for {}, responded 0d{}'.format(argument, num))
        await message.channel.send('0d' + str(num))

    async def decimal(self, message, argument, is_in_guild):
        """
        Converts a number to decimal.
        """
        # Getting the number
        num = await self.__get_num_from_argument(message, argument)

        # Error handling for not numbers
        if isinstance(num, str):
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested decimal conversion for {}, invalid'.format(argument))
            return

        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested decimal conversion for {}, responded {}'.format(argument, int(num) if num % 1 == 0 else num))
        await message.channel.send(int(num) if num % 1 == 0 else num)

    async def octal(self, message, argument, is_in_guild):
        """
        Converts a number to octal.
        """
        # Getting the number
        num = await self.__get_num_from_argument(message, argument)

        # Error handling for not numbers
        if isinstance(num, str):
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested octal conversion for {}, invalid'.format(argument))
            return

        num = self.__convert_num_from_decimal(num, 8)

        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested octal conversion for {}, responded 0o{}'.format(argument, num))
        await message.channel.send('0o' + str(num))

    async def binary(self, message, argument, is_in_guild):
        """
        Converts a number to binary.
        """
        # Getting the number
        num = await self.__get_num_from_argument(message, argument)

        # Error handling for not numbers
        if isinstance(num, str):
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested binary conversion for {}, invalid'.format(argument))
            return

        num = self.__convert_num_from_decimal(num, 2)

        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested binary conversion for {}, responded with 0b{}'.format(argument, num))
        await message.channel.send('0b' + str(num))


    # ===============================================================
    #                       OTHER COMMANDS
    # ===============================================================
    async def help_command(self, message, argument, is_in_guild):
        """
        Prints out the help response.
        """
        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested help message')
        await message.channel.send(constants.HELP_MSG.format(constants.VERSION) + (constants.HELP_MSG_DEV_ADDENDUM if message.author.id in constants.DEVELOPER_DISCORD_IDS else '```'))

    async def runtime(self, message, argument, is_in_guild):
        """
        Prints out the runtime of the bot.
        """
        # Immediately returns if bot start time was not established
        if not bot_start_time:
            log.warning(self.__get_comm_start(message, is_in_guild) + 'requested runtime, could not find start time')
            await message.channel.send('An error occurred while getting runtime, sorry! :P')
            return

        # Time delta
        time_delta = datetime.today() - bot_start_time

        # Does the thing
        bot_str = self.__calculate_time_passage(time_delta)

        # Sends report, logs message
        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested runtime, responded with ' + bot_str)
        await message.channel.send(constants.RUNTIME_PREFIX + bot_str)

    async def uptime(self, message, argument, is_in_guild):
        """
        Prints out the uptime of the bot.
        """
        # Immediately returns if bot start time was not established
        if not self.bot_uptime:
            log.warning(self.__get_comm_start(message, is_in_guild) + 'requested runtime, could not find start time')
            await message.channel.send('An error occurred while getting uptime, sorry! :P')
            return

        # Time delta
        time_delta = datetime.today() - self.bot_uptime

        # Does the thing
        bot_str = self.__calculate_time_passage(time_delta)

        # Sends report, logs message
        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested uptime, responded with ' + bot_str)
        await message.channel.send(constants.RUNTIME_PREFIX + bot_str)

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
            log.debug(self.__get_comm_start(message, is_in_guild) + 'Ordered local ip, returned ' + str(local_ip))
            await message.channel.send(local_ip)
        
        # Linux Part
        else:
            # Imports netifaces and gets the local ip's.
            import netifaces; local_ips = [pre + ': ' + netifaces.ifaddresses(pre)[netifaces.AF_INET][0]['addr'] for pre in constants.LINUX_IP_PREFIXES]

            # Sends msg and logs.
            log.debug(self.__get_comm_start(message, is_in_guild) + 'Ordered local ip, returned ' + str(local_ips))
            for local_ip in local_ips:
                await message.channel.send(local_ip)

    async def toggle_ignore_dev(self, message, argument, is_in_guild):
        """
        Toggles whether or not to ignore the developer.
        If constants.IGNORE_DEVELOPER_ONLY_WORKS_ON_LINUX is set to True, this command only works on Linux.
        """
        if constants.IGNORE_DEVELOPER_ONLY_WORKS_ON_LINUX and self.on_windows:
            log.info(self.__get_comm_start(message, is_in_guild) + 'Ordered ignore dev, but this is Windows')
            await message.channel.send('Windows: ignored ignore request')
        else:
            self.ignore_developer = not self.ignore_developer
            log.info(self.__get_comm_start(message, is_in_guild) + 'Ordered ignore dev, set to ' + str(self.ignore_developer))
            await message.channel.send(('Windows: ' if self.on_windows else 'Linux: ') + 'set to ' + str(self.ignore_developer))

    async def get_pid(self, message, argument, is_in_guild):
        """
        Gets the local PID this bot is running on.
        """
        # Gets PID
        pid = os.getpid()

        # Logs and returns PID
        log.info(self.__get_comm_start(message, is_in_guild) + 'Ordered local PID, returned ' + str(pid))
        await message.channel.send(pid)

    async def remote_reboot(self, message, argument, is_in_guild):
        """
        Since this bot runs on automatic crontabs, we can just exit and assume the scheduling will do the rest.
        However, we don't wanna reboot all willy-nilly.
        So we have a contingency!
        """
        self.reboot_confirmation = True
        log.info(self.__get_comm_start(message, is_in_guild) + 'Ordered remote reboot, confirming...')
        await message.channel.send('Confirm remote reboot? (y/n)')

    async def confirm_reboot(self, message, is_in_guild):
        """
        Confirms the reboot.
        """
        # Create response str.
        response = self.__normalize_string(message.content).lower()

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
            log.info(self.__get_comm_start(message, is_in_guild) + 'Confirmed remote restart, restarting')
            await message.channel.send('Confirmed. Performing remote reboot...')
            await message.channel.send('Bot is estimated to be back up in approximately {} seconds.'.format((next_bot_start_time - current_time).seconds))

            # Exit.
            os._exit(0)

        # No
        elif response.startswith('n'):
            self.reboot_confirmation = False
            log.info(self.__get_comm_start(message, is_in_guild) + 'Aborted remote restart')
            await message.channel.send('Remote reboot aborted.')

        # Invalid response
        else:
            log.debug(self.__get_comm_start(message, is_in_guild) + 'Invalid response to confirmation message ({})'.format(response))
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
        log.info(self.__get_comm_start(message, is_in_guild) + 'Ordered remote update.')
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
            argument_slim = self.__normalize_string(argument)
            for i in range(len(argument_slim) - 1, -1, -1):
                if argument_slim[i] not in string.digits:
                    argument_slim = argument_slim[:i] + argument_slim[i + 1:]

            # If the length of our argument isn't now 8, we tell the user that and return.
            if len(argument_slim) != 8:
                log.debug(self.__get_comm_start(message, is_in_guild) + 'Ordered log file, invalid date')
                await message.channel.send('Invalid date format. Should be YYYY-MM-DD')
                return

            # Now, we form a date.
            target_log = '{}-{}-{}.txt'.format(argument_slim[:4], argument_slim[4:6], argument_slim[6:8])
            is_today = target_log == datetime.today().strftime('%Y-%m-%d') + '.txt'

        # We see if that log file exists.
        if os.path.isfile(os.path.join(constants.LOGS_DIR, target_log)) or is_today:
            # Log then send file.
            log.info(self.__get_comm_start(message, is_in_guild) + 'Ordered log file {}, sending'.format(target_log))
            await message.channel.send(file=discord.File(os.path.join(constants.LOGS_DIR, target_log)))

        # If the log file doesn't exist, we tell the user that.
        else:
            log.debug(self.__get_comm_start(message, is_in_guild) + 'Ordered log file, file {} does not exist'.format(target_log))
            await message.channel.send('Log file {} does not exist.'.format(target_log))

    async def log_list(self, message, argument, is_in_guild):
        """
        Sends a list of all the log files in the log folder.
        """
        # Logs debug
        log.debug(self.__get_comm_start(message, is_in_guild) + 'Ordered log list.')

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


    # ===============================================================
    #               INTERNAL-USE (PRIVATE) COMMANDS
    # ===============================================================
    async def __get_num_from_argument(self, message, argument):
        # Gets usages for arguments
        argument = self.__normalize_string(argument)
        argument2 = argument.lower()

        # Nondecimal bases
        for base in self.nondecimal_bases.keys():
            if argument2.startswith(base):
                try:
                    return self.__convert_num_to_decimal(argument[2:], self.nondecimal_bases[base][0])
                except ValueError:
                    await message.channel.send(argument + ' is not a valid {} number').format(self.nondecimal_bases[base][1])
                    return ''

        # Decimal base
        try:
            return float(argument)
        except ValueError:
            await message.channel.send(argument + ' is not a valid decimal number')
            return ''

    @staticmethod
    def __get_command_from_message(message):
        """
        Gets a command from a message, with one argument after
        """
        # Immediately returns if command prefix is missing
        if not message.content.lower().startswith(constants.GLOBAL_PREFIX):
            return None, None

        # Removes global prefix from message
        message = message.content[len(constants.GLOBAL_PREFIX):]

        # Finds space or end of line -- whichever comes first, and returns
        end_index = message.find(' ')
        if not end_index + 1:
            return message, None
        return message[:end_index].lower(), message[end_index + 1:]

    @staticmethod
    def __get_closest_users(message, argument):
        """
        Gets the closest user to the given argument. Returns list of users.
        """
        # Checks to see if this message specifically mentions anyone.
        if message.mentions:
            return message.mentions
        return []

    @staticmethod
    def __calculate_time_passage(time_delta):
        """
        Creates the time delta string and reports to channel, then returns time delta string.
        """
        bot_str = ''
        if time_delta.days:
            bot_str+= str(time_delta.days) + 'd '
        if int(time_delta.seconds / 3600):
            bot_str+= str(int(time_delta.seconds / 3600)) + 'h '
        if int(time_delta.seconds / 60):
            bot_str+= str(int(time_delta.seconds % 3600 / 60)) + 'm '
        bot_str+= str(time_delta.seconds % 60) + 's '

        return bot_str

    @staticmethod
    def __normalize_string(input_str, remove_double_spaces=True):
        """
        Removes spaces at the start and end as well as double spaces in a string.
        """
        # Start spaces
        while input_str.startswith(' '):
            input_str = input_str[1:]
        # End spaces
        while input_str.endswith(' '):
            input_str = input_str[:len(input_str) - 1]
        # Double spaces
        if remove_double_spaces:
            while '  ' in input_str:
                input_str = input_str.replace('  ', ' ')
        # Code segments, spoilers, italics/bold
        input_str = input_str.strip('`').strip('*').strip('_')
        # Return
        return input_str

    @staticmethod
    def __get_comm_start(message, is_in_guild):
        """
        Gets the command prefix. Just used to cut down space.
        """
        if is_in_guild:
            return constants.COMM_LOG_PREFIX_GUILD.format(message.author, message.channel, message.guild)
        elif isinstance(message.channel, discord.DMChannel):
            return constants.COMM_LOG_PREFIX.format(message.author, message.channel)
        else:
            return constants.COMM_LOG_PREFIX.format(message.author, message.channel)

    @staticmethod
    def __convert_num_to_decimal(n, base):
        """
        Converts a number to decimal from another base.
        """
        # If there's more than 1 decimal point, we raise a ValueError.
        if n.count('.') > 1:
            raise ValueError()

        # If there is no decimal point, we take the easy way out.
        if '.' not in n:
            return int(n, base=base)

        # Otherwise, we're in for a ride.
        else:
            # Get the index of the period.
            per_index = n.find('.')

            # Take the easy way for the numbers BEFORE the decimal point.
            final_num = int(n[:per_index], base=base)

            # We add a little leniency for those below base 36 in terms of capitalization.
            if base <= 36:
                n = n.upper()

            # Do it ourselves for numbers after.
            for index in range(per_index + 1, len(n)):
                exp = per_index - index
                num_of = constants.CONVERT_CHARS.find(n[index])
                # A little error handling for -1's or stuff outside the range.
                if num_of == -1 or num_of >= base:
                    raise ValueError()
                else:
                    final_num+= base**exp * num_of

            return final_num

    @staticmethod
    def __convert_num_from_decimal(n, base):
        """
        Converts a number from decimal to another base.
        """
        # Gets maximum exponent of base
        exp = 0
        while base**(exp  + 1) <= n:
            exp+= 1

        # Adds all the numbers that aren't a multiple of base to the string.
        num_str = ''
        while n != 0 and exp >= constants.MAX_CONVERT_DEPTH:
            # Adds a decimal point if we're below 0 exp.
            if exp == -1:
                num_str+= '.'
            num_str+= constants.CONVERT_CHARS[int(n / base**exp)]
            n -= (int(n / base**exp) * base**exp)
            exp-= 1

        # Adds all the zeros between exp and 0 if exp is not below 0.
        while exp >= 0:
            num_str+= '0'
            exp-= 1

        return num_str


# Client is the thing that is basically the connection between us and Discord -- time to run.
def launch(on_windows):
    client = JadieClient(on_windows)

    # Next, start the cron loop so we don't end up running more than one of these at once.
    import cron
    cron.start_cron_loop()

    # Logging new instance
    start_str = 'Starting new instance of JadieClient'
    run_str = 'Running on {} ({})'.format(socket.gethostname(), 'Windows' if on_windows else 'Linux')
    log.info('')
    log.info('=' * (max(len(start_str), len(run_str)) + 1))
    log.info(start_str)
    log.info(run_str)
    log.info('=' * (max(len(start_str), len(run_str)) + 1))

    # All this crap around client.run occurs only if we can't connect initially.
    try:
        client.run(constants.BOT_TOKEN)
        os._exit(0)
    except ClientConnectorError:
        log.info('Cannot connect to Discord, will attempt again in 3 minutes.')

        # Sleeps for 3 minutes so we don't overdo it.
        time.sleep(180)

        os._exit(-1)

# __main__, just in case.
if __name__ == '__main__':
    # Set the working directory to what we want so our imports work correctly
    # Also checks the OS to make sure we load into the correct working directory
    on_windows = platform.system() == 'Windows'
    if on_windows:
        os.chdir('C:/Users/popki/Projects/Python/Jadi3Pi')
    else:
        os.chdir('/home/pi/Jadi3Pi')

    # Then we launch.
    launch(on_windows)

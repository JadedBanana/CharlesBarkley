# Jadi3Pi run file
# Set the working directory to what we want so our imports work correctly
import os
os.chdir('/home/pi/Jadi3Pi')

# Imports
from aiohttp.client_exceptions import ClientConnectorError
from datetime import datetime
from sys import exc_info
import constants
import discord
import logger
import random
import string
import urllib
import json
import math
import time

# Establishes logger
log = logger.JLogger()
# Gets start time
bot_start_time = datetime.today()

class JadieClient(discord.Client):
    
    # Dict of commands gives easy automation so no switch statement required
    command_dict = {}
        
    # Keeps track of who we're copying by server and then id(hehehe)
    copied_users = {}
    
    # Time since last disconnect.
    bot_uptime = None
    
    # Keeps track of if this is the first time we've connected or not
    connected_before = False
    reconnected_since = False
    
    # Keeps track of if the last attempt at randomyt was quota blocked.
    quota_blocked_last_time = False
    
    # Prefixes for bases that aren't decimal
    nondecimal_bases = {'0x': [16, 'hexadecimal'], '0d': [12, 'duodecimal'], '0o': [8, 'octal'], '0b': [2, 'binary']}    
    
    
    # ===============================================================
    #                     GLOBAL BOT COMMANDS
    # ===============================================================
    def __init__(self):
        """
        Sets up the commands.
        """
        discord.Client.__init__(self)
        # Sets the command_dict!
        self.command_dict = {
            'help': self.help_command,
            'runtime': self.runtime,
            'copy': self.copy_user,
            'stopcopying': self.stop_copying,
            'uptime': self.uptime,
            'hex': self.hexadecimal,
            'hexadecimal': self.hexadecimal,
            'duo': self.duodecimal,
            'duodec': self.duodecimal,
            'duodecimal': self.duodecimal,
            'dec': self.decimal,
            'decimal': self.decimal,
            'oct': self.octal,
            'octal': self.octal,
            'bin': self.binary,
            'binary': self.binary,
            'randomyt': self.randomyt,
            'randomyoutube': self.randomyt,
            'ytroulette': self.randomyt,
            'youtuberoulette': self.randomyt,
            'calc': self.evaluate,
            'eval': self.evaluate,
            'calculate': self.evaluate,
            'evaluate': self.evaluate
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
            
        # If the channel is a TextChannel, we check to make sure the guild exists and is good.
        is_in_guild = isinstance(message.channel, discord.TextChannel)
        if is_in_guild and not message.guild:
            return
            
        # Reactive commands (will return True if method should return now)
        # =================================================================
        if await self.copy_msg(message, is_in_guild): # Copy will copy a user's message if they're in the copy dict
            return
        
        # Prompted commands
        # ==================
        command, argument = self.__get_command_from_message(message)
        
        # Immediately returns if no command
        if not command:
            return
            
        # Grabs specific method from dict and runs command
        if command in self.command_dict.keys():
            await self.command_dict[command](message, argument, is_in_guild)
    
    
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
            await message.channel.send('Invalid user.')
            log.info(self.__get_comm_start(message, is_in_guild) + 'requested copy for user ' + argument + ', invalid user')
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
                    log.debug(self.__get_comm_start(message, is_in_guild) + 'requested copy for THIS BOT. T_T')
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
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested to stop copying people, {} users deleted from copied_users'.format(len(self.copied_users[copied_key])))
            self.copied_users.pop(copied_key)
            await message.channel.send('No longer copying people in this server.')
        else:
            await message.channel.send('Wasn\'t copying anyone here to begin with, but ok.')
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested to stop copying people, already done')
    
    async def randomyt(self, message, argument, is_in_guild):
        """Generates a random youtube link."""
        # Rolls the random chance for a rick roll...
        if random.random() < constants.YOUTUBE_RICKROLL_CHANCE:
            await message.channel.send(constants.YOUTUBE_RICKROLL_URL)
            log.info(self.__get_comm_start(message, is_in_guild) + 'requested random video, rickrolled them')
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
                await message.channel.send('Youtube quota of 100 videos reached. Try again tomorrow.')
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
        await message.channel.send(constants.YOUTUBE_VIDEO_URL_FORMAT.format(video_ids[choice]))
        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested random video, returned video id ' + video_ids[choice] + ' which was result number ' + str(choice) + ' in the results for ' + random_search)
        self.quota_blocked_last_time = False
    
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
            await message.channel.send('Syntax Error on line {}:```{}\n'.format(e.args[1][1], e.args[1][3].split('\n')[0]) + ' ' * (e.args[1][2] - 1) + '^```')
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested eval for expression {}, got a syntax error'.format(argument))
            return
        # For a type error or value error, we send that shit back too.
        except (TypeError, ValueError) as e:
            await message.channel.send(repr(e))
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested eval for expression {}, got a type error'.format(argument))
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
        """Converts a number to hexadecimal"""
        # Getting the number
        num = await self.__get_num_from_argument(message, argument)
        
        # Error handling for not numbers
        if isinstance(num, str):
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested hex conversion for number {}, invalid'.format(argument))
            return
            
        num = self.__convert_num_from_decimal(num, 16)
        
        await message.channel.send('0x' + str(num))
        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested hex conversion for number {}, responded with 0x{}'.format(argument, num))
        
    async def duodecimal(self, message, argument, is_in_guild):
        """Converts a number to duodecimal"""
        # Getting the number
        num = await self.__get_num_from_argument(message, argument)
        
        # Error handling for not numbers
        if isinstance(num, str):
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested duodec conversion for number {}, invalid'.format(argument))
            return
            
        num = self.__convert_num_from_decimal(num, 12)
        
        await message.channel.send('0d' + str(num))
        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested duodec conversion for number {}, responded with 0d{}'.format(argument, num))
        
    async def decimal(self, message, argument, is_in_guild):
        """Converts a number to decimal."""
        # Getting the number
        num = await self.__get_num_from_argument(message, argument)
        
        # Error handling for not numbers
        if isinstance(num, str):
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested decimal conversion for number {}, invalid'.format(argument))
            return
            
        await message.channel.send(int(num) if num % 1 == 0 else num)
        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested decimal conversion for number {}, responded with {}'.format(argument, int(num) if num % 1 == 0 else num))
        
    async def octal(self, message, argument, is_in_guild):
        """Converts a number to octal"""
        # Getting the number
        num = await self.__get_num_from_argument(message, argument)
        
        # Error handling for not numbers
        if isinstance(num, str):
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested octal conversion for number {}, invalid'.format(argument))
            return
            
        num = self.__convert_num_from_decimal(num, 8)
        
        await message.channel.send('0o' + str(num))
        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested octal conversion for number {}, responded with 0o{}'.format(argument, num))
        
    async def binary(self, message, argument, is_in_guild):
        """Converts a number to binary"""
        # Getting the number
        num = await self.__get_num_from_argument(message, argument)
        
        # Error handling for not numbers
        if isinstance(num, str):
            log.debug(self.__get_comm_start(message, is_in_guild) + 'requested binary conversion for number {}, invalid'.format(argument))
            return
            
        num = self.__convert_num_from_decimal(num, 2)
        
        await message.channel.send('0b' + str(num))
        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested binary conversion for number {}, responded with 0b{}'.format(argument, num))
    
    
    # ===============================================================
    #                       OTHER COMMANDS
    # ===============================================================
    async def help_command(self, message, argument, is_in_guild):
        """
        Prints out the help response.
        """
        await message.channel.send(constants.HELP_MSG.format(constants.VERSION))
        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested help message')
        
    async def runtime(self, message, argument, is_in_guild):
        """
        Prints out the runtime of the bot.
        """
        # Immediately returns if bot start time was not established
        if not bot_start_time:
            await message.channel.send('An error occurred while getting runtime, sorry! :P')
            log.warning(self.__get_comm_start(message, is_in_guild) + 'requested runtime, could not find start time')
            return
            
        # Time delta
        time_delta = datetime.today() - bot_start_time
        
        bot_str = await self.__report_time_passage(message, time_delta, constants.RUNTIME_PREFIX)
        
        # Logs message
        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested runtime, responded with ' + bot_str[len(constants.RUNTIME_PREFIX):])
        
    async def uptime(self, message, argument, is_in_guild):
        """
        Prints out the uptime of the bot.
        """
        # Immediately returns if bot start time was not established
        if not self.bot_uptime:
            await message.channel.send('An error occurred while getting uptime, sorry! :P')
            log.warning(self.__get_comm_start(message, is_in_guild) + 'requested runtime, could not find start time')
            return
            
        # Time delta
        time_delta = datetime.today() - self.bot_uptime
        
        # Does the thing
        bot_str = await self.__report_time_passage(message, time_delta, constants.UPTIME_PREFIX)
        
        # Logs message
        log.debug(self.__get_comm_start(message, is_in_guild) + 'requested uptime, responded with ' + bot_str[len(constants.UPTIME_PREFIX):])
    
    
    # ===============================================================
    #               INTERNAL-USE (PRIVATE) COMMANDS
    # ===============================================================    
    def __get_command_from_message(self, message):
        """Gets a command from a message, with one argument after"""
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
        
    def __get_closest_users(self, message, argument):
        """Gets the closest user to the given argument. Returns list of users."""
        # Checks to see if this message specifically mentions anyone.
        if message.mentions:
            return message.mentions
        return []
        
    async def __report_time_passage(self, message, time_delta, bot_str):
        """
        Creates the time delta string and reports to channel, then returns time delta string.
        """
        if time_delta.days:
            bot_str+= str(time_delta.days) + 'd '
        if int(time_delta.seconds / 3600):
            bot_str+= str(int(time_delta.seconds / 3600)) + 'h '
        if int(time_delta.seconds / 60):
            bot_str+= str(int(time_delta.seconds % 3600 / 60)) + 'm '
        bot_str+= str(time_delta.seconds % 60) + 's '
        
        # Send report
        await message.channel.send(bot_str)
        
        return bot_str
    
    @staticmethod
    def __normalize_string(string, remove_double_spaces=True):
        """Removes spaces at the start and end as well as double spaces in a string."""
        # Start spaces
        while string.startswith(' '):
            string = string[1:]
        # End spaces
        while string.endswith(' '):
            string = string[:len(string) - 1]
        # Double spaces
        if remove_double_spaces:
            while '  ' in string:
                string = string.replace('  ', ' ')
        # Return
        return string
    
    @staticmethod
    def __get_comm_start(message, is_in_guild):
        """Gets the command prefix. Just used to cut down space."""
        if is_in_guild:
            return constants.COMM_LOG_PREFIX.format(message.author, message.channel, message.guild)
        elif isinstance(message.channel, discord.DMChannel):
            return constants.COMM_LOG_PREFIX.format(message.author, message.channel, 'DM')
        else:
            return constants.COMM_LOG_PREFIX.format(message.author, message.channel, 'Group Chat')
    
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
    def __convert_num_to_decimal(n, base):
        """Converts a number to decimal from another base."""
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
        """Converts a number from decimal to another base."""
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
if __name__ == '__main__':
    client = JadieClient()
    
    # Logging new instance
    start_str = 'Starting new instance of JadieClient'
    log.info('')
    log.info('=' * (len(start_str) + 1))
    log.info(start_str)
    log.info('=' * (len(start_str) + 1))
    
    # All this crap around client.run occurs only if we can't connect initially.
    try:
        client.run(constants.BOT_TOKEN)
        exit(0)
    except ClientConnectorError:
        log.info('Cannot connect to Discord, will attempt again in 3 minutes.')
            
        # Sleeps for 3 minutes so we don't overdo it.
        time.sleep(180)
        
        exit(-1)

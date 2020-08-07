# Jadi3Pi run file
# Imports
from aiohttp.client_exceptions import ClientConnectorError
from datetime import datetime
import constants
import discord
import logger
import time
import os

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
            'uptime': self.uptime
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
        if not message or not message.content or not message.channel or not message.guild or not message.author or message.author == self.user:
            return
            
        # Reactive commands (will return True if method should return now)
        # =================================================================
        if await self.copy_msg(message): # Copy will copy a user's message if they're in the copy dict
            return
        
        # Prompted commands
        # ==================
        command, argument = self.__get_command_from_message(message)
        
        # Immediately returns if no command
        if not command:
            return
            
        # Grabs specific method from dict and runs command
        if command in self.command_dict.keys():
            await self.command_dict[command](message, argument)
    
    
    # ===============================================================
    #                        FUN COMMANDS
    # ===============================================================
    async def copy_msg(self, message):
        """
        Copies a user's message if they have been deemed COPIABLE by someone. 
        That is, unless the message is to stop copying.
        """
        if message.content.startswith('j!stopcopying') and (len(message.content) == 13 or message.content[13] == ' '):
            return
        if str(message.guild.id) in self.copied_users.keys() and message.author in self.copied_users[str(message.guild.id)]:
            await message.channel.send(message.content)
        
    async def copy_user(self, message, argument):
        """
        Marks a user down as copiable.
        Copiable users will be copied in every message they send.
        """
        # Tries to get a valid user out of the argument.
        users = self.__get_closest_users(message, argument)
        if not users:
            await message.channel.send('Invalid user.')
            log.info(self.__get_comm_start + 'requested copy for user ' + argument + ', invalid user')
            return
        
        # Adds the users to the copy dict.
        if str(message.guild.id) not in self.copied_users.keys():
            self.copied_users.update({str(message.guild.id): []})
        for user in users:
            
            # Checks to make sure it isn't self.
            if user == self.user:
                if not len(users) - 1:
                    log.debug(self.__get_comm_start + 'requested copy for THIS BOT. T_T')
                    await message.channel.send('Yeah, no, I\'m not gonna copy myself.')
                continue
                
            # Other.
            await message.channel.send('Now copying user ' + (user.nick if user.nick else str(user)))
            if user not in self.copied_users[str(message.guild.id)]:
                self.copied_users[str(message.guild.id)].append(user)
                log.info(self.__get_comm_start + 'requested copy for user ' + str(user) + ', now copying')
            else:
                log.info(self.__get_comm_start + 'requested copy for user ' + str(user) + ', already copying')
            
    async def stop_copying(self, message, argument):
        """
        Stops copying everyone in a server.
        """
        # If the thing exists in the dict
        if str(message.guild.id) in self.copied_users.keys():
            log.debug(self.__get_comm_start(message) + 'requested to stop copying people, {} users deleted from copied_users'.format(len(self.copied_users[str(message.guild.id)])))
            self.copied_users.pop(str(message.guild.id))
            await message.channel.send('No longer copying people in this server.')
        else:
            await message.channel.send('Wasn\'t copying anyone here to begin with, but ok.')
            log.debug(self.__get_comm_start(message) + 'requested to stop copying people, already done')
    
    
    # ===============================================================
    #                      UTILITY COMMANDS
    # ===============================================================
    async def help_command(self, message, argument):
        """
        Prints out the help response.
        """
        await message.channel.send(constants.HELP_MSG.format(constants.VERSION))
        log.debug(self.__get_comm_start(message) + 'requested help message')
        
    async def runtime(self, message, argument):
        """
        Prints out the runtime of the bot.
        """
        # Immediately returns if bot start time was not established
        if not bot_start_time:
            await message.channel.send('An error occurred while getting runtime, sorry! :P')
            log.warning(self.__get_comm_start(message) + 'requested runtime, could not find start time')
            return
            
        # Time delta
        time_delta = datetime.today() - bot_start_time
        
        bot_str = await self.report_time_passage(message, time_delta, constants.RUNTIME_PREFIX)
        
        # Logs message
        log.debug(self.__get_comm_start(message) + 'requested runtime, responded with ' + bot_str[len(constants.RUNTIME_PREFIX):])
        
    async def uptime(self, message, argument):
        """
        Prints out the uptime of the bot.
        """
        # Immediately returns if bot start time was not established
        if not self.bot_uptime:
            await message.channel.send('An error occurred while getting uptime, sorry! :P')
            log.warning(self.__get_comm_start(message) + 'requested runtime, could not find start time')
            return
            
        # Time delta
        time_delta = datetime.today() - self.bot_uptime
        
        # Does the thing
        bot_str = await self.report_time_passage(message, time_delta, constants.UPTIME_PREFIX)
        
        # Logs message
        log.debug(self.__get_comm_start(message) + 'requested uptime, responded with ' + bot_str[len(constants.UPTIME_PREFIX):])
        
    async def report_time_passage(self, message, time_delta, bot_str):
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
        
    @staticmethod
    def __get_comm_start(message):
        """Gets the command prefix. Just used to cut down space."""
        return constants.COMM_LOG_PREFIX.format(message.author, message.channel, message.guild) 
        
        
# Client is the thing that is basically the connection between us and Discord -- time to run.
if __name__ == '__main__':
    client = JadieClient()
    
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

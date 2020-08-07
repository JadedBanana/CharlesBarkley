# Jadi3Pi run file
# Imports
from datetime import datetime
import constants
import discord
import logger
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
    
    
    # ===============================================================
    #                     GLOBAL BOT COMMANDS
    # ===============================================================
    def __init__(self):
        discord.Client.__init__(self)
        self.command_dict = {
            'runtime': self.runtime,
            'copy': self.copy_user
        }
    
    async def on_ready(self):
        """Activates when client first links to Discord"""
        # Logs username and connection to discord
        name_str = f'{self.user} has connected to Discord'
        log.info('=' * (len(name_str) + 1))
        log.info(name_str)
        log.info('=' * (len(name_str) + 1))
        
        # Logs list of servers the bot is in
        if not self.guilds:
            log.info(f'No active guilds')
        else:
            for guild in self.guilds:
                log.info(f'Active in guild "{guild.name}" with id {guild.id}')
        
        # Spacing
        log.info('')
        
    async def on_message(self, message):
        """Reacts to messages."""
        if message.author == self.user:
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
        """Copies a user's message if they have been deemed COPIABLE by someone. 
        That is, unless the message is to stop copying."""
        if str(message.guild.id) in self.copied_users.keys() and message.author in self.copied_users[str(message.guild.id)]:
            await message.channel.send(message.content)
        
    async def copy_user(self, message, argument):
        """Marks a user down as copiable -- so they will be copied in every message they send."""
        # Tries to get a valid user out of the argument.
        users = self.__get_closest_users(message, argument)
        if not users:
            await message.channel.send('Invalid user.')
            log.info('User ' + str(message.author) + ' requested copy for user ' + argument + ', no idea who that is')
            return
        
        # Adds the users to the copy dict.
        if str(message.guild.id) not in self.copied_users.keys():
            self.copied_users.update({str(message.guild.id): []})
        for user in users:
            await message.channel.send('Now copying user ' + user.nick)
            if user not in self.copied_users[str(message.guild.id)]:
                self.copied_users[str(message.guild.id)].append(user)
                log.info('User ' + str(message.author) + ' requested copy for user ' + str(user) + ', now copying')
            else:
                log.info('User ' + str(message.author) + ' requested copy for user ' + str(user) + ', already copying')
            
            
    
    
    # ===============================================================
    #                      UTILITY COMMANDS
    # ===============================================================
    async def runtime(self, message, argument):
        """Prints out the runtime of the bot"""
        # Time delta
        time_delta = datetime.today() - bot_start_time
        
        # Get bot string
        bot_str = constants.RUNTIME_PREFIX
        if time_delta.days:
            bot_str+= str(time_delta.days) + 'd '
        if int(time_delta.seconds / 3600):
            bot_str+= str(int(time_delta.seconds / 3600)) + 'h '
        if int(time_delta.seconds / 60):
            bot_str+= str(int(time_delta.seconds % 3600 / 60)) + 'm '
        bot_str+= str(time_delta.seconds % 60) + 's '
        
        # Send report
        await message.channel.send(bot_str)
        # Logs message
        log.info('User ' + str(message.author) + ' requested runtime, responded with ' + bot_str[len(constants.RUNTIME_PREFIX):])
    
    
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
        
        
# Client is the thing that is basically the connection between us and Discord -- time to run.
if __name__ == '__main__':
    client = JadieClient()
    client.run(constants.BOT_TOKEN)

# Jadi3Pi run file
# Imports
import constants
import discord
import logger
import os

# Establishes logger
log = logger.JLogger()

class JadieClient(discord.Client):
    
    # Keeps track of who we're copying by server and then id(hehehe)
    copied_users = {}
    
    
    # ===============================================================
    #                     GLOBAL BOT COMMANDS
    # ===============================================================
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
        if copy_msg(message): # Copy will copy a user's message
            return
        
        # Prompted commands
        # ==================
        command, argument = __get_command_from_message(message)
        
        # Immediately returns if no command
        if not command:
            return
    
    
    # ===============================================================
    #                        FUN COMMANDS
    # ===============================================================
    def copy_msg(message):
        pass
    
    
    # ===============================================================
    #                      UTILITY COMMANDS
    # ===============================================================
    
    
    # ===============================================================
    #               INTERNAL-USE (PRIVATE) COMMANDS
    # ===============================================================
    def __get_command_from_message(message):
        """Gets a command from a message, with one argument after"""
        # Immediately returns if command prefix is missing
        if not message.lower().startswith(constants.GLOBAL_PREFIX):
            return None, None
            
        # Removes global prefix from message
        message = message[len(constants.GLOBAL_PREFIX):]
        
        # Finds space or end of line -- whichever comes first, and returns
        end_index = message.find(' ')
        if not end_index + 1:
            return message, None
        return message[:end_index].lower(), message[end_index + 1:]
        
        
# Client is the thing that is basically the connection between us and Discord -- time to run.
if __name__ == '__main__':
    client = JadieClient()
    client.run(constants.BOT_TOKEN)

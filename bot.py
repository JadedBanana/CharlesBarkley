# Jadi3Pi run file
# Imports
import os
import logger
import discord
import constants

# Establishes logger
log = logger.JLogger()

class JadieClient(discord.Client):
    
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
        
# Client is the thing that is basically the connection between us and Discord -- time to run.
client = JadieClient()
client.run(constants.BOT_TOKEN)

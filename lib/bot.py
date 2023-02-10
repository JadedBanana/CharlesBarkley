"""
The bot class.
The main meat of the bot. Inherits from discord.Client, is the main point at which Discord API crosses over
into self processing.
"""
# Local Imports
from lib.util import environment

# Package Imports
from aiohttp.client_exceptions import ClientConnectorError
from discord.errors import LoginFailure
from datetime import datetime
import discord
import logging
import socket
import sys


# Global bot variables
GLOBAL_PREFIX = 'j!'
VERSION_NUMBER = '0.8.6'


class JadieClient(discord.Client):

    def __init__(self):
        """
        Instantiates the bot.
        Does a lot to do so, like getting the start time and uptime, as well as loading the commands.
        """
        # Connection variables.
        # Keeps track of if this is the first time we've connected or not.
        self.connected_before = False
        self.reconnected_since = False

        # Store environment variables.
        self.global_prefix = GLOBAL_PREFIX
        self.user_id = [int(dev_id) for dev_id in environment.get("DEVELOPER_DISCORD_IDS")]

        # Discord client init
        intents = discord.Intents.default()
        discord.Client.__init__(self, intents=intents)


    async def on_ready(self):
        """
        Activates when client is ready for use on Discord (connected and ready).
        Mostly just logs the active guilds and stores the bot uptime.
        """
        # Logs username and connection to discord
        logging.info(f'{self.user} is ready')

        # Logs list of servers the bot is in
        if not self.guilds:
            logging.debug(f'No active guilds')
        else:
            for guild in self.guilds:
                logging.debug(f'Active in guild "{guild.name}" with id {guild.id}')

        # Bot uptime
        self.bot_uptime = datetime.today()


    async def on_connect(self):
        """
        Whenever the bot connects to discord, this method launches.
        Good for logging purposes.
        """
        # Connected_before ensures that we don't log the first time we go through.
        if self.connected_before:
            logging.info(f'{self.user} has reconnected to Discord')
        else:
            self.connected_before = True
        # Reconnected_since makes sure we're not putting 2 disconnect messages in a row.
        # Marks ONLY when a reconnect has happened since the last disconnect.
        self.reconnected_since = True


    async def on_disconnect(self):
        """
        Whenever the bot disconnects from discord, this method launches.
        Good for logging purposes.
        """
        # Reconnected_since makes sure we're not putting 2 disconnect messages in a row
        # Marks ONLY when a reconnect has happened since the last disconnect
        if self.reconnected_since:
            logging.info(f'{self.user} has disconnected from Discord')
            self.reconnected_since = False


# Client is the thing that is basically the connection between us and Discord -- time to run.
def launch():
    """
    Launches the JadieClient.

    Raises:
        SystemExit: Bot can't connect to Discord. Exit.
    """
    # Logging new instance
    logging.info('Starting new instance of JadieClient')
    logging.info(f'Running on {socket.gethostname()} '
                 f'({"Deployment" if environment.get("DEPLOYMENT_CLIENT") else "Development"} Version)')

    # Right here, instantiating the client object!
    client = JadieClient()

    # Attempt to connect the client.
    try:
        client.run(environment.get('BOT_TOKEN'))

    # If a connection can't be made, then log that error and exit.
    except ClientConnectorError:
        logging.critical('Cannot connect to Discord.')
        sys.exit(-1)

    # If the login was bad, then log that error and exit.
    except LoginFailure:
        logging.critical('Failed to log in to Discord.')
        sys.exit(-1)

    # If the client loop ever stops running, the process should terminate.
    finally:
        logging.critical('Bot terminated unexpectedly.')
        sys.exit(0)

# ===============================================================
#                         MAIN BOT CLASS
# ===============================================================
from aiohttp.client_exceptions import ClientConnectorError
from lib.util import environment
from datetime import datetime
import discord
import logging
import socket

class JadieClient(discord.Client):


    def __init__(self):
        """
        Instantiates the bot.
        """
        # Bot start time and bot uptime.
        self.bot_start_time = datetime.today()
        self.bot_uptime = None

        # Connection variables.
        # Keeps track of if this is the first time we've connected or not.
        self.connected_before = False
        self.reconnected_since = False

        # Load the commands.
        from lib import commands
        commands.load_commands()

        # Discord client init
        discord.Client.__init__(self)


    async def on_ready(self):
        """
        Activates when client is ready for use on Discord (connected and ready).
        Mostly just logs the active guilds and stores the bot uptime.
        """
        # Logs username and connection to discord
        logging.info(f'{self.user} is ready')

        # Logs list of servers the bot is in
        if not self.guilds:
            logging.info(f'No active guilds')
        else:
            for guild in self.guilds:
                logging.info(f'Active in guild "{guild.name}" with id {guild.id}')

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


    async def on_message(self, message):
        """
        Reacts to messages.
        """
        # Checks to make sure the message, channel, and author exist.
        if not message or not message.content or not message.channel or not message.author or message.author == self.user:
            return


# Client is the thing that is basically the connection between us and Discord -- time to run.
def launch():
    """
    Launches the JadieClient.

    Raises:
        SystemExit: Bot can't connect to Discord. Exit.
    """
    # Logging new instance
    logging.info('Starting new instance of JadieClient')
    logging.info(f'Running on {socket.gethostname()} ({"Deployment" if environment.get("DEPLOYMENT_CLIENT") else "Development"} Version)')

    # Right here, instantiating the client object!
    client = JadieClient()

    # Attempt to connect the client.
    try:
        client.run(environment.get('BOT_TOKEN'))

    # If a connection can't be made, then log that error and exit.
    except ClientConnectorError:
        logging.critical('Cannot connect to Discord.')
        exit(-1)

    # If the client loop ever stops running, the process should terminate.
    finally:
        logging.critical('Bot terminated unexpectedly')
        exit(-2)
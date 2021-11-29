"""
The bot class.
The main meat of the bot. Inherits from discord.Client, is the main point at which Discord API crosses over
into self processing.
"""
# Imports
from aiohttp.client_exceptions import ClientConnectorError
from lib.util import environment, parsing
from datetime import datetime
import discord
import logging
import socket
import sys


class JadieClient(discord.Client):

    def __init__(self):
        """
        Instantiates the bot.
        Does a lot to do so, like getting the start time and uptime, as well as loading the commands.
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
        self.public_command_dict, self.developer_command_dict, self.reactive_command_list, specialized_command_dict = commands.load_commands()
        # Load specialized commands.
        self.toggle_ignore_developer = specialized_command_dict['toggleignoredev']
        specialized_command_dict['help_init']()

        # Set variable for whether or not to ignore the developer.
        self.ignore_developer = False

        # Discord client init
        intents = discord.Intents.all()
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

        Arguments:
            message (discord.message.Message) : The discord message object that triggered this method.
        """
        # Checks to make sure the message, channel, and author exist, and that the message isn't from the bot itself.
        if not message or not message.content or not message.channel or not message.author or message.author == self.user:
            return

        # Check to see if the author was a developer.
        author_is_developer = str(message.author.id) in environment.get("DEVELOPER_DISCORD_IDS")

        # First, if the author is a developer and they're being ignored, check if this message
        # is a toggleignoredev command.
        if self.ignore_developer and author_is_developer:
            if message.content == f'{environment.get("GLOBAL_PREFIX")}toggleignoredev' or \
                    message.content.startswith(f'{environment.get("GLOBAL_PREFIX")}toggleignoredev '):
                # If so, run the command!
                return await self.toggle_ignore_developer(self, message)
            else:
                # If not, ignore.
                return

        # Second, if the author ISN'T a developer and this is a development version, then ignore them.
        if not (author_is_developer or environment.get("DEPLOYMENT_CLIENT")):
            return

        # Third, if the message's guild is bugged out, then return.
        if isinstance(message.channel, discord.TextChannel) and not message.guild:
            logging.error(f'Discord TextChannel {message.channel} does not have a guild attached to it')
            return

        # Fourth, parse the command out of the message and get the argument.
        command, argument = parsing.get_command_from_message(message)

        # Otherwise, try to get the command.
        if command:

            try:
                # Grabs command from the regular dict and tries to run it.
                if command in self.public_command_dict:
                    return await self.public_command_dict[command](self, message, argument)

                # If the author is a developer, grab the command from the developer dict.
                elif author_is_developer and command in self.developer_command_dict:
                    return await self.developer_command_dict[command](self, message, argument)

            # If any unchecked error occurred at all, log and return.
            except Exception as e:
                return logging.error(repr(e))

        # Finally, if this was a regular message, run reactive commands.
        for reactive_command in self.reactive_command_list:
            await reactive_command(self, message)


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
        sys.exit(-1)

    # If the client loop ever stops running, the process should terminate.
    finally:
        logging.critical('Bot terminated unexpectedly.')
        sys.exit(0)

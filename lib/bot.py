"""
The bot class.
The main meat of the bot. Inherits from discord.Client, is the main point at which Discord API crosses over
into self processing.
"""
# Local Imports
from lib.util import environment, parsing
from lib import commands

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
VERSION_NUMBER = '0.6.4'


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

        # Store environment variables.
        self.global_prefix = GLOBAL_PREFIX
        self.deployment_client = environment.get("DEPLOYMENT_CLIENT")

        # Load the commands.
        self.public_command_dict, self.developer_command_dict, self.reactive_command_list, specialized_command_dict = \
            commands.load_commands()
        # Load specialized commands.
        self.toggle_ignore_developer = specialized_command_dict['toggleignoredev']
        specialized_command_dict['help_init'](VERSION_NUMBER, self.global_prefix)

        # Set variable for whether or not to ignore the developer (and also store the developer's discord id's).
        self.ignore_developer = False
        self.developer_ids = [int(dev_id) for dev_id in environment.get("DEVELOPER_DISCORD_IDS")]

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
        # See if the command is functional and if the author is a developer.
        functional, author_is_developer = await self.is_functional_message(message)

        # If it isn't functional, return.
        if not functional:
            return

        # Fourth, parse the command out of the message and get the argument.
        command, argument = parsing.get_command_from_message(self.global_prefix, message)

        # Otherwise, try to get the command.
        if command:

            # Grabs command from the regular dict and tries to run it.
            if command in self.public_command_dict:
                return await commands.run_standard_command(command, self.public_command_dict[command], self, message, argument)

            # If the author is a developer, grab the command from the developer dict.
            elif author_is_developer and command in self.developer_command_dict:
                return await commands.run_standard_command(command, self.developer_command_dict[command], self, message, argument)

        # Finally, if this was a regular message, run reactive commands.
        for reactive_command in self.reactive_command_list:
            await commands.run_reactive_command(reactive_command, self, message)


    async def is_functional_message(self, message):
        """
        Sees whether or not the given message is a functional one (one that the on_message function can react to).

        Arguments:
            message (discord.message.Message) : The discord message object that triggered this method.

        Returns:
            bool, bool : The first value corresponds to whether or not the message is functional.
                         The second value corresponds to whether or not the author was a developer.
        """
        # Checks to make sure the message, channel, and author exist, and that the message isn't from the bot itself.
        if not self.message_object_has_required_attributes(message):
            return False, False

        # Check to see if the author was a developer.
        author_is_developer = message.author.id in self.developer_ids

        # Check if the developer is to be ignored, if they are a developer.
        if await self.ignore_developer_check(message, author_is_developer):
            return False, author_is_developer

        # Next, if the author ISN'T a developer and this is a development version, then ignore them.
        if not (author_is_developer or self.deployment_client):
            return False, author_is_developer

        # Return true.
        return True, author_is_developer


    def message_object_has_required_attributes(self, message):
        """
        Checks to make sure that the message object provided has all the required attributes.

        Arguments:
            message (discord.message.Message) : The discord message object that triggered this method.

        Returns:
            bool : Whether or not it has all the required attributes.
        """
        # Check for message object, content, channel, and author, and making sure we're not the author.
        if not message or not isinstance(message, discord.Message) or not message.author \
                or message.author == self.user or not message.content or not message.channel:
            return False

        # If the message should be in a guild but its guild is bugged out, then return.
        if isinstance(message.channel, discord.TextChannel) and not message.guild:
            logging.error(f'Discord TextChannel {message.channel} does not have a guild attached to it')
            return False

        # Test passed, return True.
        return True


    async def ignore_developer_check(self, message, author_is_developer):
        """
        Checks if we are to ignore the developer.
        If the message's content is a toggleignoredev command, then run the command.

        Arguments:
            message (discord.message.Message) : The discord message object that triggered this method.
            author_is_developer (bool) : Whether or not the author is a developer.

        Returns:
            bool : Whether or not to ignore this message for the rest of time.
        """
        # Check for ignoring the developer and the command.
        if self.ignore_developer and author_is_developer:
            if message.content.split(' ')[0] == f'{self.global_prefix}toggleignoredev':

                # If so, run the command!
                await self.toggle_ignore_developer(self, message)

            # Return True, since developer is ignored.
            return True

        # Developer not ignored, continue on.
        return False


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

# Jadi3Pi bot file

# Imports
from src.commands import fun_commands, utility_commands, other_commands, dev_commands
from aiohttp.client_exceptions import ClientConnectorError
from datetime import datetime
from src import constants, cron, logger, util
import platform
import discord
import socket
import os

# Outer-level crap
# Establishes logger
log = logger.JLogger()
fun_commands.log = log
utility_commands.log = log
other_commands.log = log
dev_commands.log = log

# Gets start time
bot_start_time = datetime.today()

class JadieClient(discord.Client):

    # Keeps track of who we're copying by server and then id (hehehe)
    copied_users = {}

    # Keeps track of Hunger Games.
    curr_hg = {}

    # Keeps track of if the last attempt at randomyt was quota blocked.
    quota_blocked_last_time = False

    # Dict of commands gives easy automation so no switch statement required
    public_command_dict = {}
    developer_command_dict = {}

    # Time since initial run.
    bot_start_time = bot_start_time

    # Time since last disconnect.
    bot_uptime = None

    # Keeps track of if this is the first time we've connected or not
    connected_before = False
    reconnected_since = False

    # Keep track of whether or not we should ignore the developer.
    ignore_developer = False

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
            'help': other_commands.help_command,
            'runtime': other_commands.runtime,
            'copy': fun_commands.copy_user,
            'stopcopying': fun_commands.stop_copying,
            'uptime': other_commands.uptime,
            'hex': utility_commands.hexadecimal, 'hexadecimal': utility_commands.hexadecimal,
            'duo': utility_commands.duodecimal, 'duodec': utility_commands.duodecimal, 'duodecimal': utility_commands.duodecimal,
            'dec': utility_commands.decimal, 'decimal': utility_commands.decimal,
            'oct': utility_commands.octal, 'octal': utility_commands.octal,
            'bin': utility_commands.binary, 'binary': utility_commands.binary,
            'randomyt': fun_commands.randomyt, 'randomyoutube': fun_commands.randomyt, 'ytroulette': fun_commands.randomyt, 'youtuberoulette': fun_commands.randomyt,
            'calc': utility_commands.evaluate, 'eval': utility_commands.evaluate, 'calculate': utility_commands.evaluate, 'evaluate': utility_commands.evaluate,
            'randomwiki': fun_commands.randomwiki, 'randomwikipedia': fun_commands.randomwiki, 'wikiroulette': fun_commands.randomwiki, 'wikipediaroulette': fun_commands.randomwiki,
            'ship': fun_commands.ship,
            'weather': utility_commands.weather,
            'uwu': fun_commands.uwuify, 'uwuify': fun_commands.uwuify,
            'owo': fun_commands.owoify, 'owoify': fun_commands.owoify,
            'business': fun_commands.business_only, 'businessonly': fun_commands.business_only,
            'ultimate': fun_commands.ultimate, 'talent': fun_commands.ultimate,
            'shsl': fun_commands.shsl,
            'hungergames': fun_commands.hunger_games, 'hg': fun_commands.hunger_games, 'hunger': fun_commands.hunger_games, 'hungry': fun_commands.hunger_games
        }

        # Sets the developer command_dict
        self.developer_command_dict = {
            'localip': dev_commands.get_local_ip,
            'toggleignoredev': dev_commands.toggle_ignore_dev,
            'getpid': dev_commands.get_pid, 'localpid': dev_commands.get_pid, 'pid': dev_commands.get_pid,
            'reboot': dev_commands.remote_reboot, 'restart': dev_commands.remote_reboot,
            'update': dev_commands.update_remote,
            'sendlog': dev_commands.send_log,
            'loglist': dev_commands.log_list, 'logs': dev_commands.log_list,
            'bash': dev_commands.bash
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
        if await fun_commands.copy_msg(self, message, is_in_guild): # Copy will copy a user's message if they're in the copy dict
            return
        if author_is_developer and self.reboot_confirmation:
            await dev_commands.confirm_reboot(self, message, is_in_guild)

        # Prompted commands
        # ==================
        command, argument = util.get_command_from_message(message)

        # Immediately returns if no command
        if not command:
            return

        # Grabs specific method from dict and runs command
        if command in self.public_command_dict.keys():
            await self.public_command_dict[command](self, message, argument, is_in_guild)

        # If the user is dev, we cycle through the developer dict as well.
        if author_is_developer:
            if command in self.developer_command_dict.keys():
                await self.developer_command_dict[command](self, message, argument, is_in_guild)


# Client is the thing that is basically the connection between us and Discord -- time to run.
def launch(on_windows):
    client = JadieClient(on_windows)

    # Next, start the cron loop so we don't end up running more than one of these at once.
    cron.start_cron_loop()

    # Logging new instance
    start_str = 'Starting new instance of JadieClient'
    run_str = 'Running on {} ({})'.format(socket.gethostname(), 'Windows' if on_windows else 'Linux')
    log.info('')
    log.info('=' * (max(len(start_str), len(run_str)) + 1))
    log.info(start_str)
    log.info(run_str)
    log.info('=' * (max(len(start_str), len(run_str)) + 1))

    # Making the temp dir if it doesn't exist already.
    if not os.path.isdir(constants.TEMP_DIR):
        os.mkdir(constants.TEMP_DIR)

    # All this crap around client.run occurs only if we can't connect initially.
    try:
        client.run(constants.BOT_TOKEN)
        os._exit(0)
    except ClientConnectorError:
        log.info('Cannot connect to Discord.')
        os._exit(-1)

# __main__, just in case.
if __name__ == '__main__':
    # Set the working directory to what we want so our imports work correctly
    # Also checks the OS to make sure we load into the correct working directory
    running_on_windows = platform.system() == 'Windows'
    if running_on_windows:
        os.chdir('C:/Users/popki/Projects/Python/Jadi3Pi')
    else:
        os.chdir('/home/pi/Jadi3Pi')

    # Then we launch.
    launch(running_on_windows)

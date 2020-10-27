# Jadi3Pi bot file

# Imports
from aiohttp.client_exceptions import ClientConnectorError
from datetime import datetime
import comms_other
import comms_util
import comms_dev
import comms_fun
import constants
import platform
import discord
import logger
import socket
import cron
import util
import os

# Outer-level crap
# Establishes logger
log = logger.JLogger()
comms_fun.log = log
comms_util.log = log
comms_other.log = log
comms_dev.log = log

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
            'help': comms_other.help_command,
            'runtime': comms_other.runtime,
            'copy': comms_fun.copy_user,
            'stopcopying': comms_fun.stop_copying,
            'uptime': comms_other.uptime,
            'hex': comms_util.hexadecimal, 'hexadecimal': comms_util.hexadecimal,
            'duo': comms_util.duodecimal, 'duodec': comms_util.duodecimal, 'duodecimal': comms_util.duodecimal,
            'dec': comms_util.decimal, 'decimal': comms_util.decimal,
            'oct': comms_util.octal, 'octal': comms_util.octal,
            'bin': comms_util.binary, 'binary': comms_util.binary,
            'randomyt': comms_fun.randomyt, 'randomyoutube': comms_fun.randomyt, 'ytroulette': comms_fun.randomyt, 'youtuberoulette': comms_fun.randomyt,
            'calc': comms_util.evaluate, 'eval': comms_util.evaluate, 'calculate': comms_util.evaluate, 'evaluate': comms_util.evaluate,
            'randomwiki': comms_fun.randomwiki, 'randomwikipedia': comms_fun.randomwiki, 'wikiroulette': comms_fun.randomwiki, 'wikipediaroulette': comms_fun.randomwiki,
            'ship': comms_fun.ship,
            'weather': comms_util.weather,
            'uwu': comms_fun.uwuify, 'uwuify': comms_fun.uwuify,
            'owo': comms_fun.owoify, 'owoify': comms_fun.owoify,
            'business': comms_fun.business_only, 'businessonly': comms_fun.business_only
        }

        # Sets the developer command_dict
        self.developer_command_dict = {
            'localip': comms_dev.get_local_ip,
            'toggleignoredev': comms_dev.toggle_ignore_dev,
            'getpid': comms_dev.get_pid, 'localpid': comms_dev.get_pid, 'pid': comms_dev.get_pid,
            'reboot': comms_dev.remote_reboot, 'restart': comms_dev.remote_reboot,
            'update': comms_dev.update_remote,
            'sendlog': comms_dev.send_log,
            'loglist': comms_dev.log_list, 'logs': comms_dev.log_list,
            'bash': comms_dev.bash,
            'ultimate': comms_fun.ultimate, 'talent': comms_fun.ultimate,
            'shsl': comms_fun.shsl,
            'hungergames': comms_fun.hunger_games_start, 'hg': comms_fun.hunger_games_start, 'hunger': comms_fun.hunger_games_start, 'hungry': comms_fun.hunger_games_start
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
        if str(message.channel) in self.curr_hg:
            if await comms_fun.hunger_games_update(self, message, is_in_guild): # Hunger games
                return
        elif await comms_fun.copy_msg(self, message, is_in_guild): # Copy will copy a user's message if they're in the copy dict, does not work in channels with hunger games
            return
        if author_is_developer and self.reboot_confirmation: # Reboot confirmation is dev-only
            await comms_dev.confirm_reboot(self, message, is_in_guild)

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

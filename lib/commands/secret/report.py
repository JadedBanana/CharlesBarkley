"""
Report command.
Sends a message to the reports channel in the Jadi3Pi development server.
"""
# Imports
from lib.util.logger import BotLogger
from lib.util import messaging, parsing
import discord
import logging


# The reports channel ID.
REPORTS_CHANNEL_ID = 917484720701444176


async def report(bot, message, argument):
    """
    Creates a report and sends it to the reports channel in the Jadi3Pi development server.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Get the argument. If there isn't one, then tell the user that's no good.
    argument = parsing.normalize_string(argument)
    if not argument:
        BotLogger.info(message, 'Tried to report something, no description')
        return await messaging.send_text_message(message, 'Report must have a description.')

    # Get the report string. It varies per channel type.
    if isinstance(message.channel, discord.TextChannel):
        report_str = f"Report made by user {message.author} in guild '{message.guild}', channel '{message.channel}': {argument}\n" \
                     f"{message.jump_url}"
    elif isinstance(message.channel, discord.DMChannel):
        report_str = f"Report made by user {message.author} in DMs: {argument}\n{message.jump_url}"
    else:
        report_str = f"Report made by user {message.author} in unknown channel type: {argument}\n{message.jump_url}"

    # Log the report.
    logging.warning(report_str)

    # Get the channel and send the message.
    channel = bot.get_channel(REPORTS_CHANNEL_ID)
    await channel.send(report_str)

    # Send an affirmation back.
    await messaging.send_text_message(message, 'Report submitted.')


# Command values
PUBLIC_COMMAND_DICT = {
    'report': report
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'report',
        'description': 'Creates a report that is sent to the developer.',
        'examples': [("report can't access userlist", "Reports that the userlist can't be accessed right now.")],
        'usages': ['report < description >']
    }
]
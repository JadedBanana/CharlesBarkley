"""
Toggle command commands.
Used to either toggle commands or list all disabled commands.
This file houses three commands, in reality.
"""
# Local Imports
from lib.util.logger import BotLogger as logging
from lib.util import logger, messaging, parsing

# Package Imports
import discord
import os


async def disable_command(message, argument):
    """
    Disables the given command.
    Operates on a method-level basis, meaning that commands get their METHODS disabled rather than the actual strings.
    Developer-only commands cannot be disabled.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # First, see if the argument exists.
    argument = parsing.normalize_string(argument)
    if not argument:
        logging.debug(message, 'attempted to disable command, no argument')
        return await messaging.send_text_message(message, f"Must specify a command.")

    # See if the command is in the bot's public command dict.
    argument = argument.lower()
    if argument not in bot.public_command_dict:
        logging.debug(message, f"attempted to disable command '{argument}', unknown")
        return await messaging.send_text_message(message, f"Unknown command '{argument}'.")

    # See if the command is already disabled.
    enabled_method = bot.public_command_dict[argument]
    if enabled_method in bot.disabled_commands:
        logging.debug(message, f"attempted to disable command {enabled_method}, already disabled")
        return await messaging.send_text_message(message, f"Command {enabled_method} is already disabled.")

    # Disable the command.
    bot.disabled_commands.append(enabled_method)

    # Log and send.
    logging.info(message, f"disabled command {enabled_method}")
    await messaging.send_text_message(message, f"Command {enabled_method} has been disabled.")


async def enable_command(message, argument):
    """
    Disables the given command.
    Operates on a method-level basis, meaning that commands get their METHODS disabled rather than the actual strings.
    Developer-only commands cannot be disabled.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # First, see if the argument exists.
    argument = parsing.normalize_string(argument)
    if not argument:
        logging.debug(message, 'attempted to enable command, no argument')
        return await messaging.send_text_message(message, f"Must specify a command.")

    # See if the command is in the bot's public command dict.
    argument = argument.lower()
    if argument not in bot.public_command_dict:
        logging.debug(message, f"attempted to enable command '{argument}', unknown")
        return await messaging.send_text_message(message, f"Unknown command '{argument}'.")

    # See if the command is already disabled.
    disabled_method = bot.public_command_dict[argument]
    if disabled_method not in bot.disabled_commands:
        logging.debug(message, f"attempted to enable command {disabled_method}, already enabled")
        return await messaging.send_text_message(message, f"Command {disabled_method} is already enabled.")

    # Disable the command.
    bot.disabled_commands.remove(disabled_method)

    # Log and send.
    logging.info(message, f"enabled command {disabled_method}")
    await messaging.send_text_message(message, f"Command {disabled_method} has been enabled.")


async def list_disabled_commands(message, argument):
    """
    Lists all the currently disabled commands.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Log the order.
    logging.debug(message, 'Ordered disabled commands.')

    # If there are no commands disabled, send a command saying so.
    if not bot.disabled_commands:
        return await messaging.send_text_message(message, 'There are currently no disabled commands.')

    # Create the message string.
    command_str = '\n'.join(f'{disabled_command}\t(' +
                            (", ".join(command_name for command_name in bot.public_command_dict
                                       if bot.public_command_dict[command_name] is disabled_command)) +
                            ')' for disabled_command in bot.disabled_commands)

    # Send the log message.
    await messaging.send_codeblock_message(message, command_str)


# Command values
DEVELOPER_COMMAND_DICT = {
    'disablecommand': disable_command,
    'disablecomm': disable_command,
    'disable': disable_command,
    'enablecommand': enable_command,
    'enablecomm': enable_command,
    'enable': enable_command,
    'reenablecommad': enable_command,
    'reenablecomm': enable_command,
    'reenable': enable_command,
    'disabledcommands': list_disabled_commands,
    'disabledcomms': list_disabled_commands,
    'disablelist': list_disabled_commands
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'disablecommand',
        'category': 'dev_only',
        'description': 'Disables a command. Also disables all aliases for said command.',
        'examples': [('disablecommand randomanime', "Disables the 'randomanime' command."),
                     ('disablecommand randomani', "Disables the 'randomanime' command.")],
        'aliases': ['disablecomm', 'disable'],
        'usages': ['disablecommand < command name / alias >']
    },
    {
        'command_name': 'enablecommand',
        'category': 'dev_only',
        'description': 'Enables a command. Also enables all aliases for said command.',
        'examples': [('enablecommand randomanime', "Enables the 'randomanime' command."),
                     ('enablecommand randomani', "Enables the 'randomanime' command.")],
        'aliases': ['enablecomm', 'enable', 'reenablecommand', 'reenablecomm', 'reenable'],
        'usages': ['enablecommand < command name / alias >']
    },
    {
        'command_name': 'disabledcommands',
        'category': 'dev_only',
        'description': 'Lists all the disabled commands.',
        'examples': [('disabledcommands', 'Lists all the disabled command methods.')],
        'aliases': ['disabledcomms', 'disablelist'],
        'usages': ['disabledcommands']
    }
]
"""
This __init__.py file has a method for loading the commands and methods for running commands.
"""
# Local Imports
from lib.util.logger import BotLogger as logging


def load_commands():
    """
    Loads all the commands from the sub-folders and puts them into three command dicts (one developer-only, one for general users, and
    one for specific commands hardcoded into the bot).
    Automatic method, requires no modifications to keep up-to-date.

    Raises:
        DuplicateCommandError : 2 commands are using the same name.

    Returns:
        dict, dict, list, dict : The public command dict, developer command dict, reactive command list, and specialized command dict,
                                 in that exact order.
    """
    # Imports
    from lib.util.exceptions import DuplicateCommandError
    import logging
    import pkgutil

    # Instantiating public and developer command dict.
    public_command_dict = {}
    developer_command_dict = {}
    reactive_command_list = []
    specialized_command_dict = {}

    # Load the package name of each package in 'commands' folder.
    for importer, package_name, is_package in pkgutil.iter_modules(['lib/commands']):

        # Log package name and set variable tracking commands implemented.
        logging.info(f"Loading commands from command package '{package_name}'...")
        commands_implemented = 0

        # Now that we have the package name of each module, load its sub-modules.
        for importer2, subpackage_name, is_package2 in pkgutil.iter_modules(['lib/commands/' + package_name]):
            module = importer2.find_module(subpackage_name).load_module()

            # For each module, we check for a public command dict.
            if hasattr(module, 'PUBLIC_COMMAND_DICT') and isinstance(module.PUBLIC_COMMAND_DICT, dict):

                # Iterate through each entry in the command dict and put them into the public command dict.
                for command_name, command_method in module.PUBLIC_COMMAND_DICT.items():

                    # Assert that the method is, well, a method.
                    if isinstance(command_method, type(load_commands)):

                        # Log and increment.
                        logging.info(f"Loading normal command '{command_name}' from '{package_name + '.' + subpackage_name}'")
                        commands_implemented += 1

                        # Put it in!
                        if command_name in public_command_dict or command_name in developer_command_dict:
                            raise DuplicateCommandError(command_name)
                        else:
                            public_command_dict[command_name] = command_method

            # Next, check for a developer command dict.
            if hasattr(module, 'DEVELOPER_COMMAND_DICT') and isinstance(module.DEVELOPER_COMMAND_DICT, dict):

                # Iterate through each entry in the command dict and put them into the developer command dict.
                for command_name, command_method in module.DEVELOPER_COMMAND_DICT.items():

                    # Assert that the method is, well, a method.
                    if isinstance(command_method, type(load_commands)):

                        # Log and increment.
                        logging.info(f"Loading developer command '{command_name}' from '{package_name + '.' + subpackage_name}'")
                        commands_implemented += 1

                        # Put it in!
                        if command_name in public_command_dict or command_name in developer_command_dict:
                            raise DuplicateCommandError(command_name)
                        else:
                            developer_command_dict[command_name] = command_method

            # Also check for a reactive command list.
            if hasattr(module, 'REACTIVE_COMMAND_LIST') and isinstance(module.REACTIVE_COMMAND_LIST, list):

                # Iterate through each entry in the command list and put them into the developer command dict.
                for command in module.REACTIVE_COMMAND_LIST:

                    # Assert that the method is, well, a method.
                    if isinstance(command, type(load_commands)):

                        # Log and increment.
                        logging.info(f"Loading reactive command from '{package_name + '.' + subpackage_name}'")
                        commands_implemented += 1

                        # Put it in!
                        reactive_command_list.append(command)

            # Next, check for a specialized command dict.
            if hasattr(module, 'SPECIALIZED_COMMAND_DICT') and isinstance(module.SPECIALIZED_COMMAND_DICT, dict):

                # Iterate through each entry in the command dict and put them into the specialized command dict.
                for command_name, command_method in module.SPECIALIZED_COMMAND_DICT.items():

                    # Assert that the method is, well, a method.
                    if isinstance(command_method, type(load_commands)):

                        # Log and increment.
                        logging.info(f"Loading specialized command '{command_name}' from '{package_name + '.' + subpackage_name}'")
                        commands_implemented += 1

                        # Put it in!
                        if command_name in specialized_command_dict:
                            raise DuplicateCommandError(command_name)
                        else:
                            specialized_command_dict[command_name] = command_method

            # Finally, check for an initialize method.
            if hasattr(module, 'initialize') and isinstance(module.initialize, type(load_commands)):
                module.initialize()

        # Log the total commands implemented this package.
        logging.info(f"Loaded {commands_implemented} commands from command package '{package_name}'")

    # Return the dicts.
    return public_command_dict, developer_command_dict, reactive_command_list, specialized_command_dict


async def run_standard_command(command_name, command_method, bot, message, argument):
    """
    Runs the given standard command. Uses error checking to prevent there from being no response to the user.

    Arguments:
        command_name (str) : The command name.
        command_method (method) : The command method in question.
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Try/catch for error handling
    try:
        await command_method(bot, message, argument)

    # On exception, report the error back to the user.
    except Exception as e:
        # Get the traceback_str.
        import traceback
        traceback_str = traceback.format_exc().replace('\n\n', '\n')
        while traceback_str[-1] == '\n':
            traceback_str = traceback_str[:-1]

        # Log the error.
        logging.error(message, f"Caused exception with message content '{message.content}', detected command '{command_name}', " +
                               (f"detected argument '{argument}'" if argument else 'no detected argument') + f":\n{traceback_str}")

        # Send the message.
        from lib.util import messaging
        await messaging.send_error_message(message, bot.global_prefix, traceback_str)


async def run_reactive_command(command_method, bot, message):
    """
    Runs the given reactive command. Uses error checking to prevent there from being no response to the user.

    Arguments:
        command_method (method) : The command method in question.
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Try/catch for error handling
    try:
        await command_method(bot, message)

    # On exception, report the error back to the user.
    except Exception as e:
        # Get the traceback_str.
        import traceback
        traceback_str = traceback.format_exc().replace('\n\n', '\n')
        while traceback_str[-1] == '\n':
            traceback_str = traceback_str[:-1]

        # Log the error.
        logging.error(message, f"Caused exception with message content '{message.content}', reactive command for {command_method}:\n"
                               f"{traceback_str}")

        # Send the message.
        from lib.util import messaging
        await messaging.send_error_message(message, bot.global_prefix, traceback_str)

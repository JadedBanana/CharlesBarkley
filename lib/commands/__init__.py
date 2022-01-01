"""
This __init__.py file has a method for loading the commands and methods for running commands.
"""
# Package Imports
import pkgutil

# Local Imports
from lib.util.logger import BotLogger as logging
from lib.util import messaging


def load_all_commands():
    """
    Loads all the commands from the sub-folders and puts them into five command dicts / lists (one developer-only,
    one for general users, one for specific commands hardcoded into the bot, one for reactive commands, and one
    for command initialize methods).
    Automatic method, requires no modifications to keep up-to-date.

    Raises:
        DuplicateCommandError : 2 commands are using the same name.

    Returns:
        dict, dict, list, dict, list : The public command dict, developer command dict, reactive command list,
                                       specialized command dict, and command initialize method list,
                                       in that exact order.
    """
    # Instantiating public and developer command dict.
    public_command_dict = {}
    developer_command_dict = {}
    reactive_command_list = []
    specialized_command_dict = {}
    command_initialize_method_list = []

    # Load the package name of each package in 'commands' folder.
    for importer, package_name, is_package in pkgutil.iter_modules(['lib/commands']):
        load_commands_from_package(package_name, public_command_dict, developer_command_dict, reactive_command_list,
                                   specialized_command_dict, command_initialize_method_list)

    # Return the dicts.
    return public_command_dict, developer_command_dict, reactive_command_list, specialized_command_dict, \
           command_initialize_method_list


def load_commands_from_package(package_name, public_command_dict, developer_command_dict, reactive_command_list,
                               specialized_command_dict, command_initialize_method_list):
    """
    Loads all the commands from the given package.
    Inserts them into their matching dicts / lists.

    Arguments:
        package_name (str) : The package name.
        public_command_dict (dict) : The public command dict.
        developer_command_dict (dict) : The developer command dict.
        reactive_command_list (list) : The reactive command list.
        specialized_command_dict (dict) : The specialized command dict.
        command_initialize_method_list (list) : The list of command initialize methods.

    Raises:
        DuplicateCommandError : 2 commands are using the same name for one of the dicts.
    """
    # Imports
    import logging

    # Log package name and set variable tracking commands implemented.
    logging.debug(f"Loading commands from command package '{package_name}'...")
    commands_implemented = 0

    # Now that we have the package name, load its modules.
    for importer2, module_name, is_package2 in pkgutil.iter_modules(['lib/commands/' + package_name]):
        commands_implemented += load_commands_from_module(importer2.find_module(module_name).load_module(), module_name,
                                                          package_name, public_command_dict, developer_command_dict,
                                                          reactive_command_list, specialized_command_dict,
                                                          command_initialize_method_list)

    # Log the total commands implemented this package.
    logging.debug(f"Loaded {commands_implemented} commands from command package '{package_name}'")


def load_commands_from_module(loaded_module, module_name, package_name, public_command_dict, developer_command_dict,
                              reactive_command_list, specialized_command_dict, command_initialize_method_list):
    """
    Loads all the commands from the given module.
    Inserts them into their matching dicts / lists.

    Arguments:
        loaded_module (module) : The completely loaded module.
        module_name (str) : The name of the module.
        package_name (str) : The package name.
        public_command_dict (dict) : The public command dict.
        developer_command_dict (dict) : The developer command dict.
        reactive_command_list (list) : The reactive command list.
        specialized_command_dict (dict) : The specialized command dict.
        command_initialize_method_list (list) : The list of command initialize methods.

    Raises:
        DuplicateCommandError : 2 commands are using the same name for one of the dicts.

    Returns:
        int : The number of commands that were loaded from this module.
    """
    # Set the commands_implemented variable.
    commands_implemented = 0

    # For each module, we check for a public command dict.
    commands_implemented += load_normal_commands_from_module(loaded_module, module_name, package_name,
                                                             public_command_dict, developer_command_dict, False)

    # Next, check for a developer command dict.
    commands_implemented += load_normal_commands_from_module(loaded_module, module_name, package_name,
                                                             public_command_dict, developer_command_dict, True)

    # Also check for a reactive command list.
    commands_implemented += load_reactive_commands_from_module(loaded_module, module_name, package_name,
                                                               reactive_command_list)

    # Next, check for a specialized command dict.
    commands_implemented += load_specialized_commands_from_module(loaded_module, module_name, package_name,
                                                                  specialized_command_dict)

    # Finally, check for an initialize method.
    load_initialize_method_from_module_if_exists(loaded_module, module_name, package_name,
                                                 command_initialize_method_list)

    # Return the commands implemented.
    return commands_implemented


def load_normal_commands_from_module(loaded_module, module_name, package_name, public_command_dict,
                                     developer_command_dict, load_from_developer):
    """
    Loads all the normal commands from the given module.
    Inserts them into the public_command_dict OR developer_command_dict, depending on the value of load_from_developer.

    Arguments:
        loaded_module (module) : The completely loaded module.
        module_name (str) : The name of the module.
        package_name (str) : The package name.
        public_command_dict (dict) : The public command dict.
        developer_command_dict (dict) : The developer command dict. Only used to check for duplicates.
        load_from_developer (bool) : Whether to load from the developer list rather than the public list.

    Raises:
        DuplicateCommandError : 2 commands are using the same name for one of the dicts.

    Returns:
        int : The number of commands that were loaded from this module.
    """
    # If we're loading from the developer dict, then check for a developer command dict.
    if load_from_developer:
        if hasattr(loaded_module, 'DEVELOPER_COMMAND_DICT') and isinstance(loaded_module.DEVELOPER_COMMAND_DICT, dict):
            command_dict = loaded_module.DEVELOPER_COMMAND_DICT

        # If there isn't one, then return.
        else:
            return 0

    # Not loading from developer, check for a public command dict.
    elif hasattr(loaded_module, 'PUBLIC_COMMAND_DICT') and isinstance(loaded_module.PUBLIC_COMMAND_DICT, dict):
        command_dict = loaded_module.PUBLIC_COMMAND_DICT

    # No dict, return.
    else:
        return 0

    # Return.
    return load_normal_commands_from_command_dict(
        command_dict, module_name, package_name,
        developer_command_dict if load_from_developer else public_command_dict,
        [public_command_dict, developer_command_dict], 'developer' if load_from_developer else 'public')


def load_normal_commands_from_command_dict(command_dict, module_name, package_name, target_dict,
                                           preexisting_command_dicts, command_type_str):
    """
    Loads all the normal commands from the given module.
    Inserts them into the target dict.

    Arguments:
        command_dict (dict) : The command dict, loaded straight from the module.
        module_name (str) : The name of the module.
        package_name (str) : The package name.
        target_dict (dict) : Where to put the loaded commands.
        preexisting_command_dicts (dict[]) : Preexisting command dicts.
                                             Should include the target_dict.
        command_type_str (str) : The command type. Used for logging.

    Raises:
        DuplicateCommandError : 2 commands are using the same name for one of the dicts.

    Returns:
        int : The number of commands that were loaded from this module.
    """
    # Imports
    from lib.util.exceptions import DuplicateCommandError
    import logging

    # Set the commands_implemented variable.
    commands_implemented = 0

    # Iterate through each entry in the command dict and put them into the public command dict.
    for command_name, command_method in command_dict.items():

        # Assert that the method is, well, a method.
        if isinstance(command_method, type(load_normal_commands_from_module)):

            # Log and increment.
            logging.debug(
                f"Loading {command_type_str} command '{command_name}' from '{package_name + '.' + module_name}'")
            commands_implemented += 1

            # Put it in!
            if any([command_name in preexisting_dict for preexisting_dict in preexisting_command_dicts]):
                raise DuplicateCommandError(command_name)
            else:
                target_dict[command_name] = command_method

    # Return.
    return commands_implemented


def load_reactive_commands_from_module(loaded_module, module_name, package_name, reactive_command_list):
    """
    Loads all the normal commands from the given module.
    Inserts them into the reactive_command_list.

    Arguments:
        loaded_module (module) : The completely loaded module.
        module_name (str) : The name of the module.
        package_name (str) : The package name.
        reactive_command_list (list) : The reactive command list.

    Returns:
        int : The number of commands that were loaded from this module.
    """
    # Imports
    import logging

    # Set the commands_implemented variable.
    commands_implemented = 0

    # Check for a reactive command list.
    if hasattr(loaded_module, 'REACTIVE_COMMAND_LIST') and isinstance(loaded_module.REACTIVE_COMMAND_LIST, list):

        # Iterate through each entry in the command list and put them into the developer command dict.
        for command in loaded_module.REACTIVE_COMMAND_LIST:

            # Assert that the method is, well, a method.
            if isinstance(command, type(load_all_commands)):
                # Log and increment.
                logging.debug(f"Loading reactive command from '{package_name + '.' + module_name}'")
                commands_implemented += 1

                # Put it in!
                reactive_command_list.append(command)

    # Return.
    return commands_implemented


def load_specialized_commands_from_module(loaded_module, module_name, package_name, specialized_command_dict):
    """
    Loads all the normal commands from the given module.
    Inserts them into the specialized_command_dict.

    Arguments:
        loaded_module (module) : The completely loaded module.
        module_name (str) : The name of the module.
        package_name (str) : The package name.
        specialized_command_dict (dict) : The specialized command dict.

    Raises:
        DuplicateCommandError : 2 commands are using the same name for one of the dicts.

    Returns:
        int : The number of commands that were loaded from this module.
    """
    # If there is a specialized_command_dict, then load them as if they were normal commands.
    if hasattr(loaded_module, 'SPECIALIZED_COMMAND_DICT') and isinstance(loaded_module.SPECIALIZED_COMMAND_DICT, dict):
        return load_normal_commands_from_command_dict(loaded_module.SPECIALIZED_COMMAND_DICT, module_name, package_name,
                                                      specialized_command_dict, [specialized_command_dict],
                                                      'specialized')

    # No specialized commands, return 0.
    return 0


def load_initialize_method_from_module_if_exists(loaded_module, module_name, package_name,
                                                 command_initialize_method_list):
    """
    Loads the initialize method from the module, if it exists.


    Arguments:
        loaded_module (module) : The completely loaded module.
        module_name (str) : The name of the module.
        package_name (str) : The package name.
        command_initialize_method_list (list) : The list of command initialize methods.

    Raises:
        DuplicateCommandError : 2 commands are using the same name for one of the dicts.

    Returns:
        int : The number of commands that were loaded from this module.
    """
    # Imports
    import logging

    # Check if there is an initialize method in there.
    if hasattr(loaded_module, 'initialize') and isinstance(loaded_module.initialize, type(load_all_commands)):

        # Append it.
        command_initialize_method_list.append(loaded_module.initialize)

        # Log and return.
        logging.debug(f"Loaded initializer method from '{package_name}.{module_name}'")
        return 1

    # Return.
    return 0


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

        # If the command_method is in the disabled commands, then send a response.
        if command_method in bot.disabled_commands:
            logging.debug(message, f"Tried to use disabled command {command_method}.")
            await messaging.send_text_message(message, 'That command is currently disabled, sorry!')

        # Otherwise, run the command.
        else:
            await command_method(bot, message, argument)

    # On exception, report the error back to the user.
    except Exception as e:
        # Get the traceback_str.
        import traceback
        traceback_str = traceback.format_exc().replace('\n\n', '\n').strip('\n')
        while traceback_str[-1] == '\n':
            traceback_str = traceback_str[:-1]

        # Log the error.
        logging.error(message, f"Caused exception with message content '{message.content}', detected command '{command_name}', " +
                               (f"detected argument '{argument}'" if argument else 'no detected argument') + f":\n{traceback_str}")

        # Send the message.
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
        traceback_str = traceback.format_exc().replace('\n\n', '\n').strip('\n')

        # Log the error.
        logging.error(message, f"Caused exception with message content '{message.content}', reactive command for {command_method}:\n"
                               f"{traceback_str}")

        # Send the message.
        await messaging.send_error_message(message, bot.global_prefix, traceback_str)

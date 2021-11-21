"""
This __init__.py file has a method for loading the commands.
"""

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
                for command_name in module.PUBLIC_COMMAND_DICT:

                    # Assert that the method is, well, a method.
                    if isinstance(module.PUBLIC_COMMAND_DICT[command_name], type(load_commands)):

                        # Log and increment.
                        logging.info(f"Loading normal command from '{package_name + '.' + subpackage_name}'")
                        commands_implemented += 1

                        # Put it in!
                        if command_name in public_command_dict or command_name in developer_command_dict:
                            raise DuplicateCommandError(command_name)
                        else:
                            public_command_dict[command_name] = module.PUBLIC_COMMAND_DICT[command_name]

            # Next, check for a developer command dict.
            if hasattr(module, 'DEVELOPER_COMMAND_DICT') and isinstance(module.DEVELOPER_COMMAND_DICT, dict):

                # Iterate through each entry in the command dict and put them into the developer command dict.
                for command_name in module.DEVELOPER_COMMAND_DICT:

                    # Assert that the method is, well, a method.
                    if isinstance(module.DEVELOPER_COMMAND_DICT[command_name], type(load_commands)):

                        # Log and increment.
                        logging.info(f"Loading developer command from '{package_name + '.' + subpackage_name}'")
                        commands_implemented += 1

                        # Put it in!
                        if command_name in public_command_dict or command_name in developer_command_dict:
                            raise DuplicateCommandError(command_name)
                        else:
                            developer_command_dict[command_name] = module.DEVELOPER_COMMAND_DICT[command_name]

            # Also check for a reactive command list.
            if hasattr(module, 'REACTIVE_COMMAND_LIST') and isinstance(module.REACTIVE_COMMAND_LIST, type(list)):

                # Iterate through each entry in the command list and put them into the developer command dict.
                for command in module.REACTIVE_COMMAND_LIST:

                    # Assert that the method is, well, a method.
                    if isinstance(command, type(load_commands)):

                        # Log and increment.
                        logging.info(f"Loading reactive command from '{package_name + '.' + subpackage_name}'")
                        commands_implemented += 1

                        # Put it in!
                        reactive_command_list.append(command)

            # Finally, check for a specialized command dict.
            if hasattr(module, 'SPECIALIZED_COMMAND_DICT') and isinstance(module.SPECIALIZED_COMMAND_DICT, dict):

                # Iterate through each entry in the command dict and put them into the specialized command dict.
                for command_name in module.SPECIALIZED_COMMAND_DICT:

                    # Assert that the method is, well, a method.
                    if isinstance(module.SPECIALIZED_COMMAND_DICT[command_name], type(load_commands)):

                        # Log and increment.
                        logging.info(f"Loading specialized command from '{package_name + '.' + subpackage_name}'")
                        commands_implemented += 1

                        # Put it in!
                        if command_name in specialized_command_dict:
                            raise DuplicateCommandError(command_name)
                        else:
                            specialized_command_dict[command_name] = module.SPECIALIZED_COMMAND_DICT[command_name]

        # Log the total commands implemented this package.
        logging.info(f"Loaded {commands_implemented} commands from command package '{package_name}'")

    # Return the dicts.
    return public_command_dict, developer_command_dict, reactive_command_list, specialized_command_dict
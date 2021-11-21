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

            # For each module, check if it has the attributes desired. If so, then slot it into the command dict.
            if all([hasattr(module, attribute) for attribute in ['COMMAND_NAMES', 'CALL_METHOD']]) and \
                    isinstance(module.COMMAND_NAMES, list) and isinstance(module.CALL_METHOD, type(load_commands)):

                # Decide which dict to put the command into.
                command_dict = developer_command_dict if hasattr(module, 'DEV_ONLY_COMMAND') and module.DEV_ONLY_COMMAND else public_command_dict

                # Log and increment.
                logging.info(f"Loading normal command '{package_name + '.' + subpackage_name}'")
                commands_implemented += 1

                # Put it in!
                for name in module.COMMAND_NAMES:
                    if name in command_dict:
                        raise DuplicateCommandError(name)
                    else:
                        command_dict[name] = module.CALL_METHOD

            # Reactive commands.
            if hasattr(module, 'REACTIVE_METHOD') and isinstance(module.REACTIVE_METHOD, type(load_commands)):

                # Log and increment.
                logging.info(f"Loading reactive command '{package_name + '.' + subpackage_name}'")
                commands_implemented += 1

                # Put it in!
                reactive_command_list.append(module.REACTIVE_METHOD)

            # Specialized commands.
            if package_name == 'specialized':

                # For each module, check if it has the attributes desired. If so, then slot it into the command dict.
                if all([hasattr(module, attribute) for attribute in ['COMMAND_NAME', 'CALL_METHOD']]):

                    # Check to make sure that COMMAND_NAME is a str and CALL_METHOD is a method.
                    if not (isinstance(module.COMMAND_NAME, str) and isinstance(module.CALL_METHOD, type(load_commands))):
                        continue

                    # Log and increment.
                    logging.info(f"Loading specialized command '{package_name + '.' + subpackage_name}'")
                    commands_implemented += 1

                    # Put it in!
                    specialized_command_dict[module.COMMAND_NAME] = module.CALL_METHOD

        # Log the total commands implemented this package.
        logging.info(f"Loaded {commands_implemented} commands from command package '{package_name}'")

    # Return the dicts.
    return public_command_dict, developer_command_dict, reactive_command_list, specialized_command_dict
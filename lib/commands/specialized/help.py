"""
Help command.
Pulls all the help documentation on a per-command basis and displays it when the user asks for it.
Must be initialized with the initialize() method before actually running anything.
"""
# Imports.
from lib.util import assets, environment, messaging, parsing
from lib.util.logger import BotLogger as logging


# Help embed variables.
HELP_EMBED_COLOR = (107 << 16) + (115 << 8) + 135
HELP_EMBED_DESCRIPTION = '''Type `{0}help [command]` for more help eg. `{0}help randomwiki`'''
HOME_HELP_PAGE_CUSTOM_CATEGORY_HEADERS = {
    'fun': 'Fun',
    'util': 'Utility'
}


# Stored embeds.
PUBLIC_HOME_HELP_EMBED = None
DEVELOPER_HOME_HELP_EMBED = None
COMMAND_SPECIFIC_HELP_EMBEDS = {}
HOME_HELP_PAGE_ICON = 'Jadi3Pi.png'


def initialize(global_prefix):
    """
    Initializes the help command.
    Automatic method, requires no modifications to keep up-to-date.

    Arguments:
        global_prefix (str) : The global prefix.

    Raises:
        DuplicateCommandError : 2 commands are using the same name for the help docs.
    """
    # Imports.
    from lib.util.exceptions import DuplicateCommandError

    # First, get all the command dicts.
    home_help_page_dict, command_specific_help_page_dicts = get_command_dicts()

    # Then, create embeds for all of those commands.
    # First, the home embed.
    global PUBLIC_HOME_HELP_EMBED, DEVELOPER_HOME_HELP_EMBED
    PUBLIC_HOME_HELP_EMBED, DEVELOPER_HOME_HELP_EMBED = generate_home_help_page_embeds(self.global_prefix, home_help_page_dict)

    # Second, the command-specific help embeds.
    global COMMAND_SPECIFIC_HELP_EMBEDS
    for command_name, command_specific_help_page_dict in command_specific_help_page_dicts.items():

        # Add them on with their command_name as keys.
        COMMAND_SPECIFIC_HELP_EMBEDS[command_name] = generate_command_specific_help_page_embeds(self.global_prefix, command_name,
                                                                                                command_specific_help_page_dict)
        # For aliases, add them as the aliases as keys and the parent name as the data.
        if 'aliases' in command_specific_help_page_dict:
            for alias in command_specific_help_page_dict['aliases']:

                # Detect duplicates.
                if alias in COMMAND_SPECIFIC_HELP_EMBEDS:
                    raise DuplicateCommandError(alias)

                # Add.
                COMMAND_SPECIFIC_HELP_EMBEDS[alias] = command_name


def get_command_dicts():
    """
    Gets both the home help page command dict and the command-specific help page dict.

    Returns:
        dict, dict : The home help page command dict and the command-specific help page dict, in that exact order.
    """
    # Imports.
    from lib.util.exceptions import DuplicateCommandError
    import logging as log
    import pkgutil

    # Variables keeping track of active command data.
    home_help_page_dict = {}
    command_specific_help_page_dict = {}

    # Load the package name of each package in 'commands' folder.
    for importer, package_name, is_package in pkgutil.iter_modules(['lib/commands']):

        # Log package name and set variable tracking commands implemented.
        log.info(f"Loading help documentation from command package '{package_name}'...")
        help_pages_implemented = 0

        # Now that we have the package name of each module, load its sub-modules.
        for importer2, subpackage_name, is_package2 in pkgutil.iter_modules(['lib/commands/' + package_name]):
            module = importer2.find_module(subpackage_name).load_module()

            # For each module, we check for a help documentation list.
            if hasattr(module, 'HELP_DOCUMENTATION_LIST') and isinstance(module.HELP_DOCUMENTATION_LIST, list):

                # Next, iterate through each piece of help documentation.
                for help_doc_dict in module.HELP_DOCUMENTATION_LIST:

                    # Make sure it's a dict and that there's a command name.
                    if not isinstance(help_doc_dict, dict) or not 'command_name' in help_doc_dict:
                        continue

                    # Get the command name.
                    command_name = help_doc_dict['command_name']

                    # Detect duplicate commands.
                    if command_name in COMMAND_SPECIFIC_HELP_EMBEDS:
                        raise DuplicateCommandError(command_name)

                    # Log and add 1 to the help_pages_implemented.
                    log.info(f"Loading help documentation from '{package_name + '.' + subpackage_name}' for command '{command_name}'")
                    help_pages_implemented += 1

                    # Check for command category (put into category)
                    if 'category' in help_doc_dict and isinstance(help_doc_dict['category'], str):
                        if help_doc_dict['category'] in home_help_page_dict:
                            home_help_page_dict[help_doc_dict['category']].append(command_name)
                        else:
                            home_help_page_dict[help_doc_dict['category']] = [command_name]

                    # Create a command-specific help page.
                    command_specific_help_page = {}

                    # Get the command description.
                    if 'description' in help_doc_dict and isinstance(help_doc_dict['description'], str):
                        command_specific_help_page['description'] = help_doc_dict['description']

                    # Get the command examples.
                    if 'examples' in help_doc_dict and isinstance(help_doc_dict['examples'], list):
                        # Iterate through.
                        for example in help_doc_dict['examples']:
                            # Assert that each example is a tuple and that everything in it is a string.
                            if not isinstance(example, tuple) and len(example) == 2 and \
                                    all([isinstance(example_val, str) for example_val in example]):
                                continue
                            # Add to the examples.
                            if 'examples' in command_specific_help_page:
                                command_specific_help_page['examples'].append(example)
                            else:
                                command_specific_help_page['examples'] = [example]

                    # Get the command aliases.
                    if 'aliases' in help_doc_dict and isinstance(help_doc_dict['aliases'], list):
                        # Assert that each alias is a string.
                        for alias in help_doc_dict['aliases']:
                            # Assert that each alias is a string.
                            if not isinstance(alias, str):
                                continue
                            # Add to the aliases.
                            if 'aliases' in command_specific_help_page:
                                command_specific_help_page['aliases'].append(alias)
                            else:
                                command_specific_help_page['aliases'] = [alias]

                    # Get the command usages.
                    if 'usages' in help_doc_dict and isinstance(help_doc_dict['usages'], list):
                        # Assert that each usage is a string.
                        for usage in help_doc_dict['usages']:
                            # Assert that each usage is a string.
                            if not isinstance(usage, str):
                                continue
                            # Add to the aliases.
                            if 'usages' in command_specific_help_page:
                                command_specific_help_page['usages'].append(usage)
                            else:
                                command_specific_help_page['usages'] = [usage]

                    # Add it to the dict of command-specific help pages.
                    command_specific_help_page_dict[command_name] = command_specific_help_page

        # Log the total commands implemented this package.
        log.info(f"Loaded {help_pages_implemented} help documentation pages from command package '{package_name}'")

    # Return the command dicts.
    return home_help_page_dict, command_specific_help_page_dict


def generate_home_help_page_embeds(global_prefix, home_help_page_dict):
    """
    Generates both the public and developer embeds for the home help page.

    Arguments:
        global_prefix (str) : The global prefix.
        home_help_page_dict (dict) : The home help page dict.

    Returns:
        discord.Embed, discord.Embed : The public home page embed and the developer home page embed, in that exact order.
    """
    # Imports
    import discord

    # Gets the version number.
    version_number = environment.get("VERSION_NUMBER")

    # Create the public embed.
    public_embed = discord.Embed(title='Standard Commands', colour=HELP_EMBED_COLOR,
                          description=HELP_EMBED_DESCRIPTION.format(global_prefix))
    public_embed.set_footer(text=f'Jadi3Pi Version {version_number}')

    # Create the developer embed.
    developer_embed = discord.Embed(title='Standard Commands', colour=HELP_EMBED_COLOR,
                                    description=HELP_EMBED_DESCRIPTION.format(global_prefix))
    developer_embed.set_footer(text=f'Jadi3Pi Version {version_number}')

    # For each category, add a field.
    for category, commands in home_help_page_dict.items():

        # If this is the dev_only category, save it.
        if category == 'dev_only':
            continue

        # If the category is in the HOME_HELP_PAGE_CUSTOM_CATEGORY_HEADERS, then use that instead.
        category_clean = category
        if category in HOME_HELP_PAGE_CUSTOM_CATEGORY_HEADERS:
            category_clean = HOME_HELP_PAGE_CUSTOM_CATEGORY_HEADERS[category]

        # Add the field.
        public_embed.add_field(name=category_clean, value=' '.join([f'`{command}`' for command in commands]), inline=True)
        developer_embed.add_field(name=category_clean, value=' '.join([f'`{command}`' for command in commands]), inline=True)

    # Add the dev_only commands to the developer embed.
    if 'dev_only' in home_help_page_dict:
        developer_embed.add_field(name='Developer-Only',
                                  value=' '.join([f'`{command}`' for command in home_help_page_dict['dev_only']]),
                                  inline=True)

    # Return.
    return public_embed, developer_embed


def generate_command_specific_help_page_embeds(global_prefix, command_name, command_specific_help_page_dict):
    """
    Generates both the public and developer embeds for the home help page.

    Arguments:
        global_prefix (str) : The global prefix.
        command_name (str) : The command's name.
        command_specific_help_page_dict (dict) : The command-specific help page dict.

    Returns:
        discord.Embed : The generated embed for the command-specific help page.
    """
    # Imports
    import discord

    # Create the embed.
    embed = discord.Embed(colour=HELP_EMBED_COLOR)

    # Create the first field (command name and description).
    # If the description is available, it will be the value of the field. Otherwise, a message.
    if 'description' in command_specific_help_page_dict:
        embed.add_field(name=f'Help - {global_prefix}{command_name}',
                        value=f'```{command_specific_help_page_dict["description"]}```', inline=False)
    else:
        embed.add_field(name=f'Help - {global_prefix}{command_name}',
                        value='```Description for this command is not available.```', inline=False)

    # Create the second field (examples).
    if 'examples' in command_specific_help_page_dict:
        embed.add_field(name='*Examples*', value=f'\n'.join([f'`{global_prefix}{example[0]}`\n{example[1]}'
                                                             for example in command_specific_help_page_dict['examples']]), inline=True)

    # If example field was made, then make the usages field.
    if 'usages' in command_specific_help_page_dict and 'examples' in command_specific_help_page_dict:
        embed.add_field(name='*Usages*', value=f'\n'.join([f'`{global_prefix}{usage}`'
                                                             for usage in command_specific_help_page_dict['usages']]), inline=True)

    # Create the aliases field.
    if 'aliases' in command_specific_help_page_dict:
        embed.add_field(name='*Aliases*', value=f', '.join(f'__*{alias}*__' for alias in command_specific_help_page_dict["aliases"]),
                        inline=False)

    # If example field was not made earlier, then make the usages field here.
    if 'usages' in command_specific_help_page_dict and not 'examples' in command_specific_help_page_dict:
        embed.add_field(name='*Usages*', value=f'\n'.join([f'`{global_prefix}{usage[0]}`'
                                                           for usage in command_specific_help_page_dict['usages']]), inline=True)

    # Return.
    return embed


async def help_command(bot, message, argument):
    """
    The help command function.
    Displays the appropriate help page for the argument / author specified.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Try to get an argument (command name) out of the chaos.
    intended_command = None
    if argument:
        for word in parsing.normalize_string(argument).lower().split(' '):
            if word in COMMAND_SPECIFIC_HELP_EMBEDS:
                intended_command = word

    # If there's a command found in there, then use that.
    if intended_command:
        logging.info(message, f'requested help page for command {intended_command}')

        # If it's a string, send the base command.
        if isinstance(COMMAND_SPECIFIC_HELP_EMBEDS[word], str):
            await messaging.send_embed_without_local_image(message, COMMAND_SPECIFIC_HELP_EMBEDS[COMMAND_SPECIFIC_HELP_EMBEDS[word]])
        else:
            await messaging.send_embed_without_local_image(message, COMMAND_SPECIFIC_HELP_EMBEDS[word])

    # Otherwise, send a different one depending on whether or not the author is a developer.
    elif message.author.id in bot.developer_ids:
        logging.info(message, 'requested developer home help page')
        await messaging.send_embed_with_local_image_as_thumbnail(message, DEVELOPER_HOME_HELP_EMBED,
                                                                 assets.get_asset_path(HOME_HELP_PAGE_ICON))
    else:
        logging.info(message, 'requested public home help page')
        await messaging.send_embed_with_local_image_as_thumbnail(message, PUBLIC_HOME_HELP_EMBED,
                                                                 assets.get_asset_path(HOME_HELP_PAGE_ICON))


# Command values
PUBLIC_COMMAND_DICT = {
    'help': help_command
}
SPECIALIZED_COMMAND_DICT = {
    'help_init': initialize
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'help',
        'category': 'info',
        'description': 'Displays the command list, or the specific use cases for one command.',
        'examples': [('help', 'Displays the basic list of commands.'),
                     ('help weather', 'Displays the help page for the `weather` command.')],
        'usages': ['help', 'help < command >']
    }
]
"""
Die roll command.
Rolls a variable number of die (of varying size).
Formatted like nds(+/-)a
    n : Number of die to roll
    s : Number of sides
    a : Number to add or subtract to the final roll
"""
# Package Imports
import discord
import random

# Local Imports
from lib.util.logger import BotLogger as logging
from lib.util import messaging, parsing


# Constants
VALID_ARGUMENTS_CHARS = '1234567890+-d'
EMBED_COLOR = (221 << 16) + (46 << 8) + 68
EMBED_TITLE = ':game_die: Rolling Dice'


async def die_roll(bot, message, argument):
    """
    Performs a roll of the die.
    Die roll can vary per arguments.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # First, normalize the argument.
    argument = parsing.normalize_string(argument)

    # If there isn't an argument, then perform the roll with basic 1d6+0.
    if not argument:
        return await perform_roll(message, 1, 6, 0)

    # Otherwise, remove the remaining spaces.
    argument = argument.replace(' ', '')

    # Perform argument check.
    if not await argument_valid(message, argument):
        return

    # Parse argument.
    await parse_die_roll(message, argument)


async def argument_valid(message, argument):
    """
    Checks argument for validity.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.

    Returns:
        bool : Whether or not the argument is a valid die roll string at first glance.
    """
    # Detect any bad characters.
    for arg_char in argument:
        if arg_char not in VALID_ARGUMENTS_CHARS:
            logging.info(message, f'requested die roll with argument {argument}, invalid')
            await messaging.send_text_message(message, 'Invalid die argument.')
            return False

    # Detect multiple d's.
    if argument.count('d') > 1:
        logging.info(message, f'requested die roll with argument {argument}, invalid')
        await messaging.send_text_message(message, 'Invalid die argument.')
        return False

    # If we've made it this far, return true.
    return True


async def parse_die_roll(message, argument):
    """
    Parses the argument as a die roll and calls perform_roll with the appropriate counts for everything.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Get the sides.
    count, argument = await parse_count(message, argument)

    # If the argument is no longer a string, then return.
    if not isinstance(argument, str):
        return

    # Get the addendum.
    addendum, argument = await parse_addendum(message, argument)

    # If the argument is no longer a string, then return.
    if not isinstance(argument, str):
        return

    # Get the addendum.
    sides, valid = await parse_sides(message, argument)

    # If the sides aren't valid, return.
    if not valid:
        return

    # Perform the roll.
    await perform_roll(message, count, sides, addendum)


async def parse_count(message, argument):
    """
    Gets the die count out of the argument.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.

    Returns:
        int, str : The found count and the new argument (without the count).
    """
    # If there's a d in the argument, split there.
    if 'd' in argument:
        argument_split = argument.split('d')

        # Attempt integer conversion
        try:
            count = int(argument_split[0])
            present_error = False

        # On ValueError, or count <= 0, tell user invalid number and return None.
        except ValueError:
            present_error = True
        if present_error or count <= 0:
            logging.info(message, f'requested die roll with argument {argument}, invalid die number')
            await messaging.send_text_message(message, 'Invalid number of die.')
            return None, None

        # Set the argument to be the post-split part.
        return count, argument_split[1]

    # Return the default.
    return 1, argument


async def parse_addendum(message, argument):
    """
    Gets the addendum out of the argument.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.

    Returns:
        int, str : The found addendum and the new argument (without the count).
    """
    # Set default addendum.
    addendum = 0

    # Detect + or -.
    while '+' in argument or '-' in argument:

        # Get the index of plus and minus.
        plus_index = argument.rfind('+')
        minus_index = argument.rfind('-')

        # Attempt integer conversion
        try:
            addendum += int(argument[max(plus_index, minus_index) + 1:]) * (-1 if minus_index > plus_index else 1)

        # On ValueError, or count <= 0, tell user invalid number.
        except ValueError:
            logging.info(message, f'requested die roll with argument {argument}, invalid addendum')
            await messaging.send_text_message(message, 'Invalid addendum.')
            return None, None

        # Set the argument to not include the last + / -.
        argument = argument[:max(plus_index, minus_index)]

    # Return the addendum and the argument.
    return addendum, argument


async def parse_sides(message, argument):
    """
    Gets the number of sides for the die.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.

    Returns:
        int, bool : The found addendum and whether the sides are valid.
    """
    # Detect remaining number.
    try:
        sides = int(argument)

    # On ValueError, set the sides to the default.
    except ValueError:
        return 6, True

    # If the sides are 0 or less, then tell user invalid number.
    if sides < 1:
        logging.info(message, f'requested die roll with argument {argument}, invalid sides')
        await messaging.send_text_message(message, "A die with 0 sides isn't possible.")
        return 0, False

    # Return the number of sides and true.
    return sides, True


async def perform_roll(message, count, sides, addendum):
    """
    Performs the die rolls and sends the embed with the results.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        count (int) : The number of rolls to make.
    """
    # First, get all the rolls.
    rolls = []
    for i in range(count):
        rolls.append(random.randint(1, sides))

    # Next, create the addendum string.
    addendum_str = f'{" + " if addendum > 0 else " - "}{addendum}' if addendum else ''

    # Next, create the basic embed object.
    embed = discord.Embed(title=EMBED_TITLE, colour=EMBED_COLOR,
                          description=f'[**{count}d{sides}**: {", ".join(str(roll) for roll in rolls)}]{addendum_str}\n'
                                      f'Final Result: **{sum(rolls) + addendum}**')

    # Send message and log.
    logging.info(message, f'requested die roll with {count} rolls, {sides} sides, {addendum} addendum, result {sum(rolls) + addendum}')
    await messaging.send_embed_without_local_image(message, embed)


# Command values
PUBLIC_COMMAND_DICT = {
    'roll': die_roll,
    'dieroll': die_roll,
    'dice': die_roll,
    'diceroll': die_roll
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'roll',
        'category': 'util',
        'description': 'Performs a roll of the die. Rolls can vary depending on arguments.',
        'examples': [('roll', 'Rolls one six-sided die.'),
                     ('roll 2d8', 'Rolls two eight-sided die.'),
                     ('roll 4d4+5', 'Rolls four four-sided die and adds 5 to the combined result.'),
                     ('roll 20-5', 'Rolls one twenty-sided die and subtracts 5 from the result.'),
                     ('roll 10d+5', 'Rolls ten six-sided die and adds 5 to the result.')],
        'aliases': ['dice', 'diceroll', 'dieroll'],
        'usages': ['roll', 'roll < # of sides >', 'roll < # of die >d', 'roll < # of die >d< # of sides >', 'roll +< # to add >',
                   'roll -< # to subtract >', 'roll < # of die >d+< # to add >', 'roll < # of die >d-< # to subtract >',
                   'roll < # of die >d< # of sides >+< # to add >', 'roll < # of die >d< # of sides >-< # to subtract >']
    }
]

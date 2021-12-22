"""
Copy command.
Obnoxiously copies another user's messages.
"""
# Local Imports
from lib.util.exceptions import NoUserSpecifiedError, UnableToFindUserError, CannotAccessUserlistError
from lib.util.logger import BotLogger as logging
from lib.util import arguments, discord_info, messaging

# Package Imports
import discord


# Dict of copied users, keyed by guild / channel.
COPIED_USERS = {}


async def copy_msg(bot, message):
    """
    Copies a user's message if they have been deemed COPIABLE by someone.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # If this is in a guild, check for the guild id in the COPIED_USERS. Otherwise, check using the channel id.
    copy_key = str(message.guild.id if isinstance(message.channel, discord.TextChannel) else message.channel.id)

    # Check.
    if copy_key in COPIED_USERS and message.author.id in COPIED_USERS[copy_key]:
        await messaging.send_text_message(message, message.content)


async def copy_user(bot, message, argument):
    """
    Marks a user down as COPIABLE.
    Copiable users will be copied in every message they send.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Tries to get a valid user out of the argument.
    try:
        user = arguments.get_closest_users(message, argument, limit=1)[0]

    # On NoUserSpecifiedError, request they tag a user.
    except NoUserSpecifiedError:
        logging.info(message, f"requested copy for user '{argument}', invalid")
        return await messaging.send_text_message(message, 'Please mention a user to copy.')

    # On UnableToFindUserError, tell the user they couldn't find the desired one.
    except UnableToFindUserError:
        logging.info(message, f"requested copy for user '{argument}', invalid")
        return await messaging.send_text_message(message, f"Could not find user '{argument}'.")

    # On CannotAccessUserlistError, log an error and send an apology message.
    except CannotAccessUserlistError:
        logging.error(message, 'Failed to access the userlist')
        return await messaging.send_text_message(message, 'There was an error accessing the userlist. '
                                                          'Try @ mentioning someone instead.')

    # Gets the key we'll be using for the copied_users dict.
    copy_key = str(message.guild.id if isinstance(message.channel, discord.TextChannel) else message.channel.id)

    # Checks to make sure the mentioned user isn't the bot itself.
    if user == bot.user:
        logging.info(message, 'requested copy for this bot')
        return await messaging.send_text_message(message, 'Ha, ha. Very funny. No.')

    # If the copy key isn't in the dict, add it.
    if copy_key not in COPIED_USERS:
        COPIED_USERS[copy_key] = []

    # Otherwise, copy the user.
    await messaging.send_text_message(message, f'Now copying user {user.display_name}')
    if user.id not in COPIED_USERS[copy_key]:
        COPIED_USERS[copy_key].append(user.id)
        logging.info(message, 'requested copy for user ' + str(user) + ', now copying')
    else:
        logging.info(message, 'requested copy for user ' + str(user) + ', already copying')


async def stop_copying(bot, message, argument):
    """
    Stops copying everyone in a server / channel.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Gets the key we'll be using for the copied_users dict.
    copy_key = str(message.guild.id if isinstance(message.channel, discord.TextChannel) else message.channel.id)

    # If the thing exists in the dict, delete it.
    if copy_key in COPIED_USERS:
        logging.info(message, f'requested to stop copying, {len(COPIED_USERS[copy_key])} users deleted from copied_users')
        del COPIED_USERS[copy_key]
        await messaging.send_text_message(message, 'No longer copying people in this server.')

    else:
        logging.info(message, 'requested to stop copying, already done')
        await messaging.send_text_message(message, "Wasn't copying anyone here to begin with, but ok.")


# Command values
PUBLIC_COMMAND_DICT = {
    'copy': copy_user,
    'stopcopying': stop_copying
}
REACTIVE_COMMAND_LIST = [
    copy_msg
]
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'copy',
        'category': 'fun_simple',
        'description': 'Can be used to make the bot copy someone else. How annoying!',
        'examples': [('copy @dummy#0000', 'Copies the user @dummy#0000.'),
                     ('copy dummy', "Copies the user with the name closest to 'dummy'.")],
        'usages': ['copy < user >']
    }
]
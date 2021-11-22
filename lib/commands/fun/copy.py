"""
UWU and OWO command.
Make a mockery out of people by converting their messages into uwu- or owo-speak.
"""
# Imports
from lib.util import messaging, misc
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
        await message.channel.send(message.content)


async def copy_user(bot, message, argument):
    """
    Marks a user down as copiable.
    Copiable users will be copied in every message they send.
    """
    # Tries to get a valid user out of the argument.
    try:
        users = misc.get_closest_users(message, argument, is_in_guild)
    except (ArgumentTooShortError, NoUserSpecifiedError, UnableToFindUserError):
        users = []
    if not users:
        log.info(misc.get_comm_start(message, is_in_guild) + 'requested copy for user ' + argument + ', invalid')
        await message.channel.send('Invalid user.')
        return

    # Gets the key we'll be using for the copied_users dict.
    if is_in_guild:
        copied_key = str(message.guild.id)
    else:
        copied_key = str(message.channel.id)
    if copied_key not in self.copied_users.keys():
        self.copied_users.update({copied_key: []})

    # Adds the users to the copy dict.
    for user in users:

        # Checks to make sure it isn't self.
        if user == self.user:
            if not len(users) - 1:
                log.debug(misc.get_comm_start(message, is_in_guild) + 'requested copy for this bot')
                await message.channel.send('Yeah, no, I\'m not gonna copy myself.')
            continue

        # Other.
        await message.channel.send('Now copying user ' + (user.nick if user.nick else user.name))
        if user not in self.copied_users[copied_key]:
            self.copied_users[copied_key].append(user)
            log.info(misc.get_comm_start(message, is_in_guild) + 'requested copy for user ' + str(user) + ', now copying')
        else:
            log.info(misc.get_comm_start(message, is_in_guild) + 'requested copy for user ' + str(user) + ', already copying')


async def stop_copying(bot, message, argument):
    """
    Stops copying everyone in a server.
    """
    # Gets copy key
    if is_in_guild:
        copied_key = str(message.guild.id)
    else:
        copied_key = str(message.channel.id)

    # If the thing exists in the dict
    if copied_key in self.copied_users.keys():
        log.debug(misc.get_comm_start(message, is_in_guild) + 'requested to stop copying, {} users deleted from copied_users'.format(len(self.copied_users[copied_key])))
        self.copied_users.pop(copied_key)
        await message.channel.send('No longer copying people in this server.')
    else:
        log.debug(misc.get_comm_start(message, is_in_guild) + 'requested to stop copying, already done')
        await message.channel.send('Wasn\'t copying anyone here to begin with, but ok.')
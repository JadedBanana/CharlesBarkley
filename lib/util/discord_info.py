
# Package Imports
from datetime import datetime
import discord
import logging
import pytz

# Local Imports
from lib.util.exceptions import CannotAccessUserlistError, FirstMessageInChannelError


# Timezone names for different discord VoiceRegions.
DISCORD_REGION_TIMEZONE_NAMES = {
    'us-west': 'America/Los_Angeles',
    'us-east': 'America/New_York',
    'us-south': 'America/Chicago',
    'us-central': 'America/Chicago',
    'eu_west': 'Europe/London',
    'eu_central': 'Europe/Berlin',
    'singapore': 'Singapore',
    'london': 'Europe/London',
    'sydney': 'Australia/Sydney',
    'amsterdam': 'Europe/Amsterdam',
    'frankfurt': 'Europe/Berlin',
    'brazil': 'Brazil/East',
    'hongkong': 'Hongkong',
    'russia': 'Europe/Moscow',
    'japan': 'Asia/Tokyo',
    'southafrica': 'Egypt',
    'south-korea': 'Asia/Seoul',
    'india': 'Asia/Kolkata',
    'europe': 'Europe/Berlin',
    'dubai': 'Asia/Dubai',
    'vip-us-east': 'America/New_York',
    'vip-us-west': 'America/Los_Angeles',
    'vip-amsterdam': 'Europe/Amsterdam'
}


def get_applicable_users(message, exclude_bots=True, exclude_users=None):
    """
    Returns a list of applicable users that fit the criteria provided.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
        exclude_bots (bool) : Whether or not to exclude bots from the list.
        exclude_users (list) : Which users, if any, to exclude from the list.

    Returns:
        discord.user.User[] : A list of users that fit the criteria.

    Raises:
        CannotAccessUserlistError : Can't access the userlist.
                                    This error is common when working from Windows.
    """
    # First, we get a list of all users.
    # If this is a guild, grab the users in the guild.
    if isinstance(message.channel, discord.TextChannel):
        all_users = message.guild.members

    # If this is a DM, grab the recipient.
    elif isinstance(message.channel, discord.DMChannel):
        all_users = [message.channel.recipient]

    # Otherwise (group channel), pull the recipients.
    else:
        all_users = message.channel.recipients

    # If there isn't an all_users, raise a CannotAccessUserlistError.
    if len(all_users) < 2:
        raise CannotAccessUserlistError()

    # If we were told to not include bots, we get rid of them.
    if exclude_bots:
        for i in range(len(all_users) - 1, -1, -1):
            if all_users[i].bot:
                all_users.remove(all_users[i])

    # We remove all the users in exclude_users, if any.
    if exclude_users:
        for usr in exclude_users:
            if usr in all_users:
                all_users.remove(usr)

    # Returns.
    return all_users


def get_guild_time(message):
    """
    Gets a guild's average local time.
    This is basically guessed by using the weighted guild regions.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.

    Returns:
        datetime.datetime : The average datetime across all the guild's channels.
    """
    # First, get the weighted guild regions.
    guild_regions = get_guild_regions_weighted(message)

    # List for keeping track of time weights.
    time_weights = []

    # Iterate through each guild region.
    for region, weight in guild_regions.items():

        # If the region is NOT In the discord region timezone names list, log an error and continue.
        if region.value not in DISCORD_REGION_TIMEZONE_NAMES:
            logging.error(f'VoiceRegion {region.value} completely unexpected')
            continue

        # Otherwise, add the timezone's current time to the list.
        time_weights.append((datetime.now(pytz.timezone(DISCORD_REGION_TIMEZONE_NAMES[region.value])), weight))

    # If there are no time_weights, just send the local time.
    if not time_weights:
        return datetime.now()

    # Now that all the time weights are acquired, start adding.
    time_total = 0

    # Iterate through time and weights.
    for time, weight in time_weights:

        # Add up the times.
        time_total += (time.timestamp() + time.tzinfo.utcoffset(time).total_seconds()) * weight

    # Now, average it.
    time_average = time_total / sum([weight for time, weight in time_weights])

    # Create a datetime object from that average time and return.
    return datetime.fromtimestamp(time_average)


def get_guild_regions_weighted(message):
    """
    Gets the supposed region for a guild.
    This depends on the region overrides for each voice channel.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.

    Returns:
        dict : A list of voice regions and how often they appear in each voice channel.
    """
    # First, make sure this is a guild. If it isn't, just return an empty dict.
    if not isinstance(message.channel, discord.TextChannel):
        return {}

    # Now, we keep a tally (score).
    region_count = {}

    # Iterate through voice channels.
    for voice_channel in message.guild.voice_channels:

        # Get rtc region.
        region = voice_channel.rtc_region

        # If it's None, then continue.
        if not region:
            continue

        # Add it to the region_count.
        if region in region_count:
            region_count[region] += 1
        else:
            region_count[region] = 1

    # Return the region_count.
    return region_count


async def get_message_history(message, count=100):
    """
    Gets the message history in a channel, given a message.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
        count (int) : How many messages back to retrieve.

    Returns:
        discord.message.Message[] : The most recent messages in the channel.
    """
    message_history = message.channel.history(limit=count)
    return [msg async for msg in message_history]


async def get_secondmost_recent_message(message):
    """
    Gets the second-most recent message in a channel, given a message.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.

    Returns:
        discord.message.Message : The previous message in the channel.

    Raises:
        FirstMessageInChannelError : The message this method was called with is the first message in the channel.
    """
    # Simple get statement.
    try:
        return (await get_message_history(message, 2))[1]

    # If there's an index error, raise the FirstMessageInChannelError.
    except IndexError:
        raise FirstMessageInChannelError()


async def get_reply_lineage(message, max_depth=99):
    """
    Gets the lineage of replies from this message.

    Arguments:
        message (discord.message.Message) : The discord message object we are finding the ancestry of.
        max_depth (int) : The maximum amount of replies to traverse through. Default is 99.

    Returns:
        discord.message.Message[] : The discord messages representing this message's lineage, from newest to oldest.
    """
    # Initialize reply list.
    reply_list = [message]

    # If this message is a reply, enter loop.
    if message.reference:
        reply = await message.channel.fetch_message(message.reference.message_id)

        # Get every reply upstream.
        while reply and len(reply_list) < max_depth + 1:
            reply_list.append(reply)
            if reply.reference:
                reply = await message.channel.fetch_message(reply.reference.message_id)

    # Return.
    return reply_list


class IdWrapper:
    """
    IdWrapper class is made to wrap any object with an ID.
    Mostly used as an interface.
    """

    def __init__(self, object_id):
        """
        Initializes the IdWrapper object.

        Arguments:
            object_id (int) : The object's ID.
        """
        self.id = object_id


class LightweightUser(IdWrapper):
    """
    LightweightUser class is made to store a user object in a more lightweight way.
    """

    def __init__(self, base_user):
        """
        Initializes the LightweightUser object.

        Arguments:
            base_user (discord.User) : The user to base this lightweight user off of.
        """
        # Copy over variables.
        IdWrapper.__init__(self, base_user.id)
        self.name = base_user.name
        self.display_name = base_user.display_name
        self.bot = base_user.bot
        self.roles = base_user.roles if hasattr(base_user, 'roles') else []
        self.avatar = base_user.avatar


class MessageWrapper:
    """
    MessageWrapper is there to wrap message objects that exist outside their messages so that they can
    be used with utility methods.
    """

    def __init__(self, channel_id=None):
        """
        Initializes the MessageWrapper object.

        Arguments:
            channel_id (int) : The message's channel's id.
        """
        self.channel = IdWrapper(channel_id)

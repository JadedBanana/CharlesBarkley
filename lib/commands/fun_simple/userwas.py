from lib.util.exceptions import FirstMessageInChannelError
from lib.util import discord_info, environment, messaging


async def get_messages_in_screenshot(message):
    """
    Gathers all the messages that will be in the image based on a reply chain.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # First, gather the subject message.
    try:
        subject = await discord_info.get_secondmost_recent_message(message)
    except FirstMessageInChannelError:
        return

    # Get reply chain.
    max_chain_length = environment.get('USERWAS_MAX_CHAIN_LENGTH')
    post_list = await discord_info.get_reply_lineage(subject, max_chain_length - 1)

    # If no parents were found, or we've maxed it out, return.
    post_count = len(post_list)
    if post_count == 1 or post_count == max_chain_length:
        return post_list

    # Otherwise, travel down the chain and try to find any recent parallel replies.
    original_post_list = post_list.copy()
    recent_replies = [
        msg for msg in await discord_info.get_message_history(message, environment.get('USERWAS_REPLY_CHECK_MAX_LENGTH'))
        if msg.reference and msg not in post_list
    ]
    recent_replies.reverse()
    for i in range(1, len(original_post_list)):
        message_replies = []

        # Travel through the list and identify any replies, or replies of those replies, until no new replies have been found.
        for msg in recent_replies:

            # Check against OG reply.
            if msg.reference.message_id == original_post_list[i].id:
                message_replies.append([msg])

            # Check against subsequent replies.
            else:
                for msg_list in message_replies:
                    if msg.reference.message_id == msg_list[0].id:
                        msg_list.append(msg)

        # Sort them by length descending.
        message_replies = sorted(message_replies, key=lambda list: len(list), reverse=True)

        # Iterate through. If any found are able to fit within the list without exceeding the max size, add them.
        for msg_list in message_replies:
            if len(msg_list) + len(post_list) <= max_chain_length:
                post_list += msg_list

                # If post list is now equal to max length, break.
                if len(post_list) == max_chain_length:
                    break

    # Sort messages by their id and return.
    return sorted(post_list, key=lambda msg: msg.id, reverse=True)


async def userhead(message, argument):
    """
    Generates a 4chan-style "USER WAS BANNED FOR THIS POST" edit of the previous message.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # First, get all the messages.
    messages = await get_messages_in_screenshot(message)

    print([msg.content for msg in messages])


# Command values
DEVELOPER_COMMAND_DICT = {
    'userwas': userhead
}

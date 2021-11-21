"""
Module handling message sending between the bot and Discord.
"""

async def send_text_message(message, text_str):
    """
    Sends a text message back to the channel the trigger message came from.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
        text_str (str) : The text message's intended text.
    """
    # Send the message.
    await message.channel.send(text_str)
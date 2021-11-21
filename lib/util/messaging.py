"""
Module handling message sending between the bot and Discord.
"""

async def send_text_message(trigger_message, text_str):
    """
    Sends a text message back to the channel the trigger message came from.
    """
    # Send the message.
    await trigger_message.channel.send(text_str)
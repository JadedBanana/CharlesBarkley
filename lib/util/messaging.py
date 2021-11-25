"""
Module handling message sending between the bot and Discord.
"""
# Imports
from lib.util import tempfiles
import discord


async def send_text_message(message, text_str):
    """
    Sends a text message back to the channel the trigger message came from.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
        text_str (str) : The text message's intended text.
    """
    # Attempt to send the message as a simple text.
    try:
        await message.channel.send(text_str)

    # If this happened, then the message was too long. Send as file.
    except discord.errors.HTTPException:
        # First, have the tempfiles module create a temporary text file on-disk.
        text_file_path = tempfiles.save_temporary_text_file(text_str)

        # Next, instantiate the file and send the message.
        file = discord.File(text_file_path, filename='text_message.txt')
        await message.channel.send(file=file)



async def send_image_based_embed(message, image, title, embed_color):
    """
    Sends an image-based embed back to the channel the trigger message came from.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
        image (PIL.Image) : The Image object to be sent as the embed's image.
        title (str) : The embed's title.
        embed_color (int) : The color of the embed's sidebar thing.
    """
    # First, have the tempfiles module create a temporary image on-disk.
    image_path = tempfiles.save_temporary_image(image)

    # Next, instantiate the embed object, then a file, and set the embed to use the file as its image.
    embed = discord.Embed(title=title, colour=embed_color)
    file = discord.File(image_path, filename='embed_image.png')
    embed.set_image(url='attachment://embed_image.png')

    # Finally, send the message with embed and file as attributes.
    await message.channel.send(embed=embed, file=file)

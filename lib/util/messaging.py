"""
Module handling message sending between the bot and Discord.
"""
# Imports
from lib.util import tempfiles
import discord


async def send_text_message(message, text_str):
    """
    Sends a text message back to the channel the trigger message came from.
    If the message exceeds the allowed 2000 characters, it will be sent as a file.

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


async def send_codeblock_message(message, text_str):
    """
    Sends a codeblock message.
    If the message exceeds the allowed 2000 characters, it will be split into pieces.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
        text_str (str) : The text message's intended text.
    """
    # Split the text_str into newlines.
    text_str_by_line = text_str.split('\n')

    # Create a string object to keep the current message.
    current_message_str = ''

    # Perform a for loop to go through lines.
    for i in range(len(text_str_by_line) - 1):

        # Append the current line.
        current_message_str += text_str_by_line[i] + '\n'

        # Check if the next line would push it over the edge.
        if len(current_message_str) + len(text_str_by_line[i + 1]) + 1 >= 1990:

            # Send the current_message_str, then erase.
            await message.channel.send(f'```{current_message_str}```')
            current_message_str = ''

    # Send the remaining text.
    await message.channel.send(f'```{current_message_str + text_str_by_line[-1]}```')


async def send_file(message, file_dir):
    """
    Sends a file.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
        file_dir (str) : The file directory.
    """
    await message.channel.send(file=discord.File(file_dir))


async def send_image_based_embed(message, image, title, embed_color, footer=''):
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

    # If there's a footer, set it.
    if footer:
        embed.set_footer(text=footer)

    # Finally, send the message with embed and file as attributes.
    await message.channel.send(embed=embed, file=file)


async def send_embed_with_local_image_as_thumbnail(message, embed, filepath):
    """
    Sends a pre-made embed (with a local image as the thumbnail) back to the channel the trigger message came from.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
        embed (discord.Embed) : The discord embed object that was made by whatever class called this function.
        filepath (str) : The local image's filepath.
    """
    # Load the file and insert it into the embed.
    file = discord.File(filepath, filename='embed_image.png')
    embed.set_thumbnail(url='attachment://embed_image.png')

    # Finally, send the message with embed and file as attributes.
    await message.channel.send(embed=embed, file=file)



async def send_embed_without_local_image(message, embed):
    """
    Sends a pre-made embed (with a web-hosted image) back to the channel the trigger message came from.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
        embed (discord.Embed) : The discord embed object that was made by whatever class called this function.
    """
    # Send the message.
    await message.channel.send(embed=embed)

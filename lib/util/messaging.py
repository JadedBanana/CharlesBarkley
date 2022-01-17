"""
Module handling message sending between the bot and Discord.
"""
# Local Imports
from lib.util import temp_files

# Package Imports
import discord


# Image hosting channel id and bot.
IMAGE_HOSTING_CHANNEL_ID = 932460732631621692
BOT = None


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
        # First, have the temp_files module create a temporary text file on-disk.
        text_file_path = temp_files.save_temporary_text_file(text_str)

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
    # Iterates through the codeblock message and sends it.
    for message_str in format_codeblock_message(text_str, 1990):
        await message.channel.send(message_str)


async def send_error_message(message, global_prefix, traceback_str):
    """
    Sends an error message.
    If the traceback exceeds 2000 characters, it will be split into pieces.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
        global_prefix (str) : The global prefix.
        traceback_str (str) : The exception's traceback.
    """
    # Get the codeblock message.
    traceback_strings = format_codeblock_message(traceback_str, 1600)

    # If there's only one traceback string, then just put the messages at the beginning and end.
    if len(traceback_strings) < 2:
        return await message.channel.send(f'An error occurred while processing this command:{traceback_strings[0]}'
                                          f'Please use `{global_prefix}report` to let the developer know about the '
                                          f'issue.')

    # Otherwise, send one start string and one end string, with the rest in the middle.
    # Send first message.
    await message.channel.send(f'An error occurred while processing this command:{traceback_strings[0]}')
    # Send middle message.
    for traceback_str in traceback_strings[1:-1]:
        await message.channel.send(traceback_str)
    # Send final message.
    await message.channel.send(f'{traceback_strings[-1]}Please use `{global_prefix}report` to let the developer know '
                               f'about the issue.')


async def send_file(message, file_dir):
    """
    Sends a file.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
        file_dir (str) : The file directory.
    """
    await message.channel.send(file=discord.File(file_dir))


async def send_local_image_based_embed(message, image, title, embed_color, description='', footer='', view=None,
                                       hosted_online=False):
    """
    Sends an image-based embed back to the channel the trigger message came from.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
        image (PIL.Image.Image) : The Image object to be sent as the embed's image.
        title (str) : The embed's title.
        embed_color (int) : The color of the embed's sidebar thing.
        description (str) : The embed's description, if any.
        footer (str) : The footer text, if any.
        view (discord.ui.view.View) : The discord view, if any.
        hosted_online (bool) : Whether to host this image online (and avoid sending a file).
    """
    # First, instantiate the embed object, then a file, and set the embed to use the file as its image.
    embed = discord.Embed(title=title, colour=embed_color, description=description) if description else \
        discord.Embed(title=title, colour=embed_color)

    # If there's a footer, set it.
    if footer:
        embed.set_footer(text=footer)

    # Have the temp_files module create a temporary image on-disk and create the image file..
    image_path = temp_files.save_temporary_image(image)
    file = discord.File(image_path, filename='embed_image.png')

    # If we host online, then host online by getting the image hosting channel.
    if hosted_online:
        channel = BOT.get_channel(IMAGE_HOSTING_CHANNEL_ID)

        # Send the image to the image hosting channel.
        image_path = temp_files.save_temporary_image(image)
        file = discord.File(image_path, filename='embed_image.png')
        image_message = await channel.send(file=file)

        # Extract the attachment url from the image.
        attachment_url = image_message.attachments[0].url

        # Set the image and send.
        embed.set_image(url=attachment_url)
        await message.channel.send(embed=embed, view=view)

    # Otherwise, attach the file and send.
    else:
        embed.set_image(url='attachment://embed_image.png')
        await message.channel.send(embed=embed, file=file, view=view)


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


async def send_embed_without_local_image_with_text_message(message, text_str, embed):
    """
    Sends a pre-made embed (with a web-hosted image) back to the channel the trigger message came from.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
        text_str (str) : The text message's intended text.
        embed (discord.Embed) : The discord embed object that was made by whatever class called this function.
    """
    # Send the message.
    await message.channel.send(text_str, embed=embed)


async def edit_local_image_based_embed_from_interaction(interaction, image, title, embed_color, description='',
                                                        footer='', view=None):
    """
    Edits the interaction's message to an image-based embed.

    Arguments:
        interaction (discord.interactions.Interaction) : The interaction that triggered this method.
        image (PIL.Image.Image) : The Image object to be sent as the embed's image.
        title (str) : The embed's title.
        embed_color (int) : The color of the embed's sidebar thing.
        description (str) : The embed's description, if any.
        footer (str) : The footer text, if any.
        view (discord.ui.view.View) : The discord view, if any.
    """
    # Get the image hosting channel.
    channel = BOT.get_channel(IMAGE_HOSTING_CHANNEL_ID)

    # Send the image to the image hosting channel.
    image_path = temp_files.save_temporary_image(image)
    file = discord.File(image_path, filename='embed_image.png')
    message = await channel.send(file=file)

    # Extract the attachment url from the image.
    attachment_url = message.attachments[0].url

    # Next, instantiate the embed object, and set the embed to use the file as its image.
    embed = discord.Embed(title=title, colour=embed_color, description=description) if description else \
        discord.Embed(title=title, colour=embed_color)
    embed.set_image(url=attachment_url)

    # If there's a footer, set it.
    if footer:
        embed.set_footer(text=footer)

    # Send the message with embed and file as attributes.
    await interaction.response.edit_message(embed=embed, view=view)


def format_codeblock_message(text_str, size):
    """
    Formats a codeblock message.
    Splits the message into size-character pieces.

    Arguments:
        text_str (str) : The text message's intended text.
        size (int) : The maximum character length of each segment.
                     Max should be about 1990.

    Returns:
        str[] : The list of split message strings.
    """
    # Split the text_str into newlines.
    text_str_by_line = text_str.split('\n')

    # Create a list to keep track of the codeblock messages.
    message_strs = []

    # Create a string object to keep the current message.
    current_message_str = ''

    # Perform a for loop to go through lines.
    for i in range(len(text_str_by_line) - 1):

        # Append the current line.
        current_message_str += text_str_by_line[i] + '\n'

        # Check if the next line would push it over the edge.
        if len(current_message_str) + len(text_str_by_line[i + 1]) + 1 >= size:

            # Append the current_message_str, then erase.
            message_strs.append(f'```{current_message_str}```')
            current_message_str = ''

    # Append the remaining text.
    message_strs.append(f'```{current_message_str}{text_str_by_line[-1]}```')

    # Return.
    return message_strs

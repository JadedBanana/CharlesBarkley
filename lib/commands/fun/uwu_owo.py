"""
UWU and OWO command.
Make a mockery out of people by converting their messages into uwu- or owo-speak.
"""
# Local Imports
from lib.util.exceptions import FirstMessageInChannelError
from lib.util import messaging, misc

# Package Imports
import random


# Emote replacement variables
EMOTE_CHARACTERS = '0123456789_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVQXYZ'
BASIC_REPLACE_DICT = {
    'wr': 'w',
    'WR': 'W',
    'Wr': 'W',
    'wR': 'w',
    'r': 'w',
    'R': 'W',
    'l': 'w',
    'L': 'W',
    'no': 'nyo',
    'No': 'Nyo',
    'NO': 'NYO',
    'nO': 'nYO'
}
UWU_FACES = {
    ':)': 'uwu', ':(': 'umu', ':|': 'u_u', ':-)': 'uwu', ':-(': 'umu', ':-|': 'u_u', '^_^': 'uwu',
    '^w^': 'uwu', 'O_o': 'u_u', 'o_o': 'u_u', 'o_O': 'u_u', 'O_O': 'u_u', '(:': 'uwu', ':D': 'uwu',
    'D:': 'umu', '):': 'umu'
}
OWO_FACES = {
    ':)': 'owo', ':(': 'omo', ':|': 'o_o', ':-)': 'owo', ':-(': 'omo', ':-|': 'o_o', '^_^': 'owo',
    '^w^': 'owo', 'O_o': 'o_o', 'o_o': 'o_o', 'o_O': 'o_o', 'O_O': 'o_o', '(:': 'owo', ':D': 'owo',
    'D:': 'omo', '):': 'omo'
}


def do_basic_text_replace(text):
    """
    Performs a basic text replace, just replacing everything according to the BASIC_REPLACE_DICT.

    Arguments:
        text (str) : The text to be converted to uwu- or owo-speak.
    """
    # Iterate through and do the replacements.
    for replace, replace_with in BASIC_REPLACE_DICT.items():
        text = text.replace(replace, replace_with)

    # Return text.
    return text


def do_uwu_owo_replace(text, use_owo):
    """
    Method for advanced replacement in uwu- or owo-speak.
    Replaces emoticons, but maintains emotes.

    Arguments:
        text (str) : The text to be converted to uwu- or owo-speak.
        use_owo (bool) : Whether or not to use owo. If true, will be converted to owo-speak. If false, will be converted to uwu-speak.
    """
    # Get the number of colons. This is used to detect the number of emotes.
    colon_count = text.count(':')

    # If there IS an emote, we take special care to avoid replacing any letters in them.
    if colon_count > 1:
        text_replaced = ''

        # Variables needed to perform proper emote avoidance.
        last_index = -1
        replaced_max = -1
        colons_passed = 0

        # Perform loop.
        while colons_passed < colon_count - 1:
            # Find the next colon.
            colon_index = text.index(':', last_index + 1)

            # Find the NEXT next colon.
            next_colon_index = text.index(':', colon_index + 1)

            # Test and see if all the characters between the two colons are alphanumeric.
            # Also makes sure the colons are more than 2 apart.
            is_emote = next_colon_index - colon_index > 2
            if is_emote:
                for c in text[colon_index + 1:next_colon_index]:
                    if c not in EMOTE_CHARACTERS:
                        is_emote = False

            # If this is an emote, we act accordingly.
            if is_emote:
                # We go ahead and uwuify everything up to this point.
                text_append = do_basic_text_replace(text[replaced_max + 1:colon_index])
                # Replace the faces in the text with the respective uwu- and owo- versions.
                faces = OWO_FACES if use_owo else UWU_FACES
                for face_before, face_after in faces.items():
                    text_append = text_append.replace(f' {face_before} ', f' {face_after} ')
                    # If the first character is the face.
                    if replaced_max == -1 and text_append.startswith(face_before):
                        text_append = face_after + text_append[len(face_before):]
                # Add on text_replaced to text_append.
                text_replaced += text_append

                # Add the raw emote in.
                text_replaced += text[colon_index:next_colon_index + 1]

                # Update replaced_max and other vars.
                replaced_max = next_colon_index
                last_index = next_colon_index
                colons_passed += 2

            # This isn't an emote. Update colons_passed and last_index.
            else:
                colons_passed += 1
                last_index = colon_index

        # Now that we've passed every colon, we append the rest of the text and do the text replacement.
        text_append = do_basic_text_replace(text[replaced_max + 1:])
        # Replace the faces in the text with the respective uwu- and owo- versions.
        faces = OWO_FACES if use_owo else UWU_FACES
        for face_before, face_after in faces.items():
            text_append = text_append.replace(f' {face_before} ', f' {face_after} ')
            if text_append.startswith(face_before):
                text_append = face_after + text_append[len(face_before):]
                # If the last character is the face.
                if text_append.endswith(face_before):
                    text_append = face_after + text_append[len(face_before):]
        # Add on text_replaced to text_append.
        text_replaced += text_append

        # If there isn't a face on the end, we have a random chance to add an uwu.
        if not any([text_replaced.endswith(fac) for fac in faces] + \
                   [text_replaced.endswith(fac + '.') for fac in faces] + \
                   [text_replaced.endswith(fac + '!') for fac in faces]) and \
                random.choice([True, False]):
            text_replaced += random.choice([' owo' if use_owo else ' uwu', ' >w<'])

        # Return.
        return text_replaced

    # If there is no emote, we just return the basics.
    replaced_text = do_basic_text_replace(text)
    # Replace the faces in the text with the respective uwu- and owo- versions.
    faces = OWO_FACES if use_owo else UWU_FACES
    for face_before, face_after in faces.items():
        replaced_text = replaced_text.replace(f' {face_before} ', f' {face_after} ')
        # If the first character is the face.
        if replaced_text.startswith(face_before):
            replaced_text = face_after + replaced_text[len(face_before):]
        # If the last character is the face.
        if replaced_text.endswith(face_before):
            replaced_text = face_after + replaced_text[len(face_before):]

    # If there isn't a face on the end, we have a random chance to add an uwu.
    if not any([replaced_text.endswith(fac) for fac in faces] + \
               [replaced_text.endswith(fac + '.') for fac in faces] + \
               [replaced_text.endswith(fac + '!') for fac in faces]) and \
            random.choice([True, False]):
        replaced_text += random.choice([' owo' if use_owo else ' uwu', ' >w<'])

    # Return.
    return replaced_text


async def uwu_owo_master(message, argument, use_owo=False):
    """
    Converts a message into uwu- or owo-speak.
    Since the code for both commands are very similar, they're combined into one method here.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
        use_owo (bool) : Whether or not to use owo. If true, will be converted to owo-speak. If false, will be converted to uwu-speak.
    """
    # If an argument was provided, we run the uwu / owo replace on that argument.
    if argument:
        return await messaging.send_text_message(message, do_uwu_owo_replace(argument, use_owo))

    # Otherwise, we attempt to do it on the second-most recent message.
    try:
        # Attempt to grab the second-most recent message and run the thing.
        content = (await misc.get_secondmost_recent_message(message)).content
        if content:
            await messaging.send_text_message(message, do_uwu_owo_replace(content, use_owo))

    # If we got a little error, we just pass.
    except FirstMessageInChannelError:
        pass


async def uwuify(bot, message, argument):
    """
    Converts a message / argument to uwu-speak and sends it back.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Run master method
    await uwu_owo_master(message, argument, False)


async def owoify(bot, message, argument):
    """
    Converts a message / argument to owo-speak and sends it back.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Run master method
    await uwu_owo_master(message, argument, True)


# Command values
PUBLIC_COMMAND_DICT = {
    'uwu': uwuify,
    'owo': owoify
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'uwu',
        'category': 'fun',
        'description': 'Converts a message into uwu-speak.',
        'examples': [('uwu', 'Takes all the text in the last message and converts it into uwu-speak.'),
                     ('uwu somebody once told me', "Converts 'somebody once told me' to uwu-speak.")],
        'usages': ['uwu', 'uwu < message >']
    },
    {
        'command_name': 'owo',
        'category': 'fun',
        'description': 'Converts a message into owo-speak.',
        'examples': [('owo', 'Takes all the text in the last message and converts it into owo-speak.'),
                     ('owo somebody once told me', "Converts 'somebody once told me' to owo-speak.")],
        'usages': ['owo', 'owo < message >']
    }
]
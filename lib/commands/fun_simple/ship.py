"""
Ship command.
Ships two users together. Creepy!
"""
# Local Imports
from lib.util.exceptions import NoUserSpecifiedError, UnableToFindUserError, CannotAccessUserlistError
from lib.util import arguments, assets, discord_info, messaging, temp_files
from lib.util.logger import BotLogger as logging

# Package Imports
from PIL import Image
import discord
import random


# Some helpful constants.
ICON_SIZE = 128
HEART_IMG = 'heart.png'
EMBED_COLOR = (221 << 16) + (115 << 8) + 215
NORMAL_MESSAGES = [
    "I ship {0} with {1}! Isn\'t it cute?",
    'If you ask me, {0} and {1} were meant for each other.',
    'OTP: {0} and {1}.',
    'I ship {0} and {1}. Cute, right?',
    'I like {0} and {1}. Enemies to lovers-sorta thing.',
    '{0} x {1}. No further questions.',
    'Imagine a yandere {0} going after {1}. Crazy, right?',
    '{0} and {1}. Both are huge tsunderes.',
    '{0} and {1}. Bakadere relationships are so cute, IMO.',
    'Say whatever you want. {0} and {1} is the purest, most amazing ship and I will not stand for any others.',
    "The fact that there isn't a slashfic about {0} and {1} is an absolute travesty.",
    '{0} and {1}... so soft, so pure...'
]
BASHFUL_MESSAGES = [
    ':flushed: Me? Um, well... if I had to pick... probably {1}.',
    "Wh-what are you asking me for?! W-well, it's not like I like them or anything, but... "
    'I guess I could tolerate {1}.',
    "Wh-?! What's with that look?! It's not like I like {1} or anything!",
    'Ah... I guess... {1} would be a good match for me.'
]


async def ship(bot, message, argument):
    """
    Ships 2 or more users together.
    If a user isn't tagged, it ships 2 random users together.
    If a user IS tagged, it ships them with someone random.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Make sure this command isn't being used in a DM.
    if isinstance(message.channel, discord.DMChannel):
        logging.info(message, 'requested ship, but in DMs, so invalid')
        return await messaging.send_text_message(message, 'This command cannot be used in DMs.')

    # This try/catch surrounding the whole thing is just in case we can't access the userlist.
    try:

        # Tries to get a valid user out of the argument.
        try:
            partner_1 = arguments.get_closest_users(message, argument, exclude_bots=False, limit=1)[0]

        # On UnableToFindUserError, tell the user they couldn't find the desired one.
        except UnableToFindUserError:
            logging.info(message, f"requested ship for user '{argument}', invalid")
            return await messaging.send_text_message(message, f"Could not find user '{argument}'.")

        # If no user was specified, then we just need to grab 2 users as opposed to one.
        except NoUserSpecifiedError:
            partner_1 = None

        # Grab partner 1, if necessary
        if not partner_1:
            partner_1 = random.choice(
                discord_info.get_applicable_users(message, exclude_bots=True, exclude_users=[bot.user]))

        # Grab partner 2.
        partner_2 = random.choice(discord_info.get_applicable_users(message, exclude_bots=True, exclude_users=[
            bot.user, partner_1
        ]))

        # Log this ship
        logging.info(message, f'requested ship, shipped {partner_1} and {partner_2}')

        # Gets the PFP for partner 1 and 2.
        partner_1_img = await temp_files.checkout_profile_picture_by_user_with_typing(
            partner_1, message, 'ship', (ICON_SIZE, ICON_SIZE))
        partner_2_img = await temp_files.checkout_profile_picture_by_user_with_typing(
            partner_2, message, 'ship', (ICON_SIZE, ICON_SIZE))

        # Gets the image for the heart (aww!)
        heart_img = assets.open_image(HEART_IMG)

        # Creates the ultra-wide canvas
        together_canvas = Image.new('RGBA', (ICON_SIZE * 3, ICON_SIZE))

        # Pastes the images onto the canvas in order
        together_canvas.paste(partner_1_img, (0, 0))
        together_canvas.paste(heart_img, (ICON_SIZE, 0))
        together_canvas.paste(partner_2_img, (ICON_SIZE * 2, 0))

        # Sends the simple image-based embed.
        # Vary the title based on whether or not this bot is getting shipped.
        await messaging.send_image_based_embed(message, together_canvas, random.choice(
            BASHFUL_MESSAGES if partner_1 == bot.user else NORMAL_MESSAGES).format(
            partner_1.display_name, partner_2.display_name
        ), EMBED_COLOR)

        # Cleanup -- closing Images and deleting them off disk.
        partner_1_img.close()
        partner_2_img.close()
        heart_img.close()
        together_canvas.close()

        # Retire the profile pictures.
        temp_files.retire_profile_picture_by_user(partner_1, message, 'ship')
        temp_files.retire_profile_picture_by_user(partner_2, message, 'ship')

    # On CannotAccessUserlistError, log an error and send an apology message.
    except CannotAccessUserlistError:
        logging.error(message, 'requested ship, failed to access the userlist')
        return await messaging.send_text_message(message, 'There was an error accessing the userlist. Try again later.')


# Command values
PUBLIC_COMMAND_DICT = {
    'ship': ship,
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'ship',
        'category': 'fun_simple',
        'description': 'Ships two users together.',
        'examples': [('ship', 'Creates a ship with two random users.'),
                     ('ship @dummy#0000', 'Creates a ship with the user @dummy#0000 as one of the partners.'),
                     ('ship dummy', "Creates a ship with the user with the name closest to 'dummy' as one of the partners.")],
        'usages': ['ship', 'ship < user >'],
        'restrictions': ["Can't be used in DMs.", "Can't be used in servers with only 1 user."]
    }
]

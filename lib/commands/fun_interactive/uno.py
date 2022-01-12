"""
Uno command.
Recreates the Mattel Game UNO inside the bot.
Mattel, pls don't sue.
"""
# Local Imports
from lib.util import arguments, assets, discord_info, environment, graphics, messaging, misc, parsing, tasks, temp_files
from lib.util.exceptions import CannotAccessUserlistError, InvalidHungerGamesPhaseError, NoUserSpecifiedError, \
    UnableToFindUserError
from lib.commands import fun_interactive as game_manager
from lib.util.logger import BotLogger as logging
from lib.bot import GLOBAL_PREFIX

# Package Imports
from PIL import Image, ImageOps, ImageDraw
from datetime import datetime
import discord
import random
import math
import os


# Keeps track of current games.
CURRENT_GAMES = {}

# Game generation
MAX_GAMESIZE = 10
MIN_GAMESIZE = 2
DEFAULT_GAMESIZE = 10

# Embeds.
EMBED_COLOR = (203 << 16) + (1 << 8)

# Graphics data.
LOBBY_WIDTH = 900
CARD_IMAGE_SIZE = (192, 290)
CARD_IMAGE_TYPE = '.png'

# Lobby
LOBBY_TITLE = 'Who\'s up for a game of UNO?'
LOBBY_BACKGROUND_IMAGE = 'cards/backgrounds/uno_lobby.png'
LOBBY_FAILSAFE_BACKGROUND = (203, 1, 0)
# Lobby LOGO
LOBBY_LOGO_IMAGE = 'cards/uno/logo.png'
LOBBY_LOGO_POSITION = (140, 100)
LOBBY_LOGO_SCALE = 0.5
LOBBY_LOGO_DROP_SHADOW_ALPHA = 200
LOBBY_LOGO_DROP_SHADOW_DISTANCE = 20
# Lobby CARDS
LOBBY_CARD_COLOR_DEFAULT = 'blank'
LOBBY_CARD_COLORS = ['red', 'blue', 'green', 'yellow']
LOBBY_CARD_BACKGROUND_COLORS = [(255, 23, 23), (23, 23, 255), (23, 105, 23), (255, 105, 0)]
LOBBY_CARD_PFP_SIZE = (151, 151)
LOBBY_CARD_PFP_OFFSET = (21, 70)
LOBBY_CARD_DIRECTORY = 'cards/uno/lobby'
LOBBY_CARD_SCALE = 0.7

# Cards.
CARDS = [
    0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 14, 14, 15, 15, 16, 16, 17, 17,
    18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 23, 24, 24, 25, 25, 26, 27, 27, 28, 28, 29, 29, 30, 30, 31, 31, 32, 32,
    33, 33, 34, 34, 35, 35, 36, 36, 37, 37, 38, 38, 39, 40, 40, 41, 41, 42, 42, 43, 43, 44, 44, 45, 45, 46, 46, 47, 47,
    48, 48, 49, 49, 50, 50, 51, 51, 52, 52, 52, 52, 57, 57, 57, 57
]
CARD_DATA = [
    ('red_0', 'Red 0', 0, 0), ('red_1', 'Red 1', 0, 1), ('red_2', 'Red 2', 0, 2), ('red_3', 'Red 3', 0, 3),
    ('red_4', 'Red 4', 0, 4), ('red_5', 'Red 5', 0, 5), ('red_6', 'Red 6', 0, 6), ('red_7', 'Red 7', 0, 7),
    ('red_8', 'Red 8', 0, 8), ('red_9', 'Red 9', 0, 9),
    ('red_reverse', 'Red Reverse', 0, 10), ('red_skip', 'Red Skip', 0, 11), ('red_draw2', 'Red Draw 2', 0, 12),
    ('blue_0', 'Blue 0', 1, 0), ('blue_1', 'Blue 1', 1, 1), ('blue_2', 'Blue 2', 1, 2), ('blue_3', 'Blue 3', 1, 3),
    ('blue_4', 'Blue 4', 1, 4), ('blue_5', 'Blue 5', 1, 5), ('blue_6', 'Blue 6', 1, 6), ('blue_7', 'Blue 7', 1, 7),
    ('blue_8', 'Blue 8', 1, 8), ('blue_9', 'Blue 9', 1, 9), ('blue_reverse', 'Blue Reverse', 1, 10),
    ('blue_skip', 'Blue Skip', 2, 11), ('blue_draw2', 'Blue Draw 2', 2, 12),
    ('green_0', 'Green 0', 2, 0), ('green_1', 'Green 1', 2, 1), ('green_2', 'Green 2', 2, 2),
    ('green_3', 'Green 3', 2, 3), ('green_4', 'Green 4', 2, 4), ('green_5', 'Green 5', 2, 5),
    ('green_6', 'Green 6', 2, 6), ('green_7', 'Green 7', 2, 7), ('green_8', 'Green 8', 2, 8),
    ('green_9', 'Green 9', 2, 9), ('green_reverse', 'Green Reverse', 2, 10), ('green_skip', 'Green Skip', 2, 11),
    ('green_draw2', 'Green Draw 2', 2, 12),
    ('yellow_0', 'Yellow 0', 3, 0), ('yellow_1', 'Yellow 1', 3, 1), ('yellow_2', 'Yellow 2', 3, 2),
    ('yellow_3', 'Yellow 3', 3, 3), ('yellow_4', 'Yellow 4', 3, 4), ('yellow_5', 'Yellow 5', 3, 5),
    ('yellow_6', 'Yellow 6', 3, 6), ('yellow_7', 'Yellow 7', 3, 7), ('yellow_8', 'Yellow 8', 3, 8),
    ('yellow_9', 'Yellow 9', 3, 9), ('yellow_reverse', 'Yellow Reverse', 3, 10), ('yellow_skip', 'Yellow Skip', 3, 11),
    ('yellow_draw2', 'Yellow Draw 2', 3, 12),
    ('wild', 'Wild Card', 4, 13), ('wild_red', 'Wild Card (Red)', 0, 13), ('wild_blue', 'Wild Card (Blue)', 1, 13),
    ('wild_green', 'Wild Card (Green)', 2, 13), ('wild_yellow', 'Wild Card (Yellow)', 3, 13),
    ('wild_draw4', 'Wild Draw 4', 4, 14), ('wild_red_draw4', 'Wild Draw 4 (Red)', 0, 14),
    ('wild_blue_draw4', 'Wild Draw 4 (Blue)', 1, 14), ('wild_green_draw4', 'Wild Draw 4 (Green)', 2, 14),
    ('wild_yellow_draw4', 'Wild Draw 4 (Yellow)', 3, 14),
]
REVERSE_CARDS = [10, 23, 36, 49]
SKIP_CARDS = [11, 24, 37, 50]
DRAW2_CARDS = [12, 25, 38, 51]
DRAW4_CARDS = [57, 58, 59, 60, 61]
WILD_CARDS = [52, 53, 54, 55, 56, 57, 58, 59, 60, 61]

# Miscellaneous
ALLOW_DUPLICATE_PLAYERS_IN_GAME = False  # Initialized in initialize method
EXPIRE_CHECK_INTERVAL = 60  # Initialized in initialize method
EXPIRE_SECONDS = 1800  # Initialized in initialize method
BOT = None  # Initialized in initialize method

THING = None


async def uno_start(message, argument):
    """
    Creates an uno game right inside the bot.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Make sure this command isn't being used in a DM.
    if isinstance(message.channel, discord.DMChannel):
        logging.debug(message, 'requested Uno, but in DMs, so invalid')
        return await messaging.send_text_message(message, 'This command cannot be used in DMs.')

    # Gets the hunger games key (channel id).
    uno_key = str(message.channel.id)

    # If a game is already in progress, we perform a host check.
    if uno_key in CURRENT_GAMES:

        # Host is not this user, send the game in progress message.
        if message.author.id != CURRENT_GAMES[uno_key]['host'].id:
            return await game_manager.send_game_in_progress_message(message)

        # Finally, send the pregame again.
        return await send_pregame(message, CURRENT_GAMES[uno_key])

    # If a different game is in progress, send a message saying you can only have one game at a time.
    elif game_manager.channel_in_game(uno_key):
        logging.debug(message, 'requested Uno, but other game active')
        return await game_manager.send_game_in_progress_message(message)

    # Otherwise, we instantiate a game.
    # Gets argument for how many users to start uno with.
    if argument:
        try:
            # Get a number from the argument.
            player_count = int(parsing.normalize_string(argument))
        # If the conversion doesn't work, use the default.
        except ValueError:
            player_count = DEFAULT_GAMESIZE
    # No argument, use the default player count.
    else:
        player_count = DEFAULT_GAMESIZE

    # Generate the uno dict.
    uno_dict = {'past_pregame': False, 'updated': datetime.today(), 'host': message.author, 'players': [message.author],
                'lobby_colors': [random.randint(0, 3)] + [-1 for i in range(player_count - 1)],
                'readies': [False for i in range(player_count)]}
    CURRENT_GAMES[uno_key] = uno_dict

    # Checkout the host's profile picture.
    await temp_files.checkout_profile_picture_by_user_with_typing(message.author, message, 'uno_filehold')

    # Start a task for this game's expiration.
    # tasks.add_task(f'uno_expire_{uno_key}', EXPIRE_CHECK_INTERVAL, 0, uno_detect_expiration, uno_key)

    # Send the pregame image.
    await send_pregame(message, uno_dict)
    logging.debug(message, f'started Uno instance')


async def send_pregame(message, uno_dict, title=LOBBY_TITLE):
    """
    Sends the pregame lobby thing.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        uno_dict (dict) : The full game dict.
        title (str) : The title of the embed, if any.
    """
    # Generate the player statuses image.
    image = makeimage_lobby(uno_dict)

    # Sends image, logs.
    await messaging.send_image_based_embed(message, image, title, EMBED_COLOR,
                                           description=f"Hosted by {uno_dict['host'].display_name}")


def makeimage_lobby(uno_dict):
    """
    Generates the lobby image.

    Arguments:
        uno_dict (dict) : The full game dict.

    Returns:
        PIL.Image.Image : The finalized image.
    """
    # Make the lobby image.
    lobby_image = Image.new('RGBA', (900, 600), LOBBY_FAILSAFE_BACKGROUND)

    # Get the lobby background image and paste it onto the lobby image.
    lobby_background = assets.open_image(LOBBY_BACKGROUND_IMAGE)
    lobby_image.paste(lobby_background, (0, int((600 - lobby_background.size[1]) / 2)))

    # Make the card images.
    card_images = [
        makeimage_lobby_card(uno_dict['players'][i], (i + 1) % 10, uno_dict['lobby_colors'][i])
        for i in range(len(uno_dict['players']))
    ] + [makeimage_lobby_card(None, (i + 1) % 10, 0) for i in range(len(uno_dict['players']), MAX_GAMESIZE)]

    # Resize the card images.
    for i in range(len(card_images)):
        card_images[i] = graphics.resize(card_images[i], factor=LOBBY_CARD_SCALE)

    # Make the fan from the card images.
    makeimage_card_fan(lobby_image, card_images[:int(MAX_GAMESIZE / 2)], (450, 200), 800, 50, 50)
    makeimage_card_fan(lobby_image, card_images[int(MAX_GAMESIZE / 2):], (450, 300), 800, 50, 50)

    # Get the logo image and paste it onto the lobby image.
    logo = graphics.resize(
        graphics.drop_shadow(assets.open_image(LOBBY_LOGO_IMAGE), alpha=LOBBY_LOGO_DROP_SHADOW_ALPHA,
                             distance=LOBBY_LOGO_DROP_SHADOW_DISTANCE),
        factor=LOBBY_LOGO_SCALE
    )
    graphics.transparency_paste(lobby_image, logo, LOBBY_LOGO_POSITION, centered=True)

    # Return the lobby image.
    return lobby_image


def makeimage_lobby_card(player, card_index, card_color):
    """
    Generates a lobby card for the given player and returns it.
    If the player is None, then a blank one is generated instead.

    Args:
        player (discord.User) : The player object that the card is for.
                                CAN be None.
        card_index (int) : The index of the card.
                           Must be between 0 and 9, inclusive.
        card_color (int) : The color of the card.
                           Must be between 0 and 3, inclusive.

    Returns:
        PIL.Image.Image : The finalized image.
    """
    # If there's no player, then just return the blank one.
    if not player:
        return assets.open_image(
            os.path.join(LOBBY_CARD_DIRECTORY, f'{card_index}_{LOBBY_CARD_COLOR_DEFAULT}{CARD_IMAGE_TYPE}'))

    # Create a new image to use as the base for the card image.
    player_card = Image.new('RGBA', CARD_IMAGE_SIZE)

    # Draw a colored rectangle according to the card color where the profile picture is going.
    card_drawer = ImageDraw.Draw(player_card)
    card_drawer.rectangle((
        LOBBY_CARD_PFP_OFFSET[0], LOBBY_CARD_PFP_OFFSET[1],
        LOBBY_CARD_PFP_OFFSET[0] + LOBBY_CARD_PFP_SIZE[0], LOBBY_CARD_PFP_OFFSET[1] + LOBBY_CARD_PFP_SIZE[1]),
        LOBBY_CARD_BACKGROUND_COLORS[card_color]
    )

    # Put the profile picture there.
    graphics.transparency_paste(player_card, temp_files.get_profile_picture_by_user(player, size=LOBBY_CARD_PFP_SIZE),
                                LOBBY_CARD_PFP_OFFSET)

    # Paste the card image on top.
    graphics.transparency_paste(player_card, assets.open_image(
        os.path.join(LOBBY_CARD_DIRECTORY, f'{card_index}_{LOBBY_CARD_COLORS[card_color]}{CARD_IMAGE_TYPE}')
    ), (0, 0))

    # Return.
    return player_card


def makeimage_card_fan(base_image, cards, northmost_point, radius, max_card_distance, max_card_span):
    """
    Makes a card fan and posts it onto the image.

    Arguments:
        base_image (PIL.Image.Image) : The base image to draw the card fan onto.
        cards (str[] | PIL.Image.Image[]) : A list of either strings or images.
        northmost_point (int, int) : The northmost point of the card arc.
                                     If there are an odd number of cards, then the median card will be centered here.
        radius (float) : How big the arc is.
        max_card_distance (float) : The maximum distance between cards, in degrees.
        max_card_span (float) : The maximum angle cards occupy on the curve before they start getting smushed together.
    """
    # Calculate the center of the circle, the angle between each card, and the starting angle (angle most to the right).
    arc_center = northmost_point[0], northmost_point[1] + radius
    angle_difference = min(max_card_distance, max_card_span / len(cards))
    current_card_angle = (len(cards) - 1) * angle_difference / 2

    # Iterate through each card.
    for card in cards:

        # Rotate the card.
        card = graphics.rotate(card, -current_card_angle)

        # Get the card's angle as radians.
        current_card_angle_rad = math.radians(current_card_angle)

        # Draw the card.
        graphics.transparency_paste(
            base_image, card, (
                arc_center[0] - math.sin(current_card_angle_rad) * radius,
                arc_center[1] - math.cos(current_card_angle_rad) * radius
            ), centered=True)

        # Subtract from the current_card_angle.
        current_card_angle -= angle_difference


def initialize(bot):
    """
    Initializes the command.
    In this case, uses environment variables to set default values.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
    """
    # Log.
    import logging
    logging.debug('Initializing fun_interactive.uno...')

    # Add this game's game dict to the game dicts from fun_interactive.
    game_manager.GAME_DICTS.append(CURRENT_GAMES)

    # Sets some global variables using environment.get
    global ALLOW_DUPLICATE_PLAYERS_IN_GAME, EXPIRE_CHECK_INTERVAL, EXPIRE_SECONDS, BOT
    ALLOW_DUPLICATE_PLAYERS_IN_GAME = environment.get('UNO_ALLOW_DUPLICATE_PLAYERS_IN_GAME')
    EXPIRE_CHECK_INTERVAL = environment.get('UNO_EXPIRE_CHECK_INTERVAL')
    EXPIRE_SECONDS = environment.get('UNO_EXPIRE_SECONDS')
    BOT = bot


DEVELOPER_COMMAND_DICT = {
    'uno': uno_start
}

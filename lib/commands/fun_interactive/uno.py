"""
Uno command.
Recreates the Mattel Game UNO inside the bot.
Mattel, pls don't sue.
"""
# Local Imports
from lib.util import assets, environment, graphics, messaging, misc, parsing, tasks, temp_files
from lib.util.discord_info import LightweightUser, IdWrapperList
from lib.commands import fun_interactive as game_manager
from lib.util.logger import BotLogger as logging

# Package Imports
from discord.ui import View, Button, Select
from PIL import Image, ImageDraw
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
LOBBY_LOGO_POSITION = (119, 90)
LOBBY_LOGO_SCALE = 0.4
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
LOBBY_CARD_NAME_FONT = 'urw_grotesk_extra_narrow_medium.ttf'
LOBBY_CARD_NAME_FONT_SIZE = 37
LOBBY_CARD_NAME_BORDERS = [
    (64, 170), (47, 170), (64, 170), (64, 170), (64, 170), (62, 170), (64, 170), (64, 170), (64, 170), (64, 170)
]
LOBBY_CARD_NAME_Y = 21
LOBBY_CARD_READY_FONT = 'urw_grotesk_extra_narrow_medium.ttf'
LOBBY_CARD_READY_FONT_SIZE = 20
LOBBY_CARD_READY_BORDERS = [
    (65, 171), (48, 171), (65, 171), (65, 171), (65, 171), (63, 171), (65, 171), (65, 171), (65, 171), (65, 171)
]
LOBBY_CARD_READY_Y = 56
LOBBY_CARD_ROW_WIDTHS = [5, 5, 5, 5, 5, 5, 4, 4, 4, 5, 5]

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
DISABLE_OLD_VIEW_ON_REFRESH = True  # Initialized in initialize method
BUTTONS_TIMEOUT_SECONDS = 1800  # Initialized in initialize method
EXPIRE_CHECK_INTERVAL = 60  # Initialized in initialize method
EXPIRE_SECONDS = 1200  # Initialized in initialize method
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
        return await send_pregame(message, uno_key, CURRENT_GAMES[uno_key])

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
    author = LightweightUser(message.author)
    uno_dict = {'past_pregame': False, 'updated': datetime.today(), 'host': author, 'players': IdWrapperList([author]),
                'lobby_colors': fix_lobby_colors([random.randint(0, 3) for i in range(MAX_GAMESIZE)], player_count),
                'readies': [False for i in range(MAX_GAMESIZE)], 'max_players': player_count}
    CURRENT_GAMES[uno_key] = uno_dict

    # Checkout the host's profile picture.
    await temp_files.checkout_profile_picture_by_user_with_typing(message.author, message, 'uno_filehold')

    # Start a task for this game's expiration.
    # tasks.add_task(f'uno_expire_{uno_key}', EXPIRE_CHECK_INTERVAL, 0, uno_detect_expiration, uno_key)

    # Send the pregame image.
    await send_pregame(message, uno_key, uno_dict)
    logging.debug(message, f'started Uno instance')


async def send_pregame(message, uno_key, uno_dict):
    """
    Sends the pregame lobby thing.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        uno_key (str) : The key the game is keyed under.
        uno_dict (dict) : The full game dict.
    """
    # Generate the player statuses image.
    image = makeimage_lobby(uno_dict)

    # Make a lobby view.
    lobby_view = LobbyView(uno_key, uno_dict)

    # Sends image, logs.
    await messaging.send_local_image_based_embed(message, image, LOBBY_TITLE, EMBED_COLOR,
                                                 description=f"Hosted by {uno_dict['host'].display_name}",
                                                 view=lobby_view, hosted_online=True)

    # If the view already exists in this dict, then do something about it.
    if 'lobby_views' in uno_dict:
        if DISABLE_OLD_VIEW_ON_REFRESH:
            uno_dict['lobby_views'][0].stop()
        else:
            return uno_dict['lobby_views'].append(lobby_view)

    # Store the lobby view.
    uno_dict['lobby_views'] = [lobby_view]


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
        makeimage_lobby_card((i + 1) % 10, player, color, ready) for i, (player, color, ready) in
        enumerate(zip(uno_dict['players'], uno_dict['lobby_colors'], uno_dict['readies']))
    ] + [
        makeimage_lobby_card((i + 1) % 10) for i in
        range(len(uno_dict['players']), uno_dict['max_players'])
    ]

    # Resize the card images.
    for i, card_image in enumerate(card_images):
        card_images[i] = graphics.resize(card_image, factor=LOBBY_CARD_SCALE)

    # Sort the card images into one or more rows.
    card_images_row1, card_images_row2 = card_images[:LOBBY_CARD_ROW_WIDTHS[uno_dict['max_players']]], None
    if len(card_images) != len(card_images_row1):
        card_images_row2 = card_images[LOBBY_CARD_ROW_WIDTHS[uno_dict['max_players']]:]

    # Make the fan from the card images on a new image.
    card_image = Image.new('RGBA', (900, 600), (0, 0, 0, 0))
    makeimage_card_fan(card_image, card_images_row1, (445, 210), 990, 7, 50, reverse=True)
    if card_images_row2:
        makeimage_card_fan(card_image, card_images_row2, (455, 390), 1100, 6.5, 50, reverse=True)

    # Draw a shadow on the card_image.
    card_image = graphics.drop_shadow(card_image, alpha=127, distance=LOBBY_LOGO_DROP_SHADOW_DISTANCE)

    # Paste the card image on.
    graphics.transparency_paste(lobby_image, card_image, (450, 300), centered=True)

    # Get the logo image and paste it onto the lobby image.
    logo = graphics.resize(
        graphics.drop_shadow(assets.open_image(LOBBY_LOGO_IMAGE), alpha=LOBBY_LOGO_DROP_SHADOW_ALPHA,
                             distance=LOBBY_LOGO_DROP_SHADOW_DISTANCE),
        factor=LOBBY_LOGO_SCALE
    )
    graphics.transparency_paste(lobby_image, logo, LOBBY_LOGO_POSITION, centered=True)

    # Return the lobby image.
    return lobby_image


def makeimage_lobby_card(card_index, player=None, card_color=0, ready=False):
    """
    Generates a lobby card for the given player and returns it.
    If the player is None, then a blank one is generated instead.

    Args:
        card_index (int) : The index of the card.
                           Must be between 0 and 9, inclusive.
        player (Optional[discord.User]) : The player object that the card is for.
                                          If None, then the card will be returned as a blank one.
                                          Defaults to None.
        card_color (int) : The color of the card.
                           Must be between 0 and 3, inclusive, unless the player is None.
                           Defaults to 0.
        ready (bool) : Whether the player is ready or not.
                       Defaults to False.

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

    # Write the user text and their 'ready' label, if they are ready.
    graphics.text_in_boundaries(player_card, assets.open_font(LOBBY_CARD_NAME_FONT, LOBBY_CARD_NAME_FONT_SIZE),
                                parsing.normalize_string(player.display_name, remove_emojis=True).upper(),
                                LOBBY_CARD_NAME_BORDERS[card_index], LOBBY_CARD_NAME_Y)
    if ready:
        graphics.text_in_boundaries(player_card, assets.open_font(LOBBY_CARD_READY_FONT, LOBBY_CARD_READY_FONT_SIZE),
                                    'READY', LOBBY_CARD_READY_BORDERS[card_index], LOBBY_CARD_READY_Y)

    # Return.
    return player_card


def makeimage_card_fan(base_image, cards, northmost_point, radius, max_card_distance, max_card_span, reverse=False):
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
        reverse (bool) : Whether to reverse the card drawing order (left on top, right on bottom).

    """
    # Calculate the center of the circle, the angle between each card, and the starting angle (angle most to the right).
    arc_center = northmost_point[0], northmost_point[1] + radius
    angle_difference = min(max_card_distance, max_card_span / len(cards))
    current_card_angle = (len(cards) - 1) * angle_difference / 2 * (-1 if reverse else 1)

    # If reverse, reverse the order of the cards.
    if reverse:
        cards.reverse()

    # Iterate through each card.
    for i in range(len(cards)):

        # Draw the card's shadow to the left or right depending on whether we're reversing or not.
        if i > 0:
            cards[i] = graphics.drop_shadow(cards[i], angle=90 if reverse else 270, distance=2, blur_strength=2,
                                            alpha=50)

        # Rotate the card.
        card = graphics.rotate(cards[i], -current_card_angle)

        # Get the card's angle as radians.
        current_card_angle_rad = math.radians(current_card_angle)

        # Draw the card.
        graphics.transparency_paste(
            base_image, card, (
                arc_center[0] - math.sin(current_card_angle_rad) * radius,
                arc_center[1] - math.cos(current_card_angle_rad) * radius
            ), centered=True)

        # Subtract from the current_card_angle.
        current_card_angle -= -angle_difference if reverse else angle_difference


def fix_lobby_colors(current_colors, player_count):
    """
    Fixes the given lobby colors so that the four color theorem applies.

    Arguments:
        current_colors (int[]) : The current color list.
        player_count (int) : The amount of players.

    Returns:
        int[] : The updated color list.
    """
    # Get the card row width, player count evenness, and cards on the bottom first.
    row_width = LOBBY_CARD_ROW_WIDTHS[player_count]
    rows_even = not player_count % 2
    cards_on_bottom = player_count - row_width

    # Create a card offset int to help influence the randomness a little.
    card_offset = random.randint(0, 2)

    # Iterate through, starting with the second card.
    for i, color in enumerate(current_colors):
        if not i:
            continue

        # Get the previous 2 - 3 colors.
        previous_colors = current_colors[max(0, i - 3 + (i + card_offset) % 3):i]

        # If the index is less than the row width, only consider the color to the left.
        if i < row_width:
            if color in previous_colors:
                current_colors[i] = random.choice([j for j in range(4) if j not in previous_colors])

        # If the index is equal to the row width, consider the color(s) directly above it.
        elif i == row_width:
            above_colors = [
                current_colors[int((row_width - cards_on_bottom)/2)]
            ] if rows_even else [
                current_colors[int((row_width - cards_on_bottom)/2)],
                current_colors[int((row_width - cards_on_bottom)/2) + 1]
            ]
            if color in above_colors:
                current_colors[i] = random.choice([j for j in range(4) if j not in above_colors])

        # If the index is above the row width, consider the colors above and to the left of it.
        else:
            neighboring_colors = ([
                current_colors[i - row_width + int((row_width - cards_on_bottom) / 2)],
                current_colors[i - row_width + int((row_width - cards_on_bottom) / 2) - 1]
            ] if rows_even else [
                current_colors[i - row_width + int((row_width - cards_on_bottom) / 2)],
                current_colors[i - row_width + int((row_width - cards_on_bottom) / 2) + 1]
            ]) + [previous_colors[-1]]
            if color in neighboring_colors:
                current_colors[i] = random.choice([j for j in range(4) if j not in neighboring_colors])

    # Return.
    return current_colors


class LobbyView(View):
    """
    The view that is used on the lobby screen.
    """

    def __init__(self, uno_key, uno_dict):
        """
        Initializes the LobbyView.

        Arguments:
            uno_key (str) : The key the game is keyed under.
            uno_dict (dict) : The uno dict for the given game.
        """
        # Initialize the standard view.
        View.__init__(self, timeout=BUTTONS_TIMEOUT_SECONDS)

        # Store the uno key and uno dict.
        self.uno_key = uno_key
        self.uno_dict = uno_dict

        # Create the ready button.
        self.ready_button = Button(label='Ready 0/1', style=discord.ButtonStyle.green)
        self.ready_button.callback = self.ready_callback
        self.add_item(self.ready_button)

        # Create the join button.
        self.join_button = Button(label='Join Game', style=discord.ButtonStyle.blurple)
        self.join_button.callback = self.join_callback
        self.add_item(self.join_button)

        # Create the leave button.
        self.leave_button = Button(label='Leave Game', style=discord.ButtonStyle.blurple)
        self.leave_button.callback = self.leave_callback
        self.add_item(self.leave_button)

        # Create the options button.
        self.options_button = Button(label='Options', style=discord.ButtonStyle.gray)
        self.options_button.callback = self.options_callback
        self.add_item(self.options_button)

        # Create the ready button.
        self.cancel_button = Button(label='Cancel', style=discord.ButtonStyle.red)
        self.cancel_button.callback = self.cancel_callback
        self.add_item(self.cancel_button)


    async def ready_callback(self, interaction):
        """
        The method that gets called when the 'ready' button is pushed.

        Args:
            interaction (discord.interactions.Interaction) : The interaction that triggered this method.
        """
        print(self.uno_dict)


    async def join_callback(self, interaction):
        """
        The method that gets called when the 'join' button is pushed.
        Adds the player to the game if they are not already in it OR duplicate players are allowed.
        Otherwise, sends an epheremal message back.

        Args:
            interaction (discord.interactions.Interaction) : The interaction that triggered this method.
        """
        # First, gather the user who triggered this callback.
        user = interaction.user

        # See if the user is already in the uno dict's player list. If so, send a message back.
        if any([user.id == player.id for player in self.uno_dict['players']]) and not ALLOW_DUPLICATE_PLAYERS_IN_GAME:
            logging.debug(interaction.message, 'tried to join Uno game they are already in')
            return await messaging.send_text_message_from_interaction(interaction, 'You are already in this game.')

        # See if we've already hit the maximum players.
        if len(self.uno_dict['players']) >= self.uno_dict['max_players']:
            logging.debug(interaction.message, 'tried to join Uno game with maxed out players')
            return await messaging.send_text_message_from_interaction(interaction, 'This game is full.')

        # Add the player and checkout their profile picture.
        self.uno_dict['players'].append(LightweightUser(user))
        temp_files.checkout_profile_picture_by_user(user, interaction.message, 'uno_filehold')

        # Generate the player statuses image.
        image = makeimage_lobby(self.uno_dict)

        # Edit the message before.
        logging.debug(interaction.message, f'joined Uno game as player {len(self.uno_dict["players"])}')
        await messaging.edit_local_image_based_embed_from_interaction(
            interaction, image, LOBBY_TITLE, EMBED_COLOR, description=f"Hosted by {self.uno_dict['host'].display_name}",
            footer=f'{user.display_name} has joined the game.', view=self
        )

        # Change the 'updated' thing.
        self.uno_dict['updated'] = datetime.today()


    async def leave_callback(self, interaction):
        """
        The method that gets called when the 'leave' button is pushed.

        Args:
            interaction (discord.interactions.Interaction) : The interaction that triggered this method.
        """
        # First, gather the user who triggered this callback.
        user = interaction.user

        # See if the user is in this uno dict's player list. If not, send a message back.
        if not any([user.id == player.id for player in self.uno_dict['players']]):
            logging.debug(interaction.message, 'tried to leave Uno game they werent even in')
            return await messaging.send_text_message_from_interaction(interaction, "You already aren't in this game.")

        # First, get their index(es) and reverse list.
        user_indexes = misc.get_multi_index(self.uno_dict['players'], user)
        user_indexes.reverse()

        # If the user is the host, remove their last (first?) index from the list.
        if user == self.uno_dict['host']:
            del user_indexes[-1]

        # If there are user indexes, this means the user wasn't the host (or has more than one foot in the door).
        if user_indexes:

            # Next, delete the indexes in both the player list and the ready list, and replace them if needed.
            for index in user_indexes:
                del self.uno_dict['players'][index]
                del self.uno_dict['readies'][index]
                self.uno_dict['readies'].append(False)

            # Retire the user's profile picture.
            temp_files.retire_profile_picture_by_user(user, interaction.message, 'uno_filehold')

            # Generate the player statuses image.
            image = makeimage_lobby(self.uno_dict)

            # Edit the message before.
            logging.debug(interaction.message, 'left Uno game')
            await messaging.edit_local_image_based_embed_from_interaction(
                interaction, image, LOBBY_TITLE, EMBED_COLOR,
                description=f"Hosted by {self.uno_dict['host'].display_name}",
                footer=f'{user.display_name} has left the game.', view=self
            )

        # If the user IS the host, they aren't allowed to leave.
        else:
            logging.debug(interaction.message, 'tried to leave Uno game, but as the host')
            return await messaging.send_text_message_from_interaction(
                interaction, "You can't leave this game since you're the host.\n"
                             "You can transfer host in the options menu or cancel."
            )


    async def options_callback(self, interaction):
        """
        The method that gets called when the 'options' button is pushed.

        Args:
            interaction (discord.interactions.Interaction) : The interaction that triggered this method.
        """
        print(self.uno_dict)


    async def cancel_callback(self, interaction):
        """
        The method that gets called when the 'cancel' button is pushed.

        Args:
            interaction (discord.interactions.Interaction) : The interaction that triggered this method.
        """
        # First, gather the user who triggered this callback.
        user = interaction.user

        # If the user is the host, cancel.
        if self.uno_dict['host'] == user:

            # Delete the dict from CURRENT_GAMES.
            del CURRENT_GAMES[self.uno_key]

            # Send a message.
            logging.debug(interaction.message, 'canceled uno game')
            await messaging.send_text_message_from_interaction(interaction, "Uno game canceled.",
                                                                      ephemeral=False)

            # Retire all profile pictures.
            temp_files.retire_profile_picture_by_user_bulk(self.uno_dict['players'], interaction.message,
                                                           'uno_filehold')

            # Terminate the view.
            return self.stop()

        # The user is not the host, tell them only the host can do that.
        logging.debug(interaction.message, 'tried to cancel uno game when not host')
        await messaging.send_text_message_from_interaction(interaction, "Only the host can do that.")


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
    global ALLOW_DUPLICATE_PLAYERS_IN_GAME, DISABLE_OLD_VIEW_ON_REFRESH, BUTTONS_TIMEOUT_SECONDS, \
        EXPIRE_CHECK_INTERVAL, EXPIRE_SECONDS, BOT
    ALLOW_DUPLICATE_PLAYERS_IN_GAME = environment.get('UNO_ALLOW_DUPLICATE_PLAYERS_IN_GAME')
    EXPIRE_CHECK_INTERVAL = environment.get('UNO_EXPIRE_CHECK_INTERVAL')
    EXPIRE_SECONDS = environment.get('UNO_EXPIRE_SECONDS')
    BOT = bot


DEVELOPER_COMMAND_DICT = {
    'uno': uno_start
}

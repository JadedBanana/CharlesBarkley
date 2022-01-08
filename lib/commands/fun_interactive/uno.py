"""
Uno command.
Recreates the Mattel Game UNO inside the bot.
Mattel, pls don't sue.
"""
# Local Imports
from lib.util.exceptions import CannotAccessUserlistError, InvalidHungerGamesPhaseError, NoUserSpecifiedError, \
    UnableToFindUserError
from lib.util import arguments, assets, database, discord_info, environment, messaging, misc, parsing, temp_files
from lib.commands import fun_interactive as game_manager
from lib.util.logger import BotLogger as logging
from lib.bot import GLOBAL_PREFIX

# Package Imports
from PIL import Image, ImageOps, ImageDraw
from datetime import datetime
import discord
import random


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

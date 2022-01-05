"""
Fun_interactive module.
Essentially acts as a game manager to prevent more than one from running at the same time.
"""
# Local Imports
from lib.util import messaging


# Store the game dicts.
GAME_DICTS = []


def channel_in_game(channel_id):
    """
    Returns whether the channel is in a game or not.

    Arguments:
        channel_id (str) : The (string) channel id.

    Returns:
        bool : Whether the channel is in a game in GAME_DICTS.
    """
    return any(channel_id in game_dict for game_dict in GAME_DICTS)


def send_game_in_progress_message(message):
    """
    Sends a text message back to the channel the trigger message came from notifying them that a game is already in
    progress.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered the command.
    """
    # Simply send the message.
    await messaging.send_text_message(message, 'There is already a game active in this channel.')

"""
Hunger Games command.
Essentially a BrantSteele simulator simulator.
"""
# Local Imports
from lib.util.exceptions import CannotAccessUserlistError, InvalidHungerGamesPhaseError, NoUserSpecifiedError, \
    UnableToFindUserError
from lib.util import arguments, assets, database, discord_info, environment, messaging, misc, parsing, temp_files
from lib.util.logger import BotLogger as logging
from lib.bot import GLOBAL_PREFIX

# Package Imports
from PIL import Image, ImageOps, ImageDraw
from datetime import datetime
import discord
import random


# Keeps track of current games.
CURRENT_GAMES = {}


# Hunger Games constants.
# Game generation
HG_MAX_GAMESIZE = 64
HG_MIN_GAMESIZE = 2
HG_DEFAULT_GAMESIZE = 24

# Embeds.
HG_EMBED_COLOR = (251 << 16) + (130 << 8)

# Image drawing.
HG_FONT_SIZE = 16
HG_FONT = 'arial_bold.ttf'
HG_TEXT_BUFFER = 6
HG_ICON_BUFFER = 25
HG_ICON_SIZE = 128
HG_BACKGROUND_COLOR = (93, 80, 80)

# Playerstatus embed.
HG_PLAYERSTATUS_WIDTHS = [0, 1, 2, 3, 4, 3, 3, 4, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7,
                          7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
HG_PLAYERSTATUS_ROWHEIGHT = 172
HG_PLAYERSTATUS_DEAD_PFP_DARKEN_FACTOR = 0.65
HG_STATUS_ALIVE_COLOR = (0, 255, 0)
HG_STATUS_DEAD_COLOR = (255, 102, 102)

# Action embed.
HG_ACTION_ROWHEIGHT = 175
HG_HEADER_BORDER_BUFFER = 7
HG_HEADER_TEXT_COLOR = (255, 207, 39)
HG_ACTION_PLAYER_COLOR = (251, 130, 0)
HG_HEADER_BORDER_COLOR = (255, 255, 255)
HG_HEADER_BACKGROUND_COLOR = (35, 35, 35)

# Pregame
HG_PREGAME_TITLE = 'The Reaping'
HG_PREGAME_DESCRIPTION = 'Respond one of the following:\n' \
                         'A: Add\t\t\tD: Delete\n' \
                         'S: Shuffle\t\tB: {} bots\n' \
                         'P: Proceed\t\tC: Cancel'
HG_PREGAME_ADD_TERMS = ['a', 'add']
HG_PREGAME_DELETE_TERMS = ['d', 'del', 'delete']
HG_PREGAME_TOGGLE_BOTS_TERMS = ['b', 'bot', 'bots']
HG_PREGAME_PROCEED_TERMS = ['p', 'proceed']
HG_PREGAME_CANCEL_TERMS = ['c', 'cancel']

# Midgame
HG_BEGINNING_DESCRIPTION = 'Respond one of the following:\nN: Next Action\nC: Cancel Game'
HG_MIDGAME_DESCRIPTION = 'Respond one of the following:\nN: Next Action\tP: Previous Action\nC: Cancel Game'
HG_POSTGAME_BEGINNING_DESCRIPTION = 'Respond one of the following:\nN: Next Action\n' \
                                    'R: Replay (same cast)\tS: New Game\tC: Close'
HG_POSTGAME_MIDGAME_DESCRIPTION = 'Respond one of the following:\n' \
                                  'N: Next Action\tP: Previous Action\n' \
                                  'R: Replay (same cast)\tS: New Game\tC: Close'
HG_THE_END_DESCRIPTION = 'The end! Respond one of the following:\n' \
                         'N: Next Action\tP: Previous Action\n' \
                         'R: Replay (same cast)\tS: New Game\tC: Close'
HG_FINALE_DESCRIPTION = 'Respond one of the following:\n' \
                        'P: Previous Action\n' \
                        'R: Replay (same cast)\tS: New Game\tC: Close'
HG_MIDGAME_CANCEL_TERMS = ['c', 'cancel']
HG_MIDGAME_CANCEL_CONFIRM_TERMS = ['y', 'yes']
HG_MIDGAME_CANCEL_CANCEL_TERMS = ['n', 'no']
HG_MIDGAME_NEXT_TERMS = ['n', 'next', 'proceed']
HG_MIDGAME_PREVIOUS_TERMS = ['p', 'prev', 'previous']

# Postgame
HG_POSTGAME_REPLAY_TERMS = ['r', 'replay']

# Winner / Ties
HG_COMPLETE_PHASE_TYPES = ['win', 'tie']

# Item List
# # =================SPECIAL==================
# # 0: nothing
# # 3000: 1 - 3 random items
# # 4000: 1 weapon, 1 food item, 1 health item
# # 8888: make net from rope, give food
# # 9999: take away everything and give it to everyone else
# # ================WEAPONS================
# # 1: mace
# # 2: sword
# # 3: spear
# # 4: explosives
# # 5: throwing knives
# # 6: hatchet
# # 7: slingshot
# # 8: rope
# # 9: shovel
# # 10: net
# # 11: molotov cocktail
# # 12: bow
# # 13: poison
# # 14: scissors
# # ==================FOOD=================
# # 101: clean water
# # 102: river water
# # 103: loaf of bread
# # 104: raw meat
# # =================HEALTH================
# # 201: bandages
# # 202: medicine
# # 203: first aid kit
# # ==================OTHER================
# # 301: shack
# # 302: camouflage
# # 303: cave
# # 304: high ground
# # 305: spike trap in the forest
# # 306: naked
HG_WEAPON_ITEMS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
HG_FOOD_ITEMS = [101, 102, 103, 104]
HG_HEALTH_ITEMS = [201, 202, 203]
HG_ALL_ITEMS = HG_WEAPON_ITEMS + HG_FOOD_ITEMS + HG_HEALTH_ITEMS

# Other Generation Stuff
HG_EVENT_DEFAULT_CHANCE = 0.2
HG_EVENT_DAYNIGHT_MINIMUM = 4

# Miscellaneous
NTH_SUFFIXES = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']
EXPIRE_SECONDS = None  # Initialized in initialize method


async def hunger_games_start(bot, message, argument):
    """
    Creates a hunger games simulator right inside the bot.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Make sure this command isn't being used in a DM.
    if isinstance(message.channel, discord.DMChannel):
        logging.debug(message, 'requested hunger games, but in DMs, so invalid')
        return await messaging.send_text_message(message, 'This command cannot be used in DMs.')

    # Gets the hunger games key (channel id).
    hg_key = str(message.channel.id)

    # If a game is already in progress, we forward this message to the update function.
    if hg_key in CURRENT_GAMES:
        return await hunger_games_update(bot, message)

    # Otherwise, we instantiate a game.
    # Gets argument for how many users to start hg with.
    if argument:
        try:
            # Get a number from the argument.
            player_count = int(parsing.normalize_string(argument))
        # If the conversion doesn't work, use the default.
        except ValueError:
            player_count = HG_DEFAULT_GAMESIZE
    # No argument, use the default player count.
    else:
        player_count = HG_DEFAULT_GAMESIZE

    # Generate the playerlist.
    hg_dict = {}
    worked = await pregame_shuffle(message, player_count, hg_dict)

    # If it didn't work, return.
    if not worked:
        return

    # Set in the hunger games dict.
    hg_dict['past_pregame'] = False
    hg_dict['updated'] = datetime.today()
    CURRENT_GAMES[hg_key] = hg_dict

    # Send the initial cast
    await send_pregame(message, hg_dict)
    logging.debug(message, f'started Hunger Games instance with {len(hg_dict["players"])} players')


async def hunger_games_update(bot, message):
    """
    Updates the hunger games dict for the message's channel, if it exists.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Gets the key.
    hg_key = str(message.channel.id)

    # Checks to make sure that this is a running game.
    if hg_key not in CURRENT_GAMES:
        return

    # Loads the hg_dict.
    hg_dict = CURRENT_GAMES[hg_key]

    # Splits the response out of the message content and into a list.
    response = parsing.normalize_string(message.content).lower().split(' ')
    if not response:
        return

    # If the game is already generated.
    if hg_dict['past_pregame']:
        await hunger_games_update_midgame(hg_key, hg_dict, response, message)

    # The game is not yet out of pregame, run the pregame method.
    else:
        await hunger_games_update_pregame(hg_key, hg_dict, response, message)

    # Change the 'updated' thing.
    hg_dict['updated'] = datetime.today()


async def hunger_games_detect_expiration(bot, message):
    """
    Detects expired hunger games instances and deletes them.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # If there are no active games, return.
    if not CURRENT_GAMES:
        return

    # Otherwise, get the current time.
    now = datetime.today()

    # Iterate through all the games and see if the seconds exceed the set limit.
    for hg_key, hg_dict in CURRENT_GAMES.items():
        if (now - hg_dict['updated']).seconds >= EXPIRE_SECONDS:

            # Delete it.
            clear_current_game_from_database(hg_dict)
            del CURRENT_GAMES[hg_key]

            # Retire the existing players' profile pictures.
            if 'players' in hg_dict:
                temp_files.retire_profile_picture_by_user_id_bulk(hg_dict['players'], message, 'hg_filehold')

            # Send a message quoting inactivity.
            logging.debug(message, f'Triggered hunger games expiration for channel {hg_key}')
            channel = bot.get_channel(int(hg_key))
            await channel.send('Hunger Games canceled due to inactivity.')

            # Break (the others can get canceled later.)
            return


async def hunger_games_update_pregame(hg_key, hg_dict, response, message):
    """
    Updates the hunger games dict according to how the response is formatted.
    Only triggers during pregame.

    Arguments:
        hg_key (str) : The key for the hunger games dict.
        hg_dict (dict) : The full game dict.
        response (str[]) : A list of strings representing the response.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Shuffle command.
    if any(response[0] == value for value in HG_PREGAME_SHUFFLE_TERMS):
        await hunger_games_update_pregame_shuffle(hg_key, hg_dict, response, message)

    # Add command.
    elif any(response[0] == value for value in HG_PREGAME_ADD_TERMS):
        await hunger_games_update_pregame_add(hg_key, hg_dict, response, message)

    # Delete command.
    elif any(response[0] == value for value in HG_PREGAME_DELETE_TERMS):
        await hunger_games_update_pregame_delete(hg_key, hg_dict, response, message)

    # Proceed command.
    elif any(response[0] == value for value in HG_PREGAME_PROCEED_TERMS):
        await hunger_games_update_pregame_proceed(hg_key, hg_dict, response, message)

    # Cancel command.
    elif any(response[0] == value for value in HG_PREGAME_CANCEL_TERMS):
        await hunger_games_update_cancel_confirm(hg_key, hg_dict, response, message)

    # Toggle Bots command.
    elif any(response[0] == value for value in HG_PREGAME_TOGGLE_BOTS_TERMS):
        await hunger_games_update_pregame_toggle_bots(hg_key, hg_dict, response, message)


async def hunger_games_update_pregame_shuffle(hg_key, hg_dict, response, message):
    """
    Shuffles around the players in the given hunger games dict.

    Arguments:
        hg_key (str) : The key for the hunger games dict.
        hg_dict (dict) : The full game dict.
        response (str[]) : A list of strings representing the response.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # First, see if there's a second argument.
    if len(response) > 1:
        # Attempt to pull a number from that second argument (and parse it so that it's correct).
        try:
            player_count = int(response[1])
        # If that doesn't work, set it to the current length.
        except ValueError:
            player_count = len(hg_dict['players'])

    # If there isn't a second argument, use the current length.
    else:
        player_count = len(hg_dict['players'])

    # Do the pregame shuffle.
    worked = await pregame_shuffle(message, player_count, hg_dict)

    # If it didn't work, return.
    if not worked:
        return

    # Otherwise, send a new embed.
    await send_pregame(message, hg_dict)


async def hunger_games_update_pregame_add(hg_key, hg_dict, response, message):
    """
    Adds a player to the hunger games dict.

    Arguments:
        hg_key (str) : The key for the hunger games dict.
        hg_dict (dict) : The full game dict.
        response (str[]) : A list of strings representing the response.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Cancels if the game is already max size.
    if len(hg_dict['players']) == HG_MAX_GAMESIZE:
        logging.debug(message, 'tried to add player to Hunger Games instance, max size reached')
        return await messaging.send_text_message(message, 'Maximum game size already reached.')

    # Try/catch to catch CannotAccessUserlistError.
    try:

        # First, see if there's a second argument.
        if len(response) > 1:

            # Recreate the original response (full length), and feed it into the get_closest_users thing.
            argument_str = ' '.join(response[1:])
            try:
                closest_players = arguments.get_closest_users(message, argument_str,
                                                              exclude_bots=not hg_dict['uses_bots'])

                # Iterate through the closest users and stop at the first one that's NOT in the game.
                for player in closest_players:
                    if player not in hg_dict['players']:

                        # Add the player into the game.
                        hg_dict['players'].append(player)

                        # Checkout their profile picture.
                        await temp_files.checkout_profile_picture_by_user_with_typing(player, message, 'hg_filehold',
                                                                                      return_image=False)

                        # Log and send message.
                        logging.debug(message, f'added player {player} to Hunger Games instance')
                        return await send_pregame(message, hg_dict, f'Added {player.display_name} to the game.')

                # If we didn't find a player, then send an invalid user thing.
                logging.debug(message, f"attempted to add user '{argument_str}' to hunger games instance, invalid")
                return await messaging.send_text_message(message, f"Could not find user '{argument_str}'.")

            # If no user was specified, then call this method again with only one term in the response.
            except NoUserSpecifiedError:
                return await hunger_games_update_pregame_add(hg_key, hg_dict, [response[0]], message)

            # If no user could be found, then send back old reliable.
            except UnableToFindUserError:
                logging.debug(message, f"attempted to add user '{argument_str}' to hunger games instance, invalid")
                return await messaging.send_text_message(message, f"Could not find user '{argument_str}'.")

        # If there isn't a second argument, attempt to get a completely random player.
        # First, try it without bots.
        if not hg_dict['uses_bots']:

            # Get the user list.
            user_list = discord_info.get_applicable_users(message, exclude_bots=True, exclude_users=hg_dict['players'])

            # If the user list is empty, send an appropriate message back depending on whether there are bots available.
            if not user_list:
                user_list_with_bots = discord_info.get_applicable_users(message, exclude_bots=False,
                                                                        exclude_users=hg_dict['players'])
                if user_list_with_bots:
                    logging.debug(message, 'attempted to add random user to hunger games instance, '
                                          'no non-bot users available')
                    return await messaging.send_text_message(message,
                                                             "Every user who isn't a bot is already in the game.")
                else:
                    logging.debug(message, 'attempted to add random user to hunger games instance, '
                                          'no more users available')
                    return await messaging.send_text_message(message,
                                                             "Every user in the server is already in the game.")

        # Next, try it with bots.
        else:

            # Get the user list.
            user_list = discord_info.get_applicable_users(message, exclude_bots=False, exclude_users=hg_dict['players'])

            # If the user list is empty, then tell the users that.
            if not user_list:
                logging.debug(message, 'attempted to add random user to hunger games instance, no more users available')
                return await messaging.send_text_message(message, "Every user in the server is already in the game.")

        # With the user list, grab a random user.
        added_user = random.choice(user_list)
        hg_dict['players'].append(added_user)

        # Checkout the added user.
        await temp_files.checkout_profile_picture_by_user_with_typing(added_user, message, 'hg_filehold',
                                                                      return_image=False)

        # Send the message and junk.
        logging.debug(message, f'added player {added_user} to Hunger Games instance')
        await send_pregame(message, hg_dict, f'Added {added_user.display_name} to the game.')

    # If we can't access the userlist, send an error.
    except CannotAccessUserlistError:
        logging.error(message, 'requested add random player to hunger games, failed to access the userlist')
        return await messaging.send_text_message(message, 'There was an error accessing the userlist. Try again later.')


async def hunger_games_update_pregame_delete(hg_key, hg_dict, response, message):
    """
    Deletes a player from the hunger games dict.

    Arguments:
        hg_key (str) : The key for the hunger games dict.
        hg_dict (dict) : The full game dict.
        response (str[]) : A list of strings representing the response.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Cancels if the game is already min size.
    if len(hg_dict['players']) == HG_MIN_GAMESIZE:
        logging.debug(message, 'tried to remove player from Hunger Games instance, min size reached')
        return await messaging.send_text_message(message, 'Minimum game size already reached.')

    # Try/catch to catch CannotAccessUserlistError.
    try:

        # First, see if there's a second argument.
        if len(response) > 1:

            # Recreate the original response (full length), and feed it into the get_closest_users thing.
            argument_str = ' '.join(response[1:])
            try:
                closest_players = arguments.get_closest_users(message, argument_str,
                                                              exclude_bots=not hg_dict['uses_bots'])

                # Iterate through the closest users and stop at the first one that's actually in the game.
                for player in closest_players:
                    if player in hg_dict['players']:

                        # Remove the player from the playerlist.
                        hg_dict['players'].remove(player)

                        # Retire their profile picture.
                        temp_files.retire_profile_picture_by_user(player, message, 'hg_filehold')

                        # Log and send embed.
                        logging.debug(message, f'removed player {player} from Hunger Games instance')
                        async with message.channel.typing():
                            return await send_pregame(message, hg_dict, f'Removed {player.display_name} from the game.')

                # If we didn't find a player, then send an invalid user thing.
                logging.debug(message, f"attempted to remove user '{argument_str}' from hunger games instance, invalid")
                return await messaging.send_text_message(message, f"Could not find user '{argument_str}'.")

            # If no user was specified, then call this method again with only one term in the response.
            except NoUserSpecifiedError:
                return await hunger_games_update_pregame_delete(hg_key, hg_dict, [response[0]], message)

            # If no user could be found, then send back old reliable.
            except UnableToFindUserError:
                logging.debug(message, f"attempted to remove user '{argument_str}' from hunger games instance, invalid")
                return await messaging.send_text_message(message, f"Could not find user '{argument_str}'.")

        # If there isn't a second argument, remove the last player in the game.
        removed_player = hg_dict['players'][-1]
        hg_dict['players'].remove(removed_player)

        # Retire their profile picture.
        temp_files.retire_profile_picture_by_user(removed_player, message, 'hg_filehold')

        # Send the message and junk.
        logging.debug(message, f'removed player {removed_player} from Hunger Games instance')
        async with message.channel.typing():
            await send_pregame(message, hg_dict, f'Removed {removed_player.display_name} from the game.')

    # If we can't access the userlist, send an error.
    except CannotAccessUserlistError:
        logging.error(message, 'requested add random player to hunger games, failed to access the userlist')
        return await messaging.send_text_message(message, 'There was an error accessing the userlist. Try again later.')


async def hunger_games_update_pregame_proceed(hg_key, hg_dict, response, message):
    """
    Advances the given hunger games dict to the next stage (generates the full game).

    Arguments:
        hg_key (str) : The key for the hunger games dict.
        hg_dict (dict) : The full game dict.
        response (str[]) : A list of strings representing the response.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Log and send message.
    logging.debug(message, 'initiated Hunger Games')
    await messaging.send_text_message(message, 'Generating Hunger Games instance...')

    # Set hunger games variables.
    hg_dict['past_pregame'] = True
    hg_dict['generated'] = False

    # Run the generation method.
    await generate_full_game(hg_dict, message)


async def hunger_games_update_pregame_toggle_bots(hg_key, hg_dict, response, message):
    """
    Toggles bots in the given hunger games dict.

    Arguments:
        hg_key (str) : The key for the hunger games dict.
        hg_dict (dict) : The full game dict.
        response (str[]) : A list of strings representing the response.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # If we were already using bots, then start this section.
    if hg_dict['uses_bots']:

        # This section detects if there are enough non-bot players to justify turning off bots.
        # First, make a copy of the player dict.
        hg_players_no_bots = hg_dict['players'].copy()

        # Remove all bots from the player list.
        while any([player.bot for player in hg_players_no_bots]):
            for player in hg_players_no_bots:

                # Remove the bot and retire their profile picture.
                if player.bot:
                    hg_players_no_bots.remove(player)
                    temp_files.retire_profile_picture_by_user(player, message, 'hg_filehold')

        # While there are less players than the minimum, add new players on randomly.
        while len(hg_players_no_bots) < HG_MIN_GAMESIZE:
            other_players = discord_info.get_applicable_users(message, True, hg_players_no_bots)

            # If there are other players, add a random one and checkout their profile picture.
            if other_players:
                added_player = random.choice(other_players)
                hg_players_no_bots.append(added_player)
                await temp_files.checkout_profile_picture_by_user_with_typing(added_player, message, 'hg_filehold',
                                                                              return_image=False)

            # Otherwise, send an error message.
            else:
                logging.debug(message, 'attempted to remove bots from Hunger Games instance, not enough users')
                return await messaging.send_text_message(message, 'Not enough non-bots to disallow bots.')

        # Allows it.
        # Copy over the new players list.
        hg_dict['players'] = hg_players_no_bots

        # Invert the uses_bots thing.
        hg_dict['uses_bots'] = not hg_dict['uses_bots']

        # Send message and log.
        logging.debug(message, 'removed bots from Hunger Games instance')
        async with message.channel.typing():
            await send_pregame(message, hg_dict, 'Removed bots from the game.')

    # Otherwise, use this one.
    else:
        # Invert the uses_bots thing.
        hg_dict['uses_bots'] = not hg_dict['uses_bots']

        # Log and send message.
        logging.debug(message, 'added bots to Hunger Games instance')
        async with message.channel.typing():
            await send_pregame(message, hg_dict, 'Allowed bots into the game.')


async def hunger_games_update_midgame(hg_key, hg_dict, response, message):
    """
    Updates the hunger games dict according to how the response is formatted.
    Only triggers during midgame.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        hg_key (str) : The key for the hunger games dict.
        hg_dict (dict) : The full game dict.
        response (str[]) : A list of strings representing the response.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # First, see if the dict is generated yet.
    if hg_dict['generated']:

        # Detect confirmation status.
        if hg_dict['confirm_cancel']:

            # Confirm.
            if any([response[0] == value for value in HG_MIDGAME_CANCEL_CONFIRM_TERMS]):
                await hunger_games_update_cancel_confirm(hg_key, hg_dict, response, message)

            # Deny.
            elif any([response[0] == value for value in HG_MIDGAME_CANCEL_CANCEL_TERMS]):
                return await hunger_games_update_cancel_abort(hg_key, hg_dict, response, message)

        # Next command.
        if any([response[0] == value for value in HG_MIDGAME_NEXT_TERMS]):
            await hunger_games_update_midgame_next(hg_key, hg_dict, response, message)

        # Previous command.
        elif any([response[0] == value for value in HG_MIDGAME_PREVIOUS_TERMS]):
            await hunger_games_update_midgame_previous(hg_key, hg_dict, response, message)

        # Cancel command.
        elif any([response[0] == value for value in HG_MIDGAME_CANCEL_TERMS]):
            await hunger_games_update_midgame_cancel(hg_key, hg_dict, response, message)

        # These set only activate if we're in postgame.
        elif hg_dict['complete']:

            # New game command.
            if any([response[0] == value for value in HG_POSTGAME_NEW_GAME_TERMS]):
                await hunger_games_update_postgame_new_game(hg_key, hg_dict, response, message)

            # Replay game command.
            elif any([response[0] == value for value in HG_POSTGAME_REPLAY_TERMS]):
                await hunger_games_update_postgame_replay(hg_key, hg_dict, response, message)

    # If the game isn't finished generating yet.
    elif any([response.startswith(pre) for pre in HG_MIDGAME_BE_PATIENT_TERMS]):
        await hunger_games_update_midgame_still_generating(hg_key, hg_dict, response, message)


async def hunger_games_update_midgame_next(hg_key, hg_dict, response, message):
    """
    Displays the next page(s) of the hg_dict.

    Arguments:
        hg_key (str) : The key for the hunger games dict.
        hg_dict (dict) : The full game dict.
        response (str[]) : A list of strings representing the response.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # First, see if there's a second argument.
    if len(response) > 1:
        # Attempt to pull a number from that second argument (and parse it so that it's correct).
        try:
            action_count = int(response[1])
        # If that doesn't work, set it to the current length.
        except ValueError:
            action_count = len(hg_dict['players'])

    # If there isn't a second argument, use 1.
    else:
        action_count = 1

    # Cancel abort, if it's active.
    if hg_dict['confirm_cancel']:
        await hunger_games_update_cancel_abort(hg_key, hg_dict, response, message)

    # Perform the midgame incrementing.
    if not do_increment(hg_dict, action_count, do_previous=False):
        return

    # Send the midgame message.
    async with message.channel.typing():
        await send_midgame(message, hg_dict)


async def hunger_games_update_midgame_previous(hg_key, hg_dict, response, message):
    """
    Displays the previous page(s) of the hg_dict.

    Arguments:
        hg_key (str) : The key for the hunger games dict.
        hg_dict (dict) : The full game dict.
        response (str[]) : A list of strings representing the response.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # First, see if there's a second argument.
    if len(response) > 1:
        # Attempt to pull a number from that second argument (and parse it so that it's correct).
        try:
            action_count = int(response[1])
        # If that doesn't work, set it to the current length.
        except ValueError:
            action_count = len(hg_dict['players'])

    # If there isn't a second argument, use 1.
    else:
        action_count = 1

    # Cancel abort, if it's active.
    if hg_dict['confirm_cancel']:
        await hunger_games_update_cancel_abort(hg_key, hg_dict, response, message)

    # Perform the midgame incrementing.
    if not do_increment(hg_dict, action_count, do_previous=True):
        return

    # Send the midgame message.
    async with message.channel.typing():
        await send_midgame(message, hg_dict)


async def hunger_games_update_midgame_cancel(hg_key, hg_dict, response, message):
    """
    Performs the cancellation action for midgame updates.
    Can vary depending on what stage the game is in.

    Arguments:
        hg_key (str) : The key for the hunger games dict.
        hg_dict (dict) : The full game dict.
        response (str[]) : A list of strings representing the response.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # If the game is complete, perform a normal exit.
    if hg_dict['complete']:
        # Send the message and log.
        logging.debug(message, 'finished + closed Hunger Games')
        await messaging.send_text_message(message, 'Thanks for playing!')

        # Delete the game.
        clear_current_game_from_database(hg_dict)
        del CURRENT_GAMES[hg_key]

        # Retire the existing players' profile pictures.
        if 'players' in hg_dict:
            temp_files.retire_profile_picture_by_user_id_bulk(hg_dict['players'], message, 'hg_filehold')

    elif not hg_dict['confirm_cancel']:
        # Send the message and log.
        logging.debug(message, 'requested cancel for Hunger Games')
        await messaging.send_text_message(message, 'Cancel Hunger Games? (y/n)')

        # Set the boolean value.
        hg_dict['confirm_cancel'] = True


async def hunger_games_update_midgame_still_generating(hg_key, hg_dict, response, message):
    """
    Tells the players to be patient.

    Arguments:
        hg_key (str) : The key for the hunger games dict.
        hg_dict (dict) : The full game dict.
        response (str[]) : A list of strings representing the response.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Logs and sends message.
    logging.debug(message, 'requested hunger games, still generating (impatient little sack of shit)')
    await message.channel.send('Still generating, be patient.')


async def hunger_games_update_postgame_new_game(hg_key, hg_dict, response, message):
    """
    Generate a new game with new players (delete the old one).

    Arguments:
        hg_key (str) : The key for the hunger games dict.
        hg_dict (dict) : The full game dict.
        response (str[]) : A list of strings representing the response.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Start typing.
    async with message.channel.typing():

        # Remove all the data from the database.
        clear_current_game_from_database(hg_dict)

        # Reset all the post-generation crap in the dict.
        del hg_dict['generated']
        del hg_dict['phases']
        del hg_dict['complete']
        hg_dict['past_pregame'] = False

        # This reuses all the code from hunger_games_update_pregame_shuffle, so call that.
        await hunger_games_update_pregame_shuffle(hg_key, hg_dict, response, message)


async def hunger_games_update_postgame_replay(hg_key, hg_dict, response, message):
    """
    Generate a new game with new players (delete the old one).

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        hg_key (str) : The key for the hunger games dict.
        hg_dict (dict) : The full game dict.
        response (str[]) : A list of strings representing the response.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Start typing.
    async with message.channel.typing():

        # Remove all the data from the database.
        clear_current_game_from_database(hg_dict)

        # Reset all the post-generation crap in the dict.
        del hg_dict['generated']
        del hg_dict['phases']
        del hg_dict['complete']
        hg_dict['past_pregame'] = False

        # Send the new pregame embed.
        await send_pregame(message, hg_dict)


async def hunger_games_update_cancel_confirm(hg_key, hg_dict, response, message):
    """
    Cancels the given hunger games dict (no confirmation, just delete).

    Arguments:
        hg_key (str) : The key for the hunger games dict.
        hg_dict (dict) : The full game dict.
        response (str[]) : A list of strings representing the response.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Send the message and log.
    logging.debug(message, 'canceled Hunger Games')
    await messaging.send_text_message(message, 'Hunger Games canceled.')

    # Delete it.
    clear_current_game_from_database(hg_dict)
    del CURRENT_GAMES[hg_key]

    # Retire the existing players' profile pictures.
    if 'players' in hg_dict:
        temp_files.retire_profile_picture_by_user_id_bulk(hg_dict['players'], message, 'hg_filehold')


async def hunger_games_update_cancel_abort(hg_key, hg_dict, response, message):
    """
    Aborts the cancel on the given hunger games dict.

    Arguments:
        hg_key (str) : The key for the hunger games dict.
        hg_dict (dict) : The full game dict.
        response (str[]) : A list of strings representing the response.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Send the message and log.
    logging.debug(message, ' aborted cancel for Hunger Games')
    await messaging.send_text_message(message, 'Cancel aborted.')

    # Abort the cancel.
    hg_dict['confirm_cancel'] = False


def clear_current_game_from_database(hg_dict):
    """
    Clears all the rows belonging to the given game from the database.

    Arguments:
        hg_dict (dict) : The full game dict.
    """
    # If the dict doesn't have phases in it, return.
    if 'phases' not in hg_dict:
        return

    # Iterate through the phases in the dict.
    for phase in hg_dict['phases']:
        current_game_phase = get_current_game_phase_by_id(phase[1])

        # For every game action id in the current game phase, delete it.
        if current_game_phase.game_action_ids:
            for game_action_id in current_game_phase.game_action_ids:
                database.delete_filtered(database.HG_CURRENT_GAME_ACTIONS_TABLE,
                                         database.HG_CURRENT_GAME_ACTIONS_TABLE.game_action_id == game_action_id)

        # Delete the phase.
        database.delete_filtered(database.HG_CURRENT_GAME_PHASES_TABLE,
                                 database.HG_CURRENT_GAME_PHASES_TABLE.game_phase_id == phase[1])


async def send_pregame(message, hg_dict, title=HG_PREGAME_TITLE):
    """
    Sends the pregame roster thing.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        hg_dict (dict) : The full game dict.
        title (str) : The title of the embed, if any.
    """
    # Generate the player statuses image.
    image = makeimage_player_statuses([0 for player in hg_dict['players']], hg_dict['players'])

    # Sends image, logs.
    await messaging.send_image_based_embed(message, image, title, HG_EMBED_COLOR,
                                           footer=HG_PREGAME_DESCRIPTION.format(
                                               'Disallow' if hg_dict['uses_bots'] else 'Allow'))


async def send_midgame(message, hg_dict):
    """
    Sends the midgame message after incrementing the phase.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        hg_dict (dict) : The full game dict.
    """
    # Gets the new current phase.
    current_phase = hg_dict['phases'][hg_dict['current_phase']]

    # Gets the footer we need.
    # If the game is complete, then we use a different set from the non-complete ones.
    if hg_dict['complete']:

        # At the beginning, then we can't use previous.
        if hg_dict['current_phase'] == 0 and hg_dict['action_min_index'] == 0:
            footer_str = HG_POSTGAME_BEGINNING_DESCRIPTION

        # At the end, then we can't go forward.
        elif current_phase[0] == 'kills':
            footer_str = HG_FINALE_DESCRIPTION

        # Anywhere else, have both.
        else:
            footer_str = HG_POSTGAME_MIDGAME_DESCRIPTION

    # Game is not complete, use alternate footers.
    else:

        # At the beginning, then we can't use previous.
        if hg_dict['current_phase'] == 0 and hg_dict['action_min_index'] == 0:
            footer_str = HG_BEGINNING_DESCRIPTION

        # At the end, then we can't go forward.
        elif current_phase[0] in ['win', 'tie']:
            footer_str = HG_THE_END_DESCRIPTION
            hg_dict['complete'] = True

        # Anywhere else, have both.
        else:
            footer_str = HG_MIDGAME_DESCRIPTION

    # Creates embed for act pages.
    if current_phase[0] == 'act':

        # Get the values for the action indexes.
        action_min_index = hg_dict['action_min_index']
        action_max_index = hg_dict['action_max_index']

        # Get the phase and the actions from the database.
        phase_object = get_current_game_phase_by_id(current_phase[1])
        actions = get_current_game_actions_by_current_game_phase_and_action_indexes(
            phase_object, action_min_index, action_max_index)

        # Create the embed title.
        title = phase_object.title + \
                (f', Action {action_min_index + 1}' if action_min_index == action_max_index else
                 f', Actions {action_min_index + 1} - {action_max_index + 1}') + \
                (f' / {len(phase_object.game_action_ids)}' if phase_object.complete else '')

        # Create and send the embed.
        await messaging.send_image_based_embed(
            message,
            makeimage_action(actions, hg_dict['players'], phase_object.description if action_min_index == 0 else None),
            title, HG_EMBED_COLOR, footer_str
        )

    # Creates embed for win AND tie pages.
    elif current_phase[0] == 'win':

        # Get the phase and the actions from the database.
        phase_object = get_current_game_phase_by_id(current_phase[1])
        actions = get_current_game_actions_by_current_game_phase_and_action_indexes(
            phase_object, 0, 0)

        # Create and send the embed.
        await messaging.send_image_based_embed(
            message,
            makeimage_action(actions, hg_dict['players'], phase_object.description), phase_object.title,
            HG_EMBED_COLOR, footer_str
        )

    # Creates embed for status pages.
    elif current_phase[0] == 'status':

        # Get the phase.
        phase_object = get_current_game_phase_by_id(current_phase[1])

        # Get the new death count.
        new_deaths = len([status for status in phase_object.player_statuses if status == 1])

        # Create and send the embed.
        await messaging.send_image_based_embed(
            message,
            makeimage_player_statuses(phase_object.player_statuses, hg_dict['players']),
            f'{new_deaths} cannon shot{"" if new_deaths == 1 else "s"} can be heard in the distance.', HG_EMBED_COLOR,
            footer_str
        )

    # Creates embed for placement pages.
    elif current_phase[0] == 'place':

        # Get the phase.
        phase_object = get_current_game_phase_by_id(current_phase[1])

        # Reorganize the players to be in the player status order.
        ordered_placements = sorted(zip(phase_object.player_statuses, hg_dict['players']), key=lambda pair: pair[0])
        sorted_players = [player for place, player in ordered_placements]
        sorted_placements = [place for place, player in ordered_placements]

        # Create and send the embed.
        await messaging.send_image_based_embed(
            message,
            makeimage_player_statuses(sorted_placements, sorted_players,
                                      placement=max([1] + phase_object.player_statuses)),
            'Placements', HG_EMBED_COLOR, footer_str
        )

    # Creates embed for killcount pages.
    elif current_phase[0] == 'kills':

        # Get the phase.
        phase_object = get_current_game_phase_by_id(current_phase[1])

        # Reorganize the players to be in the player status order.
        ordered_kills = sorted(zip(phase_object.player_statuses, hg_dict['players']), key=lambda pair: pair[0])
        ordered_kills.reverse()
        sorted_players = [player for place, player in ordered_kills]
        sorted_kills = [place for place, player in ordered_kills]

        # Create and send the embed.
        await messaging.send_image_based_embed(
            message,
            makeimage_player_statuses(sorted_kills, sorted_players,
                                      kills=max([1] + phase_object.player_statuses)),
            'Kills', HG_EMBED_COLOR, footer_str
        )

    # If there's an unexpected phase type, raise an exception.
    else:
        raise InvalidHungerGamesPhaseError(current_phase[0])


def do_increment(hg_dict, count, do_previous):
    """
    Increments the phase.

    Arguments:
        hg_dict (dict) : The full game dict.
        count (int) : How many action images to show, if the next phase is an action phase.
        do_previous (bool) : Whether or not to go backwards.

    Returns:
        bool : Whether or not the hg_dict was incremented.
    """
    # Gets the current phase.
    current_phase = hg_dict['phases'][hg_dict['current_phase']]

    # If the current phase is an act, then its increment changes based on the indexes.
    if current_phase[0] == 'act':
        return do_increment_act(hg_dict, count, do_previous)

    # Otherwise, increment for other normal types of pages.
    return do_increment_non_act(hg_dict, count, do_previous, current_phase[0])


def do_increment_act(hg_dict, count, do_previous):
    """
    Increments the phase (for an ACT phase).

    Arguments:
        hg_dict (dict) : The full game dict.
        count (int) : How many action images to show, if the next phase is an action phase.
        do_previous (bool) : Whether or not to go backwards.

    Returns:
        bool : Whether or not the hg_dict was incremented.
    """
    # Backwards section.
    if do_previous:

        # If we were going backwards and the previous action was the beginning of the phase,
        # then perform a special check...
        if hg_dict['action_min_index'] == 0:

            # If this is the first phase, then return False.
            if hg_dict['current_phase'] == 0:
                return False

            # Otherwise, subtract 1 from the current_phase and return True.
            hg_dict['current_phase'] -= 1
            return do_increment_act_check(hg_dict, count, do_previous)

        # Otherwise, we weren't at the beginning of the phase,
        # so we can reverse increment the action indexes and return True.
        hg_dict['action_max_index'] = hg_dict['action_min_index'] - 1
        hg_dict['action_min_index'] = max(hg_dict['action_min_index'] - count, 0)
        return True

    # If we're going forwards and the previous action was the end of the phase,
    # then add 1 to the current_phase and return True.
    if hg_dict['action_max_index'] == hg_dict['phases'][hg_dict['current_phase']][2] - 1:
        hg_dict['current_phase'] += 1
        return do_increment_act_check(hg_dict, count, do_previous)

    # Otherwise, increment the action indexes and return True.
    hg_dict['action_min_index'] = hg_dict['action_max_index'] + 1
    hg_dict['action_max_index'] = min(hg_dict['action_max_index'] + count,
                                      hg_dict['phases'][hg_dict['current_phase']][2] - 1)
    return True


def do_increment_non_act(hg_dict, count, do_previous, phase_type):
    """
    Increments the phase (for NON-ACT phases).

    Arguments:
        hg_dict (dict) : The full game dict.
        count (int) : How many action images to show, if the next phase is an action phase.
        do_previous (bool) : Whether to go backwards.
        phase_type (str) : The current phase's type.

    Returns:
        bool : Whether the hg_dict was incremented.
    """
    # If we went backwards, then just subtract 1 from the current phase.
    if do_previous:
        hg_dict['current_phase'] -= 1

    # Otherwise, first, check to make sure we're not at the end.
    else:
        # If we are, then just return False.
        if phase_type == 'kills':
            return False

        # If not, then add 1 from the current phase.
        hg_dict['current_phase'] += 1

    # Do the act check.
    return do_increment_act_check(hg_dict, count, do_previous)


def do_increment_act_check(hg_dict, count, do_previous):
    """
    Increments the phase (for NON-ACT phases).

    Arguments:
        hg_dict (dict) : The full game dict.
        count (int) : How many action images to show, if the next phase is an action phase.
        do_previous (bool) : Whether or not to go backwards.

    Returns:
        True
    """
    # Detect if the NEW current phase is an act.
    current_phase = hg_dict['phases'][hg_dict['current_phase']]
    if current_phase[0] == 'act':

        # If so, then set the action indexes depending on whether or not we're going backwards.
        # Backwards gets put at the end.
        if do_previous:
            hg_dict['action_max_index'] = current_phase[2] - 1
            hg_dict['action_min_index'] = max(hg_dict['action_max_index'] - count + 1, 0)

        # Forwards gets put at the front.
        else:
            hg_dict['action_min_index'] = 0
            hg_dict['action_max_index'] = min(count - 1, current_phase[2] - 1)

    # Return True.
    return True
        

def makeimage_player_statuses(player_statuses, players, placement=False, kills=False):
    """
    Generates a player status image.
    This can also be used to make player placement images and kill count lists.

    Arguments:
        player_statuses (int[]) : The player statuses, with indexes matching the players list.
        players (discord.User[]) : The player list.
        placement (bool) : Whether the player_statuses values are player placements.
        kills (int) : Whether the player_statuses values are kill counts.
    """
    # Splits all the players into their own rows.
    players_split = []
    current_split = []
    for i in range(len(players)):
        if len(current_split) == HG_PLAYERSTATUS_WIDTHS[len(players)]:
            players_split.append(current_split)
            current_split = []
        current_split.append(i)
    players_split.append(current_split)

    # Gets the image width and height.
    image_width = HG_ICON_SIZE * len(players_split[0]) + HG_ICON_BUFFER * (len(players_split[0]) + 1)
    image_height = HG_PLAYERSTATUS_ROWHEIGHT * len(players_split) + HG_ICON_BUFFER * (len(players_split) + 1)

    # Creates all the images and drawers that will help us make the new image.
    player_image = Image.new('RGB', (image_width, image_height), HG_BACKGROUND_COLOR)
    player_drawer = ImageDraw.Draw(player_image)
    player_font = assets.open_font(HG_FONT, HG_FONT_SIZE)

    # Sets the current y at the buffer between the top and the first icon.
    current_y = HG_ICON_BUFFER

    # Iterate through each row.
    for split in players_split:
        # Set the starting x position.
        current_x = int((image_width - (len(split) * HG_ICON_SIZE + (len(split) - 1) * HG_ICON_BUFFER)) / 2)

        # Then, iterate through each player in each row.
        for i in split:

            # Gets pfp, pastes onto image.
            makeimage_pfp(temp_files.get_profile_picture_by_user(players[i], size=(HG_ICON_SIZE, HG_ICON_SIZE)),
                          player_image, player_drawer, current_x, current_y,
                          player_statuses[i] and not placement and not kills)

            # Writes name and status / placement.
            player_name = players[i].display_name

            # If the name is too long, we put a ... at the end (thx alex!!!!!)
            if player_font.getsize(player_name)[0] > HG_ICON_SIZE:
                while player_font.getsize(player_name + '...')[0] > HG_ICON_SIZE:
                    player_name = player_name[:-1]
                player_name+= '...'

            # Draw the player name.
            player_drawer.text((current_x + int(HG_ICON_SIZE / 2 - player_font.getsize(player_name)[0] / 2),
                                current_y + HG_ICON_SIZE + HG_TEXT_BUFFER), player_name,
                               font=player_font, fill=(255, 255, 255))

            # Placement
            if placement:
                place = f'{player_statuses[i]}{NTH_SUFFIXES[player_statuses[i] % 10]} Place'
                player_drawer.text((current_x + int(HG_ICON_SIZE / 2 - player_font.getsize(place)[0] / 2),
                                    current_y + HG_ICON_SIZE + HG_FONT_SIZE + HG_TEXT_BUFFER), place, font=player_font,
                                   fill=misc.find_color_tuple_midpoint_hsv(HG_STATUS_ALIVE_COLOR, HG_STATUS_DEAD_COLOR,
                                                                           (player_statuses[i] - 1) / placement))

            # Kill Count
            elif kills:
                kill_str = f'{player_statuses[i]} {" Kill" if player_statuses[i] == 1 else " Kills"}'
                player_drawer.text((current_x + int(HG_ICON_SIZE / 2 - player_font.getsize(kill_str)[0] / 2),
                                    current_y + HG_ICON_SIZE + HG_FONT_SIZE + HG_TEXT_BUFFER), kill_str,
                                   font=player_font, fill=misc.find_color_tuple_midpoint_hsv(HG_STATUS_DEAD_COLOR,
                                                                                             HG_STATUS_ALIVE_COLOR,
                                                                                             player_statuses[i] / kills)
                                   )

            # Status
            else:
                status = 'Alive' if not player_statuses[i] else ('Deceased' if player_statuses[i] - 1 else 'Newly Deceased')
                player_drawer.text((current_x + int(HG_ICON_SIZE / 2 - player_font.getsize(status)[0] / 2),
                                    current_y + HG_ICON_SIZE + HG_FONT_SIZE + HG_TEXT_BUFFER), status, font=player_font,
                                   fill=HG_STATUS_ALIVE_COLOR if not player_statuses[i] else HG_STATUS_DEAD_COLOR)

            # Adds to current_x.
            current_x += HG_ICON_SIZE + HG_ICON_BUFFER

        # Adds to current_y.
        current_y += HG_PLAYERSTATUS_ROWHEIGHT + HG_ICON_BUFFER

    return player_image


def makeimage_action(actions, players, action_description=None):
    """
    Displays a variable number of actions at once.

    Arguments:
        actions ((hg_actions database table)[]) : The actions to put onto the image.
        players (discord.User[]) : The player list.
        action_description (str) : The action description, if any.
    """
    # Makes the font and gets the action description width, if any.
    action_font = assets.open_font(HG_FONT, HG_FONT_SIZE)
    action_desc_width = action_font.getsize(action_description)[0] if action_description else 0

    # Gets the image height.
    # Also makes the full action text while we're at it.
    image_height = HG_ACTION_ROWHEIGHT * len(actions) + HG_ICON_BUFFER + \
                   (HG_FONT_SIZE + HG_HEADER_BORDER_BUFFER * 3 if action_description else -1)
    text_sizes = []

    # Get the image width.
    # The image width is diffcult to gather, because we have to test the widths of everything.
    image_width = action_desc_width + HG_ICON_BUFFER * 2 + HG_HEADER_BORDER_BUFFER * 2 if action_description else -1

    # Iterate through each action in the list.
    for action in actions:

        # Tests for text boundaries
        full_action_text = action.text
        for i in range(len(action.players)):
            full_action_text = full_action_text.replace('{' + str(i) + '}', players[action.players[i]].display_name)

        # Calculates text widths and appends them to the text_sizes list.
        text_width = action_font.getsize(full_action_text)[0]
        image_width = max(image_width, text_width + HG_ICON_BUFFER * 2)
        text_sizes.append(text_width)

        # Tests for image boundaries
        image_width = max(image_width, HG_ICON_SIZE * len(action.players) + HG_ICON_BUFFER * (len(action.players) + 1))

    # Creates all the images and drawers that will help us make the new image.
    action_image = Image.new('RGB', (image_width, image_height), HG_BACKGROUND_COLOR)
    player_drawer = ImageDraw.Draw(action_image)

    # Sets the current y at the buffer between the top and the first icon.
    current_y = HG_ICON_BUFFER

    # Draw the description, if any.
    if action_description:

        # Sets the current x and draws the border around the description.
        current_x = int((image_width - action_desc_width) / 2)
        player_drawer.rectangle(
            [(current_x - HG_HEADER_BORDER_BUFFER,
              current_y - HG_HEADER_BORDER_BUFFER),
             (current_x + action_desc_width + HG_HEADER_BORDER_BUFFER,
              current_y + HG_FONT_SIZE + HG_HEADER_BORDER_BUFFER)],
            HG_HEADER_BACKGROUND_COLOR,
            HG_HEADER_BORDER_COLOR
        )

        # Draws the text and adds to the current y.
        player_drawer.text((current_x, HG_ICON_BUFFER), action_description, font=action_font, fill=HG_HEADER_TEXT_COLOR)
        current_y += HG_FONT_SIZE + HG_HEADER_BORDER_BUFFER * 3

    # Num keeps track of the text sizes.
    num = 0

    # Iterate through each action in the list.
    for action in actions:

        # Set the current x.
        current_x = int(image_width / 2) - int(len(action.players) / 2 * HG_ICON_SIZE) - \
                    int((len(action.players) - 1) / 2 * HG_ICON_BUFFER)

        # Gets each player's pfp and pastes it onto the image.
        for i in action.players:
            makeimage_pfp(temp_files.get_profile_picture_by_user(players[i], size=(HG_ICON_SIZE, HG_ICON_SIZE)),
                                                                 action_image, player_drawer, current_x, current_y,
                                                                 False)
            current_x += HG_ICON_SIZE + HG_ICON_BUFFER

        # Draws each part of the text.
        current_x = int((image_width - text_sizes[num]) / 2)
        current_y += HG_ICON_SIZE + HG_TEXT_BUFFER
        makeimage_action_text(action, players, player_drawer, current_x, current_y, action_font)

        # Adds to the current_y and num.
        current_y += HG_FONT_SIZE + HG_ICON_BUFFER
        num += 1

    return action_image


def makeimage_pfp(player_pfp, image, drawer, pfp_x, pfp_y, dead=False):
    """
    Draws a player's pfp at the given x and y.

    Arguments:
        player_pfp (PIL.Image) : The loaded profile picture.
        image (PIL.Image) : The base image.
        drawer (PIL.ImageDraw) : The drawer.
        pfp_x (int) : The x position of where to draw the icon.
        pfp_y (int) : The y position of where to draw the icon.
        dead (bool) : Whether or not this player is dead.
                      If they are dead, then their icon will be in grayscale and slightly darkened.
    """
    # If player dead, recolor to black and white.
    if dead:
        player_pfp = ImageOps.colorize(player_pfp.convert('L'), black=(0, 0, 0),
                                       white=misc.multiply_int_tuple(
                                           (255, 255, 255), HG_PLAYERSTATUS_DEAD_PFP_DARKEN_FACTOR),
                                       mid=misc.multiply_int_tuple(
                                           (128, 128, 128), HG_PLAYERSTATUS_DEAD_PFP_DARKEN_FACTOR))
    image.paste(player_pfp, (pfp_x, pfp_y))

    # Draws border around player icon.
    drawer.line([(pfp_x - 1, pfp_y - 1),
                 (pfp_x + HG_ICON_SIZE, pfp_y - 1),
                 (pfp_x + HG_ICON_SIZE, pfp_y + HG_ICON_SIZE),
                 (pfp_x - 1, pfp_y + HG_ICON_SIZE),
                 (pfp_x - 1, pfp_y - 1)], width=1, fill=0)


def makeimage_action_text(action, players, drawer, txt_x, txt_y, action_font):
    """
    Draws the action text for an action.

    Arguments:
        action (hg_actions database table) : The action that should be put onto the image.
        players (discord.User[]) : The player list.
        drawer (PIL.ImageDraw) : The drawer.
        txt_x (int) : The x position of where to draw the text.
        txt_y (int) : The y position of where to draw the text.
        action_font (PIL.ImageFont) : The action font.
    """
    # Create remaining_text
    remaining_text = action.text

    while remaining_text:
        # Get the index of the NEXT {n}.
        next_bracket = len(remaining_text)
        for i in range(len(action.players)):
            bracket_pos = remaining_text.find('{' + str(i) + '}')
            if not bracket_pos + 1:
                continue
            next_bracket = min(next_bracket, bracket_pos)

        # Draw the text up to the next bracket.
        drawer.text((txt_x, txt_y), remaining_text[:next_bracket], font=action_font, fill=(255, 255, 255))
        txt_x += action_font.getsize(remaining_text[:next_bracket])[0]

        # Draw the next player name.
        if next_bracket == len(remaining_text):
            break
        i = int(remaining_text[next_bracket + 1])
        drawer.text((txt_x, txt_y), players[action.players[i]].display_name, font=action_font,
                    fill=HG_ACTION_PLAYER_COLOR)
        txt_x += action_font.getsize(players[action.players[i]].display_name)[0]

        # Trim remaining_text.
        remaining_text = remaining_text[next_bracket + 3:]


async def generate_full_game(hg_dict, message):
    """
    Generates an entire Hunger Games from the users specified in the hg_dict.
    Depends on external methods to do most of the dirty work.

    Arguments:
        hg_dict (dict) : The full game dict.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Create the player statuses dict in the hg_dict.
    statuses = []
    for player in hg_dict['players']:
        statuses.append({'dead': False, 'placement': HG_MAX_GAMESIZE + 1, 'hurt': False, 'inv': [], 'kills': 0})
    hg_dict['statuses'] = statuses

    # Makes the phases.
    hg_dict['phases'] = []

    # Make the midgame parts (up to the final action (victory / tie)).
    generate_midgame(hg_dict)

    # Make the final action (victory / tie).
    generate_win_tie_phase(hg_dict)

    # Makes the placement and kill count phases.
    generate_placement_kill_count_phase(hg_dict, do_placement=True)
    generate_placement_kill_count_phase(hg_dict, do_placement=False)

    # Updates hunger games dict.
    hg_dict.update(current_phase=0, action_min_index=0, action_max_index=0, confirm_cancel=False, generated=True,
                   complete=False)
    del hg_dict['statuses']

    # Sends the first message and logs.
    logging.debug(message, 'generated complete hunger games instance')
    await send_midgame(message, hg_dict)


def generate_midgame(hg_dict):
    """
    Generates the midgame part of the hg_dict.
    This includes all actions and player status screens, as well as the final victory / tie screen.

    Arguments:
        hg_dict (dict) : The full game dict.
    """
    # First, generate the bloodbath.
    generate_action_phase(hg_dict, get_phase_by_category('bloodbath'))

    # Next, start keeping track of what the best placement is for eah loop.
    previous_loop_best_place = HG_MAX_GAMESIZE + 1

    # Enter loop as long as the game isn't over.
    if not generate_game_over(hg_dict):

        # Keep variables to keep track of day/night and turns since last event.
        day_night = 1
        turns_since_event = 0

        # Enter loop.
        while True:

            # If we should perform an event this turn (random chance that gets more likely as the game goes on),
            # then do an event.
            if day_night >= HG_EVENT_DAYNIGHT_MINIMUM and \
                    random.random() < 1 - (1 - HG_EVENT_DEFAULT_CHANCE) ** turns_since_event:

                # Choose random event and generate the actions.
                generate_action_phase(hg_dict, get_phase_by_category('event'))

                # Reset turns_since_event.
                turns_since_event = 0

            # Otherwise, perform normal day/night actions.
            else:

                # Day.
                generate_action_phase(hg_dict, get_phase_by_category('day'), day_night)

                # Detect if the game is over...
                if generate_game_over(hg_dict):
                    break

                # Night.
                generate_action_phase(hg_dict, get_phase_by_category('night'), day_night)

                # Increment the day/night and turns_since_event.
                day_night += 1
                turns_since_event += 1

            # Detect if the game is over...
            if generate_game_over(hg_dict):
                break

            # Add a new player status phase and update previous_loop_best_place.
            generate_player_status_phase(hg_dict, previous_loop_best_place)
            previous_loop_best_place = min([player['placement'] for player in hg_dict['statuses']])

    # Add a new player status phase.
    generate_player_status_phase(hg_dict, previous_loop_best_place)


def generate_action_phase(hg_dict, phase, phase_format_number=None):
    """
    Generates a single action phase.

    Arguments:
        hg_dict (dict) : The full game dict.
        phase (hg_phases database table) : The parent phase to base this phase off of.
        phase_format_number (int) : The number to use to format the phase title + description, if any.
    """
    # Generate the actions
    actions = generate_actions_outer(hg_dict, phase)

    # Generate the new statuses for each player.
    for action_entry in actions:
        generate_action_statuses(hg_dict['statuses'], action_entry[0], action_entry[1])

    # Insert the new actions into the database.
    action_ids = [
        database.insert_into_database(
            database.HG_CURRENT_GAME_ACTIONS_TABLE, action_id=action_entry[0].action_id,
            players=action_entry[1]
        ).game_action_id for action_entry in actions]

    # Insert the new phase into the database.
    hg_dict['phases'].append(
        ('act', database.insert_into_database(
            database.HG_CURRENT_GAME_PHASES_TABLE, type=phase.type,
            title=phase.title.format(phase_format_number) if phase_format_number else phase.title,
            description=phase.description.format(phase_format_number) if phase_format_number else phase.description,
            game_action_ids=action_ids
        ).game_phase_id, len(action_ids))
    )


def generate_win_tie_phase(hg_dict):
    """
    Generates a win/tie phase, depending on how the 'status' part of the hg_dict is.

    Arguments:
        hg_dict (dict) : The full game dict.
    """
    # First, detect the type of phase and get it.
    # Win alive...
    winners = [i for i in range(len(hg_dict['statuses'])) if not hg_dict['statuses'][i]['dead']]
    if winners:
        phase = get_phase_by_category('win_alive')

    # Win dead...
    else:
        winners = [i for i in range(len(hg_dict['statuses'])) if hg_dict['statuses'][i]['placement'] == 1]
        phase = get_phase_by_category('win_dead')

    # Generate the actions.
    actions = generate_actions_outer(hg_dict, phase, preset_players=winners, force_one_action=True)

    # Insert the new actions into the database.
    action_ids = [
        database.insert_into_database(
            database.HG_CURRENT_GAME_ACTIONS_TABLE, action_id=action_entry[0].action_id,
            players=action_entry[1]
        ).game_action_id for action_entry in actions]

    # Insert the new phase into the database.
    hg_dict['phases'].append(
        ('win', database.insert_into_database(
            database.HG_CURRENT_GAME_PHASES_TABLE, type=phase.type,
            title=phase.title, description=phase.description, game_action_ids=action_ids
        ).game_phase_id, 1)
    )


def generate_actions_outer(hg_dict, phase, preset_players=None, force_one_action=False):
    """
    Generates all the actions according to the given phase and slots them into the actions list.

    Arguments:
        hg_dict (dict) : The full game dict.
        phase (hg_phases database table) : The parent phase to base this phase off of.
        preset_players (int[]) : The pre-set list of players for this action, if any.
        force_one_action (bool) : Whether to force all players into one action. False by default.

    Returns:
        (hg_actions database table, int[])[] : A list of each action, along with which player indexes involve the
                                               action.
    """
    # First, make a list of all the available players' indexes.
    available_players = preset_players if preset_players else \
        [i for i in range(len(hg_dict['statuses'])) if not hg_dict['statuses'][i]['dead']]

    # Second, get all the actions w/action wrappers for the given phase.
    if force_one_action:
        normal_actions = get_normal_actions_by_phase(phase)
        trigger_action_wrappers = get_trigger_actions_by_phase(phase)
    else:
        normal_actions = get_normal_actions_by_phase(phase)
        trigger_action_wrappers = get_trigger_actions_by_phase(phase)

    # Third, make the actions list, which will store all the actions.
    actions = []

    # Iterates through all the trigger actions, picking them for all the players that are valid.
    for trigger_action_wrapper in trigger_action_wrappers:
        generate_actions_trigger(trigger_action_wrapper, hg_dict['statuses'], available_players, actions)

    # Iterates through all the actions, picking them at random for the remaining player_actions.
    while available_players:
        generate_actions_normal(normal_actions, available_players, actions)

    # Randomize the order of the actions.
    random.shuffle(actions)

    # Return.
    return actions


def generate_actions_trigger(trigger_action_wrapper, hg_statuses, available_players, actions):
    """
    Generates one trigger action. Or not. It depends.

    Arguments:
        trigger_action_wrapper (hg_action_wrappers database table) : The list of normal actions to choose from.
        hg_statuses (dict[]) : The statuses of every player in the game.
        available_players (int[]) : The list of player id's that have yet to be given actions.
        actions ((hg_actions database table, int[])[]) : The final list of actions that the picked action will be
                                                         added to.
    """
    # First, check and make sure that there are enough players available for this trigger to happen,
    # for both success and fail.
    if (trigger_action_wrapper.success_action_ids and
        len(available_players) < min(action.extra_players + 1
                                     for action in trigger_action_wrapper.success_actions)) or \
        (trigger_action_wrapper.failure_action_ids and
         len(available_players) < min(action.extra_players + 1
                                      for action in trigger_action_wrapper.failure_actions)):
        return

    # Next, establish variables for the for loop.
    chosen_actions = []

    # Enter the for loop to find valid players.
    for player in available_players:

        # Check the player's inventory, if there are inventory requirements.
        if trigger_action_wrapper.trigger_item:
            if trigger_action_wrapper.trigger_item not in hg_statuses[player]['inv']:
                continue

        # Check if player needs to be wounded.
        if trigger_action_wrapper.trigger_hurt:
            if not hg_statuses[player]['hurt']:
                continue

        # Get whether the trigger succeeded or not.
        success = random.random() <= trigger_action_wrapper.trigger_chance \
            if trigger_action_wrapper.trigger_chance else True

        # First, set a variable keeping track of the extra players and set it to the max. Forces at least one loop.
        extra_players = HG_MAX_GAMESIZE
        curr_action = None

        # If succeeded and there are success actions, then pick one until there's one with a suitable amount of players.
        if success and trigger_action_wrapper.success_action_ids:
            while extra_players > len(available_players):
                curr_action = random.choice(trigger_action_wrapper.success_actions)
                extra_players = curr_action.extra_players

        # If failed and there are failure actions, then pick one until there's one with a suitable amount of players.
        if not success and trigger_action_wrapper.failure_action_ids:
            while extra_players > len(available_players):
                curr_action = random.choice(trigger_action_wrapper.failure_actions)
                extra_players = curr_action.extra_players

        # If a new curr_action was found, then add it to the list.
        if curr_action:
            chosen_actions.append((curr_action, [player]))

    # Remove all the players with triggers from the available_players.
    for player in [action[1][0] for action in chosen_actions]:
        available_players.remove(player)

    # Shuffle the chosen_actions.
    random.shuffle(chosen_actions)

    # For every chosen action, perform one last check.
    for action in chosen_actions:

        # Check and make sure that there's enough players to perform the action.
        # If there isn't, put this player back into the available_players list and continue.
        if len(available_players) < action[0].extra_players:
            available_players.append(chosen_actions[1][0])
            continue

        # Create list of added players.
        added_players = []

        # Gather more necessary players, if any.
        for i in range(action[0].extra_players):
            added_players.append(random.choice(available_players))
            available_players.remove(added_players[-1])

        # Add the added players to the action.
        for player in added_players:
            action[1].append(player)

        # Append the action to the actions.
        actions.append(action)


def generate_actions_normal(normal_actions, available_players, actions):
    """
    Generates one normal action.

    Arguments:
        normal_actions ((hg_action_wrappers + hg_actions database table)[]) : The list of normal actions to choose from.
        available_players (int[]) : The list of player id's that have yet to be given actions.
        actions ((hg_actions database table, int[])[]) : The final list of actions that the picked action will be
                                                         added to.
    """
    # First, set a variable keeping track of the extra players and set it to the max.
    extra_players = HG_MAX_GAMESIZE

    # Take a player out and use it as the base player.
    chosen_players = [random.choice(available_players)]
    available_players.remove(chosen_players[0])

    # While loop, finds a good action.
    while extra_players > len(available_players):
        curr_action = random.choice(normal_actions)
        extra_players = curr_action.extra_players

    # Adds more players to current action, if necessary.
    for i in range(extra_players):
        chosen_players.append(random.choice(available_players))
        available_players.remove(chosen_players[-1])

    # Add the actions to the list.
    actions.append((curr_action, chosen_players))


def generate_action_statuses(hg_statuses, action, players):
    """
    Updates the statuses of players post-action in the hg_dict.

    Arguments:
        hg_statuses (dict[]) : The statuses of every player in the game.
        action (hg_actions database table) : The action that needs to trigger this status check.
        players (int[]) : The indexes of all the players in this action.
    """
    # First, we handle deaths.
    if action.kill:
        # Get the placement for this player(s).
        this_place = len(hg_statuses) - len([player for player in hg_statuses if player['dead']]) - len(action.kill) + 1
        # Iterate through the kills and update statuses accordingly.
        for kill_index in action.kill:
            hg_statuses[players[kill_index]]['dead'] = True
            hg_statuses[players[kill_index]]['placement'] = this_place

    # Next, injuries.
    if action.hurt:
        for hurt_index in action.hurt:
            hg_statuses[players[hurt_index]]['hurt'] = True

    # Kill credit.
    if action.credit:
        for credit_index in action.credit:
            hg_statuses[players[credit_index]]['kills'] += 1

    # Healing.
    if action.heal:
        for heal_index in action.heal:
            hg_statuses[players[heal_index]]['hurt'] = False

    # Items.
    if action.give:

        # Iterate through item indexes.
        for i in range(len(action.give)):

            # Item 0 (nothing).
            if action.give[i] == 0:
                continue

            # Negative item (remove their thing).
            elif action.give[i] < 0:
                try:
                    hg_statuses[players[i]]['inv'].remove(-action.give[i])
                except ValueError:
                    pass

            # Other items.
            else:

                # Special items
                # 3000, 1 - 3 random items
                if action.give[i] == 3000:
                    for j in range(random.randint(1, 3)):
                        hg_statuses[players[i]]['inv'].append(random.choice(HG_ALL_ITEMS))

                # 4000, one of each item type
                elif action.give[i] == 4000:
                    hg_statuses[players[i]]['inv'].append(random.choice(HG_WEAPON_ITEMS))
                    hg_statuses[players[i]]['inv'].append(random.choice(HG_HEALTH_ITEMS))
                    hg_statuses[players[i]]['inv'].append(random.choice(HG_FOOD_ITEMS))

                # 8888, take away rope, give food
                elif action.give[i] == 8888:
                    hg_statuses[players[i]]['inv'].remove(8)
                    hg_statuses[players[i]]['inv'].append(10)
                    hg_statuses[players[i]]['inv'].append(104)

                # 9999, take away everything and give it to everyone else
                elif action.give[i] == 9999:
                    # Iterate through and give it to other folks one at a time.
                    ind2 = 0
                    for item in hg_statuses[players[i]]['inv']:
                        hg_statuses[players[i]]['inv'].remove(item)
                        if ind2 % action.extra_players + 1 == i:
                            ind2 += 1
                        hg_statuses[players[i]]['inv'].append(item)
                        ind2 += 1

                # Any other item, just give it to them normally.
                else:
                    hg_statuses[players[i]]['inv'].append(action.give[i])


def generate_player_status_phase(hg_dict, previous_time_best_place):
    """
    Generates the entire player status phase.

    Args:
        hg_dict (dict) : The full game dict.
        previous_time_best_place (int) : The best place last time.
                                         Any players who place higher than this number will be 'newly dead' as opposed
                                         to just dead.
    """
    # Get the phase.
    phase = get_phase_by_category('status')

    # Generate the player status numbers.
    # For each index, 0 = alive, 1 = dead, 2 = newly dead.
    player_statuses = [((1 if player['placement'] < previous_time_best_place else 2) if player['dead'] else 0)
                       for player in hg_dict['statuses']]
    new_deaths = len([num for num in player_statuses if num == 2])

    # Insert the new phase into the database.
    hg_dict['phases'].append(
        ('status', database.insert_into_database(
            database.HG_CURRENT_GAME_PHASES_TABLE, type=phase.type,
            title=phase.title.format(new_deaths, 's' if new_deaths != 1 else ''), player_statuses=player_statuses
        ).game_phase_id, 1)
    )


def generate_game_over(hg_dict):
    """
    Detects whether the game is over or not.

    Arguments:
        hg_dict (dict) : The full game dict.

    Returns:
        bool : Whether the game is over or not.
    """
    return len([player for player in hg_dict['statuses'] if not player['dead']]) < 2


def generate_placement_kill_count_phase(hg_dict, do_placement):
    """
    Generates the entire placement / kill count phase.

    Args:
        hg_dict (dict) : The full game dict.
        do_placement (bool) : Whether to do placement or kill count.
    """
    # Get the phase.
    phase = get_phase_by_category('placement' if do_placement else 'kills')

    # Simply grab the player placements.
    player_placements = [player['placement' if do_placement else 'kills'] for player in hg_dict['statuses']]

    # If we're doing placements and we have any that's greater than the max_gamesize, then set that to 1.
    if do_placement:
        for i in range(len(player_placements)):
            if player_placements[i] > HG_MAX_GAMESIZE:
                player_placements[i] = 1

    # Insert the new phase into the database.
    hg_dict['phases'].append(
        ('place' if do_placement else 'kills', database.insert_into_database(
            database.HG_CURRENT_GAME_PHASES_TABLE, type=phase.type,
            title=phase.title, player_statuses=player_placements
        ).game_phase_id, 1)
    )


def get_phase_by_category(phase_category):
    """
    Gets a random phase that matches by category.

    Arguments
        phase_category (str) : The phase category to search by.

    Returns:
        hg_phases database table : One phase.
    """
    # Simple return statement.
    return random.choice([phase for phase in database.get_filtered_by(database.HG_PHASES_TABLE, category=phase_category)])


def get_normal_actions_by_phase(phase, extra_players=None):
    """
    Gets all the normal actions, combined with their action wrappers, that belong to the parent phase.

    Arguments
        phase (hg_phases database table) : The parent phase.

    Returns:
        (hg_action_wrappers + hg_actions database table)[] : The normal action wrappers,
                                                             joined with the actions they're wrapping.
    """
    # If extra_players was provided, then filter_by by it.
    if isinstance(extra_players, int):
        return [action for action in database.filter_by(
            database.join(
                database.get_filtered_by(database.HG_ACTIONS_TABLE, extra_players=extra_players),
                (
                    database.HG_ACTION_WRAPPERS_TABLE,
                    database.HG_ACTION_WRAPPERS_TABLE.single_action_id == database.HG_ACTIONS_TABLE.action_id
                )
            ),
            parent_phase_id=phase.phase_id
        )]

    # Otherwise, just do a simple return.
    return [action for action in database.get_filtered_by_joined(
        database.HG_ACTIONS_TABLE,
        (
            database.HG_ACTION_WRAPPERS_TABLE,
            database.HG_ACTION_WRAPPERS_TABLE.single_action_id == database.HG_ACTIONS_TABLE.action_id
        ),
        parent_phase_id=phase.phase_id
    )]


def get_trigger_actions_by_phase(phase):
    """
    Gets all trigger action wrappers, with their success and fail actions slapped on as attributes.

    Arguments
        phase (hg_phases database table) : The parent phase.

    Returns:
        (hg_action_wrappers database table)[] : The normal action wrappers, joined with the actions they're wrapping.
    """
    # First, get the trigger actions.
    trigger_action_wrappers = [action_wrapper for action_wrapper in
                               database.get_filtered_by(database.HG_ACTION_WRAPPERS_TABLE,
                                                        parent_phase_id=phase.phase_id, type='trigger')]

    # Next, iterate through the trigger actions and get each child action, if any.
    for action_wrapper in trigger_action_wrappers:

        # Success actions
        if action_wrapper.success_action_ids:
            action_wrapper.success_actions = []
            for action_query in [database.get_filtered_by(database.HG_ACTIONS_TABLE, action_id=success_action_id)
                                 for success_action_id in action_wrapper.success_action_ids]:
                action_wrapper.success_actions += [action for action in action_query]

        # Failure actions
        if action_wrapper.failure_action_ids:
            action_wrapper.failure_actions = []
            for action_query in [database.get_filtered_by(database.HG_ACTIONS_TABLE, action_id=failure_action_id)
                                 for failure_action_id in action_wrapper.failure_action_ids]:
                action_wrapper.failure_actions += [action for action in action_query]

    # Return.
    return trigger_action_wrappers


def get_current_game_phase_by_id(game_phase_id):
    """
    Gets the current game phase that matches the given game_phase_id.

    Arguments
        game_phase_id (id) : The game phase id.

    Returns:
        hg_current_game_phases database table : One current game phase.
    """
    # Simple return statement.
    return database.get_filtered_by(database.HG_CURRENT_GAME_PHASES_TABLE, game_phase_id=game_phase_id).first()


def get_current_game_actions_by_current_game_phase_and_action_indexes(phase_object, action_min_index, action_max_index):
    """
    Gets the current game actions belonging to the given current game phase whose indexes are between the
    action_min_index and action_max_index.

    Arguments
        game_phase_id (id) : The game phase id.

    Returns:
        hg_current_game_phases database table : One current game phase.
    """
    # First, get all the current game actions by the current game phase.
    current_game_actions = [
        database.get_filtered_by(database.HG_CURRENT_GAME_ACTIONS_TABLE, game_action_id=game_action_id).first()
        for game_action_id in phase_object.game_action_ids[action_min_index:action_max_index + 1]]

    # Next, get all the actions they reference and put the text on the respective current_game_actions.
    for game_action in current_game_actions:
        game_action.text = database.get_filtered_by(
            database.HG_ACTIONS_TABLE, action_id=game_action.action_id).first().text

    # Return.
    return current_game_actions


async def pregame_shuffle(message, player_count, hg_dict):
    """
    Shuffles a pregame hunger games cast.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        player_count (int) : The amount of players to use.
        hg_dict (dict) : The full game dict.
    """
    # Retire the existing players' profile pictures (but add a shuffle checkout that will be removed later to prevent
    # from reloading repeat players).
    if 'players' in hg_dict:
        temp_files.checkout_profile_picture_by_user_bulk(hg_dict['players'], message, 'hg_shuffle')
        temp_files.retire_profile_picture_by_user_id_bulk(hg_dict['players'], message, 'hg_filehold')

    # If the player count is more than the max or less than the minimum, set them to their capstone values.
    player_count = min(player_count, HG_MAX_GAMESIZE)
    player_count = max(player_count, HG_MIN_GAMESIZE)

    # Get the user list. If user list is < player_count people, we add bots as well.
    try:
        user_list = discord_info.get_applicable_users(message, exclude_bots=True)
        uses_bots = False
        if len(user_list) < player_count:
            user_list = discord_info.get_applicable_users(message, exclude_bots=False)
            uses_bots = True

    # If we can't access the userlist, send an error.
    except CannotAccessUserlistError:
        logging.error(message, 'requested hunger games, failed to access the userlist')
        await messaging.send_text_message(message, 'There was an error accessing the userlist. Try again later.')

        # Return False to signal failure.
        return False

    # Otherwise, we generate the players and ask if we should proceed.
    hg_players = []
    # Chooses a random player from the roster until we're out of players or we've reached the normal amount.
    for i in range(min(player_count, len(user_list))):
        next_player = random.choice(user_list)
        hg_players.append(next_player)
        user_list.remove(next_player)

    # Checkout file holdings for all the profile pictures and retire the shuffle checkout.
    await temp_files.checkout_profile_picture_by_user_bulk_with_typing(hg_players, message, 'hg_filehold')
    temp_files.retire_profile_picture_by_user_bulk(hg_players, message, 'hg_shuffle')

    # Set in players and bot bool.
    hg_dict['players'] = hg_players
    hg_dict['uses_bots'] = uses_bots

    # Return True to signal success.
    return True


def initialize():
    """
    Initializes the command.
    """
    # Sets some global variables using environment.get
    global EXPIRE_SECONDS
    EXPIRE_SECONDS = environment.get('HUNGER_GAMES_EXPIRE_SECONDS')


# Command values
PUBLIC_COMMAND_DICT = {
    'hg': hunger_games_start,
    'hunger': hunger_games_start,
    'hungergames': hunger_games_start,
    'hungry': hunger_games_start,
    'hungrygames': hunger_games_start,
    'hgames': hunger_games_start
}
REACTIVE_COMMAND_LIST = [
    hunger_games_update,
    hunger_games_detect_expiration
]
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'hungergames',
        'category': 'fun_interactive',
        'description': 'Simulates the Hunger Games simulator, using users in this Discord chat. One per channel.',
        'examples': [('hungergames', 'Generates a Hunger Games with 24 players.'),
                     ('hungergames 64', 'Generates a Hunger Games with 64 players.')],
        'aliases': ['hg', 'hunger', 'hgames'],
        'usages': ['hungergames', 'hungergames < # of players >'],
        'restrictions': ["Can't be used in DMs.", "Minimum of 2 players.", "Maximum of 64 players."],
        'reactive commands': [('a', 'Add a random player to the game. (Pregame)'),
                              ('a < player >', 'Add a specific player to the game. (Pregame)'),
                              ('d', 'Remove the last player from the game. (Pregame)'),
                              ('d < player >', 'Remove a specific player from the game. (Pregame)'),
                              ('s', 'Shuffle around the players in the game. (Pregame, Postgame)'),
                              ('s < # of players >', 'Shuffle around the specified number of players into the game. '
                                                     '(Pregame, Postgame)'),
                              ('b', 'Toggle the participation of bots in the game. (Pregame)'),
                              ('p', 'Begin the game. (Pregame)'),
                              ('n', 'Display the next action. (Midgame, Postgame)'),
                              ('n < # of actions >', 'Display the next variable number of actions. '
                                                     '(Midgame, Postgame)'),
                              ('p', 'Display the previous action. (Midgame, Postgame)'),
                              ('p < # of actions >', 'Display the previous variable number of actions. '
                                                     '(Midgame, Postgame)'),
                              ('r', 'Replay the game with the same players. (Postgame)'),
                              ('c', 'Cancel the game. (Pregame, Midgame, Postgame)'),
                              ('y', 'Confirm cancel. (Pregame, Postgame)'),
                              ('n', 'Abort cancel. (Pregame, Postgame)')]
    }
]


# Unfortunately, one or two variables have to be established all the way down here.
HG_PREGAME_SHUFFLE_TERMS = ['s', 'shuffle'] + [GLOBAL_PREFIX + command for command in PUBLIC_COMMAND_DICT]
HG_MIDGAME_BE_PATIENT_TERMS = [GLOBAL_PREFIX + command for command in PUBLIC_COMMAND_DICT]
HG_POSTGAME_NEW_GAME_TERMS = HG_PREGAME_SHUFFLE_TERMS

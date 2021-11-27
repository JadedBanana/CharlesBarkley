# =================================================================
#                         FUN COMMANDS
# =================================================================
from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageFilter
from datetime import datetime, timedelta
from lib.util.exceptions import *
import constants
import requests
import discord
import random
from lib.util import misc
import os

# Logger
log = None





def hunger_games_makeimage_pfp(playerid, image, drawer, pfp_x, pfp_y, dead=False):
    """
    Draws a player's pfp at the given x and y.
    """
    # Gathers the profile picture.
    player_pfp = misc.get_profile_picture(playerid, True)[0]
    player_pfp = player_pfp.resize((constants.HG_ICON_SIZE, constants.HG_ICON_SIZE), Image.LANCZOS if player_pfp.width > constants.HG_ICON_SIZE else Image.NEAREST)
    # If player dead, recolor to black and white.
    if dead:
        player_pfp = ImageOps.colorize(player_pfp.convert('L'), black=(0, 0, 0), white=misc.multiply_color_tuple((255, 255, 255), constants.HG_STATUS_DEAD_PFP_DARKEN_FACTOR), mid=misc.multiply_color_tuple((128, 128, 128), constants.HG_STATUS_DEAD_PFP_DARKEN_FACTOR))
    image.paste(player_pfp, (pfp_x, pfp_y))
    # Draws border around player icons.
    drawer.line([(pfp_x - 1, pfp_y - 1), (pfp_x + constants.HG_ICON_SIZE, pfp_y - 1), (pfp_x + constants.HG_ICON_SIZE, pfp_y + constants.HG_ICON_SIZE), (pfp_x - 1, pfp_y + constants.HG_ICON_SIZE), (pfp_x - 1, pfp_y - 1)], width=1, fill=0)


def hunger_games_makeimage_action_text(remaining_text, players, drawer, txt_x, txt_y, action_font):
    while remaining_text:
        # Get the index of the NEXT {n}.
        next_bracket = len(remaining_text)
        for ind in range(len(players)):
            bracket_pos = remaining_text.find('{' + str(ind) + '}')
            if not bracket_pos + 1:
                continue
            next_bracket = min(next_bracket, bracket_pos)

        # Draw the text up to the next bracket.
        drawer.text((txt_x, txt_y), remaining_text[:next_bracket], font=action_font, fill=(255, 255, 255))
        txt_x+= action_font.getsize(remaining_text[:next_bracket])[0]

        # Draw the next player name.
        if next_bracket == len(remaining_text):
            break
        ind = int(remaining_text[next_bracket + 1])
        drawer.text((txt_x, txt_y), players[ind][1], font=action_font, fill=constants.HG_ACTION_PLAYER_COLOR)
        txt_x+= action_font.getsize(players[ind][1])[0]

        # Trim remaining_text.
        remaining_text = remaining_text[next_bracket + 3:]


def hunger_games_makeimage_player_statuses(players, placement=False, kills=False):
    """
    Generates a player status image.
    The players should be a 2-dimensional list with each entry as:
    1. User ID (number)
    2. User name / nick
    3. Status (int, 0 = alive, 1 = newly dead, 2 = dead)
    This can also be used to make player placement images and kill count lists.
    """
    # Splits all the players into their own rows.
    players_split = []
    current_split = []
    for player in players:
        if len(current_split) == constants.HG_PLAYERSTATUS_WIDTHS[len(players)]:
            players_split.append(current_split)
            current_split = []
        current_split.append(player)
    players_split.append(current_split)

    # Preps to draw.
    image_width = constants.HG_ICON_SIZE * len(players_split[0]) + constants.HG_ICON_BUFFER * (len(players_split[0]) + 1)
    image_height = constants.HG_PLAYERSTATUS_ROWHEIGHT * len(players_split) + constants.HG_ICON_BUFFER * (len(players_split) + 1)
    player_statuses = Image.new('RGB', (image_width, image_height), constants.HG_BACKGROUND_COLOR)
    player_drawer = ImageDraw.Draw(player_statuses)
    player_font = ImageFont.truetype(constants.HG_PLAYERNAME_FONT, size=constants.HG_FONT_SIZE)

    # Draws each row, one after another.
    current_y = constants.HG_ICON_BUFFER
    for split in players_split:
        current_x = int((image_width - (len(split) * constants.HG_ICON_SIZE + (len(split) - 1) * constants.HG_ICON_BUFFER)) / 2)
        for player in split:
            # Gets pfp, pastes onto image.
            hunger_games_makeimage_pfp(player[0], player_statuses, player_drawer, current_x, current_y, player[2] and not placement and not kills)

            # Writes name and status / placement.
            player_name = player[1]
            # If the name is too long, we put a ... at the end (thx alex!!!!!)
            if player_font.getsize(player_name)[0] > constants.HG_ICON_SIZE:
                while player_font.getsize(player_name + '...')[0] > constants.HG_ICON_SIZE:
                    player_name = player_name[:-1]
                player_name+= '...'
            player_drawer.text((current_x + int(constants.HG_ICON_SIZE / 2 - player_font.getsize(player_name)[0] / 2), current_y + constants.HG_ICON_SIZE + constants.HG_TEXT_BUFFER), player_name, font=player_font, fill=(255, 255, 255))
            # Placement
            if placement:
                place = str(player[2]) + constants.NTH_SUFFIXES[player[2] % 10] + ' Place'
                player_drawer.text((current_x + int(constants.HG_ICON_SIZE / 2 - player_font.getsize(place)[0] / 2), current_y + constants.HG_ICON_SIZE + constants.HG_FONT_SIZE + constants.HG_TEXT_BUFFER), place, font=player_font, fill=misc.find_color_tuple_midpoint_hsv(constants.HG_STATUS_ALIVE_COLOR, constants.HG_STATUS_DEAD_COLOR, (player[2] - 1) / placement))
            # Killcount
            elif kills:
                if isinstance(kills, int):
                    kill_str = str(player[2]) + (' Kill' if player[2] == 1 else ' Kills')
                    player_drawer.text((current_x + int(constants.HG_ICON_SIZE / 2 - player_font.getsize(kill_str)[0] / 2), current_y + constants.HG_ICON_SIZE + constants.HG_FONT_SIZE + constants.HG_TEXT_BUFFER), kill_str, font=player_font, fill=misc.find_color_tuple_midpoint_hsv(constants.HG_STATUS_DEAD_COLOR, constants.HG_STATUS_ALIVE_COLOR, player[2] / kills))
                else:
                    kill_str = '0 Kills'
                    player_drawer.text((current_x + int(constants.HG_ICON_SIZE / 2 - player_font.getsize(kill_str)[0] / 2), current_y + constants.HG_ICON_SIZE + constants.HG_FONT_SIZE + constants.HG_TEXT_BUFFER), kill_str, font=player_font, fill=constants.HG_STATUS_DEAD_COLOR)
            # Status
            else:
                status = 'Alive' if not player[2] else ('Deceased' if player[2] - 1 else 'Newly Deceased')
                player_drawer.text((current_x + int(constants.HG_ICON_SIZE / 2 - player_font.getsize(status)[0] / 2), current_y + constants.HG_ICON_SIZE + constants.HG_FONT_SIZE + constants.HG_TEXT_BUFFER), status, font=player_font, fill=constants.HG_STATUS_ALIVE_COLOR if not player[2] else constants.HG_STATUS_DEAD_COLOR)

            # Adds to current_x.
            current_x+= constants.HG_ICON_SIZE + constants.HG_ICON_BUFFER

        # Adds to current_y.
        current_y+= constants.HG_PLAYERSTATUS_ROWHEIGHT + constants.HG_ICON_BUFFER

    return player_statuses


def hunger_games_makeimage_winner(players, desc=None):
    """
    Displays the winner(s).
    Like the makeimage_action method, but without all the previous and count and whatnot.
    """
    # Makes the font
    action_font = ImageFont.truetype(constants.HG_PLAYERNAME_FONT, size=constants.HG_FONT_SIZE)

    # Gets action desc width, if any.
    action_desc_width = action_font.getsize(desc)[0]

    # Gets the image width.
    # Also makes the full action text while we're at it.
    image_width = action_desc_width + constants.HG_ICON_BUFFER * 2 + constants.HG_HEADER_BORDER_BUFFER * 2 if desc else -1
    image_height = constants.HG_ACTION_ROWHEIGHT + constants.HG_ICON_BUFFER + (constants.HG_FONT_SIZE + constants.HG_HEADER_BORDER_BUFFER * 3 if desc else -1)

    # Tests for text boundaries
    # Text varies depending on how many winners there are.
    if len(players) > 1:
        full_action_text = constants.HG_TIE_EVENT[0]
        if len(players) > 2:
            for player in players[:-1]:
                full_action_text+= player[1] + constants.HG_TIE_EVENT[1]
        else:
            full_action_text+= players[0][1] + ' '
        full_action_text+= constants.HG_TIE_EVENT[2] + players[-1][1] + constants.HG_TIE_EVENT[3]
    else:
        full_action_text = constants.HG_WINNER_DEAD_EVENT if players[0][2] else constants.HG_WINNER_EVENT
        full_action_text = full_action_text.replace('{0}', players[0][1])
    text_width = action_font.getsize(full_action_text)[0]
    image_width = max(image_width, text_width + constants.HG_ICON_BUFFER * 2)
    # Tests for image boundaries
    image_width = max(image_width, constants.HG_ICON_SIZE * len(players) + constants.HG_ICON_BUFFER * (len(players) + 1))

    # Preps to draw.
    action_image = Image.new('RGB', (image_width, image_height), constants.HG_BACKGROUND_COLOR)
    player_drawer = ImageDraw.Draw(action_image)
    current_y = constants.HG_ICON_BUFFER

    # Draw the description, if any.
    if desc:
        current_x = int((image_width - action_desc_width) / 2)
        player_drawer.rectangle(
            [(current_x - constants.HG_HEADER_BORDER_BUFFER, current_y - constants.HG_HEADER_BORDER_BUFFER),
             (current_x + action_desc_width + constants.HG_HEADER_BORDER_BUFFER, current_y + constants.HG_FONT_SIZE + constants.HG_HEADER_BORDER_BUFFER)],
            constants.HG_HEADER_BACKGROUND_COLOR,
            constants.HG_HEADER_BORDER_COLOR
        )
        player_drawer.text((current_x, constants.HG_ICON_BUFFER), desc, font=action_font, fill=constants.HG_HEADER_TEXT_COLOR)
        current_y+= constants.HG_FONT_SIZE + constants.HG_HEADER_BORDER_BUFFER * 3

    # Draw the icons.
    current_x = int(image_width / 2) - int(len(players) / 2 * constants.HG_ICON_SIZE) - int((len(players) - 1) / 2 * constants.HG_ICON_BUFFER)
    # Gets each player's pfp and pastes it onto the image.
    for player in players:
        hunger_games_makeimage_pfp(player[0], action_image, player_drawer, current_x, current_y, player[2])
        current_x+= constants.HG_ICON_SIZE + constants.HG_ICON_BUFFER

    # Draws each part of the text.
    # Text varies depending on how many winners there are.
    # More than 1:
    if len(players) > 1:
        current_x = int((image_width - text_width) / 2)
        current_y += constants.HG_ICON_SIZE + constants.HG_TEXT_BUFFER
        remaining_text = [constants.HG_TIE_EVENT[0]]
        if len(players) > 2:
            for player in players[:-1]:
                remaining_text.append(player[1])
                remaining_text.append(constants.HG_TIE_EVENT[1])
            remaining_text[-1]+= constants.HG_TIE_EVENT[2]
        else:
            remaining_text.append(players[0][1] + ' ')
            remaining_text.append(constants.HG_TIE_EVENT[2])
        remaining_text.append(players[-1][1])
        remaining_text.append(constants.HG_TIE_EVENT[3])
        while remaining_text:
            # Draw the text up to the next bracket.
            player_drawer.text((current_x, current_y), remaining_text[0], font=action_font, fill=(255, 255, 255))
            current_x += action_font.getsize(remaining_text[0])[0]
            remaining_text.remove(remaining_text[0])
            if not remaining_text:
                break

            # Draw the next player name.
            player_drawer.text((current_x, current_y), remaining_text[0], font=action_font, fill=constants.HG_ACTION_PLAYER_COLOR)
            current_x += action_font.getsize(remaining_text[0])[0]
            remaining_text.remove(remaining_text[0])

    # Only 1:
    else:
        # Draws each part of the text.
        current_x = int((image_width - text_width) / 2)
        current_y += constants.HG_ICON_SIZE + constants.HG_TEXT_BUFFER
        hunger_games_makeimage_action_text(constants.HG_WINNER_DEAD_EVENT if players[0][2] else constants.HG_WINNER_EVENT, players, player_drawer, current_x, current_y, action_font)

    return action_image


def hunger_games_makeimage_action(actions, start, count=1, action_desc=None):
    """
    Displays count number of actions at once.
    """
    # Makes the font
    action_font = ImageFont.truetype(constants.HG_PLAYERNAME_FONT, size=constants.HG_FONT_SIZE)

    # Gets action desc width, if any.
    action_desc_width = action_font.getsize(action_desc)[0] if action_desc else 0

    # Gets the image width.
    # Also makes the full action text while we're at it.
    image_width = action_desc_width + constants.HG_ICON_BUFFER * 2 + constants.HG_HEADER_BORDER_BUFFER * 2 if action_desc else -1
    image_height = constants.HG_ACTION_ROWHEIGHT * count + constants.HG_ICON_BUFFER + (constants.HG_FONT_SIZE + constants.HG_HEADER_BORDER_BUFFER * 3 if action_desc else -1)
    text_sizes = []

    for ind in range(start, start + count):
        # Tests for text boundaries
        full_action_text = actions[ind]['act']
        for ind2 in range(len(actions[ind]['players'])):
            full_action_text = full_action_text.replace('{' + str(ind2) + '}', actions[ind]['players'][ind2][1])
        # Calculates text widths and appends them to the text_sizes list.
        text_width = action_font.getsize(full_action_text)[0]
        image_width = max(image_width, text_width + constants.HG_ICON_BUFFER * 2)
        text_sizes.append(text_width)
        # Tests for image boundaries
        image_width = max(image_width, constants.HG_ICON_SIZE * len(actions[ind]['players']) + constants.HG_ICON_BUFFER * (len(actions[ind]['players']) + 1))

    # Preps to draw.
    action_image = Image.new('RGB', (image_width, image_height), constants.HG_BACKGROUND_COLOR)
    player_drawer = ImageDraw.Draw(action_image)
    current_y = constants.HG_ICON_BUFFER

    # Draw the description, if any.
    if action_desc:
        current_x = int((image_width - action_desc_width) / 2)
        player_drawer.rectangle(
            [(current_x - constants.HG_HEADER_BORDER_BUFFER, current_y - constants.HG_HEADER_BORDER_BUFFER),
             (current_x + action_desc_width + constants.HG_HEADER_BORDER_BUFFER, current_y + constants.HG_FONT_SIZE + constants.HG_HEADER_BORDER_BUFFER)],
            constants.HG_HEADER_BACKGROUND_COLOR,
            constants.HG_HEADER_BORDER_COLOR
        )
        player_drawer.text((current_x, constants.HG_ICON_BUFFER), action_desc, font=action_font, fill=constants.HG_HEADER_TEXT_COLOR)
        current_y+= constants.HG_FONT_SIZE + constants.HG_HEADER_BORDER_BUFFER * 3

    # Draw the icons.
    num = 0
    for ind in range(start, start + count):
        current_x = int(image_width / 2) - int(len(actions[ind]['players']) / 2 * constants.HG_ICON_SIZE) - int((len(actions[ind]['players']) - 1) / 2 * constants.HG_ICON_BUFFER)
        # Gets each player's pfp and pastes it onto the image.
        for player in actions[ind]['players']:
            hunger_games_makeimage_pfp(player[0], action_image, player_drawer, current_x, current_y)
            current_x+= constants.HG_ICON_SIZE + constants.HG_ICON_BUFFER

        # Draws each part of the text.
        current_x = int((image_width - text_sizes[num]) / 2)
        current_y+= constants.HG_ICON_SIZE + constants.HG_TEXT_BUFFER
        hunger_games_makeimage_action_text(actions[ind]['act'], actions[ind]['players'], player_drawer, current_x, current_y, action_font)

        # Adds to the current_y and num.
        current_y+= constants.HG_FONT_SIZE + constants.HG_ICON_BUFFER
        num+= 1

    return action_image


def hunger_games_generate_statuses(hg_statuses, action):
    """
    Updates the statuses of players post-action in the hg_dict.
    """
    # First, we handle deaths.
    if 'kill' in action['full']:
        for ind in action['full']['kill']:
            hg_statuses[action['players'][ind][0]]['dead'] = True
        for ind in action['full']['kill']:
            hg_statuses[action['players'][ind][0]]['dead_num'] = [hg_statuses[player]['dead'] for player in hg_statuses].count(True) - 1

    # Next, injuries.
    if 'hurt' in action['full']:
        for ind in action['full']['hurt']:
            hg_statuses[action['players'][ind][0]]['hurt'] = True

    # Kill credit.
    if 'credit' in action['full']:
        for ind in action['full']['credit']:
            hg_statuses[action['players'][ind][0]]['kills']+= 1

    # Healing.
    if 'heal' in action['full']:
        for ind in action['full']['heal']:
            hg_statuses[action['players'][ind][0]]['hurt'] = False

    # Items.
    if 'give' in action:
        for ind in range(len(action['give'])):
            # Item 0.
            if action['give'][ind] == 0:
                continue
            elif action['give'][ind] < 0:
                hg_statuses[action['players'][ind][0]]['inv'].remove(-action['give'][ind])
            else:
                # Special items
                # 3000, 1 - 3 random items
                if action['full']['give'][ind] == 3000:
                    for i in range(random.randint(1, 3)):
                        hg_statuses[action['players'][ind][0]]['inv'].append(random.choice(constants.HG_ALL_ITEMS))
                elif action['full']['give'][ind] == 4000:
                    hg_statuses[action['players'][ind][0]]['inv'].append(random.choice(constants.HG_WEAPON_ITEMS))
                    hg_statuses[action['players'][ind][0]]['inv'].append(random.choice(constants.HG_HEALTH_ITEMS))
                    hg_statuses[action['players'][ind][0]]['inv'].append(random.choice(constants.HG_FOOD_ITEMS))
                elif action['full']['give'][ind] == 8888:
                    hg_statuses[action['players'][ind][0]]['inv'].remove(8)
                    hg_statuses[action['players'][ind][0]]['inv'].append(10)
                    hg_statuses[action['players'][ind][0]]['inv'].append(104)
                elif action['full']['give'][ind] == 9999:
                    ind2 = 0
                    for item in hg_statuses[action['players'][ind][0]]['inv']:
                        hg_statuses[action['players'][ind][0]]['inv'].remove(item)
                        if ind2 % len(action['players']) == ind:
                            ind2+= 1
                        hg_statuses[action['players'][ind2][0]]['inv'].append(item)
                        ind2+= 1
                else:
                    hg_statuses[action['players'][ind][0]]['inv'].append(action['give'][ind])

    del action['full']

def hunger_games_generate_bloodbath(hg_dict):
    """
    Generates all the actions for each player in the bloodbath.
    """
    player_actions = [uid for uid in hg_dict['statuses']]
    actions = []

    # Iterates through all the actions, picking them at random for the player_actions.
    while player_actions:
        # Creates necessary prerequisites for do while loop.
        curr_action = {'players': len(player_actions)}
        chosen_players = [random.choice(player_actions)]
        player_actions.remove(chosen_players[0])

        # While loop, finds a good action.
        while curr_action['players'] > len(player_actions):
            curr_action = random.choice(constants.HG_BLOODBATH_ACTIONS)

        # Adds more players to current action.
        for i in range(curr_action['players']):
            chosen_players.append(random.choice(player_actions))
            player_actions.remove(chosen_players[-1])

        # Add the actions to the list.
        actions.append({'players': [(player, hg_dict['statuses'][player]['name']) for player in chosen_players], 'act': curr_action['act'], 'full': curr_action})

        # Generate statuses
        hunger_games_generate_statuses(hg_dict['statuses'], actions[-1])

    # Adds to the phases.
    hg_dict['phases'].append({'type': 'act', 'act': actions, 'title': 'The Bloodbath', 'next': 1, 'prev': -1, 'desc': 'As the tributes stand upon their podiums, the horn sounds.', 'done': False})


def hunger_games_generate_normal_actions(hg_dict, action_dict, title, desc=None):
    """
    Generates all the actions for each player in the a normal action round.
    """
    player_actions = []
    for uid in hg_dict['statuses']:
        if not hg_dict['statuses'][uid]['dead']:
            player_actions.append(uid)
    actions = []

    # Iterates through triggers.
    for trigger in action_dict['trigger']:
        pass

    # Iterates through all the actions, picking them at random for the player_actions.
    while player_actions:
        # Creates necessary prerequisites for do while loop.
        curr_action = {'players': len(player_actions)}
        chosen_players = [random.choice(player_actions)]
        player_actions.remove(chosen_players[0])

        # While loop, finds a good action.
        while curr_action['players'] > len(player_actions):
            curr_action = random.choice(action_dict['normal'])

        # Adds more players to current action.
        for i in range(curr_action['players']):
            chosen_players.append(random.choice(player_actions))
            player_actions.remove(chosen_players[-1])

        # Add the actions to the list.
        actions.append({'players': [(player, hg_dict['statuses'][player]['name']) for player in chosen_players], 'act': curr_action['act'], 'full': curr_action})

    # Shuffles the actions and generates statuses.
    random.shuffle(actions)
    for curr_action in actions:
        hunger_games_generate_statuses(hg_dict['statuses'], curr_action)

    # Adds to the phases.
    if not desc:
        desc = title
    hg_dict['phases'].append({'type': 'act', 'act': actions, 'title': title, 'next': 0, 'prev': -1, 'desc': desc, 'done': False})


def hunger_games_generate_detect_dead(hg_dict):
    """
    Test for dead people.
    """
    everyone_dead = True
    two_alive = False
    for player in hg_dict['statuses']:
        if not hg_dict['statuses'][player]['dead']:
            if not everyone_dead:
                two_alive = True
                break
            else:
                everyone_dead = False
    return everyone_dead, two_alive


async def hunger_games_generate_full_game(hg_dict, message):
    """
    Generates an entire Hunger Games from the users specified in the hg_dict.
    Depends on external methods to do most of the dirty work.
    """
    # Get rid of redundant tag.
    del hg_dict['uses_bots']

    # Create player statuses.
    statuses = {}
    for player in hg_dict['players']:
        statuses[str(player.id)] = {'name': player.nick if player.nick else player.name, 'dead': False, 'hurt': False, 'inv': [], 'kills': 0}
    hg_dict['statuses'] = statuses

    # Makes the phases.
    hg_dict['phases'] = []

    # First, we have the bloodbath.
    hunger_games_generate_bloodbath(hg_dict)

    # Loop variables.
    daynight = 1
    turns_since_event = 0
    dead_last_loop = []

    # Then we cycle through stuff until one person survives or EVERYONE is dead.
    while True:
        # Test for dead people.
        tie, continue_game = hunger_games_generate_detect_dead(hg_dict)
        if not continue_game:
            break

        # Test for event.
        if daynight >= 4 and turns_since_event > 1 and random.random() < 1 - (1 - constants.HG_EVENT_DEFAULT_CHANCE)**turns_since_event:
            the_event = random.choice(constants.HG_EVENTS)
            hunger_games_generate_normal_actions(hg_dict, the_event[0], the_event[1], the_event[2])
            turns_since_event = 0

        # Otherwise, do day and night.
        else:
            # Day.
            hunger_games_generate_normal_actions(hg_dict, constants.HG_NORMAL_DAY_ACTIONS, 'Day {}'.format(daynight))

            # Test for dead people.
            tie, continue_game = hunger_games_generate_detect_dead(hg_dict)
            if not continue_game:
                break

            # Night.
            hunger_games_generate_normal_actions(hg_dict, constants.HG_NORMAL_NIGHT_ACTIONS, 'Night {}'.format(daynight))
            daynight+= 1

            if daynight >= 4:
                turns_since_event += 1

        # Test for dead people.
        tie, continue_game = hunger_games_generate_detect_dead(hg_dict)
        if not continue_game:
            break

        # Do player statuses.
        player_statuses = []
        new_deaths = 0
        for player in hg_dict['statuses']:
            player_statuses.append((player, hg_dict['statuses'][player]['name'], (2 if player in dead_last_loop else 1) if hg_dict['statuses'][player]['dead'] else 0))
            if player not in dead_last_loop and hg_dict['statuses'][player]['dead']:
                dead_last_loop.append(player)
                new_deaths+= 1
        hg_dict['phases'].append({'type': 'status', 'all': player_statuses, 'new': new_deaths})

        # Increase chances of encountering disaster next time.
        if daynight >= 4:
            turns_since_event+= 1

    # Now that the loop is broken, display cannon shots and declare winner.
    player_statuses = []
    new_deaths = 0
    for player in hg_dict['statuses']:
        player_statuses.append((player, hg_dict['statuses'][player]['name'], (2 if player in dead_last_loop else 1) if hg_dict['statuses'][player]['dead'] else 0))
        if player not in dead_last_loop and hg_dict['statuses'][player]['dead']:
            dead_last_loop.append(player)
            new_deaths+= 1
    hg_dict['phases'].append({'type': 'status', 'all': player_statuses, 'new': new_deaths})

    if tie:
        # Determine who tied
        tiees = []
        max_deathnum = -1
        for player in hg_dict['statuses']:
            if hg_dict['statuses'][player]['dead_num'] > max_deathnum:
                max_deathnum = hg_dict['statuses'][player]['dead_num']
        for player in hg_dict['statuses']:
            if max_deathnum == hg_dict['statuses'][player]['dead_num']:
                tiees.append(player)
        # Add tie phase to phases ONLY if there's more than one.
        if len(tiees) > 1:
            hg_dict['phases'].append({'type': 'tie', 'players': [(tienum, hg_dict['statuses'][tienum]['name'], True) for tienum in tiees], 'title': constants.HG_TIE_TITLE, 'desc': constants.HG_TIE_TITLE})
        # Otherwise, it's a victory, but dead.
        else:
            hg_dict['phases'].append({'type': 'win', 'players': [(tiees[0], hg_dict['statuses'][tiees[0]]['name'], True)], 'title': constants.HG_WINNER_TITLE, 'desc': constants.HG_WINNER_TITLE})

    else:
        # Determine winner
        winner = None
        for player in hg_dict['statuses']:
            if not 'dead_num' in hg_dict['statuses'][player]:
                winner = player
                break
        # Add win phase to phases
        hg_dict['phases'].append({'type': 'win', 'players': [(winner, hg_dict['statuses'][winner]['name'], False)], 'title': constants.HG_WINNER_TITLE, 'desc': constants.HG_WINNER_TITLE})

    # Makes the placement screen
    pre_placement_players = [k for k in hg_dict['statuses']]
    placements = []
    while pre_placement_players:
        min_placement = len(hg_dict['statuses'])
        current_placement_players = []
        for player in pre_placement_players:
            if 'dead_num' in hg_dict['statuses'][player]:
                if min_placement > hg_dict['statuses'][player]['dead_num']:
                    current_placement_players = [player]
                    min_placement = hg_dict['statuses'][player]['dead_num']
                elif min_placement == hg_dict['statuses'][player]['dead_num']:
                    current_placement_players.append(player)
        # If there is no change in min_placement, then the victor is found.
        if min_placement == len(hg_dict['statuses']):
            current_placement_players = pre_placement_players
            min_placement-= 1
        # Adds player to the dict.
        for player in current_placement_players:
            placements.append((player, hg_dict['statuses'][player]['name'], len(hg_dict['statuses']) - min_placement))
            pre_placement_players.remove(player)
    # Reverses placements list to sort from first to last and makes it a phase
    placements.reverse()
    hg_dict['phases'].append({'type': 'place', 'all': placements, 'max': max([place[2] for place in placements]) - 1})

    # Makes the kill screen pretty much the same way as the placement screen.
    pre_placement_players = [k for k in hg_dict['statuses']]
    kill_placements = []
    while pre_placement_players:
        max_placement = 0
        current_placement_players = []
        for player in pre_placement_players:
            if max_placement < hg_dict['statuses'][player]['kills']:
                current_placement_players = [player]
                max_placement = hg_dict['statuses'][player]['kills']
            elif max_placement == hg_dict['statuses'][player]['kills']:
                current_placement_players.append(player)
        # Adds player to the dict.
        for player in current_placement_players:
            kill_placements.append((player, hg_dict['statuses'][player]['name'], max_placement))
            pre_placement_players.remove(player)
    # Reverses placements list to sort from first to last and makes it a phase
    hg_dict['phases'].append({'type': 'kills', 'all': kill_placements, 'max': max([place[2] for place in kill_placements])})

    # Sends the first message.
    # Creates the embed.
    embed = discord.Embed(title='The Bloodbath, Action 1', colour=constants.HG_EMBED_COLOR)
    embed.set_footer(text=constants.HG_BEGINNING_DESCRIPTION)

    action_image = hunger_games_makeimage_action(hg_dict['phases'][0]['act'], 0, 1, hg_dict['phases'][0]['desc'])
    current_playerstatus_filepath = os.path.join(constants.TEMP_DIR, 'hg_player_statuses.png')
    action_image.save(current_playerstatus_filepath)
    file = discord.File(current_playerstatus_filepath, filename='hg_player_statuses.png')

    # Sends image, logs.
    embed.set_image(url='attachment://hg_player_statuses.png')
    await message.channel.send(file=file, embed=embed)

    # Updates hunger games dict.
    del hg_dict['statuses']
    hg_dict['current_phase'] = 0
    hg_dict['confirm_cancel'] = False
    hg_dict['generated'] = True
    hg_dict['complete'] = False


def hunger_games_set_embed_image(image, embed):
    current_image_filepath = os.path.join(constants.TEMP_DIR, constants.HG_IMAGE_PATH)
    image.save(current_image_filepath)
    file = discord.File(current_image_filepath, filename='hg_image_filepath.png')
    embed.set_image(url='attachment://hg_image_filepath.png')
    return file


async def hunger_games_send_pregame(message, players, title, uses_bots):
    """
    Sends the pregame roster thing.
    """
    # Makes sure all the player icons are downloaded.
    for user in players:
        image_locale = os.path.join(constants.TEMP_DIR, str(user.id) + constants.PFP_FILETYPE)
        if not os.path.isfile(image_locale):
            image_bytes = requests.get(user.avatar_url).content
            # Writes image to disk
            with open(image_locale, 'wb') as w:
                w.write(image_bytes)

    # Creates embed.
    embed = discord.Embed(title=title, colour=constants.HG_EMBED_COLOR)
    embed.set_footer(text=constants.HG_PREGAME_DESCRIPTION.format('Disallow' if uses_bots else 'Allow'))

    # Has image created, sets image on embed.
    player_statuses = hunger_games_makeimage_player_statuses([(player.id, player.nick if player.nick else player.name, 0) for player in players])
    file = hunger_games_set_embed_image(player_statuses, embed)

    # Sends image, logs.
    await message.channel.send(file=file, embed=embed)


async def hunger_games_send_midgame(message, is_in_guild, hg_dict, count=1, do_previous=False, do_increment=True):
    """
    Sends all midgame embeds, regardless of type.
    """
    current_phase = hg_dict['phases'][hg_dict['current_phase']]

    # Creates embed for act pages.
    if current_phase['type'] == 'act':
        # This section increments the actions in the phase.
        if do_previous:
            # Previous
            # This part checks if this action is the first in the list.
            # We don't want our phase to be -1.
            if current_phase['prev'] == -1:
                if hg_dict['current_phase'] == 0:
                    return
                hg_dict['current_phase']-= 1
                current_phase['next'] = 0
                await hunger_games_send_midgame(message, is_in_guild, hg_dict, count, do_previous=True, do_increment=False)
                return
            else:
                # Normal increment.
                start = max(0, current_phase['prev'] - count + 1)
                if start + count > current_phase['prev']:
                    count = current_phase['prev'] - start + 1
                current_phase['prev'] = start - 1
                current_phase['next'] = start + count
        else:
            # Next
            action_count = len(current_phase['act'])
            # There is no check for next, because the final phase is a kill type, not an act type.
            if current_phase['next'] == action_count:
                hg_dict['current_phase']+= 1
                current_phase['prev'] = action_count - 1
                await hunger_games_send_midgame(message, is_in_guild, hg_dict, count, do_previous=False, do_increment=False)
                return
            else:
                # Normal increment.
                start = current_phase['next']
                if start + count > action_count:
                    count = action_count - start
                current_phase['prev'] = start - 1
                current_phase['next'] = start + count
        # Standard embed creation.
        action_nums = (start + 1, start + count)
        embed = discord.Embed(title=current_phase['title'] + (', Action {}'.format(action_nums[0]) if action_nums[1] == action_nums[0] else ', Actions {} - {}'.format(action_nums[0], action_nums[1])) + (' / ' + str(len(current_phase['act'])) if current_phase['done'] else ''), colour=constants.HG_EMBED_COLOR)
        player_actions = hunger_games_makeimage_action(current_phase['act'], start, count, current_phase['desc'] if start == 0 else None)
        file = hunger_games_set_embed_image(player_actions, embed)

    # Embeds through everything else act pretty differently.
    else:
        # If we increment, then we increment.
        if do_increment:
            if do_previous:
                hg_dict['current_phase']-= 1
                current_phase = hg_dict['phases'][hg_dict['current_phase']]
            else:
                # We check here to make sure we're not at the end.
                if current_phase['type'] == 'kills':
                    return
                hg_dict['current_phase']+= 1
                current_phase = hg_dict['phases'][hg_dict['current_phase']]
            # Check if we're now in an act.
            if current_phase['type'] == 'act':
                await hunger_games_send_midgame(message, is_in_guild, hg_dict, count, do_previous=do_previous, do_increment=False)
                return

        # Creates embed for win AND tie pages.
        if current_phase['type'] in ['win', 'tie']:
            embed = discord.Embed(title=current_phase['title'], colour=constants.HG_EMBED_COLOR)
            player_actions = hunger_games_makeimage_winner(current_phase['players'], current_phase['desc'])
            file = hunger_games_set_embed_image(player_actions, embed)

        # Creates embed for status pages.
        elif current_phase['type'] == 'status':
            embed = discord.Embed(title='{} cannon shot{} can be heard in the distance.'.format(current_phase['new'], '' if current_phase['new'] == 1 else 's'), colour=constants.HG_EMBED_COLOR)
            player_statuses = hunger_games_makeimage_player_statuses(current_phase['all'])
            file = hunger_games_set_embed_image(player_statuses, embed)

        # Creates embed for placement pages.
        elif current_phase['type'] == 'place':
            embed = discord.Embed(title='Placements', colour=constants.HG_EMBED_COLOR)
            player_statuses = hunger_games_makeimage_player_statuses(current_phase['all'], placement=current_phase['max'])
            file = hunger_games_set_embed_image(player_statuses, embed)

        # Creates embed for killcount pages.
        elif current_phase['type'] == 'kills':
            embed = discord.Embed(title='Kills', colour=constants.HG_EMBED_COLOR)
            player_statuses = hunger_games_makeimage_player_statuses(current_phase['all'], kills=current_phase['max'])
            file = hunger_games_set_embed_image(player_statuses, embed)

        # Creates embed for other pages.
        else:
            log.error(misc.get_comm_start(message, is_in_guild) + ' invalid hunger games phase type {}'.format(current_phase['type']))
            return

    # Sets footer, sends image, logs.
    if hg_dict['complete']:
        # We're at the front of the game
        if hg_dict['current_phase'] == 0 and hg_dict['phases'][hg_dict['current_phase']]['prev'] == -1:
            embed.set_footer(text=constants.HG_POSTGAME_BEGINNING_DESCRIPTION)
        # We're at the end of the game
        elif current_phase['type'] == 'kills':
            embed.set_footer(text=constants.HG_FINALE_DESCRIPTION)
        # We're anywhere else
        else:
            embed.set_footer(text=constants.HG_POSTGAME_MIDGAME_DESCRIPTION)
    else:
        # We're at the front of the game
        if hg_dict['current_phase'] == 0 and hg_dict['phases'][hg_dict['current_phase']]['prev'] == -1:
            embed.set_footer(text=constants.HG_BEGINNING_DESCRIPTION)
        # Game complete!
        elif current_phase['type'] in constants.HG_COMPLETE_PHASE_TYPES:
            hg_dict['complete'] = True
            embed.set_footer(text=constants.HG_THE_END_DESCRIPTION)
        # We're anywhere else in the game
        else:
            embed.set_footer(text=constants.HG_MIDGAME_DESCRIPTION)
    # Send message
    await message.channel.send(file=file, embed=embed)


async def hunger_games_pregame_shuffle(self, message, is_in_guild, player_count, uses_bots):
    """
    Shuffles a pregame hunger games cast.
    """
    # Get the user list.
    user_list = misc.get_applicable_users(message, is_in_guild, not uses_bots)
    if len(user_list) < constants.HG_MIN_GAMESIZE:
        self.curr_hg.pop(str(message.channel.id))
        await message.channel.send('Not enough users in server.')
        log.debug(misc.get_comm_start(message, is_in_guild) + ' requested hunger games, not enough people')

    # Otherwise, we generate the players and ask if we should proceed.
    else:
        # Get the players.
        hg_players = []
        for i in range(min(player_count, len(user_list))):
            next_player = random.choice(user_list)
            hg_players.append(next_player)
            user_list.remove(next_player)

        # Set in players and actions.
        hg_full_game = {'players': hg_players, 'past_pregame': False, 'uses_bots': uses_bots}
        self.curr_hg[str(message.channel.id)] = hg_full_game

        # Send the updated cast
        await hunger_games_send_pregame(message, hg_players, constants.HG_PREGAME_TITLE, uses_bots)
        log.debug(misc.get_comm_start(message, is_in_guild) + 'shuffled Hunger Games instance with {} players'.format(player_count))


async def hunger_games_update(self, message, is_in_guild):
    """
    Updates a hunger games dict.
    """
    hg_dict = self.curr_hg[str(message.channel.id)]
    response = message.content.lower()

    # If the game is already generated.
    if hg_dict['past_pregame']:
        if hg_dict['generated']:
            # First, cancel confirmations.
            if hg_dict['confirm_cancel']:
                if any([response == 'y', response == 'yes']):
                    del self.curr_hg[str(message.channel.id)]
                    await message.channel.send('Hunger Games canceled.')
                    log.debug(misc.get_comm_start(message, is_in_guild) + 'canceled Hunger Games')
                    return True

                elif any([response == 'n', response == 'no']):
                    hg_dict['confirm_cancel'] = False
                    await message.channel.send('Understood, cancel aborted.')
                    return True

            # Next command (custom size).
            elif any([response.startswith(pre) for pre in ['n ', 'next ']]):
                # Gets the first argument after the next.
                response = response.split(' ')[1]
                try:
                    response = int(response)
                except ValueError:
                    return
                # Passes it along to the send_midgame function
                await hunger_games_send_midgame(message, is_in_guild, hg_dict, count=max(1, response))
                hg_dict['updated'] = datetime.today()
                return True

            # Next command.
            elif any([response == 'n', 'response' == 'next']):
                await hunger_games_send_midgame(message, is_in_guild, hg_dict)
                hg_dict['updated'] = datetime.today()
                return True

            # Previous command (custom size).
            elif any([response.startswith(pre) for pre in ['p ', 'prev ', 'previous']]):
                if hg_dict['current_phase'] == 0 and hg_dict['phases'][hg_dict['current_phase']]['prev'] == -1:
                    return
                else:
                    # Gets the first argument after the previous.
                    response = response.split(' ')[1]
                    try:
                        response = int(response)
                    except ValueError:
                        return
                    # Passes it along to the send_midgame function
                    await hunger_games_send_midgame(message, is_in_guild, hg_dict, count=max(1, response))
                    hg_dict['updated'] = datetime.today()
                    return True

            # Previous command.
            elif any([response == 'p', response == 'prev', response == 'previous']):
                if hg_dict['current_phase'] == 0 and hg_dict['phases'][hg_dict['current_phase']]['prev'] == -1:
                    return
                else:
                    await hunger_games_send_midgame(message, is_in_guild, hg_dict, do_previous=True)
                    hg_dict['updated'] = datetime.today()
                    return True

            # Cancel command.
            elif any([response == 'cancel', response == 'c']):
                if hg_dict['complete']:
                    del self.curr_hg[str(message.channel.id)]
                    await message.channel.send('Thanks for playing!')
                    log.debug(misc.get_comm_start(message, is_in_guild) + 'finished + closed Hunger Games')
                    return True

                elif not hg_dict['confirm_cancel']:
                    hg_dict['confirm_cancel'] = True
                    await message.channel.send('Cancel Hunger Games? (y/n)')
                    return True

        # If the game isn't finished generating yet.
        elif any([response.startswith(pre) for pre in ['j!hg ', 'j!hunger ', 'j!hungergames ', 'j!hungry ']] + [response == 'j!hg', response == 'j!hunger', response == 'j!hungergames', response == 'j!hungry']):
            await message.channel.send('Still generating, be patient.')
            hg_dict['updated'] = datetime.today()
            return True

    # The game is not yet out of pregame.
    else:
        # Shuffle command (but of a different size).
        if any([response.startswith(pre) for pre in ['j!hg ', 'j!hunger ', 'j!hungergames ', 'j!hungry ', 's ', 'shuffle ']]):
            try:
                player_count = int(response.split(' ')[1])
                if player_count > constants.HG_MAX_GAMESIZE:
                    player_count = constants.HG_MAX_GAMESIZE
                elif player_count < constants.HG_MIN_GAMESIZE:
                    player_count = constants.HG_MIN_GAMESIZE
            except ValueError:
                player_count = len(hg_dict['players'])
            await hunger_games_pregame_shuffle(self, message, is_in_guild, player_count, uses_bots=hg_dict['uses_bots'])
            hg_dict['updated'] = datetime.today()
            return True

        # Shuffle command.
        elif any([response == 's', response == 'shuffle', response == 'j!hg', response == 'j!hunger', response == 'j!hungergames', response == 'j!hungry']):
            await hunger_games_pregame_shuffle(self, message, is_in_guild, len(hg_dict['players']), uses_bots=hg_dict['uses_bots'])
            hg_dict['updated'] = datetime.today()
            return True

        # Replace command (improper use).
        elif any([response == 'r', response == 'replace']):
            await message.channel.send('Mention two users to replace one with the other.')
            hg_dict['updated'] = datetime.today()
            return True

        elif any([response.startswith('r '), response.startswith('replace ')]):
            # Gets the first two users in the thing.
            try:
                modified_players = misc.get_closest_users(message, response[2:] if response.startswith('r ') else response[8:], is_in_guild, not hg_dict['uses_bots'], limit=2)
            except (NoUserSpecifiedError, ArgumentTooShortError, UnableToFindUserError):
                await message.channel.send('Invalid user(s).')
                log.debug(misc.get_comm_start(message, is_in_guild) + 'attempted to add a player to Hunger Games instance, invalid')
                hg_dict['updated'] = datetime.today()
                return True
            # Conditional
            if modified_players[0] in hg_dict['players']:
                # Both players are in the game
                if modified_players[1] in hg_dict['players']:
                    await message.channel.send('{} is already in the game.'.format(modified_players[1]))
                    log.debug(misc.get_comm_start(message, is_in_guild) + 'tried to replace a player in Hunger Games instance, second already there')
                # First player in game, second not
                else:
                    hg_dict['players'].insert(hg_dict['players'].index(modified_players[0]), modified_players[1])
                    hg_dict['players'].remove(modified_players[0])
                    await hunger_games_send_pregame(message, hg_dict['players'], 'Replaced {} with {}.'.format(modified_players[0].nick if modified_players[0].nick else modified_players[0].name, modified_players[1].nick if modified_players[1].nick else modified_players[1].name), hg_dict['uses_bots'])
                    log.debug(misc.get_comm_start(message, is_in_guild) + 'replaced a player in Hunger Games instance')
            else:
                # First player not in game
                await message.channel.send('{} isn\'t in the game.'.format(modified_players[0]))
                log.debug(misc.get_comm_start(message, is_in_guild) + 'tried to replace a player in Hunger Games instance, first isn\'t there')
            hg_dict['updated'] = datetime.today()
            return True

        # Add command.
        elif any([response == 'a', response == 'add']):
            # Cancels if the game is already max size.
            if len(hg_dict['players']) == constants.HG_MAX_GAMESIZE:
                await message.channel.send('Max size already reached.')
                log.debug(misc.get_comm_start(message, is_in_guild) + 'tried to add player to Hunger Games instance, max size reached')
            else:
                # Cancels if no more members to add to game.
                able_users = misc.get_applicable_users(message, is_in_guild, hg_dict['uses_bots'], hg_dict['players'])
                if not able_users:
                    await message.channel.send('No more users not already in the game.')
                    log.debug(misc.get_comm_start(message, is_in_guild) + 'tried to add player to Hunger Games instance, no more users')
                # Otherwise, goes on.
                else:
                    added_player = random.choice(able_users)
                    hg_dict['players'].append(added_player)
                    await hunger_games_send_pregame(message, hg_dict['players'], 'Added {} to the game.'.format(added_player.nick if added_player.nick else added_player.name), hg_dict['uses_bots'])
                    log.debug(misc.get_comm_start(message, is_in_guild) + 'added a player to Hunger Games instance')
            hg_dict['updated'] = datetime.today()
            return True

        # Add command, but specific user
        elif any([response.startswith('a '), response.startswith('add ')]):
            # Cancels if the game is already max size.
            if len(hg_dict['players']) == constants.HG_MAX_GAMESIZE:
                await message.channel.send('Max size already reached.')
                log.debug(misc.get_comm_start(message, is_in_guild) + 'tried to add player to Hunger Games instance, max size reached')
            else:
                # Attempts to add a player.
                try:
                    added_player = misc.get_closest_users(message, response[2:] if response.startswith('a ') else response[4:], is_in_guild, not hg_dict['uses_bots'], limit=1)[0]
                except (NoUserSpecifiedError, ArgumentTooShortError, UnableToFindUserError):
                    await message.channel.send('Invalid user.')
                    log.debug(misc.get_comm_start(message, is_in_guild) + 'attempted to add a player to Hunger Games instance, invalid')
                    hg_dict['updated'] = datetime.today()
                    return True
                if added_player in hg_dict['players']:
                    await message.channel.send('{} is already in the game.'.format(added_player))
                    log.debug(misc.get_comm_start(message, is_in_guild) + 'attempted to add a player to Hunger Games instance, already there')
                else:
                    hg_dict['players'].append(added_player)
                    await hunger_games_send_pregame(message, hg_dict['players'], 'Added {} to the game.'.format(added_player.nick if added_player.nick else added_player.name), hg_dict['uses_bots'])
                    log.debug(misc.get_comm_start(message, is_in_guild) + 'added a player to Hunger Games instance')
            hg_dict['updated'] = datetime.today()
            return True

        # Delete command.
        elif any([response == 'd', response == 'del', response == 'delete']):
            # Cancels if the game is already min size.
            if len(hg_dict['players']) == constants.HG_MIN_GAMESIZE:
                await message.channel.send('Min size already reached.')
                log.debug(misc.get_comm_start(message, is_in_guild) + 'tried to remove player to Hunger Games instance, min size reached')
            else:
                # Removes player on the end.
                removed_player = hg_dict['players'].pop(-1)
                await hunger_games_send_pregame(message, hg_dict['players'], 'Removed {} from the game.'.format(removed_player.nick if removed_player.nick else removed_player.name), hg_dict['uses_bots'])
                log.debug(misc.get_comm_start(message, is_in_guild) + 'removed player from Hunger Games instance')
            hg_dict['updated'] = datetime.today()
            return True

        # Delete command, but specific user
        elif any([response.startswith('d '), response.startswith('del '), response.startswith('delete ')]):
            # Cancels if the game is already min size.
            if len(hg_dict['players']) == constants.HG_MIN_GAMESIZE:
                await message.channel.send('Min size already reached.')
                log.debug(misc.get_comm_start(message, is_in_guild) + 'tried to remove player to Hunger Games instance, min size reached')
            else:
                # Attempts to find player.
                try:
                    removed_player = misc.get_closest_users(message, response[2:] if response.startswith('d ') else (response[4:] if response.starswith('del ') else response[7:]), is_in_guild, not hg_dict['uses_bots'], limit=1)[0]
                except (NoUserSpecifiedError, ArgumentTooShortError, UnableToFindUserError):
                    await message.channel.send('Invalid user.')
                    log.debug(misc.get_comm_start(message, is_in_guild) + 'attempted to remove a player from Hunger Games instance, invalid')
                    hg_dict['updated'] = datetime.today()
                    return True
                if removed_player in hg_dict['players']:
                    hg_dict['players'].remove(removed_player)
                    await hunger_games_send_pregame(message, hg_dict['players'], 'Removed {} from the game.'.format(removed_player.nick if removed_player.nick else removed_player.name), hg_dict['uses_bots'])
                    log.debug(misc.get_comm_start(message, is_in_guild) + 'removed a player from Hunger Games instance')
                else:
                    await message.channel.send('{} isn\'t in the game.'.format(removed_player))
                    log.debug(misc.get_comm_start(message, is_in_guild) + 'attempted to remove a player from Hunger Games instance, not there')
            hg_dict['updated'] = datetime.today()
            return True

        # Allow / disallow bots command.
        elif any([response == 'b', response == 'disallow bots', response == 'allow bots', response == 'allow', response == 'disallow']):
            if hg_dict['uses_bots']:
                # Cancels if not enough non-bots
                hg_players_no_bots = hg_dict['players'].copy()
                while any([player.bot for player in hg_players_no_bots]):
                    for player in hg_players_no_bots:
                        if player.bot:
                            hg_players_no_bots.remove(player)
                while len(hg_players_no_bots) < constants.HG_MIN_GAMESIZE:
                    other_players = misc.get_applicable_users(message, is_in_guild, True, hg_players_no_bots)
                    if other_players:
                        hg_players_no_bots.append(random.choice(other_players))
                    else:
                        await message.channel.send('Not enough non-bots to disallow bots.')
                        log.debug(misc.get_comm_start(message, is_in_guild) + 'attempted to remove bots from Hunger Games instance, not enough users')
                        hg_dict['updated'] = datetime.today()
                        return True
                # Allows it.
                hg_dict['uses_bots'] = False
                hg_dict['players'] = hg_players_no_bots
                await hunger_games_send_pregame(message, hg_dict['players'], 'Removed bots from the game.', hg_dict['uses_bots'])
                log.debug(misc.get_comm_start(message, is_in_guild) + 'removed bots from Hunger Games instance')
            else:
                hg_dict['uses_bots'] = True
                await hunger_games_send_pregame(message, hg_dict['players'], 'Allowed bots into the game.', hg_dict['uses_bots'])
                log.debug(misc.get_comm_start(message, is_in_guild) + 'added bots to Hunger Games instance')
            hg_dict['updated'] = datetime.today()
            return True

        # Proceed command.
        elif any([response == 'p', response == 'proceed']):
            await message.channel.send('Generating Hunger Games instance...')
            log.debug(misc.get_comm_start(message, is_in_guild) + 'initiated Hunger Games')
            hg_dict['past_pregame'] = True
            hg_dict['generated'] = False
            await hunger_games_generate_full_game(hg_dict, message)
            hg_dict['updated'] = datetime.today()
            return True

        # Cancel command.
        elif any([response == 'c', response == 'cancel']):
            await message.channel.send('Hunger Games canceled.')
            log.debug(misc.get_comm_start(message, is_in_guild) + 'canceled Hunger Games')
            del self.curr_hg[str(message.channel.id)]
            hg_dict['updated'] = datetime.today()
            return True


async def hunger_games_start(self, message, argument, is_in_guild):
    """
    Creates a hunger games simulator right inside the bot.
    """
    hg_key = str(message.channel.id)

    # If a game is already in progress, we forward this message.
    if hg_key in self.curr_hg.keys():
        await hunger_games_update(self, message, is_in_guild)

    else:
        # Gets argument for how many users to start hg with.
        if argument:
            try:
                player_count = int(argument)
                if player_count > constants.HG_MAX_GAMESIZE:
                    player_count = constants.HG_MAX_GAMESIZE
                elif player_count < constants.HG_MIN_GAMESIZE:
                    player_count = constants.HG_MIN_GAMESIZE
            except ValueError:
                player_count = 24
        else:
            player_count = 24

        # Get the user list. If user list is < player_count people, we add bots as well.
        user_list = misc.get_applicable_users(message, is_in_guild, True)
        uses_bots = False
        if len(user_list) < player_count:
            user_list = misc.get_applicable_users(message, is_in_guild, False)
            uses_bots = True
        # If there still aren't enough users, we send error.
        if len(user_list) < constants.HG_MIN_GAMESIZE:
            if len(user_list) == 1:
                await message.channel.send('There was an error accessing userlist.')
                log.error(misc.get_comm_start(message, is_in_guild) + ' requested hunger games, bugged userlist')
            else:
                await message.channel.send('Not enough users in server.')
                log.debug(misc.get_comm_start(message, is_in_guild) + ' requested hunger games, not enough people')

        # Otherwise, we generate the players and ask if we should proceed.
        else:
            # Get the players.
            hg_players = []
            for i in range(min(player_count, len(user_list))):
                next_player = random.choice(user_list)
                hg_players.append(next_player)
                user_list.remove(next_player)

            # Set in players and actions.
            hg_full_game = {'players': hg_players, 'past_pregame': False, 'uses_bots': uses_bots, 'updated': datetime.today()}
            self.curr_hg.update({hg_key: hg_full_game})

            # Send the initial cast
            await hunger_games_send_pregame(message, hg_players, constants.HG_PREGAME_TITLE, uses_bots)
            log.debug(misc.get_comm_start(message, is_in_guild) + 'started Hunger Games instance with {} players'.format(len(hg_players)))

async def thank_you(self, message, argument, is_in_guild):
    """
    Thanks the bot!
    :D
    """
    log.debug(misc.get_comm_start(message, is_in_guild) + 'thanked the bot')
    await message.channel.send(random.choice(constants.THANKYOU_RESPONSES))
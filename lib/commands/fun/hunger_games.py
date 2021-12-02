"""
Hunger Games command.
Essentially a BrantSteele simulator simulator.
"""
# Imports.
from lib.util.exceptions import CannotAccessUserlistError, NoUserSpecifiedError, UnableToFindUserError
from lib.util import arguments, assets, environment, messaging, misc, parsing, tempfiles
from PIL import Image, ImageOps, ImageFont, ImageDraw
from lib.util.logger import BotLogger as logging
from datetime import datetime
import discord
import random
import os


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
HG_PLAYERSTATUS_WIDTHS = [0, 1, 2, 3, 4, 3, 3, 4, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8,
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
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
HG_POSTGAME_BEGINNING_DESCRIPTION = 'Respond one of the following:\nN: Next Action\nR: Replay (same cast)\tS: New Game\tC: Close'
HG_POSTGAME_MIDGAME_DESCRIPTION = 'Respond one of the following:\nN: Next Action\tP: Previous Action\nR: Replay (same cast)\tS: New Game\tC: Close'
HG_THE_END_DESCRIPTION = 'The end! Respond one of the following:\nN: Next Action\tP: Previous Action\nR: Replay (same cast)\tS: New Game\tC: Close'
HG_FINALE_DESCRIPTION = 'Respond one of the following:\nP: Previous Action\nR: Replay (same cast)\tS: New Game\tC: Close'

# Winner / Ties
HG_WINNER_TITLE = 'The Winner'
HG_TIE_TITLE = 'The Winners'
HG_WINNER_EVENT = 'The winner is {0}!'
HG_WINNER_DEAD_EVENT = 'The winner is {0}! However, they died too, so it\'s sort of a hollow victory.'
HG_TIE_EVENT = ('Since they died at the same time, it\'s a tie between ', ', ', 'and ', '!')
HG_COMPLETE_PHASE_TYPES = ['win', 'tie']

# Item List
# # =================DEBUG==================
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
HG_WEAPON_ITEMS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
HG_FOOD_ITEMS = [101, 102, 103, 104]
HG_HEALTH_ITEMS = [201, 202, 203]
HG_ALL_ITEMS = HG_WEAPON_ITEMS + HG_FOOD_ITEMS + HG_HEALTH_ITEMS

# Actions
HG_BLOODBATH_ACTIONS = [
    {'players': 0, 'act': '{0} runs away from the Cornucopia.'},
    {'players': 0, 'act': '{0} runs away from the Cornucopia.'},
    {'players': 0, 'act': '{0} grabs a sword.', 'give': [2]},
    {'players': 0, 'act': '{0} takes a spear from the Cornucopia.', 'give': [3]},
    {'players': 0, 'act': '{0} finds a bag full of explosives.', 'give': [4]},
    {'players': 0, 'act': '{0} grabs a backpack and retreats.', 'give': [4000]},
    {'players': 0, 'act': '{0} takes only a pair of scissors.', 'give': [14]},
    {'players': 0, 'act': '{0} takes a handful of throwing knives.', 'give': [5]},
    {'players': 0, 'act': '{0} accidentally steps on a landmine and explodes.', 'kill': [0]},
    {'players': 0, 'act': '{0} grabs a bottle of alcohol and a rag.', 'give': [11]},
    {'players': 0, 'act': '{0} grabs a first aid kit and runs away.', 'give': [203]},
    {'players': 0, 'act': '{0} grabs a bow and makes a getaway.', 'give': [12]},
    {'players': 0, 'act': '{0} stubs their toe on a grenade. It explodes, killing them.', 'kill': [0]},
    {'players': 0, 'act': '{0} escapes with a lighter and some rope.', 'give': [8]},
    {'players': 1, 'act': '{0} rips a mace out of {1}\'s hands.', 'give': [1, 0]},
    {'players': 1, 'act': '{0} throws a knife into {1}\'s head.', 'kill': [1]},
    {'players': 1, 'act': '{0} strangles {1} after engaging in a fist fight.', 'kill': [1], 'credit': [0]},
    {'players': 1, 'act': '{0} stabs {1} with a tree branch.', 'kill': [1], 'credit': [0]},
    {'players': 1, 'act': '{0} breaks {1}\'s nose for a basket of bread.', 'hurt': [1], 'credit': [0]},
    {'players': 2, 'act': '{0}, {1}, and {2} work together to get as many supplies as possible.', 'give': [3000, 3000, 3000]},
    {'players': 2, 'act': '{0} and {1} work together to drown {2}.', 'kill': [2], 'credit': [0, 1]},
    {'players': 2, 'act': '{0}, {1}, and {2} get into a fight. {1} triumphantly kills them both.', 'kill': [0, 2], 'credit': [1]}
]
HG_NORMAL_DAY_ACTIONS = {
    'trigger': [
        {'needs': 302, 'chance': 0.8, 'success': [{'players': 0, 'act': '{0} continues to hide in the bushes.'}, {'players': 1, 'act': '{0} waits until the perfect moment to pop out of the bushes, ambushing {1} and killing them.', 'kill': [1], 'give': [-302, 0]}], 'fail': [{'players': 1, 'act': '{0} is discovered by {1}, who immediately bashes in their skull with a rock.', 'kill': [0]}]},
        {'needs': 304, 'chance': 0.75, 'success': [{'players': 1, 'act': '{0} is attacked by {1}, but {0} has the high ground, so they manage to defeat {1}.', 'give': [-304, 0], 'kill': [1], 'credit': [0]}], 'fail': [{'players': 0, 'give': [-304]}]},
        {'needs': 1, 'chance': 0.1, 'success': [{'players': 1, 'act': '{0} uses their mace to beat {1} to death.', 'kill':[1], 'credit': [0]}]},
        {'needs': 2, 'chance': 0.2, 'success': [{'players': 1, 'act': '{0} cuts down {1} with a sword.', 'kill': [1], 'credit': [0]}, {'players': 1, 'act': '{0} attempts to swing their sword at {1}, but {1} is able to disarm them and use it against them.', 'kill': [0], 'give': [-2, 2]}]},
        {'needs': 3, 'chance': 0.2, 'success': [{'players': 0, 'act': '{0} accidentally impales themselves with a spear.', 'kill': [0]}, {'players': 1, 'act': '{0} impales {1} with a spear.', 'kill': [1], 'credit': [0], 'give': [-3, 0]}]},
        {'needs': 4, 'chance': 0.2, 'success': [{'players': 1, 'act': '{0} creates a landmine from their explosives. An hour later, {1} steps on it and explodes.', 'kill': [1], 'credit': [0], 'give': [-4, 0]}, {'players': 0, 'act': '{0} creates a landmine from their explosives.'}, {'players': 0, 'act': '{0} attempts to create a landmine from their explosives, but blows themselves up in the process.', 'kill': [0]}]},
        {'needs': 5, 'chance': 0.2, 'success': [{'players': 1, 'act': '{0} lands a throwing knife right in the middle of {1}\'s chest.', 'kill': [1], 'give': [-5, 0], 'credit': [0]}, {'players': 1, 'act': '{0} throws a throwing knife through {1}\'s arm. {1} rips it out and throws it back at {0}, killing them.', 'kill': [0], 'credit': [1], 'give': [-5, 0], 'hurt': [1]}]},
        {'needs': 6, 'chance': 0.2, 'success': [{'players': 1, 'act': '{0} brutally executes {1} with a hatchet.', 'kill': [1], 'credit': [0]}]},
        {'needs': 7, 'chance': 0.2, 'success': [{'players': 1, 'act': '{0} uses their slingshot to shoot {1} out of a tree, killing them.', 'kill': [1], 'credit': [0]}]},
        {'needs': 8, 'chance': 0.2, 'success': [{'players': 1, 'act': '{0} creates a net from their rope, which they use to catch food.', 'give': [8888]}]},
        {'needs': 12, 'chance': 0.8, 'success': [{'players': 0, 'act': '{0} practices their archery.'}], 'fail': [{'players': 1, 'act': '{0} successfully shoots an arrow into {1}\'s head.', 'kill': [1], 'credit': [0]}, {'players': 1, 'act': '{0} shoots an arrow at {1}, but misses, giving away their position. They drop the bow and run.', 'give': [-12, 0]}]},
        {'needs': 13, 'chance': 0.3, 'success': [{'players': 1, 'act': '{0} poisons {1}\'s drink. They drink it and die.', 'give': [-13, 0], 'credit': [0]}]},
        {'needs': 301, 'chance': 0.9, 'success': [{'players': 4, 'act': '{0} has their camp raided by {1}, {2}, {3}, and {4}.', 'give': [9999, 0, 0, 0, 0]}, {'players': 0, 'act': '{0} defends their stronghold.'}]},
        {'needs': 303, 'chance': 0.9, 'success': [{'players': 4, 'act': '{0} has their camp raided by {1}, {2}, {3}, and {4}.', 'give': [9999, 0, 0, 0, 0]}, {'players': 0, 'act': '{0} defends their stronghold.'}]},
        {'needs': 103, 'chance': 0.1, 'success': [{'players': 2, 'act': '{0} successfully uses food as a motive to get {1} to kill {2}.', 'kill': [2], 'credit': [1], 'give': [-103, 0, 0]}]}
    ],
    'normal': [
        {'players': 0, 'act': '{0} receives clean water from an unknown sponsor.', 'give': [101]},
        {'players': 0, 'act': '{0} receives medical supplies from an unknown sponsor.', 'give': [201]},
        {'players': 0, 'act': '{0} constructs a shack.', 'give': [301]},
        {'players': 0, 'act': '{0} discovers a river.', 'give': [102]},
        {'players': 0, 'act': '{0} travels to higher ground.', 'give': [304]},
        {'players': 0, 'act': '{0} tries to sleep through the day.'},
        {'players': 0, 'act': '{0} discovers a cave.', 'give': [303]},
        {'players': 0, 'act': '{0} finds a hatchet embedded into a tree.', 'give': [6]},
        {'players': 0, 'act': '{0} camouflages themselves in the bushes.', 'give': [302]},
        {'players': 0, 'act': '{0} dies of dysentery.', 'kill': [0]},
        {'players': 0, 'act': '{0} cries to themselves.'},
        {'players': 0, 'act': '{0} wanders around aimlessly.'},
        {'players': 0, 'act': '{0} makes a slingshot.', 'give': [7]},
        {'players': 0, 'act': '{0} eats some berries.'},
        {'players': 0, 'act': '{0} makes a wooden spear.', 'give': [3]},
        {'players': 0, 'act': '{0} picks flowers.'},
        {'players': 0, 'act': '{0} is stung by bees.', 'hurt': [0]},
        {'players': 0, 'act': '{0} is pricked by thorns while picking berries.', 'hurt': [0]},
        {'players': 0, 'act': '{0} finds some rope.', 'give': [8]},
        {'players': 0, 'act': '{0} receives a bottle of poison from an unknown sponsor.', 'give': [13]},
        {'players': 0, 'act': '{0} eats some poisonous berries by accident.', 'kill': [0]},
        {'players': 1, 'act': '{0} uses a rock to break {1}\'s arm.', 'hurt': [1]},
        {'players': 1, 'act': '{0} and {1} split up to look for resources.'},
        {'players': 1, 'act': '{0} sprains their ankle while running away from {1}.', 'hurt': [0]},
        {'players': 1, 'act': '{0} and {1} work together for the day.'},
        {'players': 1, 'act': '{0} tracks down and kills {1}.', 'kill': [1], 'credit': [0]},
        {'players': 1, 'act': '{0} defeats {1} in a fight, but spares their life.', 'hurt': [1]},
        {'players': 1, 'act': '{0} begs for {1} to kill them. They refuse, keeping {0} alive.'},
        {'players': 1, 'act': '{0} pushes {1} off a cliff.', 'kill': [1], 'credit': [0]},
        {'players': 1, 'act': '{0} and {1} engage in a fist fight, but accidentally fall off a cliff together.', 'kill': [0, 1]},
        {'players': 1, 'act': '{0} attempts to climb a tree, but falls on {1}, killing them both.', 'kill': [0, 1], 'credit': [0]},
        {'players': 2, 'act': '{0} pushes a boulder down a hill, which flattens both {1} and {2}.', 'kill': [1, 2], 'credit': [0, 0]},
        {'players': 2, 'act': '{0} overhears {1} and {2} talking in the distance.'},
        {'players': 3, 'act': '{0} forces {1} to kill either {2} or {3}. They choose {2}.', 'kill': [2], 'credit': [1]},
        {'players': 3, 'act': '{0} forces {1} to kill either {2} or {3}. They choose {3}.', 'kill': [3], 'credit': [1]}
    ]
}
HG_NORMAL_NIGHT_ACTIONS = {
    'trigger': [
        {'needs': 302, 'chance': 0.8, 'success': [{'players': 0, 'act': '{0} continues to hide in the bushes.'}, {'players': 1, 'act': '{0} waits until the perfect moment to pop out of the bushes, ambushing {1} and killing them.', 'kill': [1], 'credit': [0], 'give': [-302, 0]}], 'fail': [{'players': 1, 'act': '{0} is discovered by {1}, who immediately bashes in their skull with a rock.', 'kill': [0], 'credit': [1]}]},
        {'wounded': True, 'needs': 203, 'success': [{'players': 0, 'act': '{0} tends to their wounds.', 'heal': [0], 'give': [-203]}]},
        {'wounded': True, 'needs': 201, 'chance': 0.9, 'success': [{'players': 0, 'act': '{0} tends to their wounds.', 'heal': [0], 'give': [-201]}]},
        {'wounded': True, 'needs': 202, 'chance': 0.5, 'success': [{'players': 0, 'act': '{0} tends to their wounds.', 'heal': [0], 'give': [-202]}]},
        {'wounded': True, 'chance': 0.2, 'success': [{'players': 0, 'act': '{0} tends to their wounds.', 'heal': [0], 'give': [-202]}], 'fail': [{'players': 0, 'act': '{0} dies from their wounds.', 'kill': [0]}]},
        {'needs': 303, 'chance': 0.2, 'success': [{'players': 1, 'act': '{0} has their cave discovered by {1}, who pushes them onto a stalagmite, impaling them.', 'kill': [0], 'credit': [1]}, {'players': 1, 'act': '{0}\'s stronghold is discovered by {1}, who then strangles {0}.', 'kill': [0], 'credit': [1]}], 'fail': [{'players': 0, 'act': '{0} sleeps peacefully in their cave for the night.', 'give': -301}]},
        {'needs': 9, 'chance': 0.1, 'success': [{'players': 1, 'act': '{0} uses their shovel to bury {1} alive.', 'kill': [1], 'credit': [0]}]},
        {'needs': 14, 'chance': 0.3, 'success': [{'players': 1, 'act': '{0} stabs a hole right through {1}\'s throat using their scissors.', 'kill': [1], 'credit': [0]}]},
        {'needs': 104, 'success': [{'players': 0, 'act': '{0} cooks their meat over the fire.', 'give': [-104]}]}
    ],
    'normal': [
        {'players': 0, 'act': '{0} passes out from exhaustion.'},
        {'players': 0, 'act': '{0} screams for help.'},
        {'players': 0, 'act': '{0} questions their sanity.'},
        {'players': 0, 'act': '{0} stays awake all night.'},
        {'players': 0, 'act': '{0} thinks about winning.'},
        {'players': 0, 'act': '{0} dies from hypothermia.', 'kill': [0]},
        {'players': 0, 'act': '{0} prays to every god they can think of.'},
        {'players': 0, 'act': '{0} cannot handle the circumstances and commits suicide.', 'kill': [0]},
        {'players': 0, 'act': '{0} cries themselves to sleep.'},
        {'players': 0, 'act': '{0} thinks about home.'},
        {'players': 0, 'act': '{0} loses sight of where they are.'},
        {'players': 0, 'act': '{0} receives fresh food from an unknown sponsor.', 'give': [103]},
        {'players': 0, 'act': '{0} receives explosives from an unknown sponsor.', 'give': [4]},
        {'players': 1, 'act': '{0} convinces {1} to snuggle.'},
        {'players': 1, 'act': '{0} and {1} hold hands.'},
        {'players': 1, 'act': '{0} pushes {1} into their own fire, burning them alive.', 'kill': [1], 'credit': [0]},
        {'players': 1, 'act': '{0} and {1} talk about their place in the universe.'},
        {'players': 1, 'act': '{0} and {1} make up stories to entertain themselves.'},
        {'players': 2, 'act': '{0} and {1} team up to ambush {2}.', 'kill': [2], 'credit': [0, 1]},
        {'players': 3, 'act': '{0} fends {1}, {2}, and {3} away from their fire.'},
        {'players': 5, 'act': '{0}, {1}, and {2} unsuccessfully ambush {3}, {4}, and {5}, who kill them instead.', 'kill': [0, 1, 2], 'credit': [3, 4, 5, 3, 4, 5, 3, 4, 5]},
        {'players': 5, 'act': '{0}, {1}, and {2} successfully ambush {3}, {4}, and {5}.', 'kill': [3, 4, 5], 'credit': [0, 1, 2, 0, 1, 2, 0, 1, 2]}
    ]
}
HG_RESTOCK_EVENT = {
    'trigger': [

    ],
    'normal': [
        {'players': 0, 'act': '{0} decides not to go to the feast.'},
        {'players': 0, 'act': '{0} grabs a bundle of dry clothes and runs.'},
        {'players': 1, 'act': '{0} destroys {1}\'s memoirs out of spite.'},
        {'players': 0, 'act': '{0} steps on a landmine near the Cornucopia.', 'kill': [0]},
        {'players': 1, 'act': '{0} and {1} fight over raw meat, but {1} gives up and flees.', 'give': [104, 0]}
    ]
}
HG_FIRE_EVENT = {
    'trigger': [
        {'needs': 10, 'success': [{'players': 1, 'act': '{0} uses their net to capture {1} and toss them into the fire.', 'kill': [1], 'credit': [0]}]}
    ],
    'normal': [
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': 'A fireball strikes {0}, killing them.', 'kill': [0]},
        {'players': 0, 'act': '{0} is singed by the flames, but survives.', 'hurt': [0]},
        {'players': 1, 'act': '{0} helps {1} get to higher ground.'},
        {'players': 1, 'act': '{0} pushes {1} into a river, sacrificing themselves.', 'kill': [0]},
        {'players': 1, 'act': '{0} falls to the ground, but kicks {1} hard enough to push them into the fire.', 'kill': [0, 1], 'credit': [0]},
        {'players': 1, 'act': '{0} kills {1} in order to utilize a body of water safely.', 'kill': [1], 'credit': [0]},
        {'players': 1, 'act': '{0} and {1} fail to find a safe spot and suffocate.', 'kill': [0, 1]}
    ]
}
HG_FLOOD_EVENT = {
    'trigger': [
        {'needs': 10, 'success': [{'players': 1, 'act': '{0} uses their net to capture {1} and toss them into the water.', 'kill': [1], 'credit': [0]}]}
    ],
    'normal': [
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} falls into the water, but miraculously survives.'},
        {'players': 0, 'act': '{0} is swept away by the flood.', 'kill': [0]},
        {'players': 0, 'act': '{0} climbs up a tree, but the waters snap the tree in half, taking the whole thing out.', 'kill': [0]},
        {'players': 1, 'act': '{0} helps {1} get to higher ground.'},
        {'players': 1, 'act': '{0} pushes {1} into the water.', 'kill': [1], 'credit': [0]},
        {'players': 2, 'act': '{0} throws {1} and {2} to safety, sacrificing themselves.', 'kill': [0]},
    ]
}
HG_TORNADO_EVENT = {
    'trigger': [
        {'needs': 10, 'success': [{'players': 1, 'act': '{0} uses their net to capture {1} and toss them into the storm.'}]}
    ],
    'normal': [
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} is carried away by the storm.', 'kill': [0]},
        {'players': 1, 'act': '{0} lets {1} into their shelter.'},
        {'players': 1, 'act': '{0} kicks {1} away, letting them be sucked up by the tornado.', 'kill': [1], 'credit': [0]},
        {'players': 1, 'act': '{0} and {1} run away from the storm together, but as {1} is carried away, they grab {0}, leading them both to their deaths.', 'kill': [0, 1], 'credit': [1]},
        {'players': 1, 'act': '{0} can\'t handle the circumstances and offers themselves to the storm.', 'kill': [0]},
    ]
}
HG_EVENT_DEFAULT_CHANCE = 0.2
HG_EVENTS = [
    (HG_FLOOD_EVENT, 'The Flood', 'A vicious flood suddenly appears out of nowhere and sweeps through the Arena.'),
    (HG_FIRE_EVENT, 'The Fire', 'A sudden bolt of lightning sparks a fire, which explodes into a massive Arena-wide forest fire.'),
    (HG_TORNADO_EVENT, 'The Tornado', 'Winds in the Arena pick up and a tornado begins to tear its way through the Arena.'),
    (HG_RESTOCK_EVENT, 'The Replenishing', 'The Cornucopia is restocked with food, weapons, and medical supplies.')
]

# Miscellaneous
NTH_SUFFIXES = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']


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
        logging.info(message, 'requested ship, but in DMs, so invalid')
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
    logging.info(message, f'started Hunger Games instance with {len(hg_dict["players"])} players')


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
        await hunger_games_update_pregame_cancel(hg_key, hg_dict, response, message)

    # Toggle Bots command.
    elif any(response[0] == value for value in HG_PREGAME_TOGGLE_BOTS_TERMS):
        await hunger_games_update_pregame_toggle_bots(hg_key, hg_dict, response, message)

    # Change the 'updated' thing.
    hg_dict['updated'] = datetime.today()


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
        logging.info(message, 'tried to add player to Hunger Games instance, max size reached')
        return await messaging.send_text_message(message, 'Maximum game size already reached.')

    # Try/catch to catch CannotAccessUserlistError.
    try:

        # First, see if there's a second argument.
        if len(response) > 1:

            # Recreate the original response (full length), and feed it into the get_closest_users thing.
            argument_str = ' '.join(response[1:])
            try:
                closest_players = arguments.get_closest_users(message, argument_str, exclude_bots=not hg_dict['uses_bots'])

                # Iterate through the closest users and stop at the first one that's NOT in the game.
                for player in closest_players:
                    if player not in hg_dict['players']:
                        hg_dict['players'].append(player)
                        logging.info(message, f'added player {player} to Hunger Games instance')
                        return await send_pregame(message, hg_dict, f'Added {misc.get_photogenic_username(player)} to the game.')

                # If we didn't find a player, then send an invalid user thing.
                logging.info(message, f"attempted to add user '{argument_str}' to hunger games instance, invalid")
                return await messaging.send_text_message(message, f"Could not find user '{argument_str}'.")

            # If no user was specified, then call this method again with only one term in the response.
            except NoUserSpecifiedError:
                return await hunger_games_update_pregame_add(hg_key, hg_dict, [response[0]], message)

            # If no user could be found, then send back old reliable.
            except UnableToFindUserError:
                logging.info(message, f"attempted to add user '{argument_str}' to hunger games instance, invalid")
                return await messaging.send_text_message(message, f"Could not find user '{argument_str}'.")

        # If there isn't a second argument, attempt to get a completely random player.
        # First, try it without bots.
        if not hg_dict['uses_bots']:

            # Get the user list.
            user_list = misc.get_applicable_users(message, exclude_bots=True, exclude_users=hg_dict['players'])

            # If the user list is empty, then send an appropriate message back depending on whether or not there are bots available.
            if not user_list:
                user_list_with_bots = misc.get_applicable_users(message, exclude_bots=False, exclude_users=hg_dict['players'])
                if user_list_with_bots:
                    logging.info(message, 'attempted to add random user to hunger games instance, no non-bot users available')
                    return await messaging.send_text_message(message, "Every user who isn't a bot is already in the game.")
                else:
                    logging.info(message, 'attempted to add random user to hunger games instance, no more users available')
                    return await messaging.send_text_message(message, "Every user in the server is already in the game.")

        # Next, try it with bots.
        else:

            # Get the user list.
            user_list = misc.get_applicable_users(message, exclude_bots=False, exclude_users=hg_dict['players'])

            # If the user list is empty, then tell the users that.
            if not user_list:
                logging.info(message, 'attempted to add random user to hunger games instance, no more users available')
                return await messaging.send_text_message(message, "Every user in the server is already in the game.")

        # With the user list, grab a random user.
        added_user = random.choice(user_list)
        hg_dict['players'].append(added_user)

        # Send the message and junk.
        logging.info(message, f'added player {added_user} to Hunger Games instance')
        await send_pregame(message, hg_dict, f'Added {misc.get_photogenic_username(added_user)} to the game.')

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
        logging.info(message, 'tried to remove player from Hunger Games instance, min size reached')
        return await messaging.send_text_message(message, 'Minimum game size already reached.')

    # Try/catch to catch CannotAccessUserlistError.
    try:

        # First, see if there's a second argument.
        if len(response) > 1:

            # Recreate the original response (full length), and feed it into the get_closest_users thing.
            argument_str = ' '.join(response[1:])
            try:
                closest_players = arguments.get_closest_users(message, argument_str, exclude_bots=not hg_dict['uses_bots'])

                # Iterate through the closest users and stop at the first one that's actually in the game.
                for player in closest_players:
                    if player in hg_dict['players']:
                        hg_dict['players'].remove(player)
                        logging.info(message, f'removed player {player} from Hunger Games instance')
                        return await send_pregame(message, hg_dict, f'Removed {misc.get_photogenic_username(player)} from the game.')

                # If we didn't find a player, then send an invalid user thing.
                logging.info(message, f"attempted to remove user '{argument_str}' from hunger games instance, invalid")
                return await messaging.send_text_message(message, f"Could not find user '{argument_str}'.")

            # If no user was specified, then call this method again with only one term in the response.
            except NoUserSpecifiedError:
                return await hunger_games_update_pregame_delete(hg_key, hg_dict, [response[0]], message)

            # If no user could be found, then send back old reliable.
            except UnableToFindUserError:
                logging.info(message, f"attempted to remove user '{argument_str}' from hunger games instance, invalid")
                return await messaging.send_text_message(message, f"Could not find user '{argument_str}'.")

        # If there isn't a second argument, remove the last player in the game.
        removed_player = hg_dict['players'][-1]
        hg_dict['players'].remove(removed_player)

        # Send the message and junk.
        logging.info(message, f'removed player {removed_player} from Hunger Games instance')
        await send_pregame(message, hg_dict, f'Removed {misc.get_photogenic_username(removed_player)} from the game.')

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
    logging.info(message, 'initiated Hunger Games')
    await messaging.send_text_message(message, 'Generating Hunger Games instance...')

    # Set hunger games variables.
    hg_dict['past_pregame'] = True
    hg_dict['generated'] = False

    # Run the generation method.
    await generate_full_game(hg_dict, message)


async def hunger_games_update_pregame_cancel(hg_key, hg_dict, response, message):
    """
    Cancels the given hunger games dict (no confirmation, just delete).

    Arguments:
        hg_key (str) : The key for the hunger games dict.
        hg_dict (dict) : The full game dict.
        response (str[]) : A list of strings representing the response.
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Send the message and log.
    await messaging.send_text_message(message, 'Hunger Games canceled.')
    logging.info(message, 'canceled Hunger Games (pregame)')

    # Delete it.
    del CURRENT_GAMES[hg_key]


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
                if player.bot:
                    hg_players_no_bots.remove(player)
        # While there are less players than the minimum, add new players on randomly.
        while len(hg_players_no_bots) < HG_MIN_GAMESIZE:
            other_players = misc.get_applicable_users(message, True, hg_players_no_bots)
            # If there are other players, add a random one.
            if other_players:
                hg_players_no_bots.append(random.choice(other_players))
            # Otherwise, send an error message.
            else:
                logging.info(message, 'attempted to remove bots from Hunger Games instance, not enough users')
                return await messaging.send_text_message(message, 'Not enough non-bots to disallow bots.')

        # Allows it.
        # Copy over the new players list.
        hg_dict['players'] = hg_players_no_bots

        # Invert the uses_bots thing.
        hg_dict['uses_bots'] = not hg_dict['uses_bots']

        # Send message and log.
        logging.info(message, 'removed bots from Hunger Games instance')
        await send_pregame(message, hg_dict, 'Removed bots from the game.')

    # Otherwise, use this one.
    else:
        # Invert the uses_bots thing.
        hg_dict['uses_bots'] = not hg_dict['uses_bots']

        # Log and send message.
        logging.info(message, 'added bots to Hunger Games instance')
        await send_pregame(message, hg_dict, 'Allowed bots into the game.')


async def hunger_games_update_midgame(hg_key, hg_dict, response, message):

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
            await send_midgame(message, is_in_guild, hg_dict, count=max(1, response))
            hg_dict['updated'] = datetime.today()
            return True

        # Next command.
        elif any([response == 'n', 'response' == 'next']):
            await send_midgame(message, is_in_guild, hg_dict)
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
                await send_midgame(message, is_in_guild, hg_dict, count=max(1, response))
                hg_dict['updated'] = datetime.today()
                return True

        # Previous command.
        elif any([response == 'p', response == 'prev', response == 'previous']):
            if hg_dict['current_phase'] == 0 and hg_dict['phases'][hg_dict['current_phase']]['prev'] == -1:
                return
            else:
                await send_midgame(message, is_in_guild, hg_dict, do_previous=True)
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
    elif any([response.startswith(pre) for pre in HG_MIDGAME_BE_PATIENT_TERMS]):
        await hunger_games_update_midgame_still_generating(hg_key, hg_dict, response, message)


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
    logging.info(message, 'requested hunger games, still generating (impatient little sack of shit)')
    await message.channel.send('Still generating, be patient.')


async def send_pregame(message, hg_dict, title=HG_PREGAME_TITLE):
    """
    Sends the pregame roster thing.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        hg_dict (dict) : The full game dict.
        title (str) : The title of the embed, if any.
    """
    # Get all the player data.
    player_data = [(misc.get_photogenic_username(player),
                    tempfiles.checkout_profile_picture_by_user(player, message, 'hg_pregame', (HG_ICON_SIZE, HG_ICON_SIZE)), 0)
                   for player in hg_dict['players']]

    # Generate the player statuses image.
    image = makeimage_player_statuses(player_data)

    # Sends image, logs.
    await messaging.send_image_based_embed(message, image, title, HG_EMBED_COLOR,
                                           footer=HG_PREGAME_DESCRIPTION.format('Disallow' if hg_dict['uses_bots'] else 'Allow'))


async def send_midgame(message, is_in_guild, hg_dict, count=1, do_previous=False, do_increment=True):
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
                await send_midgame(message, is_in_guild, hg_dict, count, do_previous=True, do_increment=False)
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
                await send_midgame(message, is_in_guild, hg_dict, count, do_previous=False, do_increment=False)
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
        player_actions = makeimage_action(current_phase['act'], start, count, current_phase['desc'] if start == 0 else None)
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
                await send_midgame(message, is_in_guild, hg_dict, count, do_previous=do_previous, do_increment=False)
                return

        # Creates embed for win AND tie pages.
        if current_phase['type'] in ['win', 'tie']:
            embed = discord.Embed(title=current_phase['title'], colour=constants.HG_EMBED_COLOR)
            player_actions = makeimage_winner(current_phase['players'], current_phase['desc'])
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


def makeimage_player_statuses(players, placement=False, kills=False):
    """
    Generates a player status image.
    This can also be used to make player placement images and kill count lists.

    Arguments:
        players (str, PIL.Image, int)[] : The players, organized as a list of tuples.
                                          The first entry should be the player's photogenic username.
                                          The second entry should be the player's icon.
                                          The third entry should be one of three values if both placement and kills are False:
                                              0: Alive
                                              1: Newly Dead
                                              2: Dead
                                         Otherwise, they should be the placement or the kill count of each player.
        placement (bool) : Whether or not the third value in players is player placements.
        kills (str) : Whether or not the third value in players is kills.
    """
    # Splits all the players into their own rows.
    players_split = []
    current_split = []
    for player in players:
        if len(current_split) == HG_PLAYERSTATUS_WIDTHS[len(players)]:
            players_split.append(current_split)
            current_split = []
        current_split.append(player)
    players_split.append(current_split)

    # Gets the image width and height.
    image_width = HG_ICON_SIZE * len(players_split[0]) + HG_ICON_BUFFER * (len(players_split[0]) + 1)
    image_height = HG_PLAYERSTATUS_ROWHEIGHT * len(players_split) + HG_ICON_BUFFER * (len(players_split) + 1)

    # Creates all the images and drawers that will help us make the new image.
    player_statuses = Image.new('RGB', (image_width, image_height), HG_BACKGROUND_COLOR)
    player_drawer = ImageDraw.Draw(player_statuses)
    player_font = assets.open_font(HG_FONT, HG_FONT_SIZE)

    # Sets the current y at the buffer between the top and the first icon.
    current_y = HG_ICON_BUFFER

    # Iterate through each row.
    for split in players_split:
        # Set the starting x position.
        current_x = int((image_width - (len(split) * HG_ICON_SIZE + (len(split) - 1) * HG_ICON_BUFFER)) / 2)

        # Then, iterate through each player in each row.
        for player in split:

            # Gets pfp, pastes onto image.
            makeimage_pfp(player[1].copy(), player_statuses, player_drawer, current_x, current_y,
                          player[2] and not placement and not kills)

            # Writes name and status / placement.
            player_name = player[0]

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
                place = f'{player[2]}{NTH_SUFFIXES[player[2] % 10]} Place'
                player_drawer.text((current_x + int(HG_ICON_SIZE / 2 - player_font.getsize(place)[0] / 2),
                                    current_y + HG_ICON_SIZE + HG_FONT_SIZE + HG_TEXT_BUFFER), place, font=player_font,
                                   fill=misc.find_color_tuple_midpoint_hsv(HG_STATUS_ALIVE_COLOR, HG_STATUS_DEAD_COLOR,
                                                                           (player[2] - 1) / placement))

            # Killcount
            elif kills:
                if isinstance(kills, int):
                    kill_str = f'{player[2]} {" Kill" if player[2] == 1 else " Kills"}'
                    player_drawer.text((current_x + int(HG_ICON_SIZE / 2 - player_font.getsize(kill_str)[0] / 2),
                                        current_y + HG_ICON_SIZE + HG_FONT_SIZE + HG_TEXT_BUFFER), kill_str, font=player_font,
                                       fill=misc.find_color_tuple_midpoint_hsv(HG_STATUS_DEAD_COLOR, HG_STATUS_ALIVE_COLOR,
                                                                               player[2] / kills))
                else:
                    kill_str = '0 Kills'
                    player_drawer.text((current_x + int(HG_ICON_SIZE / 2 - player_font.getsize(kill_str)[0] / 2),
                                        current_y + HG_ICON_SIZE + HG_FONT_SIZE + HG_TEXT_BUFFER), kill_str, font=player_font,
                                       fill=misc.find_color_tuple_midpoint_hsv(HG_STATUS_DEAD_COLOR, HG_STATUS_ALIVE_COLOR,
                                                                               player[2] / kills))

            # Status
            else:
                status = 'Alive' if not player[2] else ('Deceased' if player[2] - 1 else 'Newly Deceased')
                player_drawer.text((current_x + int(HG_ICON_SIZE / 2 - player_font.getsize(status)[0] / 2),
                                    current_y + HG_ICON_SIZE + HG_FONT_SIZE + HG_TEXT_BUFFER), status, font=player_font,
                                   fill=HG_STATUS_ALIVE_COLOR if not player[2] else HG_STATUS_DEAD_COLOR)

            # Adds to current_x.
            current_x += HG_ICON_SIZE + HG_ICON_BUFFER

        # Adds to current_y.
        current_y += HG_PLAYERSTATUS_ROWHEIGHT + HG_ICON_BUFFER

    return player_statuses


def makeimage_action(player_images, actions, start, count=1, action_desc=None):
    """
    Displays count number of actions at once.

    player_images (dict) : A dict of player profile pictures, with the profile pictures keyed by player ids.
    actions (dict[]) : A list of dicts detailing all the actions in this phase.
    start (int) : What index to start at.
    count (int) : How many actions to put into this image.
    action_desc (str) : The action description, if any.
    """
    # Makes the font and gets the action description width, if any.
    action_font = assets.open_font(HG_FONT, HG_FONT_SIZE)
    action_desc_width = action_font.getsize(action_desc)[0] if action_desc else 0

    # Gets the image height.
    # Also makes the full action text while we're at it.
    image_height = HG_ACTION_ROWHEIGHT * count + HG_ICON_BUFFER + (HG_FONT_SIZE + HG_HEADER_BORDER_BUFFER * 3 if action_desc else -1)
    text_sizes = []

    # Get the image width.
    # The image width is diffcult to gather, because we have to test the widths of everything.
    image_width = action_desc_width + HG_ICON_BUFFER * 2 + HG_HEADER_BORDER_BUFFER * 2 if action_desc else -1

    # Iterate through each action in the range.
    for ind in range(start, start + count):

        # Tests for text boundaries
        full_action_text = actions[ind]['act']
        for ind2 in range(len(actions[ind]['players'])):
            full_action_text = full_action_text.replace('{' + str(ind2) + '}', actions[ind]['players'][ind2][1])

        # Calculates text widths and appends them to the text_sizes list.
        text_width = action_font.getsize(full_action_text)[0]
        image_width = max(image_width, text_width + HG_ICON_BUFFER * 2)
        text_sizes.append(text_width)

        # Tests for image boundaries
        image_width = max(image_width, HG_ICON_SIZE * len(actions[ind]['players']) + HG_ICON_BUFFER * (len(actions[ind]['players']) + 1))

    # Creates all the images and drawers that will help us make the new image.
    action_image = Image.new('RGB', (image_width, image_height), HG_BACKGROUND_COLOR)
    player_drawer = ImageDraw.Draw(action_image)

    # Sets the current y at the buffer between the top and the first icon.
    current_y = HG_ICON_BUFFER

    # Draw the description, if any.
    if action_desc:

        # Sets the current x and draws the border around the description.
        current_x = int((image_width - action_desc_width) / 2)
        player_drawer.rectangle(
            [(current_x - HG_HEADER_BORDER_BUFFER, current_y - HG_HEADER_BORDER_BUFFER),
             (current_x + action_desc_width + HG_HEADER_BORDER_BUFFER, current_y + HG_FONT_SIZE + HG_HEADER_BORDER_BUFFER)],
            HG_HEADER_BACKGROUND_COLOR,
            HG_HEADER_BORDER_COLOR
        )

        # Draws the text and adds to the current y.
        player_drawer.text((current_x, HG_ICON_BUFFER), action_desc, font=action_font, fill=HG_HEADER_TEXT_COLOR)
        current_y += HG_FONT_SIZE + HG_HEADER_BORDER_BUFFER * 3

    # Num keeps track of the text sizes.
    num = 0

    # Iterate through all the actions.
    for ind in range(start, start + count):

        # Set the current x.
        current_x = int(image_width / 2) - int(len(actions[ind]['players']) / 2 * HG_ICON_SIZE) - \
                    int((len(actions[ind]['players']) - 1) / 2 * HG_ICON_BUFFER)

        # Gets each player's pfp and pastes it onto the image.
        for player in actions[ind]['players']:
            makeimage_pfp(player_images[player[0]], action_image, player_drawer, current_x, current_y)
            current_x += HG_ICON_SIZE + HG_ICON_BUFFER

        # Draws each part of the text.
        current_x = int((image_width - text_sizes[num]) / 2)
        current_y += HG_ICON_SIZE + HG_TEXT_BUFFER
        makeimage_action_text(actions[ind]['act'], actions[ind]['players'], player_drawer, current_x, current_y, action_font)

        # Adds to the current_y and num.
        current_y += HG_FONT_SIZE + HG_ICON_BUFFER
        num += 1

    return action_image


def makeimage_winner(players, desc=None):
    """
    Displays the winner(s).
    Like the makeimage_action method, but without all the previous and count and whatnot.
    """
    # Makes the font
    action_font = ImageFont.truetype()

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
        makeimage_pfp(player[0], action_image, player_drawer, current_x, current_y, player[2])
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
        makeimage_action_text(constants.HG_WINNER_DEAD_EVENT if players[0][2] else constants.HG_WINNER_EVENT, players, player_drawer, current_x, current_y, action_font)

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
                                       white=misc.multiply_color_tuple((255, 255, 255), HG_PLAYERSTATUS_DEAD_PFP_DARKEN_FACTOR),
                                       mid=misc.multiply_color_tuple((128, 128, 128), HG_PLAYERSTATUS_DEAD_PFP_DARKEN_FACTOR))
    image.paste(player_pfp, (pfp_x, pfp_y))

    # Draws border around player icon.
    drawer.line([(pfp_x - 1, pfp_y - 1),
                 (pfp_x + HG_ICON_SIZE, pfp_y - 1),
                 (pfp_x + HG_ICON_SIZE, pfp_y + HG_ICON_SIZE),
                 (pfp_x - 1, pfp_y + HG_ICON_SIZE),
                 (pfp_x - 1, pfp_y - 1)], width=1, fill=0)


def makeimage_action_text(remaining_text, players, drawer, txt_x, txt_y, action_font):
    # TODO
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
        drawer.text((txt_x, txt_y), players[ind][1], font=action_font, fill=HG_ACTION_PLAYER_COLOR)
        txt_x+= action_font.getsize(players[ind][1])[0]

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
    # Get rid of redundant tag.
    del hg_dict['uses_bots']

    # Create player statuses dict in the hg_dict.
    statuses = {}
    for player in hg_dict['players']:
        statuses[player.id] = {'name': misc.get_photogenic_username(player), 'dead': False, 'hurt': False, 'inv': [], 'kills': 0}
    hg_dict['statuses'] = statuses

    # Makes the phases.
    hg_dict['phases'] = []

    # First, we generate the bloodbath.
    generate_bloodbath(hg_dict)

    # Loop variables.
    # day_night keeps track of what number day / night it was.
    day_night = 1
    # Self-explanatory.
    turns_since_event = 0
    dead_last_loop = []

    # Then we cycle through stuff until one person survives or EVERYONE is dead.
    while True:

        # Test for dead people at the start of the loop.
        tie, continue_game = generate_detect_dead(hg_dict)
        if not continue_game:
            break

        # Test for event.
        # Events can only occur at day/night 4. The chances of an event slowly increase over time.
        # If an event occurs, normal day/night actions are not taken.
        if day_night >= 4 and turns_since_event > 1 and random.random() < 1 - (1 - HG_EVENT_DEFAULT_CHANCE)**turns_since_event:
            # Choose random event and generate the actions.
            the_event = random.choice(HG_EVENTS)
            generate_normal_actions(hg_dict, the_event[0], the_event[1], the_event[2])
            # Reset turns_since_event.
            turns_since_event = 0

        # Otherwise, do normal day and night events.
        else:
            # Day.
            generate_normal_actions(hg_dict, HG_NORMAL_DAY_ACTIONS, 'Day {}'.format(day_night))

            # Test for dead people.
            tie, continue_game = generate_detect_dead(hg_dict)
            if not continue_game:
                break

            # Night.
            generate_normal_actions(hg_dict, HG_NORMAL_NIGHT_ACTIONS, 'Night {}'.format(day_night))
            day_night += 1

        # Test for dead people.
        tie, continue_game = generate_detect_dead(hg_dict)
        if not continue_game:
            break

        # Add a new player status page.
        player_statuses = []
        new_deaths = 0

        # Iterate through all the players.
        for player in hg_dict['statuses']:
            player_statuses.append((player, hg_dict['statuses'][player]['name'],
                                    (2 if player in dead_last_loop else 1) if hg_dict['statuses'][player]['dead'] else 0))

            # Adds to dead_last_loop if they're dead THIS loop.
            if player not in dead_last_loop and hg_dict['statuses'][player]['dead']:
                dead_last_loop.append(player)
                new_deaths += 1

        # Add the player status dict to the phases.
        hg_dict['phases'].append({'type': 'status', 'all': player_statuses, 'new': new_deaths})

        # Increase chances of encountering disaster next time.
        if day_night >= 4:
            turns_since_event += 1

    # Now that the loop is broken, display cannon shots and declare winner.
    # First, make a new player status page.
    player_statuses = []
    new_deaths = 0

    # Iterate through all the players.
    for player in hg_dict['statuses']:
        player_statuses.append((player, hg_dict['statuses'][player]['name'],
                                (2 if player in dead_last_loop else 1) if hg_dict['statuses'][player]['dead'] else 0))

    # Add the player status dict to the phases.
    hg_dict['phases'].append({'type': 'status', 'all': player_statuses, 'new': new_deaths})

    # If there's a tie, run this part.
    if tie:

        # Determine who tied
        tiees = []
        # Get the maximum death number for placement purposes.
        max_deathnum = -1

        # Get the max death num.
        for player in hg_dict['statuses']:
            max_deathnum = max(max_deathnum, hg_dict['statuses'][player]['dead_num'])

        # For each player, if their death num equals the max, then append that to the tiees.
        for player in hg_dict['statuses']:
            if max_deathnum == hg_dict['statuses'][player]['dead_num']:
                tiees.append(player)

        # Add tie phase to phases ONLY if there's more than one.
        if len(tiees) > 1:
            hg_dict['phases'].append({'type': 'tie', 'players': [(tienum, hg_dict['statuses'][tienum]['name'], True) for tienum in tiees],
                                      'title': HG_TIE_TITLE, 'desc': HG_TIE_TITLE})

        # Otherwise, it's a victory, but dead.
        else:
            hg_dict['phases'].append({'type': 'win', 'players': [(tiees[0], hg_dict['statuses'][tiees[0]]['name'], True)],
                                      'title': HG_WINNER_TITLE, 'desc': HG_WINNER_TITLE})

    # Not a tie, run this next part.
    else:

        # Determine winner by who doesn't have a death number.
        winner = None
        for player in hg_dict['statuses']:
            if 'dead_num' not in hg_dict['statuses'][player]:
                winner = player
                break

        # Add win phase to phases
        hg_dict['phases'].append({'type': 'win', 'players': [(winner, hg_dict['statuses'][winner]['name'], False)],
                                  'title': HG_WINNER_TITLE, 'desc': HG_WINNER_TITLE})

    # Makes the placement screen.
    generate_placement_screen(hg_dict)

    # Makes the kill count screen.
    generate_kill_count_screen(hg_dict)

    # Re-do the playerlist in the hg_dict.
    new_players = {}
    for player in hg_dict['players']:
        new_players[player.id] = tempfiles.checkout_profile_picture_by_user(player, message, 'hunger_games_full',
                                                                            (HG_ICON_SIZE, HG_ICON_SIZE))
    hg_dict['players'] = new_players

    # Updates hunger games dict.
    del hg_dict['statuses']
    hg_dict['current_phase'] = 0
    hg_dict['confirm_cancel'] = False
    hg_dict['generated'] = True
    hg_dict['complete'] = False

    # Sends the first message and logs.
    logging.info(message, 'generated complete hunger games instance')
    await messaging.send_image_based_embed(
        message,
        makeimage_action(hg_dict['players'], hg_dict['phases'][0]['act'], 0, 1, hg_dict['phases'][0]['desc']),
        'The Bloodbath, Action 1', HG_EMBED_COLOR, HG_BEGINNING_DESCRIPTION
    )


def generate_bloodbath(hg_dict):
    """
    Generates all the actions for each player in the bloodbath.
    This is just like any other list of actions, but they're a lot more simplified because there are no prerequisite ones.

    Arguments:
        hg_dict (dict) : The full game dict.
    """
    # Player_actions stores the user id of everyone who hasn't had an action yet.
    player_actions = [uid for uid in hg_dict['statuses']]
    # Actions stores all the actions.
    actions = []

    # Iterates through all the actions, picking them at random for the player_actions.
    while player_actions:

        # Creates necessary prerequisites for do while loop.
        # Create a current action with a length of player actions so that the while loop will trigger.
        curr_action = {'players': len(player_actions)}
        # Take a player out and use it as the base player.
        chosen_players = [random.choice(player_actions)]
        player_actions.remove(chosen_players[0])

        # While loop, finds a good action.
        while curr_action['players'] > len(player_actions):
            curr_action = random.choice(HG_BLOODBATH_ACTIONS)

        # Adds more players to current action, if necessary.
        for i in range(curr_action['players']):
            chosen_players.append(random.choice(player_actions))
            player_actions.remove(chosen_players[-1])

        # Add the actions to the list.
        actions.append({'players': [(player, hg_dict['statuses'][player]['name']) for player in chosen_players], 'act': curr_action['act'],
                        'full': curr_action})

        # Generate statuses
        generate_statuses(hg_dict['statuses'], actions[-1])

    # Adds to the phases.
    hg_dict['phases'].append({'type': 'act', 'act': actions, 'title': 'The Bloodbath', 'next': 1, 'prev': -1,
                              'desc': 'As the tributes stand upon their podiums, the horn sounds.', 'done': False})


def generate_normal_actions(hg_dict, action_dict, title, desc=None):
    """
    Generates all the actions for each player in the a normal action round.

    Arguments:
        hg_dict (dict) : The full game dict.
        action_dict (dict) : The action dict.
        title (str) : The action title.
        desc (str) : The action description, if any.
    """
    # Player_actions stores the user id of everyone who hasn't had an action yet.
    # Unlike in generate_bloodbath, this version excludes people who are dead.
    player_actions = []
    for uid in hg_dict['statuses']:
        if not hg_dict['statuses'][uid]['dead']:
            player_actions.append(uid)
    # Actions stores all the actions.
    actions = []

    # Iterates through triggers.
    # TODO: Add trigger actions
    for trigger in action_dict['trigger']:
        pass

    # Iterates through all the actions, picking them at random for the player_actions.
    while player_actions:

        # Creates necessary prerequisites for do while loop.
        # Create a current action with a length of player actions so that the while loop will trigger.
        curr_action = {'players': len(player_actions)}
        # Take a player out and use it as the base player.
        chosen_players = [random.choice(player_actions)]
        player_actions.remove(chosen_players[0])

        # While loop, finds a good action.
        while curr_action['players'] > len(player_actions):
            curr_action = random.choice(action_dict['normal'])

        # Adds more players to current action, if necessary.
        for i in range(curr_action['players']):
            chosen_players.append(random.choice(player_actions))
            player_actions.remove(chosen_players[-1])

        # Add the actions to the list.
        actions.append({'players': [(player, hg_dict['statuses'][player]['name']) for player in chosen_players], 'act': curr_action['act'],
                        'full': curr_action})

    # Shuffles the actions and generates statuses.
    random.shuffle(actions)
    for curr_action in actions:
        generate_statuses(hg_dict['statuses'], curr_action)

    # Adds to the phases.
    if not desc:
        desc = title
    hg_dict['phases'].append({'type': 'act', 'act': actions, 'title': title, 'next': 0, 'prev': -1, 'desc': desc, 'done': False})


def generate_statuses(hg_statuses, action):
    """
    Updates the statuses of players post-action in the hg_dict.

    Arguments:
        hg_statuses (dict) : The statuses of every player in the game.
        action (dict) : The action that needs to trigger this status check.
    """
    # First, we handle deaths.
    if 'kill' in action['full']:
        # Mark player as dead.
        for ind in action['full']['kill']:
            hg_statuses[action['players'][ind][0]]['dead'] = True
        # Mark player's place in the game.
        for ind in action['full']['kill']:
            hg_statuses[action['players'][ind][0]]['dead_num'] = [hg_statuses[player]['dead'] for player in hg_statuses].count(True) - 1

    # Next, injuries.
    if 'hurt' in action['full']:
        for ind in action['full']['hurt']:
            hg_statuses[action['players'][ind][0]]['hurt'] = True

    # Kill credit.
    if 'credit' in action['full']:
        for ind in action['full']['credit']:
            hg_statuses[action['players'][ind][0]]['kills'] += 1

    # Healing.
    if 'heal' in action['full']:
        for ind in action['full']['heal']:
            hg_statuses[action['players'][ind][0]]['hurt'] = False

    # Items.
    if 'give' in action:
        for ind in range(len(action['give'])):

            # Item 0 (nothing).
            if action['give'][ind] == 0:
                continue

            # Negative item (remove their thing).
            elif action['give'][ind] < 0:
                hg_statuses[action['players'][ind][0]]['inv'].remove(-action['give'][ind])

            # Other items.
            else:

                # Special items
                # 3000, 1 - 3 random items
                if action['full']['give'][ind] == 3000:
                    for i in range(random.randint(1, 3)):
                        hg_statuses[action['players'][ind][0]]['inv'].append(random.choice(HG_ALL_ITEMS))

                # 4000, one of each item type
                elif action['full']['give'][ind] == 4000:
                    hg_statuses[action['players'][ind][0]]['inv'].append(random.choice(HG_WEAPON_ITEMS))
                    hg_statuses[action['players'][ind][0]]['inv'].append(random.choice(HG_HEALTH_ITEMS))
                    hg_statuses[action['players'][ind][0]]['inv'].append(random.choice(HG_FOOD_ITEMS))

                # 8888, take away rope, give food
                elif action['full']['give'][ind] == 8888:
                    hg_statuses[action['players'][ind][0]]['inv'].remove(8)
                    hg_statuses[action['players'][ind][0]]['inv'].append(10)
                    hg_statuses[action['players'][ind][0]]['inv'].append(104)

                # 9999, take away everything and give it to everyone else
                elif action['full']['give'][ind] == 9999:
                    # Iterate through and give it to other folks one at a time.
                    ind2 = 0
                    for item in hg_statuses[action['players'][ind][0]]['inv']:
                        hg_statuses[action['players'][ind][0]]['inv'].remove(item)
                        if ind2 % len(action['players']) == ind:
                            ind2 += 1
                        hg_statuses[action['players'][ind2][0]]['inv'].append(item)
                        ind2 += 1

                # Any other item, just give it to them normally.
                else:
                    hg_statuses[action['players'][ind][0]]['inv'].append(action['give'][ind])

    # Delete the 'full' tag on the action.
    del action['full']


def generate_detect_dead(hg_dict):
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


def generate_placement_screen(hg_dict):
    """
    Generates the placement screen.

    Arguments:
        hg_dict (dict) : The full game dict.
    """
    # First, makes a list of placements.
    pre_placement_players = [k for k in hg_dict['statuses']]
    placements = []

    # While not everyone has been placed, iterate through the loop.
    while pre_placement_players:

        # The min_placement keeps track of the minimum placement.
        min_placement = len(hg_dict['statuses'])
        current_placement_players = []

        # Iterate through the players.
        # Get the minimum placement and the players in that placement.
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
            min_placement -= 1

        # Adds player to the dict.
        for player in current_placement_players:
            placements.append((player, hg_dict['statuses'][player]['name'], len(hg_dict['statuses']) - min_placement))
            pre_placement_players.remove(player)

    # Reverses placements list to sort from first to last and adds the placement to the phases.
    placements.reverse()
    hg_dict['phases'].append({'type': 'place', 'all': placements, 'max': max([place[2] for place in placements]) - 1})


def generate_kill_count_screen(hg_dict):
    """
    Generates the kill count screen.

    Arguments:
        hg_dict (dict) : The full game dict.
    """
    # First, makes a list of placements.
    pre_placement_players = [k for k in hg_dict['statuses']]
    kill_placements = []

    # While not everyone has been placed, iterate through the loop.
    while pre_placement_players:

        # The max_placement keeps track of the maximum placement.
        max_placement = 0
        current_placement_players = []

        # Iterate through the players.
        # Get the maximum placement and the players in that placement.
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


def hunger_games_set_embed_image(image, embed):
    current_image_filepath = os.path.join(constants.TEMP_DIR, constants.HG_IMAGE_PATH)
    image.save(current_image_filepath)
    file = discord.File(current_image_filepath, filename='hg_image_filepath.png')
    embed.set_image(url='attachment://hg_image_filepath.png')
    return file


async def pregame_shuffle(message, player_count, hg_dict):
    """
    Shuffles a pregame hunger games cast.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        player_count (int) : The amount of players to use.
        hg_dict (dict) : The full game dict.
    """
    # If the player count is more than the max or less than the minimum, set them to their capstone values.
    player_count = min(player_count, HG_MAX_GAMESIZE)
    player_count = max(player_count, HG_MIN_GAMESIZE)

    # Get the user list. If user list is < player_count people, we add bots as well.
    try:
        user_list = misc.get_applicable_users(message, exclude_bots=True)
        uses_bots = False
        if len(user_list) < player_count:
            user_list = misc.get_applicable_users(message, exclude_bots=False)
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

    # Set in players and bot bool.
    hg_dict['players'] = hg_players
    hg_dict['uses_bots'] = uses_bots

    # Return True to signal success.
    return True


# Command values
DEVELOPER_COMMAND_DICT = {
    'hg': hunger_games_start
}
REACTIVE_COMMAND_LIST = [
    hunger_games_update
]


# Unfortunately, one or two variables have to be established all the way down here.
HG_PREGAME_SHUFFLE_TERMS = ['s', 'shuffle'] + [environment.get('GLOBAL_PREFIX') + command for command in DEVELOPER_COMMAND_DICT]
HG_MIDGAME_BE_PATIENT_TERMS = [environment.get('GLOBAL_PREFIX') + command for command in DEVELOPER_COMMAND_DICT]

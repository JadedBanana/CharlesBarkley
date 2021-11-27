
# Hunger Games
# =================DEBUG==================
# 0: nothing
# 3000: 1 - 3 random items
# 4000: 1 weapon, 1 food item, 1 health item
# 8888: make net from rope, give food
# 9999: take away everything and give it to everyone else
# ================WEAPONS================
# 1: mace
# 2: sword
# 3: spear
# 4: explosives
# 5: throwing knives
# 6: hatchet
# 7: slingshot
# 8: rope
# 9: shovel
# 10: net
# 11: molotov cocktail
# 12: bow
# 13: poison
# 14: scissors
# ==================FOOD=================
# 101: clean water
# 102: river water
# 103: loaf of bread
# 104: raw meat
# =================HEALTH================
# 201: bandages
# 202: medicine
# 203: first aid kit
# ==================OTHER================
# 301: shack
# 302: camouflage
# 303: cave
# 304: high ground
HG_WEAPON_ITEMS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
HG_FOOD_ITEMS = [101, 102, 103, 104]
HG_HEALTH_ITEMS = [201, 202, 203]
HG_ALL_ITEMS = HG_WEAPON_ITEMS + HG_FOOD_ITEMS + HG_HEALTH_ITEMS
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
# Pregame
HG_MIN_GAMESIZE = 2
HG_MAX_GAMESIZE = 48
HG_PREGAME_TITLE = 'The Reaping'
HG_PREGAME_DESCRIPTION = 'Respond one of the following:\nS: Shuffle\t\tR: Replace\nA: Add\t\t\tD: Delete\t\tB: {} bots\nP: Proceed\t\tC: Cancel'
# Winner / Ties
HG_WINNER_TITLE = 'The Winner'
HG_TIE_TITLE = 'The Winners'
HG_WINNER_EVENT = 'The winner is {0}!'
HG_WINNER_DEAD_EVENT = 'The winner is {0}! However, they died too, so it\'s sort of a hollow victory.'
HG_TIE_EVENT = ('Since they died at the same time, it\'s a tie between ', ', ', 'and ', '!')
HG_COMPLETE_PHASE_TYPES = ['win', 'tie']
# Graphics
HG_PLAYERSTATUS_WIDTHS = [0, 1, 2, 3, 4, 3, 3, 4, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
HG_PLAYERSTATUS_ROWHEIGHT = 172
HG_PLAYERNAME_FONT = 'assets/arial_bold.ttf'
HG_ACTION_ROWHEIGHT = 175
HG_FONT_SIZE = 16
HG_ICON_SIZE = 128
HG_ICON_BUFFER = 25
HG_TEXT_BUFFER = 6
HG_HEADER_BORDER_BUFFER = 7
HG_BACKGROUND_COLOR = (93, 80, 80)
HG_HEADER_TEXT_COLOR = (255, 207, 39)
HG_STATUS_ALIVE_COLOR = (0, 255, 0)
HG_STATUS_DEAD_COLOR = (255, 102, 102)
HG_STATUS_DEAD_PFP_DARKEN_FACTOR = 0.65
HG_ACTION_PLAYER_COLOR = (251, 130, 0)
HG_HEADER_BORDER_COLOR = (255, 255, 255)
HG_HEADER_BACKGROUND_COLOR = (35, 35, 35)
HG_EMBED_COLOR = (251 << 16) + (130 << 8)
# Descriptions
HG_BEGINNING_DESCRIPTION = 'Respond one of the following:\nN: Next Action\nC: Cancel Game'
HG_MIDGAME_DESCRIPTION = 'Respond one of the following:\nN: Next Action\tP: Previous Action\nC: Cancel Game'
HG_POSTGAME_BEGINNING_DESCRIPTION = 'Respond one of the following:\nN: Next Action\nR: Replay (same cast)\tS: New Game\tC: Close'
HG_POSTGAME_MIDGAME_DESCRIPTION = 'Respond one of the following:\nN: Next Action\tP: Previous Action\nR: Replay (same cast)\tS: New Game\tC: Close'
HG_THE_END_DESCRIPTION = 'The end! Respond one of the following:\nN: Next Action\tP: Previous Action\nR: Replay (same cast)\tS: New Game\tC: Close'
HG_FINALE_DESCRIPTION = 'Respond one of the following:\nP: Previous Action\nR: Replay (same cast)\tS: New Game\tC: Close'
# Events
HG_EVENT_DEFAULT_CHANCE = 0.2
HG_EVENTS = [
    (HG_FLOOD_EVENT, 'The Flood', 'A vicious flood suddenly appears out of nowhere and sweeps through the Arena.'),
    (HG_FIRE_EVENT, 'The Fire', 'A sudden bolt of lightning sparks a fire, which explodes into a massive Arena-wide forest fire.'),
    (HG_TORNADO_EVENT, 'The Tornado', 'Winds in the Arena pick up and a tornado begins to tear its way through the Arena.'),
    (HG_RESTOCK_EVENT, 'The Replenishing', 'The Cornucopia is restocked with food, weapons, and medical supplies.')
]
# Files
HG_IMAGE_PATH = 'current_hg_image.png'

# Thank you
THANKYOU_RESPONSES = [
    ':)',
    ':D',
    'You\'re welcome!',
    'It\'s my pleasure.',
    'I aim to please!',
    'Hehe, I\'m just doing my job!',
    ':blush:'
]

# Help message
HELP_MSG = '''```
======================
  Jadi3Pi {} Help
======================
   (PREFIX: j!)

===============
      FUN
===============
- copy: Mention someone to start copying their every word
- stopcopying: Stop copying everyone in this server
- uwu: Convert a message to uwu-speak.
- ship: Ship two random users together. Tag another user to ship them with a random someone else.
- randomyt / randomyoutube: Generate a random YouTube video
- randomwiki / randomwikipedia: Generate a random English Wikipedia page

===============
    UTILITY
===============
- weather: Give the name of a city and will report the current weather at that location
- calc / eval: Evaluates a mathematical expression
- hex / hexadecimal: Converts a number to hexadecimal
- duo / duodec / duodecimal: Converts a number to duodecimal
- dec / decimal: Converts a number to decimal
- oct / octal: Converts a number to octal
- bin / binary: Converts a number to binary

===============
     OTHER
===============
- help: Display this message
- runtime: Display the amount of time this bot has been running for
- uptime: Display the amount of time this bot has been connected to Discord for
'''

# Dev-only section for help message
HELP_MSG_DEV_ADDENDUM = '''
===============
   DEV-ONLY
===============
- getpid: Returns the local PID of this process
- localip: Returns the local ip the bot is running from
- toggleignoredev: Toggles whether or not to ignore developer on Linux side
- loglist: Sends a list of all the log files in the logs folder
- sendlog: Sends the log for today, or a specific date (YYYY-MM-DD)
- update: Trigger remote update (pull from Git master branch)
- reboot: Trigger remote reboot
```'''

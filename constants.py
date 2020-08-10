# Constants file
# General use
VERSION = '0.1.8'
DEVELOPER_DISCORD_IDS = [
    110194551586570240,   # Jade
    158429528874680320    # Jabe
]
ON_WINDOWS_ONLY_RESPOND_TO_DEV = True
IGNORE_DEVELOPER_ONLY_WORKS_ON_LINUX = True

# Logging constants
DEFAULT_LEVEL = 0
LOG_TO_CONSOLE = True
LOG_TO_FILE = True
DO_LEVEL_HEADERS = True
DO_TIMESTAMPS = True
LOGS_DIR = 'logs'

# Server, channel, user
COMM_LOG_PREFIX = '{} ({}, {}): '

# Bot stuff
# Global crap
BOT_TOKEN = 'NzQwNjEwMTc2MDM3NTUyMTc4.Xyrg-Q.8jBguEMXHXFmZvXOY5UAdXu4FE0'
GLOBAL_PREFIX = 'j!'

# YouTube
YOUTUBE_API_KEY = 'AIzaSyDfdrytJZ4Ft9W76VdR-t4HOZTOR7ESMEg'
YOUTUBE_QUOTA_RESET_HOUR = 3
YOUTUBE_RICKROLL_URL = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
YOUTUBE_RICKROLL_CHANCE = 0.0002
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}'
YOUTUBE_SEARCH_COUNT = 100
YOUTUBE_SEARCH_LENGTHS = [1, 2, 3, 4, 5]
YOUTUBE_SEARCH_WEIGHTS = [36, 1296, 46656, 1679616, 60466176]
YOUTUBE_VIDEO_URL_FORMAT = 'https://www.youtube.com/watch?v={}'

# Ultimates
ULTIMATE_PRONOUNS = [
    ['you', 'they'],
    ['your', 'their'],
    ["you're", "they're"],
    ['yourself', 'themselves'],
    ["you've", "they've"],
    ["you'll", "they'll"],
    ['You', 'They'],
    ['Your', 'Their'],
    ["You're", "They're"],
    ['Yourself', 'Themselves'],
    ["You've", "They've"],
    ["You'll", "They'll"]
]
ULTIMATE_TITLES = {
    '???': '! Guess {0} don\'t remember, huh? Well, better hope it\'s a good one.',
    'Actress': '! Try as they might, no one could ever hope to emulate the passion {0} put into {1} performances!',
    'Adventurer': '! Who doesn\'t love discovering lands unknown? Thrills and new discoveries are right up {1} alley!',
    'Affluent Progeny': '. Heir to the world\'s elite, {0} are destined to rule the world from the shadows.',
    'Akido Master': '! Hi-yah!',
    'Analyst': '. {6} can dissect any situation and see things most other people can\'t.',
    'Angler': '. No one really gets how to gut a fish quite like {0}.',
    'Animator': '! Don\'t forget! Anime is art!',
    'Anthropologist': '. {6} know more about the Salem Witch Trials than anyone else on Earth.',
    'Archer': '! {8} like Hawkeye up in here!',
    'Architect': '. {6} can build you a nice house... for a small fee, of course.',
    'Artist': '! Pretty colors and lifelike statues are {1} whole deal!',
    'Assassin': '. Here\'s the target. You have 24 hours.',
    'Astronaut': '! {6} can reach the stars for sure! If anyone can, it\'s {0}!',
    'Baseball Player': '! Batter up!',
    'Beatboxer': '',
    'Blacksmith': '! Daggers and knives and swords, oh my!',
    'Biker Gang Leader': '! Rev your fucking engines! Let\'s tear up this town!',
    'Biologist': '. {7} favorite joke is that one about mitosis.',
    'Bodyguard': '. Are {0} prepared to lay down {1} life?',
    'Botanist': '! Ooh, pretty!',
    'Bounty Hunter': '. Feel like hunting down any criminals?',
    'Boxer': '! *DING-DING-DING!* It\'s a TKO!',
    'Breakdancer': '! Kick it!',
    'Breeder': '! Use {1} prowess in the dark arts to... potty-train this dog!',
    'Broadway Singer': '. What\'s {1} favorite musical?',
    'CGI Artist': '! It looks so *real!*',
    'Cheerleader': '! {12}, they\'re the one, if they don\'t win then that\'s no fun!',
    'Chemist': '. Man, that\'s such a boron career. It\'s too basic, if you ask me.',
    'Child Caregiver': '. {8} basically like a goblin herder.',
    'Clairvoyant': '! {6} and {1} 30% accuracy rate can predict ANY crime that probably won\'t happen!',
    'Clown': '! {8} a clown! Honk honk! :o)',
    'Composer': '',
    'Con Artist': '{8} a slimy bastard who can convince anyone anything is a good idea.',
    'Confectioner': '! How sweet of {0}!',
    'Conspiracy Theorist': '. So {0} think the moon landing was faked, huh? Well, have you heard the MOON is fake, too?',
    'Curator': '. {7} collection is far more impressive than the Smithsonian.',
    'Despair': '',
    'Detective': '! And the killer is... you!',
    'Drug Dealer': '',
    'Drummer': '',
    'DJ': '! Lay down some beats, man!',
    'Electrical Engineer': '',
    'Entomologist': '... so, if I find a spider, do I bring it to you?',
    'Entrepreneur': '',
    'Epidemiologist': '',
    'Exorcist': '',
    'Fanfic Creator': '! So, what next? Maybe a slow-burn coffee shop AU with some self-inserts, a handful of OC\'s, F/F and M/M, a little OOC if necessary, but all in all just fanservice fic for Danganronpa?',
    'Farmer': '! Do {1} have a dog named Bingo? Or... just Ingo? Or Ngo?',
    'Fashionista': '! Looking cool, {8}!',
    'Film Director': '! When on set, nobody questions {1} judgement.',
    'Forum Admin': '. {10} seen some serious shit.',
    'Gambler': '',
    'Gamer': '',
    'Golfer': '. No one can beat the power of a true Scottish swing.',
    'Guitarist': '',
    'Gymnast': '',
    'Hacker': '. {6} didn\'t actually get {1} title from some school official, {0} got it by hacking into the servers and giving it to {3}.',
    'Hairstylist': '',
    'Hope': '',
    'Housekeeper': '',
    'Hypnotist': '',
    'Idol': '',
    'Impostor': '. No one truly knows who {0} are beneath the mask... or that {2} even wearing one at all.',
    'Internet Troll': '. {8} really good at pissing people off online.',
    'Inventor': '',
    'Landscaper': '',
    'Lawyer': '',
    'Lucky Student': '',
    'Magician': '! Prepare to be amazed!',
    'Maid': '',
    'Martial Artist': '',
    'Makeup Artist': '',
    'Matchmaker': '',
    'Mechanic': '. Every tractor {0} work on is sexy.',
    'Medium': '',
    'Merchant': '',
    'Meteorologist': '',
    'Model': '',
    'Moral Compass': '. {6} are the best at telling other people how to act.',
    'Musician': '',
    'Neurologist': '',
    'Ninja': ', lying hidden in the shadows. Watch out.',
    'Nurse': '',
    'Pharmacist': '. It\'s not totally clear how {0} managed to become one at such a young age, but regardless, {0} are.',
    'Photographer': '',
    'Poet': '. {6} just have a way with words others can only dream of matching.',
    'Prankster': '. What devious thing did {0} do to get this title...?',
    'Prisoner': '',
    'Puppeteer': '',
    'Psychologist': '',
    'Physicist': '',
    'Pianist': '',
    'Pilot': '',
    'Policeman': '',
    'Priest': '. With just a wave of {1} hand, {0} can enlighten hundreds at a time.',
    'Princess': '',
    'Programmer': '',
    'Pyrotechnician': '',
    'Researcher': '',
    'Robot': '',
    'Sailor': '',
    'Scout': '. Though high adventure may be fun, there is nothing quite like giving back to one\'s community.',
    'Secret Agent': '. {10} got a license to kill and {0} aren\'t afraid to use it.',
    'Secretary': '',
    'Serial Killer': '',
    'SFX Artist': '',
    'Skiier': '',
    'Soccer Player': '',
    'Soldier': '',
    'Sniper': '',
    'Snowboarder': '',
    'Surgeon': '',
    'Street Fighter': '',
    'Student Council President': '',
    'Stunt Double': '',
    'Superhero': '',
    'Supervillain': '! What separates a regular villain from a super one? Why, presentation, of course!',
    'Supreme Leader': '',
    'Survivor': '',
    'Swimmer': '',
    'Swordsperson': '',
    'Tailor': '',
    'Team Manager': '',
    'Tennis Pro': '',
    'Test Subject': '',
    'Therapist': '. Of course, {0} can\'t talk about it that much, since patient confidentiality is {1} number 1 priority.',
    'Traditional Dancer': '',
    'Translator': '. {7} ability to be fluent in so many language baffles scientists.',
    'Vegabond': '',
    'VFX Artist': '. {6} had it better in the 80\'s.',
    'Violinist': '',
    'Voice Actor': '. {8} able to switch voices on a dime, and none of them sound anything alike.',
    'Watchmaker': '',
    'Wrestler': '',
    'Writer': '',
    'Yakuza': '',
    'Yoga Guru': '. All {1} chakras are open and flowing the sweet nectar of the soul.'
}

# Globals for the eval function
import math
import util

EVAL_GLOBALS = {
    # Math overall
    'math': math,
    # Math constants
    'pi': math.pi, 'e': math.e, 'tau': math.tau, 'inf': math.inf, 'nan': math.nan,
    # Easy baby shit
    'ceil': math.ceil, 'ncr': util.comb, 'comb': util.comb, 'copysign': math.copysign,
    'fabs': math.fabs, 'abs': math.fabs, 'factorial': math.factorial, 'floor': math.floor,
    'fmod': math.fmod, 'frexp': math.frexp, 'fsum': math.fsum, 'gcd': math.gcd,
    'isclose': math.isclose, 'isfinite': math.isfinite, 'isinf': math.isinf,
    'isinfinite': math.isinf, 'isnan': math.isnan, 'ldexp': math.ldexp,
    'modf': math.modf, 'npr': util.perm, 'perm': util.perm, 'prod': util.prod,
    'product': util.prod, 'remainder': math.remainder, 'trunc': math.trunc,
    'truncate': math.trunc,
    # Power and logarithmic
    'exp': math.exp, 'expm1': math.expm1, 'log': math.log, 'log1p': math.log1p,
    'log2': math.log2, 'log10': math.log10, 'pow': math.pow, 'sqrt': math.sqrt,
    # Trig
    'acos': math.acos, 'asin': math.asin, 'atan': math.atan, 'atan2': math.atan2,
    'cos': math.cos, 'hypot': math.hypot, 'sin': math.sin, 'tan': math.tan,
    # Angles shit
    'deg': math.degrees, 'degrees': math.degrees, 'rad': math.radians,
    'radians': math.radians,
    # Hyperbolas
    'acosh': math.acosh, 'asinh': math.asinh, 'atanh': math.atanh, 'cosh': math.cosh,
    'sinh': math.sinh, 'tanh': math.tanh,
    # Other
    'erf': math.erf, 'erfc': math.erfc, 'gamma': math.gamma, 'lgamma': math.lgamma
}

# Conversion chars
CONVERT_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+_'
MAX_CONVERT_DEPTH = -16

# Runtime and Uptime
RUNTIME_PREFIX = 'Bot has been running for '
UPTIME_PREFIX = 'Bot has been connected for '

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
- randomyt / randomyoutube: Generate a random YouTube video

===============
    UTILITY
===============
- calc / eval: Give a math equation and it will be evaluated as one (python eval() function)
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
- localip: Returns the local ip the bot is running from
- toggleignoredev: Toggles whether or not to ignore developer on Linux side
```'''
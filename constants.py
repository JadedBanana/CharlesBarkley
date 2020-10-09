# Constants file
# General use
VERSION = '0.3.3'

# Developer stuff
DEVELOPER_DISCORD_IDS = [
    110194551586570240,   # Jade
    158429528874680320,   # Jabe
    444250440801189891,   # Alex
    620226160328179722    # Megu-Nee
]
ON_WINDOWS_ONLY_RESPOND_TO_DEV = True
IGNORE_DEVELOPER_ONLY_WORKS_ON_LINUX = True
TEMP_DIR = 'temp'

# Crontab shit
CRONTAB_CHECK_FILE = '.croncheck'
CRONTAB_WAIT_INTERVAL = 45
CRONTAB_STR_LENGTH = 24
CRONTAB_STR_CHARS = '1234567890-=_+()*&^%$#@!~`qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFG HJKLZXCVBNM[]{};\':",.<>?/|\\'

# Logging constants
DEFAULT_LEVEL = 0
LOG_TO_CONSOLE = True
LOG_TO_FILE = True
DO_LEVEL_HEADERS = True
DO_TIMESTAMPS = True
LOGS_DIR = 'logs'

# Server, channel, user
COMM_LOG_PREFIX_GUILD = '{} ({}, {}): '
COMM_LOG_PREFIX = '{} ({}): '

# Bot stuff
# Global crap
BOT_TOKEN = 'NzQwNjEwMTc2MDM3NTUyMTc4.Xyrg-Q.8jBguEMXHXFmZvXOY5UAdXu4FE0'
GLOBAL_PREFIX = 'j!'

# YouTube
YOUTUBE_API_KEY = 'AIzaSyAHuBNRF1Ts5VKoqPnln57ojnrUVGUXINU'
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
    ['you', 'them'],
    ['You', 'They'],
    ['Your', 'Their'],
    ["You're", "They're"],
    ['Yourself', 'Themselves'],
    ["You've", "They've"],
    ["You'll", "They'll"],
    ['You', 'Them']
]
ULTIMATE_TITLES = {
    '???': '! Guess {0} don\'t remember, huh? Well, better hope it\'s a good one.',
    'Actress': '! Try as they might, no one could ever hope to emulate the passion {0} put into {1} performances!',
    'Adventurer': '! Well, who doesn\'t love discovering lands unknown?',
    'Affluent Progeny': '. Heir to the world\'s elite, {0} are destined to rule the world from the shadows.',
    'Akido Master': '! Hi-yah!',
    'Analyst': '. {7} can dissect any situation and see things most other people can\'t.',
    'Angler': '. No one really gets how to gut a fish quite like {0}.',
    'Animator': '! Don\'t forget! Anime is art!',
    'Anthropologist': '. {7} know more about the Salem Witch Trials than anyone else on Earth.',
    'Archer': '! {9} like Hawkeye up in here!',
    'Architect': '. {8} houses are absolutely exquisite.',
    'Artist': '! Pretty colors and lifelike statues are {1} whole deal!',
    'Assassin': '. Here\'s the target. You have 24 hours.',
    'Astronaut': '! {7} can reach the stars for sure! If anyone can, it\'s {6}!',
    'Baseball Player': '! Batter up!',
    'Beatboxer': '! Boots and cats and boots and cats...',
    'Blacksmith': '! Daggers and knives and swords, oh my!',
    'Biker Gang Leader': '! Rev your fucking engines! Let\'s tear up this town!',
    'Biologist': '. {8} favorite joke is that one about mitosis.',
    'Bodyguard': '. Are {0} prepared to lay down {1} life?',
    'Botanist': '! Ooh, pretty!',
    'Bounty Hunter': '. Feel like hunting down any criminals?',
    'Boxer': '! *DING-DING-DING!* It\'s a TKO!',
    'Breakdancer': '! Kick it!',
    'Breeder': '! Use {1} prowess in the dark arts to... potty-train this dog!',
    'Broadway Singer': '. What\'s {1} favorite musical?',
    'CGI Artist': '! It looks so *real!*',
    'Cheerleader': '! {14}, they\'re the one, if they don\'t win then that\'s no fun!',
    'Chemist': '. Man, that\'s such a boron career. It\'s too basic, if you ask me.',
    'Child Caregiver': '. {9} basically like a goblin herder.',
    'Clairvoyant': '! {7} and {1} 30% accuracy rate can predict ANY crime that probably won\'t happen!',
    'Clown': '! {9} a clown! Honk honk! :o)',
    'Composer': '. Popping out songs one after another ain\'t easy, but it\'s {1} way of life.',
    'Con Artist': '{9} a slimy bastard who can convince anyone anything is a good idea.',
    'Confectioner': '! How sweet of {0}!',
    'Conspiracy Theorist': '. So you think the moon landing was faked, huh? Well, have you heard the MOON is fake, too?',
    'Cook': '! Bon Appetit!',
    'Curator': '. {8} collection is far more impressive than the Smithsonian.',
    'Despair': '. Despair is not a goal, or a set of principles, or a lifestyle, or even an instinct... It\'s what defines {6} as {14}!',
    'Detective': '! And the killer is... you!',
    'Drug Dealer': '. {11} stuck some stuff in some pretty gross places to get to the top, but {0} don\'t regret it.',
    'Drummer': '! Any band is only as good as its drummer!',
    'DJ': '! Lay down some beats, man!',
    'Entomologist': '... so, if I find a spider, do I bring it to you?',
    'Entrepreneur': '',
    'Exorcist': '. The power of Christ compels you!',
    'Fanfic Creator': '! So, what next? Maybe a slow-burn coffee shop AU with some self-inserts, a handful of OC\'s, F/F and M/M, a little OOC if necessary, but all in all just fanservice fic for Danganronpa?',
    'Farmer': '! Do {1} have a dog named Bingo? Or... just Ingo? Or Ngo?',
    'Fashionista': '! Looking cool, {9}!',
    'Film Director': '! When on set, nobody questions {1} judgement.',
    'Forum Admin': '. {11} seen some serious shit.',
    'Gambler': '',
    'Gamer': '',
    'Golfer': '. No one can beat the power of a true Scottish swing.',
    'Guitarist': '',
    'Gymnast': '',
    'Hacker': '. {7} didn\'t actually get {1} title from some school official, {0} got it by hacking into the servers and giving it to {3}.',
    'Hairstylist': '',
    'Hope': '',
    'Housekeeper': '! You\'re the ultimate cleaning machine!',
    'Hypnotist': '. People ought to be cautious around {6} -- let down your guard for even a second and you can no longer think for yourself.',
    'Idol': '',
    'Impostor': '. No one truly knows who {0} are beneath the mask... or that {2} even wearing one at all.',
    'Internet Troll': '. {9} really good at pissing people off online.',
    'Inventor': '',
    'Lawyer': '',
    'Lucky Student': '',
    'Magician': '! Prepare to be amazed!',
    'Maid': '',
    'Martial Artist': '',
    'Makeup Artist': '',
    'Matchmaker': '',
    'Mechanic': '. Every tractor {0} work on is sexy.',
    'Medium': '',
    'Merchant': '. No one knows supply and demand better than {6}, and {0} always have just enough stock to match what the public desires.',
    'Model': '',
    'Moral Compass': '. {7} are the best at telling other people how to act.',
    'Musician': '',
    'Neurologist': '',
    'Ninja': ', lying hidden in the shadows. Watch out.',
    'Nurse': '',
    'Pharmacist': '. It\'s not totally clear how {0} managed to become one at such a young age, but regardless, {0} are.',
    'Photographer': '! Say cheese!',
    'Poet': '. {7} just have a way with words others can only dream of matching.',
    'Prankster': '. What devious thing did {0} do to get this title...?',
    'Prisoner': '',
    'Puppeteer': '. No strings on {1} puppets, no sir!',
    'Psychologist': '',
    'Pianist': '',
    'Pilot': '. Do a barrel roll!',
    'Police Officer': '',
    'Priest': '. With just a wave of {1} hand, {0} can enlighten hundreds at a time.',
    'Princess': '',
    'Programmer': '! Did you know this bot is written in Python using the discord.py API?',
    'Pyrotechnician': '. \'Cause baby, you\'re a firework!',
    'Robot': '! Beep boop bop beep!',
    'Sailor': '',
    'Scout': '. Though high adventure may be fun, there is nothing quite like giving back to one\'s community.',
    'Secret Agent': '. {7} have a license to kill and {0} aren\'t afraid to use it.',
    'Serial Killer': '',
    'SFX Artist': '',
    'Skiier': '',
    'Soccer Player': '',
    'Soldier': '',
    'Sniper': '. Headshot.',
    'Snowboarder': '. It\'s like being a skiier, but way cooler.',
    'Surgeon': '',
    'Street Fighter': '',
    'Stunt Double': '',
    'Superhero': '',
    'Supervillain': '! What separates a regular villain from a super one? Why, presentation, of course!',
    'Supreme Leader': '',
    'Survivor': '',
    'Swimmer': '! {7} swear {0} could swim across the ocean if it was legal!',
    'Swordsman': '. While most others spend their time playing video games or watching TV, {0} study the blade.',
    'Tailor': '. Capes aren\'t usually fashionable, but the way {0} make it, anyone can rock that shit.',
    'Team Manager': '',
    'Tennis Pro': '',
    'Test Subject': 'The Enrichment Center is committed to the well being of all participants. Cake and grief counseling will be available at the conclusion of the test.',
    'Therapist': '. Of course, {0} can\'t talk about it that much, since patient confidentiality is {1} number 1 priority.',
    'Traditional Dancer': '',
    'Translator': '. {8} ability to be fluent in so many language baffles scientists.',
    'VFX Artist': '. {7} had it better in the 80\'s.',
    'Violinist': '',
    'Voice Actor': '. {9} able to switch voices on a dime, and none of them sound anything alike.',
    'Wrestler': '! Let\'s settle this in the ring!',
    'Writer': '',
    'Yakuza': '',
    'Yoga Guru': '. All {1} chakras are open and flowing the sweet nectar of the soul.'
}

# Weather constants
WEATHER_API_KEY = 'fbe576aaab00abc563182f75b9725115'
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?appid={}&q={}'
WEATHER_ALT_COUNTRY_CODES = {
    'BO': 'Bolivia', 'FK': 'Falkland Islands', 'FM': 'Micronesia', 'GB': 'United Kingdom', 'IR': 'Iran', 'KP': 'North Korea',
    'KR': 'South Korea', 'LA': 'Laos', 'MD': 'Moldova', 'PS': 'Palestine', 'RU': 'Russia', 'SX': 'Sint Maarten',
    'SY': 'Syria', 'TW': 'Taiwan', 'TZ': 'Tanzania', 'US': 'United States', 'VE': 'Venezuela', 'VN': 'Vietnam'
}
WEATHER_CREDIT_TEXT = 'Powered by OpenWeatherMap'
WEATHER_EMBED_COLOR_DEFAULT = (235 << 16) + (110 << 8) + 75
WEATHER_EMBED_COLORS_BY_ICON = {
    '01d': (235 << 16) + (110 << 8) + 75, '02d': (235 << 16) + (110 << 8) + 75, '10d': (235 << 16) + (110 << 8) + 75, '11d': (235 << 16) + (110 << 8) + 75, '11n': (235 << 16) + (110 << 8) + 75,
    '03d': (242 << 16) + (242 << 8) + 242, '03n': (242 << 16) + (242 << 8) + 242, '04d': (242 << 16) + (242 << 8) + 242, '04n': (242 << 16) + (242 << 8) + 242, '13d': (242 << 16) + (242 << 8) + 242, '13n': (242 << 16) + (242 << 8) + 242, '50d': (242 << 16) + (242 << 8) + 242, '50n': (242 << 16) + (242 << 8) + 242,
    '01n': (72 << 16) + (72 << 8) + 74, '02n': (72 << 16) + (72 << 8) + 74, '09d': (72 << 16) + (72 << 8) + 74, '09n': (72 << 16) + (72 << 8) + 74, '10n': (72 << 16) + (72 << 8) + 74
}
WEATHER_KELVIN_SUB = 273.15
WEATHER_THUMBNAIL_URL = 'http://openweathermap.org/img/wn/{}@4x.png'
WEATHER_WIND_DIRECTIONS = {
    'North': 22.5, 'Northeast': 67.5, 'East': 112.5,
    'Southeast': 157.5, 'South': 202.5, 'Southeast': 247.5,
    'East': 292.5, 'Northeast': 337.5, 'North': 382.5
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

# Shipping
SHIP_HEART_IMG = 'assets/heart.png'
SHIP_ICON_SIZE = 128
SHIP_MESSAGES = [
    'I ship {} with {}! Isn\'t it cute?',
    'If you ask me, {} and {} were meant for each other.',
    'OTP: {} and {}.',
    'I ship {} and {}. Cute, right?',
    'I like {} and {}. Enemies to lovers-sorta thing.',
    '{} x {}. No further questions.',
    'Imagine a yandere {} going after {}. Crazy, right?',
    '{} and {}. Both are huge tsunderes.',
    '{} and {}. Bakadere relationships are so cute, IMO.',
    'Say whatever you want. {} and {} is the purest, most amazing ship and I will not stand for any others.'
]

# Uwu
EMOTE_CHARACTERS = '0123456789_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVQXYZ'
UWU_FACES = {
    ':)': 'uwu', ':(': 'umu', ':|': 'u_u', ':-)': 'uwu', ':-(': 'umu', ':-|': 'u_u', '^_^': 'uwu',
    '^w^': 'uwu', 'O_o': 'u_u', 'o_o': 'u_u', 'o_O': 'u_u', 'O_O': 'u_u', '(:': 'uwu', ':D': 'uwu',
    'D:': 'umu', '):': 'umu'
}
OWO_FACES = {
    ':)': 'owo', ':(': 'omo', ':|': 'o_o', ':-)': 'owo', ':-(': 'omo', ':-|': 'o_o', '^_^': 'owo',
    '^w^': 'owo', 'O_o': 'o_o', 'o_o': 'o_o', 'o_O': 'o_o', 'O_O': 'o_o', '(:': 'owo', ':D': 'owo',
    'D:': 'omo', '):': 'omo'
}

# Conversion chars
CONVERT_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+_'
MAX_CONVERT_DEPTH = -16

# Runtime and Uptime
RUNTIME_PREFIX = 'Bot has been running for '
UPTIME_PREFIX = 'Bot has been connected for '

# Ip methods
LINUX_IP_PREFIXES = ['lo', 'eth0']

# Image Manipulation crap
PFP_SIZE_PREFIX = '?size='
PFP_FILETYPE = '.webp'
PFP_DEFAULT_SIZE = 1024

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
- getpid: Returns the local PID of this process
- localip: Returns the local ip the bot is running from
- toggleignoredev: Toggles whether or not to ignore developer on Linux side
- loglist: Sends a list of all the log files in the logs folder
- sendlog: Sends the log for today, or a specific date (YYYY-MM-DD)
- update: Trigger remote update (pull from Git master branch)
- reboot: Trigger remote reboot
```'''

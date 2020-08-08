# Constants file
# General use
VERSION = '0.1.4'

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
BOT_TOKEN = 'NzQwNjEwMTc2MDM3NTUyMTc4.Xyrg-Q.8jBguEMXHXFmZvXOY5UAdXu4FE0'
GLOBAL_PREFIX = 'j!'

YOUTUBE_API_KEY = 'AIzaSyDfdrytJZ4Ft9W76VdR-t4HOZTOR7ESMEg'
YOUTUBE_RICKROLL_URL = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
YOUTUBE_RICKROLL_CHANCE = 0.0002
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}'
YOUTUBE_SEARCH_COUNT = 100
YOUTUBE_SEARCH_LENGTHS = [1, 2, 3, 4, 5]
YOUTUBE_SEARCH_WEIGHTS = [36, 1296, 46656, 1679616, 60466176]
YOUTUBE_VIDEO_URL_FORMAT = 'https://www.youtube.com/watch?v={}'

import math
import util
EVAL_GLOBALS = {
	# Math overall
	'math': math,
	# Math constants
	'pi': math.pi, 'e': math.e, 'tau': math.tau, 'inf': math.inf, 'nan': math.nan,
	# Easy baby shit
	'ceil': math.ceil, 'ncr': util.comb, 'comb': util.comb,	'copysign': math.copysign, 
	'fabs': math.fabs, 	'abs': math.fabs, 'factorial': math.factorial, 'floor': math.floor,
	'fmod': math.fmod, 'frexp': math.frexp,	'fsum': math.fsum, 'gcd': math.gcd, 
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

CONVERT_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+_'
MAX_CONVERT_DEPTH = -16

RUNTIME_PREFIX = 'Bot has been running for '
UPTIME_PREFIX = 'Bot has been connected for '

HELP_MSG ='''```
Jadi3Pi {} Help
PREFIX: j!

===============
      FUN
===============
copy: Mention someone to start copying their every word
stopcopying: Stop copying everyone in this server
randomyt / randomyoutube: Generate a random YouTube video

===============
    UTILITY
===============
calc / eval: Give a math equation and it will be evaluated as one (python eval() function)
hex / hexadecimal: Converts a number to hexadecimal
duo / duodec / duodecimal: Converts a number to duodecimal
dec / decimal: Converts a number to decimal
oct / octal: Converts a number to octal
bin / binary: Converts a number to binary

===============
     OTHER
===============
help: Display this message
runtime: Display the amount of time this bot has been running for
uptime: Display the amount of time this bot has been connected to Discord for
```'''

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
YOUTUBE_VIDEO_URL_FORMAT = 'https://www.youtube.com/watch?v={}'
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}'
YOUTUBE_SEARCH_COUNT = 100
YOUTUBE_SEARCH_LENGTHS = [1, 2, 3, 4, 5]
YOUTUBE_SEARCH_WEIGHTS = [36, 1296, 46656, 1679616, 60466176]

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

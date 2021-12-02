




# Winner / Ties
HG_WINNER_TITLE = 'The Winner'
HG_TIE_TITLE = 'The Winners'
HG_WINNER_EVENT = 'The winner is {0}!'
HG_WINNER_DEAD_EVENT = 'The winner is {0}! However, they died too, so it\'s sort of a hollow victory.'
HG_TIE_EVENT = ('Since they died at the same time, it\'s a tie between ', ', ', 'and ', '!')
HG_COMPLETE_PHASE_TYPES = ['win', 'tie']
# Graphics

HG_HEADER_BORDER_BUFFER = 7
HG_HEADER_TEXT_COLOR = (255, 207, 39)
HG_ACTION_PLAYER_COLOR = (251, 130, 0)
HG_HEADER_BORDER_COLOR = (255, 255, 255)
HG_HEADER_BACKGROUND_COLOR = (35, 35, 35)
# Descriptions
HG_BEGINNING_DESCRIPTION = 'Respond one of the following:\nN: Next Action\nC: Cancel Game'
HG_MIDGAME_DESCRIPTION = 'Respond one of the following:\nN: Next Action\tP: Previous Action\nC: Cancel Game'
HG_POSTGAME_BEGINNING_DESCRIPTION = 'Respond one of the following:\nN: Next Action\nR: Replay (same cast)\tS: New Game\tC: Close'
HG_POSTGAME_MIDGAME_DESCRIPTION = 'Respond one of the following:\nN: Next Action\tP: Previous Action\nR: Replay (same cast)\tS: New Game\tC: Close'
HG_THE_END_DESCRIPTION = 'The end! Respond one of the following:\nN: Next Action\tP: Previous Action\nR: Replay (same cast)\tS: New Game\tC: Close'
HG_FINALE_DESCRIPTION = 'Respond one of the following:\nP: Previous Action\nR: Replay (same cast)\tS: New Game\tC: Close'
# Events
# Files
HG_IMAGE_PATH = 'current_hg_image.png'

# Thank you


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

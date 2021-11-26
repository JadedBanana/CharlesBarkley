# =================================================================
#                        UTILITY COMMANDS
# =================================================================
from dateutil.tz import tzoffset
from datetime import datetime
import constants
import requests
import discord
from lib.util import misc

# Logging
log = None

async def evaluate(self, message, argument, is_in_guild):
    """
    Does math and shit.
    It's very basic, if your command needs 2 lines or a semicolon you're better off doing it yourself.
    """
    # Replace all the ^ with **.
    argument = argument.replace('^', '**').strip('`')

    # Print statements list for when we sub print() for our own thing.
    print_statements = []
    def add_to_print(m = None):
        print_statements.append(m)

    # Copies global vars to create local vars.
    local_globals = constants.EVAL_GLOBALS.copy()
    local_globals.update({'print': add_to_print, 'printf': add_to_print})

    # We surround our eval in a try statement so we can catch some errors.
    try:
        evaluated = eval(argument, local_globals)
    # For a syntax error, we actually SEND THE ERROR back to the user.
    except SyntaxError as e:
        log.debug(misc.get_comm_start(message, is_in_guild) + 'requested eval for expression {}, got a syntax error'.format(argument))
        await message.channel.send('Syntax Error on line {}:```{}\n'.format(e.args[1][1], e.args[1][3].split('\n')[0]) + ' ' * (e.args[1][2] - 1) + '^```')
        return
    # For a type error or value error, we send that shit back too.
    except (TypeError, ValueError) as e:
        log.debug(misc.get_comm_start(message, is_in_guild) + 'requested eval for expression {}, got a type error'.format(argument))
        await message.channel.send(repr(e))
        return

    # Prints out the print statements.
    for ps in print_statements:
        await message.channel.send(repr(ps))

    # Sends the evaluated value.
    if evaluated:
        await message.channel.send(repr(evaluated))

    # Logs evaluated value.
    log.debug(misc.get_comm_start(message, is_in_guild) + 'requested eval for expression {}'.format(argument))


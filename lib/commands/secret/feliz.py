"""
Feliz command.
Gets the current time then returns an appropriate image depending on the day of the week.
"""
# Local Imports
from lib.util import assets, messaging, misc, parsing
from lib.util.logger import BotLogger as logging

# Package Imports
import os


# Argument support.
FELIZ_ARGUMENTS = {
    'monday': 0,
    'lunes': 0,
    'tuesday': 1,
    'martes': 1,
    'wednesday': 2,
    'miercoles': 2,
    'thursday': 3,
    'jueves': 3,
    'friday': 4,
    'viernes': 4,
    'saturday': 5,
    'sabado': 5,
    'sunday': 6,
    'domingo': 6
}
# What number corresponds to what day.
NUMBER_DAYS = {
    0: 'lunes',
    1: 'martes',
    2: 'miercoles',
    3: 'jueves',
    4: 'viernes',
    5: 'sabado',
    6: 'domingo'
}


async def feliz(bot, message, argument):
    """
    The master feliz function.
    Can have a varying intended date, and parse arguments.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Store the intended date. This will change based on the argument.
    intended_date = -1

    # If an argument was supplied, then see if any of the feliz arguments appeared in there.
    # If so, overwrite the intended date to be something else.
    if argument:
        for word in parsing.normalize_string(argument).lower().split(' '):
            if word in FELIZ_ARGUMENTS:
                intended_date = FELIZ_ARGUMENTS[word]

    # Get the current date and time.
    current_datetime = misc.get_guild_time(message)

    # Get the day of the week.
    actual_date = current_datetime.weekday()

    # Log the order.
    if intended_date == -1:
        logging.info(message, f'queria saber cual dia del semana es hoy, feliz {NUMBER_DAYS[actual_date]}!')
    elif intended_date == actual_date:
        logging.info(message, f'queria celebrar el dia del semana con espacios, feliz {argument}! '
                              f'Feliz {NUMBER_DAYS[actual_date]}!')
    else:
        logging.info(message, f'queria celebrar el dia del semana con espacios, pero no es '
                              f'{argument}, no, por que seria {NUMBER_DAYS[intended_date]}?! '
                              f'Hoy es {NUMBER_DAYS[actual_date]}!')

    # Send the message.
    await feliz_send_image(message, intended_date if intended_date != -1 else actual_date,
                           actual_date != intended_date and not intended_date == -1)


async def feliz_lunes(bot, message, argument):
    """
    Feliz function for monday.
    Will see if it's ACTUALLY monday and make the image mad if it isn't.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Get the current date and time.
    current_datetime = misc.get_guild_time(message)

    # Get the day of the week.
    actual_date = current_datetime.weekday()

    # Log the order.
    if actual_date == 0:
        logging.info(message, f'queria celebrar el dia del semana, feliz lunes!')
    else:
        logging.info(message, f'queria celebrar el dia del semana, pero no es lunes, es {NUMBER_DAYS[actual_date]}!')

    # Send the message.
    await feliz_send_image(message, 0, actual_date != 0)


async def feliz_martes(bot, message, argument):
    """
    Feliz function for tuesday.
    Will see if it's ACTUALLY tuesday and make the image mad if it isn't.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Get the current date and time.
    current_datetime = misc.get_guild_time(message)

    # Get the day of the week.
    actual_date = current_datetime.weekday()

    # Log the order.
    if actual_date == 1:
        logging.info(message, f'queria celebrar el dia del semana, feliz martes!')
    else:
        logging.info(message, f'queria celebrar el dia del semana, pero no es martes, es {NUMBER_DAYS[actual_date]}!')

    # Send the message.
    await feliz_send_image(message, 1, actual_date != 1)


async def feliz_miercoles(bot, message, argument):
    """
    Feliz function for wednesday.
    Will see if it's ACTUALLY wednesday and make the image mad if it isn't.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Get the current date and time.
    current_datetime = misc.get_guild_time(message)

    # Get the day of the week.
    actual_date = current_datetime.weekday()

    # Log the order.
    if actual_date == 2:
        logging.info(message, f'queria celebrar el dia del semana, feliz miercoles!')
    else:
        logging.info(message, f'queria celebrar el dia del semana, pero no es miercoles, es {NUMBER_DAYS[actual_date]}!')

    # Send the message.
    await feliz_send_image(message, 2, actual_date != 2)


async def feliz_jueves(bot, message, argument):
    """
    Feliz function for thursday.
    Will see if it's ACTUALLY thursday and make the image mad if it isn't.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Get the current date and time.
    current_datetime = misc.get_guild_time(message)

    # Get the day of the week.
    actual_date = current_datetime.weekday()

    # Log the order.
    if actual_date == 3:
        logging.info(message, f'queria celebrar el dia del semana, feliz jueves!')
    else:
        logging.info(message, f'queria celebrar el dia del semana, pero no es jueves, es {NUMBER_DAYS[actual_date]}!')

    # Send the message.
    await feliz_send_image(message, 3, actual_date != 3)


async def feliz_viernes(bot, message, argument):
    """
    Feliz function for friday.
    Will see if it's ACTUALLY friday and make the image mad if it isn't.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Get the current date and time.
    current_datetime = misc.get_guild_time(message)

    # Get the day of the week.
    actual_date = current_datetime.weekday()

    # Log the order.
    if actual_date == 4:
        logging.info(message, f'queria celebrar el dia del semana, feliz viernes!')
    else:
        logging.info(message, f'queria celebrar el dia del semana, pero no es viernes, es {NUMBER_DAYS[actual_date]}!')

    # Send the message.
    await feliz_send_image(message, 4, actual_date != 4)


async def feliz_sabado(bot, message, argument):
    """
    Feliz function for saturday.
    Will see if it's ACTUALLY saturday and make the image mad if it isn't.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Get the current date and time.
    current_datetime = misc.get_guild_time(message)

    # Get the day of the week.
    actual_date = current_datetime.weekday()

    # Log the order.
    if actual_date == 5:
        logging.info(message, f'queria celebrar el dia del semana, feliz sabado!')
    else:
        logging.info(message, f'queria celebrar el dia del semana, pero no es sabado, es {NUMBER_DAYS[actual_date]}!')

    # Send the message.
    await feliz_send_image(message, 5, actual_date != 5)


async def feliz_domingo(bot, message, argument):
    """
    Feliz function for sunday.
    Will see if it's ACTUALLY sunday and make the image mad if it isn't.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Get the current date and time.
    current_datetime = misc.get_guild_time(message)

    # Get the day of the week.
    actual_date = current_datetime.weekday()

    # Log the order.
    if actual_date == 6:
        logging.info(message, f'queria celebrar el dia del semana, feliz domingo!')
    else:
        logging.info(message, f'queria celebrar el dia del semana, pero no es domingo, es {NUMBER_DAYS[actual_date]}!')

    # Send the message.
    await feliz_send_image(message, 6, actual_date != 6)


async def feliz_send_image(message, day, angry):
    """
    The feliz sending function.
    Sends the image based on the day and whether or not they're angry.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        day (int) : The integer date of today. 0 = monday, 1 = tuesday, and so on.
        angry (bool) : Whether or not the anime girl in the picture should be pissed off because TODAY IS NOT THAT DAY.
    """

    # Get where to pull the image from based on the day and whether it's angry.
    image_folder = os.path.join('feliz', 'angry' if angry else 'happy', NUMBER_DAYS[day])

    # Get the random picture.
    picture = assets.get_random_file_from_folder(image_folder)

    # Send the message.
    await messaging.send_file(message, picture)


# Command values
PUBLIC_COMMAND_DICT = {
    'feliz': feliz,
    'felizmonday': feliz_lunes,
    'felizlunes': feliz_lunes,
    'feliztuesday': feliz_martes,
    'felizmartes': feliz_martes,
    'felizwednesday': feliz_miercoles,
    'felizmiercoles': feliz_miercoles,
    'felizthursday': feliz_jueves,
    'felizjueves': feliz_jueves,
    'felizfriday': feliz_viernes,
    'felizviernes': feliz_viernes,
    'felizsaturday': feliz_sabado,
    'felizsabado': feliz_sabado,
    'felizsunday': feliz_domingo,
    'felizdomingo': feliz_domingo
}
HELP_DOCUMENTATION_LIST = [
    {
        'command_name': 'feliz',
        'description': 'Celebrates whatever day of the week it is.',
        'examples': [('feliz', 'Celebrates the day that is today!'),
                     ('feliz jueves', "Celebrates that it's Thursday (but ONLY on Thursday).")],
        'usages': ['feliz', 'feliz < day of the week >']
    }
]
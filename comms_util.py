# =================================================================
#                        UTILITY COMMANDS
# =================================================================
from dateutil.tz import tzoffset
from datetime import datetime
from iso3166 import countries
from math import fabs
import constants
import requests
import discord
import util

# Logging
log = None

async def weather(self, message, argument, is_in_guild):
    """
    Gets the current weather for the given city/state/province.
    """
    # Test the argument.
    if not argument:
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested weather, empty city value')
        await message.channel.send('Invalid city.')
        return

    # Normalize the argument
    argument = util.normalize_string(argument)

    # Testing again.
    if not argument:
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested weather, empty city value')
        await message.channel.send('Invalid city.')
        return

    # Simple request call.
    response = requests.get(constants.WEATHER_API_URL.format(constants.WEATHER_API_KEY, argument))
    weather_json = response.json()

    # If we didn't get weather_json or it's broken, we tell the user that.
    if not weather_json or 'cod' not in weather_json.keys():
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested weather, think it\'s broken')
        await message.channel.send('Weather service is down, please be patient.')
        return

    # If the code is a 404, then we tell the user they have an invalid city.
    if weather_json['cod'] == 404 or any([key not in weather_json.keys() for key in ['name', 'sys', 'main']]):
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested weather for city {}, invalid'.format(argument))
        await message.channel.send('Invalid city.')
        return

    # Otherwise, we get the weather. If there are latitude and longitude included, we also put those there.
    if 'coord' in weather_json.keys() and 'lat' in weather_json['coord'].keys() and 'lat' in weather_json['coord'].keys():
        lat = weather_json['coord']['lat']; lon = weather_json['coord']['lon']
        latdeg = int(fabs(lat)); latmin = str(int((fabs(lat) % 1) * 100)); latmin = '0' + latmin if len(latmin) < 2 else latmin; latdir = 'N' if lat > 0 else ('S' if lat < 0 else '')
        londeg = int(fabs(lon)); lonmin = str(int((fabs(lon) % 1) * 100)); lonmin = '0' + lonmin if len(lonmin) < 2 else lonmin; londir = 'E' if lon > 0 else ('W' if lon < 0 else '')
        lon_lat = '{}\N{DEGREE SIGN}{}"{}, {}\N{DEGREE SIGN}{}"{}'.format(latdeg, latmin, latdir, londeg, lonmin, londir)
    else:
        lon_lat = 'No coordinates available'

    # Get the color for the embed.
    embed_color = constants.WEATHER_EMBED_COLOR_DEFAULT
    if 'weather' in weather_json.keys() and len(weather_json['weather']) > 0 and 'icon' in weather_json['weather'][0].keys() and weather_json['weather'][0]['icon']:
        if weather_json['weather'][0]['icon'] in constants.WEATHER_EMBED_COLORS_BY_ICON.keys():
            embed_color = constants.WEATHER_EMBED_COLORS_BY_ICON[weather_json['weather'][0]['icon']]
        else:
            log.error('New weather icon {}, please create embed colors for it asap!'.format(weather_json['weather'][0]['icon']))

    # Creates the embed
    embed = discord.Embed(title='Weather for {}, {}'.format(weather_json['name'], constants.WEATHER_ALT_COUNTRY_CODES[weather_json['sys']['country']] if weather_json['sys']['country'] in constants.WEATHER_ALT_COUNTRY_CODES.keys() else countries.get(weather_json['sys']['country']).name), colour=embed_color, description=lon_lat)
    embed.set_footer(text=constants.WEATHER_CREDIT_TEXT)

    # Formats a kelvin temperature in celsius and fahrenheit, rounded to nearest degree.
    def format_temperature(temp_num):
        return '{}\N{DEGREE SIGN}C / {}\N{DEGREE SIGN}F'.format(int(temp_num - constants.WEATHER_KELVIN_SUB + 0.5), int((temp_num - constants.WEATHER_KELVIN_SUB) * 1.8 + 32 + 0.5))

    # Adds temperature to embed
    if 'temp' in weather_json['main'].keys() and (isinstance(weather_json['main']['temp'], float) or isinstance(weather_json['main']['temp'], int)):
        embed.add_field(name='Current Temp.', value=format_temperature(weather_json['main']['temp']) + ' \u200b \u200b \u200b', inline=True)
    else:
        embed.add_field(name='Current Temp.', value='Unavailable \u200b \u200b \u200b', inline=True)

    # Adds status + thumbnail to embed
    if 'weather' in weather_json.keys() and len(weather_json['weather']) > 0:
        if 'description' in weather_json['weather'][0].keys() and weather_json['weather'][0]['description']:
            embed.add_field(name='Status', value=util.upper_per_word(weather_json['weather'][0]['description']) + ' \u200b \u200b \u200b', inline=True)
        elif 'main' in weather_json['weather'][0].keys() and weather_json['weather'][0]['main']:
            embed.add_field(name='Status', value=util.upper_per_word(weather_json['weather'][0]['main']) + ' \u200b \u200b \u200b', inline=True)
        else:
            embed.add_field(name='Status', value='Unavailable \u200b \u200b \u200b', inline=True)
        if 'icon' in weather_json['weather'][0].keys() and weather_json['weather'][0]['icon']:
            embed.set_thumbnail(url=constants.WEATHER_THUMBNAIL_URL.format(weather_json['weather'][0]['icon']))
    else:
        embed.add_field(name='Status', value='Unavailable \u200b \u200b \u200b', inline=True)

    # Adds blank space
    embed.add_field(name='\u200b', value='\u200b', inline=True)

    # Adds feels like to embed
    if 'feels_like' in weather_json['main'].keys() and (isinstance(weather_json['main']['feels_like'], float) or isinstance(weather_json['main']['feels_like'], int)):
        embed.add_field(name='Feels Like', value=format_temperature(weather_json['main']['feels_like']) + ' \u200b \u200b \u200b', inline=True)
    else:
        embed.add_field(name='Feels Like', value='Unavailable \u200b \u200b \u200b', inline=True)

    # Adds low to embed
    if 'temp_min' in weather_json['main'].keys() and (isinstance(weather_json['main']['temp_min'], float) or isinstance(weather_json['main']['temp_min'], int)):
        embed.add_field(name='Low Temp.', value=format_temperature(weather_json['main']['temp_min']) + ' \u200b \u200b \u200b', inline=True)
    else:
        embed.add_field(name='Low Temp.', value='Unavailable \u200b \u200b \u200b', inline=True)

    # Adds high to embed
    if 'temp_max' in weather_json['main'].keys() and (isinstance(weather_json['main']['temp_max'], float) or isinstance(weather_json['main']['temp_max'], int)):
        embed.add_field(name='High Temp.', value=format_temperature(weather_json['main']['temp_max']) + ' \u200b \u200b \u200b', inline=True)
    else:
        embed.add_field(name='High Temp.', value='Unavailable \u200b \u200b \u200b', inline=True)

    # Adds humidity to embed
    if 'humidity' in weather_json['main'].keys() and (isinstance(weather_json['main']['humidity'], float) or isinstance(weather_json['main']['humidity'], int)):
        embed.add_field(name='Humidity', value='{}% \u200b \u200b \u200b'.format(int(weather_json['main']['humidity'])), inline=True)
    else:
        embed.add_field(name='Humidity', value='Unavailable \u200b \u200b \u200b', inline=True)

    # Adds pressure to embed
    if 'pressure' in weather_json['main'].keys() and (isinstance(weather_json['main']['pressure'], float) or isinstance(weather_json['main']['pressure'], int)):
        embed.add_field(name='Air Pressure', value='{} hPa \u200b \u200b \u200b'.format(int(weather_json['main']['pressure'])), inline=True)
    else:
        embed.add_field(name='Humidity', value='Unavailable \u200b \u200b \u200b', inline=True)

    # Adds visibility to embed
    if 'visibility' in weather_json.keys() and (isinstance(weather_json['visibility'], float) or isinstance(weather_json['visibility'], int)):
        embed.add_field(name='Visibility', value='{} m / {} ft \u200b \u200b \u200b'.format(int(weather_json['main']['pressure']), int(weather_json['main']['pressure'] * 3.28084)), inline=True)
    else:
        embed.add_field(name='Visibility', value='Unavailable \u200b \u200b \u200b', inline=True)

    # Adds wind stuff to embed
    if 'wind' in weather_json.keys():
        direction = ''
        if 'deg' in weather_json['wind'].keys() and (isinstance(weather_json['wind']['deg'], float) or isinstance(weather_json['wind']['deg'], int)):
            for cardinal, max_angle in constants.WEATHER_WIND_DIRECTIONS.items():
                if weather_json['wind']['deg'] <= max_angle:
                    direction = cardinal
                    break
        if 'speed' in weather_json['wind'].keys() and (isinstance(weather_json['wind']['speed'], float) or isinstance(weather_json['wind']['speed'], int)):
            embed.add_field(name='Wind Speed', value='{} kmh / {} mph {} \u200b \u200b \u200b'.format(int(weather_json['wind']['speed'] * 3.6), int(weather_json['wind']['speed'] * 2.23694), direction), inline=True)
        else:
            embed.add_field(name='Wind Speed', value='Unavailable', inline=True)
        if 'gust' in weather_json['wind'].keys() and (isinstance(weather_json['wind']['gust'], float) or isinstance(weather_json['wind']['gust'], int)):
            embed.add_field(name='Wind Gust', value='{} kmh / {} mph {} \u200b \u200b \u200b'.format(int(weather_json['wind']['gust'] * 3.6), int(weather_json['wind']['gust'] * 2.23694), direction), inline=True)
        else:
            embed.add_field(name='Wind Gust', value='Unavailable \u200b \u200b \u200b', inline=True)
    else:
        embed.add_field(name='Wind Speed', value='Unavailable \u200b \u200b \u200b', inline=True)
        embed.add_field(name='Wind Gust', value='Unavailable \u200b \u200b \u200b', inline=True)

    # Adds blank space
    embed.add_field(name='\u200b', value='\u200b', inline=True)

    # Adds local time
    if 'timezone' in weather_json.keys() and isinstance(weather_json['timezone'], int):
        local_timezone = tzoffset('placeholder', weather_json['timezone'])
        local_time = datetime.now(local_timezone)
        embed.add_field(name='Local Time', value=local_time.strftime('%H:%M (%I:%M %p)') + ' \u200b \u200b \u200b', inline=True)
    else:
        embed.add_field(name='Local Time', value='Unavailable \u200b \u200b \u200b', inline=True)

    # Adds sunrise
    if local_timezone and 'sunrise' in weather_json['sys'].keys() and isinstance(weather_json['sys']['sunrise'], int):
        dr = datetime.utcfromtimestamp(weather_json['sys']['sunrise'] + weather_json['timezone'])
        embed.add_field(name='Sunrise Time', value=dr.strftime('%H:%M (%I:%M %p)') + ' \u200b \u200b \u200b', inline=True)
    else:
        embed.add_field(name='Sunrise Time', value='Unavailable \u200b \u200b \u200b', inline=True)

    # Adds sunset
    if local_timezone and 'sunrise' in weather_json['sys'].keys() and isinstance(weather_json['sys']['sunset'], int):
        dr = datetime.utcfromtimestamp(weather_json['sys']['sunset'] + weather_json['timezone'])
        embed.add_field(name='Sunset Time', value=dr.strftime('%H:%M (%I:%M %p)') + ' \u200b \u200b \u200b', inline=True)
    else:
        embed.add_field(name='Sunset Time', value='Unavailable \u200b \u200b \u200b', inline=True)

    await message.channel.send(embed=embed)


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
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested eval for expression {}, got a syntax error'.format(argument))
        await message.channel.send('Syntax Error on line {}:```{}\n'.format(e.args[1][1], e.args[1][3].split('\n')[0]) + ' ' * (e.args[1][2] - 1) + '^```')
        return
    # For a type error or value error, we send that shit back too.
    except (TypeError, ValueError) as e:
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested eval for expression {}, got a type error'.format(argument))
        await message.channel.send(repr(e))
        return

    # Prints out the print statements.
    for ps in print_statements:
        await message.channel.send(repr(ps))

    # Sends the evaluated value.
    if evaluated:
        await message.channel.send(repr(evaluated))

    # Logs evaluated value.
    log.debug(util.get_comm_start(message, is_in_guild) + 'requested eval for expression {}'.format(argument))


def convert_num_from_decimal(n, base):
    """
    Converts a number from decimal to another base.
    """
    # Gets maximum exponent of base
    exp = 0
    while base**(exp  + 1) <= n:
        exp+= 1

    # Adds all the numbers that aren't a multiple of base to the string.
    num_str = ''
    while n != 0 and exp >= constants.MAX_CONVERT_DEPTH:
        # Adds a decimal point if we're below 0 exp.
        if exp == -1:
            num_str+= '.'
        num_str+= constants.CONVERT_CHARS[int(n / base ** exp)]
        n -= (int(n / base**exp) * base**exp)
        exp-= 1

    # Adds all the zeros between exp and 0 if exp is not below 0.
    while exp >= 0:
        num_str+= '0'
        exp-= 1

    return num_str


def convert_num_to_decimal(n, base):
    """
    Converts a number to decimal from another base.
    """
    # If there's more than 1 decimal point, we raise a ValueError.
    if n.count('.') > 1:
        raise ValueError()

    # If there is no decimal point, we take the easy way out.
    if '.' not in n:
        return int(n, base=base)

    # Otherwise, we're in for a ride.
    else:
        # Get the index of the period.
        per_index = n.find('.')

        # Take the easy way for the numbers BEFORE the decimal point.
        final_num = int(n[:per_index], base=base)

        # We add a little leniency for those below base 36 in terms of capitalization.
        if base <= 36:
            n = n.upper()

        # Do it ourselves for numbers after.
        for index in range(per_index + 1, len(n)):
            exp = per_index - index
            num_of = constants.CONVERT_CHARS.find(n[index])
            # A little error handling for -1's or stuff outside the range.
            if num_of == -1 or num_of >= base:
                raise ValueError()
            else:
                final_num+= base**exp * num_of

        return final_num


async def get_num_from_argument(message, argument):
    # Gets usages for arguments
    argument = util.normalize_string(argument)
    argument2 = argument.lower()

    # Nondecimal bases
    for base in constants.NONDECIMAL_BASES.keys():
        if argument2.startswith(base):
            try:
                return convert_num_to_decimal(argument[2:], constants.NONDECIMAL_BASES[base][0])
            except ValueError:
                await message.channel.send(argument + ' is not a valid {} number').format(constants.NONDECIMAL_BASES[base][1])
                return ''

    # Decimal base
    try:
        return float(argument)
    except ValueError:
        await message.channel.send(argument + ' is not a valid decimal number')
        return ''


async def hexadecimal(self, message, argument, is_in_guild):
    """
    Converts a number to hexadecimal.
    """
    # Getting the number
    num = await get_num_from_argument(message, argument)

    # Error handling for not numbers
    if isinstance(num, str):
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested hex conversion for {}, invalid'.format(argument))
        return

    num = convert_num_from_decimal(num, 16)

    await message.channel.send('0x' + str(num))
    log.debug(util.get_comm_start(message, is_in_guild) + 'requested hex conversion for {}, responded 0x{}'.format(argument, num))


async def duodecimal(self, message, argument, is_in_guild):
    """
    Converts a number to duodecimal.
    """
    # Getting the number
    num = await get_num_from_argument(message, argument)

    # Error handling for not numbers
    if isinstance(num, str):
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested duodec conversion for {}, invalid'.format(argument))
        return

    num = convert_num_from_decimal(num, 12)

    log.debug(util.get_comm_start(message, is_in_guild) + 'requested duodec conversion for {}, responded 0d{}'.format(argument, num))
    await message.channel.send('0d' + str(num))


async def decimal(self, message, argument, is_in_guild):
    """
    Converts a number to decimal.
    """
    # Getting the number
    num = await get_num_from_argument(message, argument)

    # Error handling for not numbers
    if isinstance(num, str):
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested decimal conversion for {}, invalid'.format(argument))
        return

    log.debug(util.get_comm_start(message, is_in_guild) + 'requested decimal conversion for {}, responded {}'.format(argument, int(num) if num % 1 == 0 else num))
    await message.channel.send(int(num) if num % 1 == 0 else num)


async def octal(self, message, argument, is_in_guild):
    """
    Converts a number to octal.
    """
    # Getting the number
    num = await get_num_from_argument(message, argument)

    # Error handling for not numbers
    if isinstance(num, str):
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested octal conversion for {}, invalid'.format(argument))
        return

    num = convert_num_from_decimal(num, 8)

    log.debug(util.get_comm_start(message, is_in_guild) + 'requested octal conversion for {}, responded 0o{}'.format(argument, num))
    await message.channel.send('0o' + str(num))


async def binary(self, message, argument, is_in_guild):
    """
    Converts a number to binary.
    """
    # Getting the number
    num = await get_num_from_argument(message, argument)

    # Error handling for not numbers
    if isinstance(num, str):
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested binary conversion for {}, invalid'.format(argument))
        return

    num = convert_num_from_decimal(num, 2)

    log.debug(util.get_comm_start(message, is_in_guild) + 'requested binary conversion for {}, responded with 0b{}'.format(argument, num))
    await message.channel.send('0b' + str(num))

async def birthday(self, message, argument, is_in_guild):
    """
    Sets a user to be reminded about a person's birthday or lists all birthdays the person will be reminded of.
    """
    # Normalize argument
    argument = util.normalize_string(argument)

    if argument:
        # Adding birthday
        if argument.startswith('add '):
            # Split up argument.
            argument = argument[4:]
            lastspace = argument.rfind(' ')
            if lastspace + 1:
                name = argument[:lastspace]
                date = argument[lastspace + 1:]

                # Check if valid date
                for c in date:
                    if c not in constants.BIRTHDAY_DATE_CHARS:
                            log.debug(util.get_comm_start(message, is_in_guild) + 'ran birthday command with invalid date'.format(argument))
                            await message.channel.send('Invalid date.')


        # Listing birthdays
        elif argument.startswith('list '):
            return

        # Removing birthdays
        elif argument.startswith('remove '):
            return

    log.debug(util.get_comm_start(message, is_in_guild) + 'ran birthday command with no / incorrect arguments'.format(argument))
    await message.channel.send('```Usage:\nj!birthday add [Name / User] MM/DD\nj!birthday add [Name / User] MM/DD/YYYY\nj!birthday remove [Name / User]\nj!birthday list```')
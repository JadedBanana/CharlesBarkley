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
from lib.util import misc

# Logging
log = None

async def weather(self, message, argument, is_in_guild):
    """
    Gets the current weather for the given city/state/province.
    """
    # Test the argument.
    if not argument:
        log.debug(misc.get_comm_start(message, is_in_guild) + 'requested weather, empty city value')
        await message.channel.send('Invalid city.')
        return

    # Normalize the argument
    argument = misc.normalize_string(argument)

    # Testing again.
    if not argument:
        log.debug(misc.get_comm_start(message, is_in_guild) + 'requested weather, empty city value')
        await message.channel.send('Invalid city.')
        return

    # Simple request call.
    response = requests.get(constants.WEATHER_API_URL.format(constants.WEATHER_API_KEY, argument))
    weather_json = response.json()

    # If we didn't get weather_json or it's broken, we tell the user that.
    if not weather_json or 'cod' not in weather_json.keys():
        log.debug(misc.get_comm_start(message, is_in_guild) + 'requested weather, think it\'s broken')
        await message.channel.send('Weather service is down, please be patient.')
        return

    # If the code is a 404, then we tell the user they have an invalid city.
    if weather_json['cod'] == 404 or any([key not in weather_json.keys() for key in ['name', 'sys', 'main']]):
        log.debug(misc.get_comm_start(message, is_in_guild) + 'requested weather for city {}, invalid'.format(argument))
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
            embed.add_field(name='Status', value=misc.upper_per_word(weather_json['weather'][0]['description']) + ' \u200b \u200b \u200b', inline=True)
        elif 'main' in weather_json['weather'][0].keys() and weather_json['weather'][0]['main']:
            embed.add_field(name='Status', value=misc.upper_per_word(weather_json['weather'][0]['main']) + ' \u200b \u200b \u200b', inline=True)
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


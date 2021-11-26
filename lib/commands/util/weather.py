"""
Weather command.
Displays the weather in a given city.
"""
# Imports
from lib.util import arguments, environment, messaging, misc, parsing
from lib.util.logger import BotLogger as logging
from dateutil.tz import tzoffset, UTC
from datetime import datetime
from iso3166 import countries
from math import fabs
import requests
import discord


# Weather constants
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?appid={}&q={}'
WEATHER_ALT_COUNTRY_CODES = {
    'BO': 'Bolivia', 'FK': 'Falkland Islands', 'FM': 'Micronesia', 'GB': 'United Kingdom', 'IR': 'Iran',
    'KP': 'North Korea', 'KR': 'South Korea', 'LA': 'Laos', 'MD': 'Moldova', 'PS': 'Palestine', 'RU': 'Russia',
    'SX': 'Sint Maarten', 'SY': 'Syria', 'TW': 'Taiwan', 'TZ': 'Tanzania', 'US': 'United States', 'VE': 'Venezuela',
    'VN': 'Vietnam'
}
WEATHER_CREDIT_TEXT = 'Powered by OpenWeatherMap'
WEATHER_EMBED_COLOR_DEFAULT = (235 << 16) + (110 << 8) + 75
WEATHER_EMBED_COLORS_BY_ICON = {
    '01d': (235 << 16) + (110 << 8) + 75, '02d': (235 << 16) + (110 << 8) + 75, '10d': (235 << 16) + (110 << 8) + 75,
    '11d': (235 << 16) + (110 << 8) + 75, '11n': (235 << 16) + (110 << 8) + 75, '03d': (242 << 16) + (242 << 8) + 242,
    '03n': (242 << 16) + (242 << 8) + 242, '04d': (242 << 16) + (242 << 8) + 242, '04n': (242 << 16) + (242 << 8) + 242,
    '13d': (242 << 16) + (242 << 8) + 242, '13n': (242 << 16) + (242 << 8) + 242, '50d': (242 << 16) + (242 << 8) + 242,
    '50n': (242 << 16) + (242 << 8) + 242, '01n': (72 << 16) + (72 << 8) + 74, '02n': (72 << 16) + (72 << 8) + 74,
    '09d': (72 << 16) + (72 << 8) + 74, '09n': (72 << 16) + (72 << 8) + 74, '10n': (72 << 16) + (72 << 8) + 74
}
WEATHER_KELVIN_SUB = 273.15
WEATHER_THUMBNAIL_URL = 'http://openweathermap.org/img/wn/{}@4x.png'
WEATHER_WIND_DIRECTIONS = {
    'North': 22.5, 'Northeast': 67.5, 'East': 112.5,
    'Southeast': 157.5, 'South': 202.5, 'Southwest': 247.5,
    'West': 292.5, 'Northwest': 337.5, 'North2': 382.5
}


async def get_weather_dict(message, argument):
    """
    Performs the API call to get the weather dict and makes sure that it's suitable for parsing.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.

    Returns:
        dict : The weather JSON, accessed from OpenWeatherMap.
    """
    # Normalize the argument.
    argument = parsing.normalize_string(argument)

    # If no argument, then report it as an invalid city.
    if not argument:
        logging.info(message, 'requested weather, empty city value')
        return await messaging.send_text_message(message, 'Invalid city.')

    # Simple request call to get our weather.
    response = requests.get(WEATHER_API_URL.format(environment.get('WEATHER_API_KEY'), argument))
    weather_json = response.json()

    # If we didn't get weather_json or it's broken, we tell the user that.
    if not weather_json or 'cod' not in weather_json:
        logging.info(message, "requested weather, think it's broken")
        return await messaging.send_text_message(message, 'Weather service is down, please try again later.')

    # If the code is a 404, then we tell the user they have an invalid city.
    if weather_json['cod'] == 404 or any([key not in weather_json for key in ['name', 'sys', 'main']]):
        logging.info(message, f'requested weather for city {argument}, invalid')
        return await messaging.send_text_message(message, 'Invalid city.')

    # If the dict is broken, then we tell the user that the weather data for that city is unavailable.
    if not isinstance(weather_json['name'], str) or not isinstance(weather_json['sys'], dict) \
            or not isinstance(weather_json['main'], dict):
        logging.info(message, f'requested weather for city {argument}, fucked up weather dict')
        return await messaging.send_text_message(message, 'Weather data for that city is currently unavailable, sorry!')

    # All else passed, return the weather json.
    return weather_json


def get_city(weather_dict):
    """
    Gets the city of the weather dict.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        str : The name of the city.
    """
    return weather_dict['name']


def get_country(weather_dict):
    """
    Gets the country of the weather dict.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        str : The country name.
    """
    # Check for country code in the weather_dict.
    if 'country' in weather_dict['sys'] and isinstance(weather_dict['sys']['country'], str):

        # If it's an alternative country code, return that.
        if weather_dict['sys']['country'] in WEATHER_ALT_COUNTRY_CODES:
            return WEATHER_ALT_COUNTRY_CODES[weather_dict['sys']['country']]

        # Otherwise, return the iso3166 country.
        return countries.get(weather_dict['sys']['country']).name

    # Return unknown country
    return 'Unknown Country'


def get_longitude_latitude(weather_dict):
    """
    Gets the longitude and latitude of the weather dict.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        str : The coordinates string.
    """
    # Check for the longitude and latitude in the weather_dict.
    if 'coord' in weather_dict and isinstance(weather_dict['coord'], dict) and \
            'lat' in weather_dict['coord'] and 'lon' in weather_dict['coord'] \
            and (isinstance(weather_dict['coord']['lat'], int) or isinstance(weather_dict['coord']['lat'], float)) \
            and (isinstance(weather_dict['coord']['lon'], int) or isinstance(weather_dict['coord']['lon'], float)):

        # Latitude Part 1 (get the number part of it)
        latitude_num = weather_dict['coord']['lat']
        latitude_num_formatted = f'{fabs(latitude_num):.02f}'
        latitude_num_split = latitude_num_formatted.split('.')

        # Longitude Part 2 (split into degrees and minutes)
        latitude_degrees = latitude_num_split[0]
        latitude_minutes = latitude_num_split[1]
        latitude_sign = 'N' if latitude_num > 0 else ('S' if latitude_num < 0 else '')

        # Longitude Part 1 (get the number part of it)
        longitude_num = weather_dict['coord']['lon']
        longitude_num_formatted = f'{fabs(longitude_num):.02f}'
        longitude_num_split = longitude_num_formatted.split('.')

        # Longitude Part 2 (split into degrees and minutes)
        longitude_degrees = longitude_num_split[0]
        longitude_minutes = longitude_num_split[1]
        longitude_sign = 'E' if longitude_num > 0 else ('W' if longitude_num < 0 else '')

        return f'{latitude_degrees}\N{DEGREE SIGN}{latitude_minutes}"{latitude_sign}, ' \
               f'{longitude_degrees}\N{DEGREE SIGN}{longitude_minutes}"{longitude_sign}'

    # No coordinates available, return an excuse.
    return 'No coordinates available'


def get_current_temp(weather_dict):
    """
    Gets the current temperature from the weather dict.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        str : The current temperature, represented as a string.
    """
    # Check if the temperature exists in the dict.
    if 'temp' in weather_dict['main'] and (isinstance(weather_dict['main']['temp'], float)
                                           or isinstance(weather_dict['main']['temp'], int)):

        # Return the formatted temperature.
        return format_temperature(weather_dict['main']['temp'])

    # Unavailable, return Unavailable.
    return 'Unavailable'


def get_feels_like(weather_dict):
    """
    Gets the 'feels like' temperature from the weather dict.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        str : The 'feels like' temperature, represented as a string.
    """
    # Check if the temperature exists in the dict.
    if 'feels_like' in weather_dict['main'] and (isinstance(weather_dict['main']['feels_like'], float)
                                                 or isinstance(weather_dict['main']['feels_like'], int)):

        # Return the formatted temperature.
        return format_temperature(weather_dict['main']['feels_like'])

    # Unavailable, return Unavailable.
    return 'Unavailable'


def get_low_temp(weather_dict):
    """
    Gets the temperature low from the weather dict.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        str : The low, represented as a string.
    """
    # Check if the temperature exists in the dict.
    if 'temp_min' in weather_dict['main'] and (isinstance(weather_dict['main']['temp_min'], float)
                                               or isinstance(weather_dict['main']['temp_min'], int)):

        # Return the formatted temperature.
        return format_temperature(weather_dict['main']['temp_min'])

    # Unavailable, return Unavailable.
    return 'Unavailable'


def get_high_temp(weather_dict):
    """
    Gets the temperature high from the weather dict.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        str : The high, represented as a string.
    """
    # Check if the temperature exists in the dict.
    if 'temp_max' in weather_dict['main'] and (isinstance(weather_dict['main']['temp_max'], float)
                                               or isinstance(weather_dict['main']['temp_max'], int)):

        # Return the formatted temperature.
        return format_temperature(weather_dict['main']['temp_max'])

    # Unavailable, return Unavailable.
    return 'Unavailable'


def get_status(weather_dict):
    """
    Gets the weather status from the weather dict.
    The status is stuff like, 'partly cloudy' or 'light showers' or 'clear skies' or whatever.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        str : The status.
    """
    # See if the 'weather' entry exists.
    if 'weather' in weather_dict and isinstance(weather_dict['weather'], list) and len(weather_dict['weather']) > 0:

        # Pull it from the 'description' key.
        if 'description' in weather_dict['weather'][0] and weather_dict['weather'][0]['description'] \
                and isinstance(weather_dict['weather'][0]['description'], str):
            return misc.upper_per_word(weather_dict['weather'][0]['description'])

        # Pull it from the 'main' key.
        elif 'main' in weather_dict['weather'][0] and weather_dict['weather'][0]['main'] \
                and isinstance(weather_dict['weather'][0]['main'], str):
            return misc.upper_per_word(weather_dict['weather'][0]['main'])

    # Unavailable, return Unavailable.
    return 'Unavailable'


def get_humidity(weather_dict):
    """
    Gets the humidity index from the weather dict.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        str : The humidity percentage, represented as a string.
    """
    # See if the 'humidity' entry exists.
    if 'humidity' in weather_dict['main'] and (isinstance(weather_dict['main']['humidity'], float)
                                                      or isinstance(weather_dict['main']['humidity'], int)):

        # Return it.
        return f'{int(weather_dict["main"]["humidity"])}%'

    # Unavailable, return Unavailable.
    return 'Unavailable'


def get_air_pressure(weather_dict):
    """
    Gets the air pressure, in kPa, from the weather dict.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        str : The air pressure in kPa, represented as a string.
    """
    # See if the 'pressure' entry exists.
    if 'pressure' in weather_dict['main'] and (isinstance(weather_dict['main']['pressure'], float)
                                                      or isinstance(weather_dict['main']['pressure'], int)):

        # Return it.
        return f'{int(weather_dict["main"]["pressure"]) / 10} kPa'

    # Unavailable, return Unavailable.
    return 'Unavailable'


def get_visibility(weather_dict):
    """
    Gets the visibility, in both meters and feet, from the weather dict.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        str : The visibility represented as a string.
    """
    # See if the 'visibility' entry exists.
    if 'visibility' in weather_dict and (isinstance(weather_dict['visibility'], float)
                                         or isinstance(weather_dict['visibility'], int)):

        # Grab the visibility.
        visibility_meters = weather_dict["visibility"]

        # OpenWeatherMap maxes this out at 10km. Check for >9999.
        if visibility_meters > 9999:
            return 'Unhindered'

        # Less than 10km, return.
        return f'{int(visibility_meters)} m / {int(visibility_meters * 3.28084)} ft'

    # Unavailable, return Unavailable.
    return 'Unavailable'


def get_wind_speed(weather_dict):
    """
    Gets the wind speed, in kilometers per hour and miles per hour, from the weather dict.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        str : The wind speed in both kilometers per hour and miles per hour.
    """
    # See if there is a speed thing in there.
    if 'speed' in weather_dict['wind'] and (isinstance(weather_dict['wind']['speed'], float)
                                            or isinstance(weather_dict['wind']['speed'], int)):

        # Return.
        return f'{int(weather_dict["wind"]["speed"] * 3.6)} kmh / {int(weather_dict["wind"]["speed"] * 2.23694)} mph'

    # Unavailable, return Unavailable.
    return 'Unavailable'


def get_wind_gust(weather_dict):
    """
    Gets the wind gust, in kilometers per hour and miles per hour, from the weather dict.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        str : The wind gust in both kilometers per hour and miles per hour.
    """
    # See if there is a gust thing in there.
    if 'gust' in weather_dict['wind'] and (isinstance(weather_dict['wind']['gust'], float)
                                            or isinstance(weather_dict['wind']['gust'], int)):

        # Return.
        return f'{int(weather_dict["wind"]["gust"] * 3.6)} kmh / {int(weather_dict["wind"]["gust"] * 2.23694)} mph'

    # Unavailable, return Unavailable.
    return 'Unavailable'


def get_wind_direction(weather_dict):
    """
    Gets the wind direction (cardinal direction).

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        str : The wind direction as a cardinal direction (North, East, South, West).
    """
    # Establish a direction variable.
    direction = None

    # See if there is a degree thing in there.
    if 'deg' in weather_dict['wind'] and (isinstance(weather_dict['wind']['deg'], float)
                                          or isinstance(weather_dict['wind']['deg'], int)):

        # Iterate through the cardinal direction dict and update the direction.
        for cardinal, max_angle in WEATHER_WIND_DIRECTIONS.items():

            # If the degrees is less than the direction given in the dict, then break with that direction set.
            # Also remove the 2, for North2.
            if weather_dict['wind']['deg'] <= max_angle:
                direction = cardinal.strip('2')
                break

    # Return.
    return direction


def get_wind_attributes(weather_dict):
    """
    Gets wind speed, gust, and direction.
    Acts as a wrapper for get_wind_speed, get_wind_gust, and get_wind_direction.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        str, str, str : The wind speed, gust, and direction in that order.
    """
    # Check if the 'wind' attribute exists in the weather dict.
    if 'wind' in weather_dict and isinstance(weather_dict['wind'], dict):

        # Get all three.
        wind_speed = get_wind_speed(weather_dict)
        wind_gust = get_wind_gust(weather_dict)
        wind_direction = get_wind_direction(weather_dict)

        # Return.
        return wind_speed, wind_gust, wind_direction

    # Unavailable, return unavailable attributes
    return 'Unavailable', 'Unavailable', None


def get_embed_color(weather_dict):
    """
    Gets the embed color given the weather conditions in the weather dict.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        int : The embed's color.
    """
    # See if an icon was supplied with the weather data.
    if 'weather' in weather_dict and len(weather_dict['weather']) > 0 and 'icon' in weather_dict['weather'][0] \
            and weather_dict['weather'][0]['icon']:

        # See if the icon has an associated embed color. Return that.
        if weather_dict['weather'][0]['icon'] in WEATHER_EMBED_COLORS_BY_ICON:
            return WEATHER_EMBED_COLORS_BY_ICON[weather_dict['weather'][0]['icon']]

        # If the icon doesn't have an associated embed color, then log an error and return the default.
        else:
            logging.error(f'New weather icon {weather_dict["weather"][0]["icon"]}, '
                          f'please create embed colors for it asap!')

    # Worst case, nothing was found, so return the default.
    return WEATHER_EMBED_COLOR_DEFAULT


def get_embed_icon(weather_dict):
    """
    Gets the embed icon URL given the weather conditions in the weather dict.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        str : The URL to the embed icon.
    """
    # See if an icon was supplied with the weather data.
    if 'weather' in weather_dict and len(weather_dict['weather']) > 0 and 'icon' in weather_dict['weather'][0] \
            and weather_dict['weather'][0]['icon']:

        # Return the icon URL.
        return WEATHER_THUMBNAIL_URL.format(weather_dict['weather'][0]['icon'])

    # Worst case, nothing was found, so return None.
    return None


def get_time_zone(weather_dict):
    """
    Gets the time zone from the weather dict.

    Arguments:
        weather_dict (dict) : The weather dict.

    Returns:
        dateutil.tz.tzoffset : The timezone offset.
    """
    # Check for timezone data.
    if 'timezone' in weather_dict and isinstance(weather_dict['timezone'], int):

        # Return the timezone.
        return tzoffset('placeholder', weather_dict['timezone'])

    # Worst case, nothing was found, so return None.
    return None


def get_local_time(time_zone):
    """
    Gets the local time from the time zone.

    Arguments:
        time_zone (dateutil.tz.tzoffset) : The local time zone.

    Returns:
        str : The local time.
    """
    # If the time zone exists, getting the local time is easy.
    if time_zone:
        local_time = datetime.now(time_zone)
        return local_time.strftime('%H:%M (%I:%M %p)')

    # Worst case, nothing was found, so return Unavailable.
    return 'Unavailable'


def get_sunrise_time(weather_dict, time_zone):
    """
    Gets the sunrise time from the weather dict.
    If time_zone is supplied, it will be in local time as opposed to UTC.

    Arguments:
        weather_dict (dict) : The weather dict.
        time_zone (dateutil.tz.tzoffset) : The local time zone.

    Returns:
        str : The sunrise time.
    """
    # See if the sunrise is in the weather dict.
    if 'sunrise' in weather_dict['sys'] and isinstance(weather_dict['sys']['sunrise'], int):

        # If the timezone exists, then we can pull it from the dict and return.
        if time_zone:
            sunrise_time = datetime.utcfromtimestamp(weather_dict['sys']['sunrise'] + weather_dict['timezone'])
            return sunrise_time.strftime('%H:%M (%I:%M %p)')

        # Otherwise, we make it in UTC.
        sunrise_time = datetime.utcfromtimestamp(weather_dict['sys']['sunrise'])
        return sunrise_time.strftime('%H:%M (%I:%M %p) UTC')

    # Worst case, nothing was found, so return Unavailable.
    return 'Unavailable'


def get_sunset_time(weather_dict, time_zone):
    """
    Gets the sunset time from the weather dict.
    If time_zone is supplied, it will be in local time as opposed to UTC.

    Arguments:
        weather_dict (dict) : The weather dict.
        time_zone (dateutil.tz.tzoffset) : The local time zone.

    Returns:
        str : The sunset time.
    """
    # See if the sunset is in the weather dict.
    if 'sunset' in weather_dict['sys'] and isinstance(weather_dict['sys']['sunset'], int):

        # If the timezone exists, then we can pull it from the dict and return.
        if time_zone:
            sunset_time = datetime.utcfromtimestamp(weather_dict['sys']['sunset'] + weather_dict['timezone'])
            return sunset_time.strftime('%H:%M (%I:%M %p)')

        # Otherwise, we make it in UTC.
        sunset_time = datetime.utcfromtimestamp(weather_dict['sys']['sunset'])
        return sunset_time.strftime('%H:%M (%I:%M %p) UTC')

    # Worst case, nothing was found, so return Unavailable.
    return 'Unavailable'


def format_temperature(temp_kelvin):
    """
    Formats the given temperature (in Kelvin) into a readable string, with both degrees celsius and fahrenheit.

    Arguments:
        temp_kelvin (float) : The temperature, in Kelvin.

    Returns:
        str : The temperature string, with celsius first then fahrenheit.
    """
    return f'{int(temp_kelvin - WEATHER_KELVIN_SUB + 0.5)}\N{DEGREE SIGN}C / ' \
           f'{int((temp_kelvin - WEATHER_KELVIN_SUB) * 1.8 + 32 + 0.5)}\N{DEGREE SIGN}F'


async def weather(bot, message, argument):
    """
    Gets the current weather for the given city/state/province.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Get the weather dict.
    weather_dict = await get_weather_dict(message, argument)

    # If the weather_dict wasn't returned, then just return.
    if not weather_dict:
        return

    # Log.
    logging.info(message, f'requested weather for city {argument}')

    # Gather city name and country, as well as longitude and latitude.
    city = get_city(weather_dict)
    country = get_country(weather_dict)
    longitude_latitude = get_longitude_latitude(weather_dict)

    # Get temperatures.
    current_temp = get_current_temp(weather_dict)
    feels_like = get_feels_like(weather_dict)
    low_temp = get_low_temp(weather_dict)
    high_temp = get_high_temp(weather_dict)

    # Get status, humidity, air pressure, visibility.
    status = get_status(weather_dict)
    humidity = get_humidity(weather_dict)
    air_pressure = get_air_pressure(weather_dict)
    visibility = get_visibility(weather_dict)

    # Get wind speed, wind gust, and wind direction.
    # These are all coagulated into one because of some shared IF statements.
    wind_speed, wind_gust, wind_direction = get_wind_attributes(weather_dict)

    # Get local time, sunrise time, sunset time.
    time_zone = get_time_zone(weather_dict)
    local_time = get_local_time(time_zone)
    sunrise_time = get_sunrise_time(weather_dict, time_zone)
    sunset_time = get_sunset_time(weather_dict, time_zone)

    # Get the color for the embed, as well as the icon.
    icon = get_embed_icon(weather_dict)
    embed_color = get_embed_color(weather_dict)

    # Create the embed and set its footer + icon.
    embed = discord.Embed(title=f'Weather for {city}, {country}', colour=embed_color, description=longitude_latitude)
    embed.set_footer(text=WEATHER_CREDIT_TEXT)
    if icon:
        embed.set_thumbnail(url=icon)

    # Add the first row (current temp, status, blank space)
    embed.add_field(name='Current Temp.', value=current_temp, inline=True)
    embed.add_field(name='Status', value=status, inline=True)
    embed.add_field(name='\u200b', value='\u200b', inline=True)

    # Add the second row (feels like, low, high)
    embed.add_field(name='Feels Like', value=feels_like, inline=True)
    embed.add_field(name='Low Temp.', value=low_temp, inline=True)
    embed.add_field(name='High Temp.', value=high_temp, inline=True)

    # Add the third row (humidity, pressure, visibility)
    embed.add_field(name='Humidity', value=humidity, inline=True)
    embed.add_field(name='Pressure', value=air_pressure, inline=True)
    embed.add_field(name='Visibility', value=visibility, inline=True)

    # Add the fourth row (wind speed, wind gust, blank space)
    embed.add_field(name='Wind Speed',
                    value=wind_speed + (f' {wind_direction}' if wind_direction and wind_speed != 'Unavailable' else ''),
                    inline=True)
    embed.add_field(name='Wind Gust',
                    value=wind_gust + (f' {wind_direction}' if wind_direction and wind_gust != 'Unavailable' else ''),
                    inline=True)
    embed.add_field(name='\u200b', value='\u200b', inline=True)

    # Add the fifth row (humidity, pressure, visibility)
    embed.add_field(name='Local Time', value=local_time, inline=True)
    embed.add_field(name='Sunrise Time', value=sunrise_time, inline=True)
    embed.add_field(name='Sunset Time', value=sunset_time, inline=True)

    # For each field, add a little space so that none of the attributes are all smooshed together.
    for field in embed.fields:
        field.name = field.name + ' \u200b \u200b \u200b'

    # Send message.
    await messaging.send_embed_without_local_image(message, embed)


# Command values
PUBLIC_COMMAND_DICT = {
    'weather': weather
}

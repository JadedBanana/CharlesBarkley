"""
Random Youtube command.
Uses the YouTube API to pull a random Youtube video by searching with a randomized string of 1 to 5 characters.
Has a limit of 100 uses per day due to Youtube API token limits.
"""
# Imports
from lib.util import environment, messaging, misc
from lib.util.logger import BotLogger as logging
from datetime import datetime, timedelta
import random
import string
import urllib
import json


# A lot of constants important for the Youtube API.
YOUTUBE_QUOTA_RESET_HOUR = 3
YOUTUBE_VIDEO_URL_FORMAT = 'https://www.youtube.com/watch?v={}'
YOUTUBE_SEARCH_URL_FORMAT = \
    'https://www.googleapis.com/youtube/v3/search?key={0}&maxResults={1}&part=snippet&type=video&q={2}'
YOUTUBE_SEARCH_RESULTS_LIMIT = 100
YOUTUBE_SEARCH_LENGTHS = [1, 2, 3, 4, 5]
YOUTUBE_SEARCH_WEIGHTS = [36, 1296, 46656, 1679616, 60466176]
YOUTUBE_RICKROLL_URL = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
YOUTUBE_QUOTA_REACHED = False


async def get_random_video(message):
    """
    Gets a random video and sends it to the channel.
    Has a random chance for it to just be a rick roll.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # Rolls the random chance for a rick roll...
    if random.random() < 1/environment.get('YOUTUBE_RICKROLL_CHANCE'):
        logging.info(message, 'requested random video, rickrolled them')
        return await messaging.send_text_message(message, YOUTUBE_RICKROLL_URL)

    # Random chance failed, perform the normal random youtube video generation.
    search_results = {'items': []}

    # While there are no items in the search results, loop and try to get some.
    while not search_results['items']:
        # Gets random search term.
        random_search = ''.join(
            random.choice(string.ascii_uppercase + string.digits)
            for i in range(random.choices(YOUTUBE_SEARCH_LENGTHS, weights=YOUTUBE_SEARCH_WEIGHTS)[0]))

        # Generates the URL from the format.
        url = YOUTUBE_SEARCH_URL_FORMAT.format(
            environment.get('YOUTUBE_API_KEY'), YOUTUBE_SEARCH_RESULTS_LIMIT, random_search)

        # Open the URL and load the results.
        url_data = urllib.request.urlopen(url)
        video_data = url_data.read()

        # Gets the search results.
        encoding = url_data.info().get_content_charset('utf-8')
        search_results = json.loads(video_data.decode(encoding))

    # Now that search results have been achieved, gather the video ID's.
    video_ids = [video['id']['videoId'] for video in search_results['items']]

    # Pick a random video ID.
    choice = random.randint(0, len(video_ids) - 1)

    # Return selected video.
    logging.info(message, f'requested random video, returned video id {video_ids[choice]} '
                          f'which was result {str(choice)} in results for {random_search}')
    await messaging.send_text_message(message, YOUTUBE_VIDEO_URL_FORMAT.format(video_ids[choice]))


async def quota_reached_send_message(message):
    """
    Reports when the quota has been reached and sends a message.
    Message tells when the quota will be reset.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
    """
    # First, log that the quota has been reached thanks to THIS Bozo.
    logging.info(message, 'requested random video, quota reached')

    # Next, we get the time delta between now and when the quota should be reset.
    # This starts by getting a target time variable, set to today.
    target_time = datetime.today()

    # If we are beyond the quota reset time, we add 1 to the target date.
    if target_time.hour >= YOUTUBE_QUOTA_RESET_HOUR:
        target_time = target_time + timedelta(days=1)

    # Then we create a new date from the target_time.
    target_time = datetime(year=target_time.year, month=target_time.month, day=target_time.day, hour=YOUTUBE_QUOTA_RESET_HOUR)

    # Get time until quota and return that.
    quota_str = misc.calculate_time_passage(target_time - datetime.now())
    await messaging.send_text_message(message, f'Youtube quota of 100 videos reached. Try again in {quota_str}')


async def random_youtube_master(bot, message, argument):
    """
    Generates a random youtube link.
    In the case of the Youtube Token Quota being hit, an appropriate error message will be presented to the user.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Attempts to get the random video.
    try:
        await get_random_video(message)

    # urllib.error.HTTPError happens when the quota has been reached.
    except urllib.error.HTTPError:
        await quota_reached_send_message(message)


# Command values
PUBLIC_COMMAND_DICT = {
    'randomyt': random_youtube_master,
    'randomyoutube': random_youtube_master
}
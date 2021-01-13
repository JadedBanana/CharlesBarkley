# =================================================================
#                         FUN COMMANDS
# =================================================================
from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageFilter
from datetime import datetime, timedelta
from exceptions import *
import constants
import wikipedia
import requests
import discord
import random
import string
import urllib
import json
import util
import os

# Logger
log = None

async def copy_msg(self, message, is_in_guild):
    """
    Copies a user's message if they have been deemed COPIABLE by someone.
    That is, unless the message is to stop copying.
    """
    if message.content.startswith('j!stopcopying') and (len(message.content) == 13 or message.content[13] == ' '):
        return
    # Inside guilds
    if is_in_guild:
        if str(message.guild.id) in self.copied_users.keys() and message.author in self.copied_users[str(message.guild.id)]:
            await message.channel.send(message.content)
    # Inside DM's and Group Chats
    else:
        if str(message.channel.id) in self.copied_users.keys() and message.author in self.copied_users[str(message.channel.id)]:
            await message.channel.send(message.content)


async def copy_user(self, message, argument, is_in_guild):
    """
    Marks a user down as copiable.
    Copiable users will be copied in every message they send.
    """
    # Tries to get a valid user out of the argument.
    try:
        users = util.get_closest_users(message, argument, is_in_guild)
    except (ArgumentTooShortError, NoUserSpecifiedError, UnableToFindUserError):
        users = []
    if not users:
        log.info(util.get_comm_start(message, is_in_guild) + 'requested copy for user ' + argument + ', invalid')
        await message.channel.send('Invalid user.')
        return

    # Gets the key we'll be using for the copied_users dict.
    if is_in_guild:
        copied_key = str(message.guild.id)
    else:
        copied_key = str(message.channel.id)
    if copied_key not in self.copied_users.keys():
        self.copied_users.update({copied_key: []})

    # Adds the users to the copy dict.
    for user in users:

        # Checks to make sure it isn't self.
        if user == self.user:
            if not len(users) - 1:
                log.debug(util.get_comm_start(message, is_in_guild) + 'requested copy for this bot')
                await message.channel.send('Yeah, no, I\'m not gonna copy myself.')
            continue

        # Other.
        await message.channel.send('Now copying user ' + (user.nick if user.nick else user.name))
        if user not in self.copied_users[copied_key]:
            self.copied_users[copied_key].append(user)
            log.info(util.get_comm_start(message, is_in_guild) + 'requested copy for user ' + str(user) + ', now copying')
        else:
            log.info(util.get_comm_start(message, is_in_guild) + 'requested copy for user ' + str(user) + ', already copying')


async def stop_copying(self, message, argument, is_in_guild):
    """
    Stops copying everyone in a server.
    """
    # Gets copy key
    if is_in_guild:
        copied_key = str(message.guild.id)
    else:
        copied_key = str(message.channel.id)

    # If the thing exists in the dict
    if copied_key in self.copied_users.keys():
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested to stop copying, {} users deleted from copied_users'.format(len(self.copied_users[copied_key])))
        self.copied_users.pop(copied_key)
        await message.channel.send('No longer copying people in this server.')
    else:
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested to stop copying, already done')
        await message.channel.send('Wasn\'t copying anyone here to begin with, but ok.')


async def uwuify(self, message, argument, is_in_guild, use_owo=False):
    """
    Weplaces all the r's in a message with w's.
    Lol.
    """
    def do_uwu_replace(text):
        """
        Method for advanced replacement, so that we avoid replacing characters in emotes.
        """
        colon_count = text.count(':')
        # If there IS an emote, we take special care.
        if colon_count > 1:
            # uwuify all the text ASIDE from emotes.
            text_uwued = ''
            # Indexes that will be needed to do this properly.
            last_index = -1
            uwued_max = -1
            colons_passed = 0

            # Perform loop.
            while colons_passed < colon_count - 1:
                # Find the next colon.
                colon_index = text.index(':', last_index + 1)

                # Find the NEXT next colon.
                next_colon_index = text.index(':', colon_index + 1)

                # Test and see if all the characters between the two colons are alphanumeric.
                # Also makes sure the colons are more than 2 apart.
                is_emote = next_colon_index - colon_index > 2
                if is_emote:
                    for c in text[colon_index + 1:next_colon_index]:
                        if c not in constants.EMOTE_CHARACTERS:
                            is_emote = False

                # If this is an emote, we act accordingly.
                if is_emote:
                    # We go ahead and uwuify everything up to this point.
                    uwu_append = text[uwued_max + 1:colon_index].replace('r', 'w').replace('R', 'W').replace('l', 'w').replace('L', 'W').replace('no', 'nyo').replace('NO', 'NYO').replace('nO', 'nYO').replace('No', 'Nyo')
                    faces = constants.OWO_FACES if use_owo else constants.UWU_FACES
                    for key in faces.keys():
                        uwu_append = uwu_append.replace(' ' + key, ' ' + faces[key])
                        if uwued_max == -1 and uwu_append.startswith(key):
                            uwu_append = faces[key] + uwu_append[len(key):]
                    text_uwued += uwu_append

                    # Add the raw emote in.
                    text_uwued += text[colon_index:next_colon_index + 1]

                    # Update uwued_max and other vars.
                    uwued_max = next_colon_index
                    last_index = next_colon_index
                    colons_passed += 2

                # This isn't an emote.
                else:
                    colons_passed += 1
                    last_index = colon_index

            # Appends everything else that hasn't been appended yet
            uwu_append = text[uwued_max + 1:].replace('r', 'w').replace('R', 'W').replace('l', 'w').replace('L', 'W').replace('no', 'nyo').replace('NO', 'NYO').replace('nO', 'nYO').replace('No', 'Nyo')
            faces = constants.OWO_FACES if use_owo else constants.UWU_FACES
            for key in faces.keys():
                uwu_append = uwu_append.replace(' ' + key, ' ' + faces[key])
                if uwu_append.startswith(key):
                    uwu_append = faces[key] + uwu_append[len(key):]
            for key in constants.UWU_OWO_FIND_AND_REPLACE.keys():
                uwu_append = uwu_append.replace(key, constants.UWU_OWO_FIND_AND_REPLACE[key])
            text_uwued += uwu_append

            # If there isn't a face on the end, we add an uwu.
            if not any([text_uwued.endswith(fac) for fac in faces] + [text_uwued.endswith(fac + '.') for fac in faces] + [text_uwued.endswith(fac + '!') for fac in faces]):
                text_uwued += random.choice([' owo' if use_owo else ' uwu', ' >w<'])

            return text_uwued

        # If there is no emote, we just return the basics.
        replaced_text = text.replace('r', 'w').replace('R', 'W').replace('l', 'w').replace('L', 'W').replace('no', 'nyo').replace('NO', 'NYO').replace('nO', 'nYO').replace('No', 'Nyo')
        faces = constants.OWO_FACES if use_owo else constants.UWU_FACES
        for key in faces.keys():
            replaced_text = replaced_text.replace(' ' + key, ' ' + faces[key])
            if replaced_text.startswith(key):
                replaced_text = faces[key] + replaced_text[len(key):]

        # If there isn't a face on the end, we add an uwu.
        if not any([replaced_text.endswith(fac) for fac in faces] + [replaced_text.endswith(fac + '.') for fac in faces] + [replaced_text.endswith(fac + '!') for fac in faces]):
            replaced_text += random.choice([' owo' if use_owo else ' uwu', ' >w<'])

        return replaced_text

    # If an argument was provided, we uwuify it.
    if argument:
        await message.channel.send(do_uwu_replace(argument))

    # Otherwise, we attempt to do it on the second-most recent message.
    else:
        try:
            content = await util.get_secondmost_recent_message(message.channel)
            if content:
                await message.channel.send(do_uwu_replace(content))
        # If we got a little error, we pass.
        except FirstMessageInChannelError:
            pass


async def owoify(self, message, argument, is_in_guild):
    await uwuify(self, message, argument, is_in_guild, True)


async def business_only(self, message, argument, is_in_guild):
    """
    Takes a message and makes the most serious shit out of it.
    Business only.
    """

    def do_busy_replace(text):
        # Remove all double spaces.
        while '  ' in input_str:
            input_str = input_str.replace('  ', ' ')

        # Replace all emotes.
        for key in constants.BUSINESS_EMOTE_FIND_AND_REPLACE:
            text = text.replace(' ' + key + ' ', ' ' + constants.BUSINESS_EMOTE_FIND_AND_REPLACE[key] + ' ')

        return str(text)

    # If an argument was provided, we business replace it.
    if argument:
        await message.channel.send(do_busy_replace(argument))

    # Otherwise, we attempt to do it on the second-most recent message.
    else:
        try:
            content = await util.get_secondmost_recent_message(message.channel)
            if content:
                await message.channel.send(do_busy_replace(content))
        # If we got a little error, we pass.
        except FirstMessageInChannelError:
            pass


async def ship(self, message, argument, is_in_guild):
    """
    Ships 2 or more users together.
    If a user isn't tagged, it ships the author and a random user.
    If a user IS tagged, it ships them with someone random.
    """
    # Gets the user from the argument.
    try:
        partner_1 = util.get_closest_users(message, argument, is_in_guild, exclude_bots=False, limit=1)[0]
    except (UnableToFindUserError, ArgumentTooShortError):
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested ship for user ' + argument + ', invalid')
        await message.channel.send('Invalid user.')
        return
    except NoUserSpecifiedError:
        partner_1 = None

    # If an argument wasn't passed, we do BOTH the shipping ourselves.
    users_choices = []
    if not partner_1:
        try:
            # Gets valid users.
            users_choices = util.get_applicable_users(message, is_in_guild, exclude_bots=True)
            # Getting the two users.
            partner_1 = random.choice(users_choices)
            users_choices.remove(partner_1)
            partner_2 = random.choice(users_choices)
        except IndexError:
            if len(users_choices) <= 1:
                await message.channel.send('There was an error accessing userlist.')
                log.error(util.get_comm_start(message, is_in_guild) + ' requested shop, bugged userlist')
            else:
                log.debug(util.get_comm_start(message, is_in_guild) + 'Requested ship, not enough users')
                await message.channel.send('There aren\'t enough users in here to form a ship!')
            return

    else:
        try:
            # Gets valid users.
            users_choices = util.get_applicable_users(message, is_in_guild, exclude_bots=not partner_1.bot, exclude_users=[partner_1])
            # Getting the second user.
            partner_2 = random.choice(users_choices)
        except IndexError:
            log.debug(util.get_comm_start(message, is_in_guild) + 'Requested ship, not enough users')
            await message.channel.send('There aren\'t enough users in here to form a ship!')
            return

    # Log this ship
    log.debug(util.get_comm_start(message, is_in_guild) + 'Requested ship, shipped {} and {}'.format(partner_1, partner_2))

    # Gets the PFP for partner 1 and 2. Also resizes them
    partner_1_img, partner_1_filepath = util.get_profile_picture(partner_1)
    partner_1_img = partner_1_img.resize((constants.SHIP_ICON_SIZE, constants.SHIP_ICON_SIZE), Image.LANCZOS if partner_1_img.width > constants.SHIP_ICON_SIZE else Image.NEAREST)
    partner_2_img, partner_2_filepath = util.get_profile_picture(partner_2)
    partner_2_img = partner_2_img.resize((constants.SHIP_ICON_SIZE, constants.SHIP_ICON_SIZE), Image.LANCZOS if partner_2_img.width > constants.SHIP_ICON_SIZE else Image.NEAREST)

    # Gets the image for the heart (aww!)
    heart_img = Image.open(constants.SHIP_HEART_IMG)

    # Creates the ultra-wide canvas
    together_canvas = Image.new('RGBA', (constants.SHIP_ICON_SIZE * 3, constants.SHIP_ICON_SIZE))

    # Pastes the images onto the canvas in order
    together_canvas.paste(partner_1_img, (0, 0))
    together_canvas.paste(heart_img, (constants.SHIP_ICON_SIZE, 0))
    together_canvas.paste(partner_2_img, (constants.SHIP_ICON_SIZE * 2, 0))

    # Saves the canvas to disk
    current_ship_filepath = os.path.join(constants.TEMP_DIR, 'current_ship.png')
    together_canvas.save(current_ship_filepath)

    embed = discord.Embed(title=random.choice(constants.SHIP_MESSAGES).format(partner_1.nick if partner_1.nick else partner_1.name, partner_2.nick if partner_2.nick else partner_2.name), colour=constants.SHIP_EMBED_COLOR)
    file = discord.File(current_ship_filepath, filename='ship_image.png')
    embed.set_image(url='attachment://ship_image.png')

    await message.channel.send(file=file, embed=embed)

    # Cleanup -- closing Images and deleting them off disk.
    partner_1_img.close()
    partner_2_img.close()
    heart_img.close()
    together_canvas.close()
    os.remove(partner_1_filepath)
    os.remove(partner_2_filepath)
    os.remove(current_ship_filepath)


async def ultimate(self, message, argument, is_in_guild, shsl=False):
    """
    Assigns the user an ultimate talent, like in Danganronpa.
    """
    # Gets the user from the argument.
    try:
        student = util.get_closest_users(message, argument, is_in_guild, exclude_bots=False, limit=1)[0]
    except (UnableToFindUserError, ArgumentTooShortError):
        log.debug(util.get_comm_start(message, is_in_guild) + 'requested ultimate for user ' + argument + ', invalid')
        await message.channel.send('Invalid user.')
        return
    except NoUserSpecifiedError:
        student = None

    # Gets the talent.
    talent = random.choice([key for key in constants.ULTIMATE_TALENTS.keys()])
    talent_dict = constants.ULTIMATE_TALENTS[talent]

    # Gets the character.
    # character = random.choice(talent_dict['char'])
    character = 'komaeda_nagito'
    character_dict = constants.ULTIMATE_CHARACTER_ATTRIBUTES[character]
    if 'colors' not in character_dict:
        character_dict.update({'colors': {'bottom': (255, 255, 255), 'middle': (255, 255, 255), 'top': (255, 255, 255), 'name': (128, 128, 128)}})

    # Creates the title string.
    title_str = ((student.nick if student.nick else str(student.name)) + ' is ' if student else 'You are ') + 'the ' + ('SHSL' if shsl else 'Ultimate') + ' {}'.format(talent) + talent_dict['desc']
    for i in range(len(constants.ULTIMATE_PRONOUNS)):
        title_str = title_str.replace('{' + str(i) + '}', constants.ULTIMATE_PRONOUNS[i][1 if student else 0])
    title_str.replace('{14}', (student.nick if student.nick else str(student.name)) if student else (message.author.nick if message.author.nick else str(message.author.name)))

    # Creates the image layers.
    background_bottom = Image.open(constants.ULTIMATE_BACKGROUND_BOTTOM)
    background_middle = Image.open(constants.ULTIMATE_BACKGROUND_MIDDLE)
    background_top = Image.open(constants.ULTIMATE_BACKGROUND_TOP)
    student_sprite = Image.open(os.path.join(constants.ULTIMATE_CHARACTER_FOLDER, character + constants.ULTIMATE_SPRITE_FILETYPE))
    user_name = Image.new('L', (1280, 720))
    user_colorchar = Image.new('L', (1280, 720))
    user_border = Image.new('L', (1280, 720))
    talent_text = Image.new('L', (1280, 720))
    talent_blur = Image.new('L', (1280, 720))

    # Creates user name without emoji.
    student_name = (student.nick if student.nick else str(student.name)) if student else (message.author.nick if message.author.nick else str(message.author.name));
    i = 0
    while i < len(student_name):
        if ord(student_name[i]) > constants.ULTIMATE_NAME_MAX_ORD:
            student_name = student_name.strip(student_name[i])
        else:
            i += 1
    student_name = util.normalize_string(student_name, remove_double_spaces=True)

    # Creates standard user name (white).
    user_writer = ImageDraw.Draw(user_name)
    user_font = ImageFont.truetype(constants.ULTIMATE_NAME_FONT, size=100)
    user_writer.text((835 - int(user_font.getsize(student_name)[0] / 2), 0), student_name, font=user_font, fill=255)
    user_name = user_name.rotate(-12.5, center=(-8, 200), resample=Image.BILINEAR, translate=(0, 154))

    # Creates colored user letter.
    user_writer = ImageDraw.Draw(user_colorchar)
    user_writer.text((835 - int(user_font.getsize(student_name)[0] / 2), 0), student_name[0], font=user_font, fill=255)
    user_colorchar = user_colorchar.rotate(-12.5, center=(-8, 200), resample=Image.BILINEAR, translate=(0, 154))

    # Creates user border.
    user_writer = ImageDraw.Draw(user_border)
    user_writer.text((831 - int(user_font.getsize(student_name)[0] / 2), 0), student_name, font=user_font, stroke_width=5, fill=255)
    user_border = user_border.rotate(-12.5, center=(-8, 200), resample=Image.BILINEAR, translate=(0, 150))

    # Creates talent text.
    talent_writer = ImageDraw.Draw(talent_text)
    talent_font = ImageFont.truetype(constants.ULTIMATE_TALENT_FONT, size=54)
    talent_writer.text((855 - int(talent_font.getsize(('SHSL ' if shsl else 'Ultimate ') + talent)[0] / 2), 0), ('SHSL ' if shsl else 'Ultimate ') + talent, font=talent_font, fill=255)
    talent_text = talent_text.rotate(-12.5, center=(0, 205), resample=Image.BILINEAR, translate=(-40, 279))

    # Creates talent blur.
    talent_writer = ImageDraw.Draw(talent_blur)
    talent_writer.text((855 - int(talent_font.getsize(('SHSL ' if shsl else 'Ultimate ') + talent)[0] / 2), 0), ('SHSL ' if shsl else 'Ultimate ') + talent, font=talent_font, stroke_width=2, fill=255)
    talent_blur = talent_blur.rotate(-12.5, center=(0, 202), resample=Image.BILINEAR, translate=(-40, 279))
    talent_blur = talent_blur.filter(ImageFilter.GaussianBlur(10))

    # Modifying / customizing the ultimate colors to better fit the talent.
    background_bottom = ImageOps.colorize(background_bottom.convert('L'), black=(0, 0, 0), white=talent_dict['colors']['bottom'] if 'colors' in talent_dict else character_dict['colors']['bottom'])
    background_middle_2 = ImageOps.colorize(background_middle.convert('L'), black=(0, 0, 0), white=talent_dict['colors']['middle'] if 'colors' in talent_dict else character_dict['colors']['middle']).convert('RGB')
    background_top_2 = ImageOps.colorize(background_top.convert('L'), black=(0, 0, 0), white=(255, 255, 255), mid=talent_dict['colors']['top'] if 'colors' in talent_dict else character_dict['colors']['top'])
    student_sprite_black = ImageOps.colorize(student_sprite.convert('L'), black=(0, 0, 0), white=(0, 0, 0))
    user_colorchar_c = ImageOps.colorize(user_colorchar.convert('L'), black=(0, 0, 0), white=talent_dict['colors']['name'] if 'colors' in talent_dict else character_dict['colors']['name'])
    user_border_c = ImageOps.colorize(user_border.convert('L'), black=(0, 0, 0), white=(0, 0, 0))
    talent_text_c = ImageOps.colorize(talent_text.convert('L'), black=(0, 0, 0), white=(0, 0, 0))
    talent_blur_c = ImageOps.colorize(talent_blur.convert('L'), black=(255, 255, 255), white=talent_dict['colors']['name'] if 'colors' in talent_dict else character_dict['colors']['name'])

    # Merges the image layers.
    ultimate_image = background_bottom
    ultimate_image.paste(background_middle_2, (0, 0), background_middle)
    ultimate_image.paste(background_top_2, (0, 0), background_top)
    ultimate_image.paste(user_border_c, (0, 0), user_border)
    ultimate_image.paste(user_name, (0, 0), user_name)
    ultimate_image.paste(user_colorchar_c, (0, 0), user_colorchar)
    ultimate_image.paste(talent_blur_c, (0, 0), talent_blur)
    ultimate_image.paste(talent_blur_c, (-12, -4), talent_blur)
    ultimate_image.paste(talent_text_c, (0, 0), talent_text)
    ultimate_image.paste(student_sprite_black, (constants.ULTIMATE_SPRITE_X - int(student_sprite.size[0] / 2) - 75, ultimate_image.size[1] - student_sprite.size[1]), student_sprite)
    ultimate_image.paste(student_sprite, (constants.ULTIMATE_SPRITE_X - int(student_sprite.size[0] / 2), ultimate_image.size[1] - student_sprite.size[1] + 30), student_sprite)

    # Saves the image to disk
    current_ultimate_filepath = os.path.join(constants.TEMP_DIR, 'current_ultimate.png')
    ultimate_image.save(current_ultimate_filepath)

    # Creates the embed.
    embed = discord.Embed(title=title_str, colour=((221 << 16) + (115 << 8) + 215))
    file = discord.File(current_ultimate_filepath, filename='ultimate_image.png')
    embed.set_image(url='attachment://ultimate_image.png')

    await message.channel.send(file=file, embed=embed)


async def shsl(self, message, argument, is_in_guild):
    await ultimate(self, message, argument, is_in_guild, True)


async def randomyt(self, message, argument, is_in_guild):
    """
    Generates a random youtube link.
    """
    # Rolls the random chance for a rick roll...
    if random.random() < constants.YOUTUBE_RICKROLL_CHANCE:
        log.info(util.get_comm_start(message, is_in_guild) + 'requested random video, rickrolled them')
        await message.channel.send(constants.YOUTUBE_RICKROLL_URL)
        return

    # Otherwise...
    search_results = {'items': []}
    while not search_results['items']:
        # Gets random search term and searches
        random_search = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(random.choices(constants.YOUTUBE_SEARCH_LENGTHS, weights=constants.YOUTUBE_SEARCH_WEIGHTS)[0]))
        url_data = constants.YOUTUBE_SEARCH_URL.format(constants.YOUTUBE_API_KEY, constants.YOUTUBE_SEARCH_COUNT, random_search)

        # Opens url
        try:
            url_data = urllib.request.urlopen(url_data)
            data = url_data.read()

        # The only reason we would have an error is if quota has been reached. We tell the user that here.
        except urllib.error.HTTPError:
            # First, we get the time delta between now and when the quota should be reset.
            current_time = datetime.today()
            target_time = datetime.today()

            # If we are beyond the quota reset time, we add 1 to the target date.
            if current_time.hour >= constants.YOUTUBE_QUOTA_RESET_HOUR:
                target_time = target_time + timedelta(days=1)

            # Then we create a new date from the target_time.
            target_time = datetime(year=target_time.year, month=target_time.month, day=target_time.day, hour=constants.YOUTUBE_QUOTA_RESET_HOUR)

            # Get time until quota and return that.
            quota_str = util.calculate_time_passage(target_time - current_time)
            await message.channel.send('Youtube quota of 100 videos reached. Try again in {}'.format(quota_str))
            # We only put out the quota if it's the first time doing so today.
            if not self.quota_blocked_last_time:
                log.warning(util.get_comm_start(message, is_in_guild) + 'requested random video, quota reached')
                self.quota_blocked_last_time = True
            return

        # Decodes data and makes it into a dict
        encoding = url_data.info().get_content_charset('utf-8')
        search_results = json.loads(data.decode(encoding))

    # Create list of video id's
    video_ids = [video['id']['videoId'] for video in search_results['items']]

    # Pick one
    choice = random.randint(0, len(video_ids) - 1)

    # Return selected video.
    log.debug(util.get_comm_start(message, is_in_guild) + 'requested random video, returned video id ' + video_ids[choice] + ' which was result ' + str(choice) + ' in results for ' + random_search)
    await message.channel.send(constants.YOUTUBE_VIDEO_URL_FORMAT.format(video_ids[choice]))
    self.quota_blocked_last_time = False


async def randomwiki(self, message, argument, is_in_guild):
    """
    Generates a random youtube link.
    """
    # Simple call.
    wiki_page = wikipedia.page(wikipedia.random(1))

    log.debug(util.get_comm_start(message, is_in_guild) + 'requested random wikipedia page, returned {}'.format(wiki_page))
    await message.channel.send(wiki_page.url)


def hunger_games_makeimage_pfp(playerid, image, drawer, pfp_x, pfp_y, dead=False):
    """
    Draws a player's pfp at the given x and y.
    """
    # Gathers the profile picture.
    player_pfp = util.get_profile_picture(playerid, True)[0]
    player_pfp = player_pfp.resize((constants.HG_ICON_SIZE, constants.HG_ICON_SIZE), Image.LANCZOS if player_pfp.width > constants.HG_ICON_SIZE else Image.NEAREST)
    # If player dead, recolor to black and white.
    if dead:
        player_pfp = ImageOps.colorize(player_pfp.convert('L'), black=(0, 0, 0), white=util.multiply_color_tuple((255, 255, 255), constants.HG_STATUS_DEAD_PFP_DARKEN_FACTOR), mid=util.multiply_color_tuple((128, 128, 128), constants.HG_STATUS_DEAD_PFP_DARKEN_FACTOR))
    image.paste(player_pfp, (pfp_x, pfp_y))
    # Draws border around player icons.
    drawer.line([(pfp_x - 1, pfp_y - 1), (pfp_x + constants.HG_ICON_SIZE, pfp_y - 1), (pfp_x + constants.HG_ICON_SIZE, pfp_y + constants.HG_ICON_SIZE), (pfp_x - 1, pfp_y + constants.HG_ICON_SIZE), (pfp_x - 1, pfp_y - 1)], width=1, fill=0)


def hunger_games_makeimage_action_text(remaining_text, players, drawer, txt_x, txt_y, action_font):
    while remaining_text:
        # Get the index of the NEXT {n}.
        next_bracket = len(remaining_text)
        for ind in range(len(players)):
            bracket_pos = remaining_text.find('{' + str(ind) + '}')
            if not bracket_pos + 1:
                continue
            next_bracket = min(next_bracket, bracket_pos)

        # Draw the text up to the next bracket.
        drawer.text((txt_x, txt_y), remaining_text[:next_bracket], font=action_font, fill=(255, 255, 255))
        txt_x+= action_font.getsize(remaining_text[:next_bracket])[0]

        # Draw the next player name.
        if next_bracket == len(remaining_text):
            break
        ind = int(remaining_text[next_bracket + 1])
        drawer.text((txt_x, txt_y), players[ind][1], font=action_font, fill=constants.HG_ACTION_PLAYER_COLOR)
        txt_x+= action_font.getsize(players[ind][1])[0]

        # Trim remaining_text.
        remaining_text = remaining_text[next_bracket + 3:]


def hunger_games_makeimage_player_statuses(players, placement=False):
    """
    Generates a player status image.
    The players should be a 2-dimensional list with each entry as:
    1. User ID (number)
    2. User name / nick
    3. Status (int, 0 = alive, 1 = newly dead, 2 = dead)
    This can also be used to make player placement images.
    """
    # Splits all the players into their own rows.
    players_split = []
    current_split = []
    for player in players:
        if len(current_split) == constants.HG_PLAYERSTATUS_WIDTHS[len(players)]:
            players_split.append(current_split)
            current_split = []
        current_split.append(player)
    players_split.append(current_split)

    # Preps to draw.
    image_width = constants.HG_ICON_SIZE * len(players_split[0]) + constants.HG_ICON_BUFFER * (len(players_split[0]) + 1)
    image_height = constants.HG_PLAYERSTATUS_ROWHEIGHT * len(players_split) + constants.HG_ICON_BUFFER * (len(players_split) + 1)
    player_statuses = Image.new('RGB', (image_width, image_height), constants.HG_BACKGROUND_COLOR)
    player_drawer = ImageDraw.Draw(player_statuses)
    player_font = ImageFont.truetype(constants.HG_PLAYERNAME_FONT, size=constants.HG_FONT_SIZE)

    # Draws each row, one after another.
    current_y = constants.HG_ICON_BUFFER
    for split in players_split:
        current_x = int((image_width - (len(split) * constants.HG_ICON_SIZE + (len(split) - 1) * constants.HG_ICON_BUFFER)) / 2)
        for player in split:
            # Gets pfp, pastes onto image.
            hunger_games_makeimage_pfp(player[0], player_statuses, player_drawer, current_x, current_y, player[2] and not placement)

            # Writes name and status / placement.
            player_name = player[1]
            # If the name is too long, we put a ... at the end (thx alex!!!!!)
            if player_font.getsize(player_name)[0] > constants.HG_ICON_SIZE:
                while player_font.getsize(player_name + '...')[0] > constants.HG_ICON_SIZE:
                    player_name = player_name[:-1]
                player_name+= '...'
            player_drawer.text((current_x + int(constants.HG_ICON_SIZE / 2 - player_font.getsize(player_name)[0] / 2), current_y + constants.HG_ICON_SIZE + constants.HG_TEXT_BUFFER), player_name, font=player_font, fill=(255, 255, 255))
            # Placement
            if placement:
                pass
            # Status
            else:
                status = 'Alive' if not player[2] else ('Deceased' if player[2] - 1 else 'Newly Deceased')
                player_drawer.text((current_x + int(constants.HG_ICON_SIZE / 2 - player_font.getsize(status)[0] / 2), current_y + constants.HG_ICON_SIZE + constants.HG_FONT_SIZE + constants.HG_TEXT_BUFFER), status, font=player_font, fill=constants.HG_STATUS_ALIVE_COLOR if not player[2] else constants.HG_STATUS_DEAD_COLOR)

            # Adds to current_x.
            current_x+= constants.HG_ICON_SIZE + constants.HG_ICON_BUFFER

        # Adds to current_y.
        current_y+= constants.HG_PLAYERSTATUS_ROWHEIGHT + constants.HG_ICON_BUFFER

    return player_statuses


def hunger_games_makeimage_winner(players, desc=None):
    """
    Displays the winner(s).
    Like the makeimage_action method, but without all the previous and count and whatnot.
    """
    # Makes the font
    action_font = ImageFont.truetype(constants.HG_PLAYERNAME_FONT, size=constants.HG_FONT_SIZE)

    # Gets action desc width, if any.
    action_desc_width = action_font.getsize(desc)[0]

    # Gets the image width.
    # Also makes the full action text while we're at it.
    image_width = action_desc_width + constants.HG_ICON_BUFFER * 2 + constants.HG_HEADER_BORDER_BUFFER * 2 if desc else -1
    image_height = constants.HG_ACTION_ROWHEIGHT + constants.HG_ICON_BUFFER + (constants.HG_FONT_SIZE + constants.HG_HEADER_BORDER_BUFFER * 3 if desc else -1)

    # Tests for text boundaries
    # Text varies depending on how many winners there are.
    if len(players) > 1:
        full_action_text = constants.HG_TIE_EVENT[0]
        if len(players) > 2:
            for player in players[:-1]:
                full_action_text+= player[1] + constants.HG_TIE_EVENT[1]
        else:
            full_action_text+= players[0][1] + ' '
        full_action_text+= constants.HG_TIE_EVENT[2] + players[-1][1] + constants.HG_TIE_EVENT[3]
    else:
        full_action_text = constants.HG_WINNER_DEAD_EVENT if players[0][2] else constants.HG_WINNER_EVENT
        full_action_text = full_action_text.replace('{0}', players[0][1])
    text_width = action_font.getsize(full_action_text)[0]
    image_width = max(image_width, text_width + constants.HG_ICON_BUFFER * 2)
    # Tests for image boundaries
    image_width = max(image_width, constants.HG_ICON_SIZE * len(players) + constants.HG_ICON_BUFFER * (len(players) + 1))

    # Preps to draw.
    action_image = Image.new('RGB', (image_width, image_height), constants.HG_BACKGROUND_COLOR)
    player_drawer = ImageDraw.Draw(action_image)
    current_y = constants.HG_ICON_BUFFER

    # Draw the description, if any.
    if desc:
        current_x = int((image_width - action_desc_width) / 2)
        player_drawer.rectangle(
            [(current_x - constants.HG_HEADER_BORDER_BUFFER, current_y - constants.HG_HEADER_BORDER_BUFFER),
             (current_x + action_desc_width + constants.HG_HEADER_BORDER_BUFFER, current_y + constants.HG_FONT_SIZE + constants.HG_HEADER_BORDER_BUFFER)],
            constants.HG_HEADER_BACKGROUND_COLOR,
            constants.HG_HEADER_BORDER_COLOR
        )
        player_drawer.text((current_x, constants.HG_ICON_BUFFER), desc, font=action_font, fill=constants.HG_HEADER_TEXT_COLOR)
        current_y+= constants.HG_FONT_SIZE + constants.HG_HEADER_BORDER_BUFFER * 3

    # Draw the icons.
    current_x = int(image_width / 2) - int(len(players) / 2 * constants.HG_ICON_SIZE) - int((len(players) - 1) / 2 * constants.HG_ICON_BUFFER)
    # Gets each player's pfp and pastes it onto the image.
    for player in players:
        hunger_games_makeimage_pfp(player[0], action_image, player_drawer, current_x, current_y, player[2])
        current_x+= constants.HG_ICON_SIZE + constants.HG_ICON_BUFFER

    # Draws each part of the text.
    # Text varies depending on how many winners there are.
    # More than 1:
    if len(players) > 1:
        current_x = int((image_width - text_width) / 2)
        current_y += constants.HG_ICON_SIZE + constants.HG_TEXT_BUFFER
        remaining_text = [constants.HG_TIE_EVENT[0]]
        if len(players) > 2:
            for player in players[:-1]:
                remaining_text.append(player[1])
                remaining_text.append(constants.HG_TIE_EVENT[1])
            remaining_text[-1]+= constants.HG_TIE_EVENT[2]
        else:
            remaining_text.append(players[0][1] + ' ')
            remaining_text.append(constants.HG_TIE_EVENT[2])
        remaining_text.append(players[-1][1])
        remaining_text.append(constants.HG_TIE_EVENT[3])
        while remaining_text:
            # Draw the text up to the next bracket.
            player_drawer.text((current_x, current_y), remaining_text[0], font=action_font, fill=(255, 255, 255))
            current_x += action_font.getsize(remaining_text[0])[0]
            remaining_text.remove(remaining_text[0])
            if not remaining_text:
                break

            # Draw the next player name.
            player_drawer.text((current_x, current_y), remaining_text[0], font=action_font, fill=constants.HG_ACTION_PLAYER_COLOR)
            current_x += action_font.getsize(remaining_text[0])[0]
            remaining_text.remove(remaining_text[0])

    # Only 1:
    else:
        # Draws each part of the text.
        current_x = int((image_width - text_width) / 2)
        current_y += constants.HG_ICON_SIZE + constants.HG_TEXT_BUFFER
        hunger_games_makeimage_action_text(constants.HG_WINNER_DEAD_EVENT if players[0][2] else constants.HG_WINNER_EVENT, players, player_drawer, current_x, current_y, action_font)

    return action_image


def hunger_games_makeimage_action(actions, start, count=1, do_previous=False, action_desc=None):
    """
    Displays count number of actions at once.
    """
    # Makes the font
    action_font = ImageFont.truetype(constants.HG_PLAYERNAME_FONT, size=constants.HG_FONT_SIZE)

    # Gets action desc width, if any.
    action_desc_width = action_font.getsize(action_desc)[0] if action_desc else 0

    # Gets the image width.
    # Also makes the full action text while we're at it.
    image_width = action_desc_width + constants.HG_ICON_BUFFER * 2 + constants.HG_HEADER_BORDER_BUFFER * 2 if action_desc else -1
    image_height = constants.HG_ACTION_ROWHEIGHT * count + constants.HG_ICON_BUFFER + (constants.HG_FONT_SIZE + constants.HG_HEADER_BORDER_BUFFER * 3 if action_desc else -1)
    text_sizes = []

    for ind in range(start - count + 1 if do_previous else start, start + 1 if do_previous else start + count):
        if ind == len(actions):
            break
        # Tests for text boundaries
        full_action_text = actions[ind]['act']
        for ind2 in range(len(actions[ind]['players'])):
            full_action_text = full_action_text.replace('{' + str(ind2) + '}', actions[ind]['players'][ind2][1])
        # Calculates text widths and appends them to the text_sizes list.
        text_width = action_font.getsize(full_action_text)[0]
        image_width = max(image_width, text_width + constants.HG_ICON_BUFFER * 2)
        text_sizes.append(text_width)
        # Tests for image boundaries
        image_width = max(image_width, constants.HG_ICON_SIZE * len(actions[ind]['players']) + constants.HG_ICON_BUFFER * (len(actions[ind]['players']) + 1))

    # Preps to draw.
    action_image = Image.new('RGB', (image_width, image_height), constants.HG_BACKGROUND_COLOR)
    player_drawer = ImageDraw.Draw(action_image)
    current_y = constants.HG_ICON_BUFFER

    # Draw the description, if any.
    if action_desc:
        current_x = int((image_width - action_desc_width) / 2)
        player_drawer.rectangle(
            [(current_x - constants.HG_HEADER_BORDER_BUFFER, current_y - constants.HG_HEADER_BORDER_BUFFER),
             (current_x + action_desc_width + constants.HG_HEADER_BORDER_BUFFER, current_y + constants.HG_FONT_SIZE + constants.HG_HEADER_BORDER_BUFFER)],
            constants.HG_HEADER_BACKGROUND_COLOR,
            constants.HG_HEADER_BORDER_COLOR
        )
        player_drawer.text((current_x, constants.HG_ICON_BUFFER), action_desc, font=action_font, fill=constants.HG_HEADER_TEXT_COLOR)
        current_y+= constants.HG_FONT_SIZE + constants.HG_HEADER_BORDER_BUFFER * 3

    # Draw the icons.
    num = 0
    for ind in range(start - count + 1 if do_previous else start, start + 1 if do_previous else start + count):
        current_x = int(image_width / 2) - int(len(actions[ind]['players']) / 2 * constants.HG_ICON_SIZE) - int((len(actions[ind]['players']) - 1) / 2 * constants.HG_ICON_BUFFER)
        # Gets each player's pfp and pastes it onto the image.
        for player in actions[ind]['players']:
            hunger_games_makeimage_pfp(player[0], action_image, player_drawer, current_x, current_y)
            current_x+= constants.HG_ICON_SIZE + constants.HG_ICON_BUFFER

        # Draws each part of the text.
        current_x = int((image_width - text_sizes[num]) / 2)
        current_y+= constants.HG_ICON_SIZE + constants.HG_TEXT_BUFFER
        hunger_games_makeimage_action_text(actions[ind]['act'], actions[ind]['players'], player_drawer, current_x, current_y, action_font)

        # Adds to the current_y and num.
        current_y+= constants.HG_FONT_SIZE + constants.HG_ICON_BUFFER
        num+= 1

    return action_image


def hunger_games_generate_statuses(hg_statuses, action):
    """
    Updates the statuses of players post-action in the hg_dict.
    """
    # First, we handle deaths.
    if 'kill' in action['full']:
        for ind in action['full']['kill']:
            hg_statuses[action['players'][ind][0]]['dead'] = True
        for ind in action['full']['kill']:
            hg_statuses[action['players'][ind][0]]['dead_num'] = [hg_statuses[player]['dead'] for player in hg_statuses].count(True) - 1

    # Next, injuries.
    if 'hurt' in action['full']:
        for ind in action['full']['hurt']:
            hg_statuses[action['players'][ind][0]]['hurt'] = True

    # Healing.
    if 'heal' in action['full']:
        for ind in action['full']['heal']:
            hg_statuses[action['players'][ind][0]]['hurt'] = False

    # Items.
    if 'give' in action:
        for ind in range(len(action['give'])):
            # Item 0.
            if action['give'][ind] == 0:
                continue
            elif action['give'][ind] < 0:
                hg_statuses[action['players'][ind][0]]['inv'].remove(-action['give'][ind])
            else:
                # Special items
                # 3000, 1 - 3 random items
                if action['full']['give'][ind] == 3000:
                    for i in range(random.randint(1, 3)):
                        hg_statuses[action['players'][ind][0]]['inv'].append(random.choice(constants.HG_ALL_ITEMS))
                elif action['full']['give'][ind] == 4000:
                    hg_statuses[action['players'][ind][0]]['inv'].append(random.choice(constants.HG_WEAPON_ITEMS))
                    hg_statuses[action['players'][ind][0]]['inv'].append(random.choice(constants.HG_HEALTH_ITEMS))
                    hg_statuses[action['players'][ind][0]]['inv'].append(random.choice(constants.HG_FOOD_ITEMS))
                elif action['full']['give'][ind] == 8888:
                    hg_statuses[action['players'][ind][0]]['inv'].remove(8)
                    hg_statuses[action['players'][ind][0]]['inv'].append(10)
                    hg_statuses[action['players'][ind][0]]['inv'].append(104)
                elif action['full']['give'][ind] == 9999:
                    ind2 = 0
                    for item in hg_statuses[action['players'][ind][0]]['inv']:
                        hg_statuses[action['players'][ind][0]]['inv'].remove(item)
                        if ind2 % len(action['players']) == ind:
                            ind2+= 1
                        hg_statuses[action['players'][ind2][0]]['inv'].append(item)
                        ind2+= 1
                else:
                    hg_statuses[action['players'][ind][0]]['inv'].append(action['give'][ind])

    del action['full']

def hunger_games_generate_bloodbath(hg_dict):
    """
    Generates all the actions for each player in the bloodbath.
    """
    player_actions = [uid for uid in hg_dict['statuses']]
    actions = []

    # Iterates through all the actions, picking them at random for the player_actions.
    while player_actions:
        # Creates necessary prerequisites for do while loop.
        curr_action = {'players': len(player_actions)}
        chosen_players = [random.choice(player_actions)]
        player_actions.remove(chosen_players[0])

        # While loop, finds a good action.
        while curr_action['players'] > len(player_actions):
            curr_action = random.choice(constants.HG_BLOODBATH_ACTIONS)

        # Adds more players to current action.
        for i in range(curr_action['players']):
            chosen_players.append(random.choice(player_actions))
            player_actions.remove(chosen_players[-1])

        # Add the actions to the list.
        actions.append({'players': [(player, hg_dict['statuses'][player]['name']) for player in chosen_players], 'act': curr_action['act'], 'full': curr_action})

        # Generate statuses
        hunger_games_generate_statuses(hg_dict['statuses'], actions[-1])

    # Adds to the phases.
    hg_dict['phases'].append({'type': 'act', 'act': actions, 'title': 'The Bloodbath', 'next': 1, 'prev': -1, 'desc': 'As the tributes stand upon their podiums, the horn sounds.', 'done': False})


def hunger_games_generate_normal_actions(hg_dict, action_dict, title, desc=None):
    """
    Generates all the actions for each player in the a normal action round.
    """
    player_actions = []
    for uid in hg_dict['statuses']:
        if not hg_dict['statuses'][uid]['dead']:
            player_actions.append(uid)
    actions = []

    # Iterates through triggers.
    for trigger in action_dict['trigger']:
        pass

    # Iterates through all the actions, picking them at random for the player_actions.
    while player_actions:
        # Creates necessary prerequisites for do while loop.
        curr_action = {'players': len(player_actions)}
        chosen_players = [random.choice(player_actions)]
        player_actions.remove(chosen_players[0])

        # While loop, finds a good action.
        while curr_action['players'] > len(player_actions):
            curr_action = random.choice(action_dict['normal'])

        # Adds more players to current action.
        for i in range(curr_action['players']):
            chosen_players.append(random.choice(player_actions))
            player_actions.remove(chosen_players[-1])

        # Add the actions to the list.
        actions.append({'players': [(player, hg_dict['statuses'][player]['name']) for player in chosen_players], 'act': curr_action['act'], 'full': curr_action})

    # Shuffles the actions and generates statuses.
    random.shuffle(actions)
    for curr_action in actions:
        hunger_games_generate_statuses(hg_dict['statuses'], curr_action)

    # Adds to the phases.
    if not desc:
        desc = title
    hg_dict['phases'].append({'type': 'act', 'act': actions, 'title': title, 'next': 0, 'prev': -1, 'desc': desc, 'done': False})


def hunger_games_generate_detect_dead(hg_dict):
    """
    Test for dead people.
    """
    everyone_dead = True
    two_alive = False
    for player in hg_dict['statuses']:
        if not hg_dict['statuses'][player]['dead']:
            if not everyone_dead:
                two_alive = True
                break
            else:
                everyone_dead = False
    return everyone_dead, two_alive


async def hunger_games_generate_full_game(hg_dict, message):
    """
    Generates an entire Hunger Games from the users specified in the hg_dict.
    Depends on external methods to do most of the dirty work.
    """
    # Get rid of redundant tag.
    del hg_dict['uses_bots']

    # Create player statuses.
    statuses = {}
    for player in hg_dict['players']:
        statuses[str(player.id)] = {'name': player.nick if player.nick else player.name, 'dead': False, 'hurt': False, 'inv': []}
    hg_dict['statuses'] = statuses

    # Makes the phases.
    hg_dict['phases'] = []

    # First, we have the bloodbath.
    hunger_games_generate_bloodbath(hg_dict)

    # Loop variables.
    daynight = 1
    turns_since_event = 0
    dead_last_loop = []

    # Then we cycle through stuff until one person survives or EVERYONE is dead.
    while True:
        # Test for dead people.
        tie, continue_game = hunger_games_generate_detect_dead(hg_dict)
        if not continue_game:
            break

        # Test for event.
        if daynight >= 4 and turns_since_event > 1 and random.random() < 1 - (1 - constants.HG_EVENT_DEFAULT_CHANCE)**turns_since_event:
            the_event = random.choice(constants.HG_EVENTS)
            hunger_games_generate_normal_actions(hg_dict, the_event[0], the_event[1], the_event[2])
            turns_since_event = 0

        # Otherwise, do day and night.
        else:
            # Day.
            hunger_games_generate_normal_actions(hg_dict, constants.HG_NORMAL_DAY_ACTIONS, 'Day {}'.format(daynight))

            # Test for dead people.
            tie, continue_game = hunger_games_generate_detect_dead(hg_dict)
            if not continue_game:
                break

            # Night.
            hunger_games_generate_normal_actions(hg_dict, constants.HG_NORMAL_NIGHT_ACTIONS, 'Night {}'.format(daynight))
            daynight+= 1

            if daynight >= 4:
                turns_since_event += 1

        # Test for dead people.
        tie, continue_game = hunger_games_generate_detect_dead(hg_dict)
        if not continue_game:
            break

        # Do player statuses.
        player_statuses = []
        new_deaths = 0
        for player in hg_dict['statuses']:
            player_statuses.append((player, hg_dict['statuses'][player]['name'], (2 if player in dead_last_loop else 1) if hg_dict['statuses'][player]['dead'] else 0))
            if player not in dead_last_loop and hg_dict['statuses'][player]['dead']:
                dead_last_loop.append(player)
                new_deaths+= 1
        hg_dict['phases'].append({'type': 'status', 'all': player_statuses, 'new': new_deaths})

        # Increase chances of encountering disaster next time.
        if daynight >= 4:
            turns_since_event+= 1

    # Now that the loop is broken, display cannon shots and declare winner.
    player_statuses = []
    new_deaths = 0
    for player in hg_dict['statuses']:
        player_statuses.append((player, hg_dict['statuses'][player]['name'], (2 if player in dead_last_loop else 1) if hg_dict['statuses'][player]['dead'] else 0))
        if player not in dead_last_loop and hg_dict['statuses'][player]['dead']:
            dead_last_loop.append(player)
            new_deaths+= 1
    hg_dict['phases'].append({'type': 'status', 'all': player_statuses, 'new': new_deaths})

    if tie:
        # Determine who tied
        tiees = []
        max_deathnum = -1
        for player in hg_dict['statuses']:
            if hg_dict['statuses'][player]['dead_num'] > max_deathnum:
                max_deathnum = hg_dict['statuses'][player]['dead_num']
        for player in hg_dict['statuses']:
            if max_deathnum == hg_dict['statuses'][player]['dead_num']:
                tiees.append(player)
        # Add tie phase to phases ONLY if there's more than one.
        if len(tiees) > 1:
            hg_dict['phases'].append({'type': 'tie', 'players': [(tienum, hg_dict['statuses'][tienum]['name'], True) for tienum in tiees], 'title': constants.HG_TIE_TITLE, 'desc': constants.HG_TIE_TITLE})
        # Otherwise, it's a victory, but dead.
        else:
            hg_dict['phases'].append({'type': 'win', 'players': [(tiees[0], hg_dict['statuses'][tiees[0]]['name'], True)], 'title': constants.HG_WINNER_TITLE, 'desc': constants.HG_WINNER_TITLE})

    else:
        # Determine winner
        winner = None
        for player in hg_dict['statuses']:
            if not 'dead_num' in hg_dict['statuses'][player]:
                winner = player
                break
        # Add win phase to phases
        hg_dict['phases'].append({'type': 'win', 'players': [(winner, hg_dict['statuses'][winner]['name'], False)], 'title': constants.HG_WINNER_TITLE, 'desc': constants.HG_WINNER_TITLE})

    # Makes the placement screen
    pre_placement_players = [k for k in hg_dict['statuses']]
    placements = []
    while pre_placement_players:
        min_placement = len(hg_dict['statuses'])
        current_placement_players = []
        for player in pre_placement_players:
            if 'dead_num' in hg_dict['statuses'][player]:
                if min_placement > hg_dict['statuses'][player]['dead_num']:
                    current_placement_players = [player]
                    min_placement = hg_dict['statuses'][player]['dead_num']
                elif min_placement == hg_dict['statuses'][player]['dead_num']:
                    current_placement_players.append(player)
        # If there is no change in min_placement, then the victor is found.
        if min_placement == len(hg_dict['statuses']):
            current_placement_players = pre_placement_players
            min_placement-= 1
        # Adds player to the dict.
        for player in current_placement_players:
            placements.append((player, hg_dict['statuses'][player]['name'], len(hg_dict['statuses']) - min_placement))
            pre_placement_players.remove(player)
    # Reverses placements list to sort from first to last and makes it a phase
    placements.reverse()
    hg_dict['phases'].append({'type': 'place', 'all': placements})

    # Sends the first message.
    # Creates the embed.
    embed = discord.Embed(title='The Bloodbath, Action 1', colour=constants.HG_EMBED_COLOR)
    embed.set_footer(text=constants.HG_BEGINNING_DESCRIPTION)

    action_image = hunger_games_makeimage_action(hg_dict['phases'][0]['act'], 0, 1, False, hg_dict['phases'][0]['desc'])
    current_playerstatus_filepath = os.path.join(constants.TEMP_DIR, 'hg_player_statuses.png')
    action_image.save(current_playerstatus_filepath)
    file = discord.File(current_playerstatus_filepath, filename='hg_player_statuses.png')

    # Sends image, logs.
    embed.set_image(url='attachment://hg_player_statuses.png')
    await message.channel.send(file=file, embed=embed)

    # Updates hunger games dict.
    del hg_dict['statuses']
    hg_dict['current_phase'] = 0
    hg_dict['confirm_cancel'] = False
    hg_dict['generated'] = True


def hunger_games_set_embed_image(image, embed):
    current_image_filepath = os.path.join(constants.TEMP_DIR, constants.HG_IMAGE_PATH)
    image.save(current_image_filepath)
    file = discord.File(current_image_filepath, filename='hg_image_filepath.png')
    embed.set_image(url='attachment://hg_image_filepath.png')
    return file


async def hunger_games_send_pregame(message, players, title, uses_bots):
    """
    Sends the pregame roster thing.
    """
    # Makes sure all the player icons are downloaded.
    for user in players:
        image_locale = os.path.join(constants.TEMP_DIR, str(user.id) + constants.PFP_FILETYPE)
        if not os.path.isfile(image_locale):
            image_bytes = requests.get(user.avatar_url).content
            # Writes image to disk
            with open(image_locale, 'wb') as w:
                w.write(image_bytes)

    # Creates embed.
    embed = discord.Embed(title=title, colour=constants.HG_EMBED_COLOR)
    embed.set_footer(text=constants.HG_PREGAME_DESCRIPTION.format('Disallow' if uses_bots else 'Allow'))

    # Has image created, sets image on embed.
    player_statuses = hunger_games_makeimage_player_statuses([(player.id, player.nick if player.nick else player.name, 0) for player in players])
    file = hunger_games_set_embed_image(player_statuses, embed)

    # Sends image, logs.
    await message.channel.send(file=file, embed=embed)


async def hunger_games_send_midgame(message, is_in_guild, hg_dict, count=1, do_previous=False):
    """
    Sends all midgame embeds, regardless of type.
    """
    current_phase = hg_dict['phases'][hg_dict['current_phase']]

    # Brings us to a different phase if we're at the end or beginning of one.
    if current_phase['type'] == 'act':
        if do_previous and current_phase['prev'] < 0:
            current_phase['next'] = 0
            hg_dict['current_phase']-= 1
            current_phase = hg_dict['phases'][hg_dict['current_phase']]
        elif not do_previous and current_phase['next'] >= len(current_phase['act']):
            current_phase['prev'] = len(current_phase['act']) - 1
            current_phase['done'] = True
            hg_dict['current_phase']+= 1
            current_phase = hg_dict['phases'][hg_dict['current_phase']]
    else:
        if do_previous:
            hg_dict['current_phase']-= 1
            current_phase = hg_dict['phases'][hg_dict['current_phase']]
        else:
            hg_dict['current_phase']+= 1
            current_phase = hg_dict['phases'][hg_dict['current_phase']]

    # Creates embed for act pages.
    if current_phase['type'] == 'act':
        action_nums = ((current_phase['prev'] - count + 1 if do_previous else current_phase['next']) + 1, (current_phase['prev'] + 1 if do_previous else current_phase['next'] + count))
        embed = discord.Embed(title=current_phase['title'] + (', Action {}'.format(action_nums[0]) if action_nums[1] == action_nums[0] else ', Actions {} - {}'.format(action_nums[0], action_nums[1])) + (' / ' + str(len(current_phase['act'])) if current_phase['done'] else ''), colour=constants.HG_EMBED_COLOR)
        player_actions = hunger_games_makeimage_action(current_phase['act'], current_phase['prev'] if do_previous else current_phase['next'], count, do_previous, current_phase['desc'] if ((current_phase['prev'] if do_previous else current_phase['next']) - count + 1 if do_previous else (current_phase['prev'] if do_previous else current_phase['next'])) == 0 else None)
        file = hunger_games_set_embed_image(player_actions, embed)
    # Creates embed for win AND tie pages.
    elif current_phase['type'] in ['win', 'tie']:
        embed = discord.Embed(title=current_phase['title'], colour=constants.HG_EMBED_COLOR)
        player_actions = hunger_games_makeimage_winner(current_phase['players'], current_phase['desc'])
        file = hunger_games_set_embed_image(player_actions, embed)
    # Creates embed for status pages.
    elif current_phase['type'] == 'status':
        embed = discord.Embed(title='{} cannon shot{} can be heard in the distance.'.format(current_phase['new'], '' if current_phase['new'] == 1 else 's'), colour=constants.HG_EMBED_COLOR)
        player_statuses = hunger_games_makeimage_player_statuses(current_phase['all'])
        file = hunger_games_set_embed_image(player_statuses, embed)
    # Creates embed for placement pages.
    elif current_phase['type'] == 'place':
        embed = discord.Embed(title='Placements', colour=constants.HG_EMBED_COLOR)
        player_statuses = hunger_games_makeimage_player_statuses(current_phase['all'], placement=True)
        file = hunger_games_set_embed_image(player_statuses, embed)
    # Creates embed for other pages.
    else:
        log.error(util.get_comm_start(message, is_in_guild) + ' invalid hunger games phase type {}'.format(current_phase['type']))

    # Sets footer, sends image, logs.
    if hg_dict['current_phase'] == 0 and hg_dict['phases'][hg_dict['current_phase']]['prev'] == -1:
        embed.set_footer(text=constants.HG_BEGINNING_DESCRIPTION)
    else:
        embed.set_footer(text=constants.HG_MIDGAME_DESCRIPTION)
    await message.channel.send(file=file, embed=embed)

    # Increments next and prev in the action for acts.
    if current_phase['type'] == 'act':
        if do_previous:
            current_phase['prev'] = max(-1, current_phase['prev'] - count)
            current_phase['next'] = current_phase['prev'] + 2
        else:
            current_phase['next'] = min(len(current_phase['act']), current_phase['next'] + count)
            current_phase['prev'] = current_phase['next'] - 2


async def hunger_games_pregame_shuffle(self, message, is_in_guild, player_count, uses_bots):
    """
    Shuffles a pregame hunger games cast.
    """
    # Get the user list.
    user_list = util.get_applicable_users(message, is_in_guild, not uses_bots)
    if len(user_list) < constants.HG_MIN_GAMESIZE:
        self.curr_hg.pop(str(message.channel.id))
        await message.channel.send('Not enough users in server.')
        log.debug(util.get_comm_start(message, is_in_guild) + ' requested hunger games, not enough people')

    # Otherwise, we generate the players and ask if we should proceed.
    else:
        # Get the players.
        hg_players = []
        for i in range(min(player_count, len(user_list))):
            next_player = random.choice(user_list)
            hg_players.append(next_player)
            user_list.remove(next_player)

        # Set in players and actions.
        hg_full_game = {'players': hg_players, 'past_pregame': False, 'uses_bots': uses_bots}
        self.curr_hg[str(message.channel.id)] = hg_full_game

        # Send the updated cast
        await hunger_games_send_pregame(message, hg_players, constants.HG_PREGAME_TITLE, uses_bots)
        log.debug(util.get_comm_start(message, is_in_guild) + 'shuffled Hunger Games instance with {} players'.format(player_count))


async def hunger_games_update(self, message, is_in_guild):
    """
    Updates a hunger games dict.
    """
    hg_dict = self.curr_hg[str(message.channel.id)]
    response = message.content.lower()

    # If the game is already generated.
    if hg_dict['past_pregame']:
        if hg_dict['generated']:
            # Next command (custom size).
            if any([response.startswith(pre) for pre in ['n ', 'next ']]):
                pass

            # Next command.
            elif any([response == 'n', 'response' == 'next']):
                await hunger_games_send_midgame(message, is_in_guild, hg_dict)
                hg_dict['updated'] = datetime.today()
                return True

            # Previous command (custom size).
            elif any([response.startswith(pre) for pre in ['p ', 'prev ', 'previous']]):
                if hg_dict['current_phase'] == 0 and hg_dict['phases'][hg_dict['current_phase']]['prev'] == -1:
                    return
                else:
                    hg_dict['updated'] = datetime.today()
                    return True

            # Previous command.
            elif any([response == 'p', response == 'prev', response == 'previous']):
                if hg_dict['current_phase'] == 0 and hg_dict['phases'][hg_dict['current_phase']]['prev'] == -1:
                    return
                else:
                    await hunger_games_send_midgame(message, is_in_guild, hg_dict, do_previous=True)
                    hg_dict['updated'] = datetime.today()
                    return True

        # If the game isn't generated yet.
        elif any([response.startswith(pre) for pre in ['j!hg ', 'j!hunger ', 'j!hungergames ', 'j!hungry ']] + [response == 'j!hg', response == 'j!hunger', response == 'j!hungergames', response == 'j!hungry']):
            await message.channel.send('Still generating, be patient.')
            hg_dict['updated'] = datetime.today()
            return True

    # The game is not yet generated.
    else:
        # Shuffle command (but of a different size).
        if any([response.startswith(pre) for pre in ['j!hg ', 'j!hunger ', 'j!hungergames ', 'j!hungry ', 's ', 'shuffle ']]):
            try:
                player_count = int(response.split(' ')[1])
                if player_count > constants.HG_MAX_GAMESIZE:
                    player_count = constants.HG_MAX_GAMESIZE
                elif player_count < constants.HG_MIN_GAMESIZE:
                    player_count = constants.HG_MIN_GAMESIZE
            except ValueError:
                player_count = len(hg_dict['players'])
            await hunger_games_pregame_shuffle(self, message, is_in_guild, player_count, uses_bots=hg_dict['uses_bots'])
            hg_dict['updated'] = datetime.today()
            return True

        # Shuffle command.
        elif any([response == 's', response == 'shuffle', response == 'j!hg', response == 'j!hunger', response == 'j!hungergames', response == 'j!hungry']):
            await hunger_games_pregame_shuffle(self, message, is_in_guild, len(hg_dict['players']), uses_bots=hg_dict['uses_bots'])
            hg_dict['updated'] = datetime.today()
            return True

        # Replace command (improper use).
        elif any([response == 'r', response == 'replace']):
            await message.channel.send('Mention two users to replace one with the other.')
            hg_dict['updated'] = datetime.today()
            return True

        elif any([response.startswith('r '), response.startswith('replace ')]):
            # Gets the first two users in the thing.
            try:
                modified_players = util.get_closest_users(message, response[2:] if response.startswith('r ') else response[8:], is_in_guild, not hg_dict['uses_bots'], limit=2)
            except (NoUserSpecifiedError, ArgumentTooShortError, UnableToFindUserError):
                await message.channel.send('Invalid user(s).')
                log.debug(util.get_comm_start(message, is_in_guild) + 'attempted to add a player to Hunger Games instance, invalid')
                hg_dict['updated'] = datetime.today()
                return True
            # Conditional
            if modified_players[0] in hg_dict['players']:
                # Both players are in the game
                if modified_players[1] in hg_dict['players']:
                    await message.channel.send('{} is already in the game.'.format(modified_players[1]))
                    log.debug(util.get_comm_start(message, is_in_guild) + 'tried to replace a player in Hunger Games instance, second already there')
                # First player in game, second not
                else:
                    hg_dict['players'].insert(hg_dict['players'].index(modified_players[0]), modified_players[1])
                    hg_dict['players'].remove(modified_players[0])
                    await hunger_games_send_pregame(message, hg_dict['players'], 'Replaced {} with {}.'.format(modified_players[0].nick if modified_players[0].nick else modified_players[0].name, modified_players[1].nick if modified_players[1].nick else modified_players[1].name), hg_dict['uses_bots'])
                    log.debug(util.get_comm_start(message, is_in_guild) + 'replaced a player in Hunger Games instance')
            else:
                # First player not in game
                await message.channel.send('{} isn\'t in the game.'.format(modified_players[0]))
                log.debug(util.get_comm_start(message, is_in_guild) + 'tried to replace a player in Hunger Games instance, first isn\'t there')
            hg_dict['updated'] = datetime.today()
            return True

        # Add command.
        elif any([response == 'a', response == 'add']):
            # Cancels if the game is already max size.
            if len(hg_dict['players']) == constants.HG_MAX_GAMESIZE:
                await message.channel.send('Max size already reached.')
                log.debug(util.get_comm_start(message, is_in_guild) + 'tried to add player to Hunger Games instance, max size reached')
            else:
                # Cancels if no more members to add to game.
                able_users = util.get_applicable_users(message, is_in_guild, hg_dict['uses_bots'], hg_dict['players'])
                if not able_users:
                    await message.channel.send('No more users not already in the game.')
                    log.debug(util.get_comm_start(message, is_in_guild) + 'tried to add player to Hunger Games instance, no more users')
                # Otherwise, goes on.
                else:
                    added_player = random.choice(able_users)
                    hg_dict['players'].append(added_player)
                    await hunger_games_send_pregame(message, hg_dict['players'], 'Added {} to the game.'.format(added_player.nick if added_player.nick else added_player.name), hg_dict['uses_bots'])
                    log.debug(util.get_comm_start(message, is_in_guild) + 'added a player to Hunger Games instance')
            hg_dict['updated'] = datetime.today()
            return True

        # Add command, but specific user
        elif any([response.startswith('a '), response.startswith('add ')]):
            # Cancels if the game is already max size.
            if len(hg_dict['players']) == constants.HG_MAX_GAMESIZE:
                await message.channel.send('Max size already reached.')
                log.debug(util.get_comm_start(message, is_in_guild) + 'tried to add player to Hunger Games instance, max size reached')
            else:
                # Attempts to add a player.
                try:
                    added_player = util.get_closest_users(message, response[2:] if response.startswith('a ') else response[4:], is_in_guild, not hg_dict['uses_bots'], limit=1)[0]
                except (NoUserSpecifiedError, ArgumentTooShortError, UnableToFindUserError):
                    await message.channel.send('Invalid user.')
                    log.debug(util.get_comm_start(message, is_in_guild) + 'attempted to add a player to Hunger Games instance, invalid')
                    hg_dict['updated'] = datetime.today()
                    return True
                if added_player in hg_dict['players']:
                    await message.channel.send('{} is already in the game.'.format(added_player))
                    log.debug(util.get_comm_start(message, is_in_guild) + 'attempted to add a player to Hunger Games instance, already there')
                else:
                    hg_dict['players'].append(added_player)
                    await hunger_games_send_pregame(message, hg_dict['players'], 'Added {} to the game.'.format(added_player.nick if added_player.nick else added_player.name), hg_dict['uses_bots'])
                    log.debug(util.get_comm_start(message, is_in_guild) + 'added a player to Hunger Games instance')
            hg_dict['updated'] = datetime.today()
            return True

        # Delete command.
        elif any([response == 'd', response == 'del', response == 'delete']):
            # Cancels if the game is already min size.
            if len(hg_dict['players']) == constants.HG_MIN_GAMESIZE:
                await message.channel.send('Min size already reached.')
                log.debug(util.get_comm_start(message, is_in_guild) + 'tried to remove player to Hunger Games instance, min size reached')
            else:
                # Removes player on the end.
                removed_player = hg_dict['players'].pop(-1)
                await hunger_games_send_pregame(message, hg_dict['players'], 'Removed {} from the game.'.format(removed_player.nick if removed_player.nick else removed_player.name), hg_dict['uses_bots'])
                log.debug(util.get_comm_start(message, is_in_guild) + 'removed player from Hunger Games instance')
            hg_dict['updated'] = datetime.today()
            return True

        # Delete command, but specific user
        elif any([response.startswith('d '), response.startswith('del '), response.startswith('delete ')]):
            # Cancels if the game is already min size.
            if len(hg_dict['players']) == constants.HG_MIN_GAMESIZE:
                await message.channel.send('Min size already reached.')
                log.debug(util.get_comm_start(message, is_in_guild) + 'tried to remove player to Hunger Games instance, min size reached')
            else:
                # Attempts to find player.
                try:
                    removed_player = util.get_closest_users(message, response[2:] if response.startswith('d ') else (response[4:] if response.starswith('del ') else response[7:]), is_in_guild, not hg_dict['uses_bots'], limit=1)[0]
                except (NoUserSpecifiedError, ArgumentTooShortError, UnableToFindUserError):
                    await message.channel.send('Invalid user.')
                    log.debug(util.get_comm_start(message, is_in_guild) + 'attempted to remove a player from Hunger Games instance, invalid')
                    hg_dict['updated'] = datetime.today()
                    return True
                if removed_player in hg_dict['players']:
                    hg_dict['players'].remove(removed_player)
                    await hunger_games_send_pregame(message, hg_dict['players'], 'Removed {} from the game.'.format(removed_player.nick if removed_player.nick else removed_player.name), hg_dict['uses_bots'])
                    log.debug(util.get_comm_start(message, is_in_guild) + 'removed a player from Hunger Games instance')
                else:
                    await message.channel.send('{} isn\'t in the game.'.format(removed_player))
                    log.debug(util.get_comm_start(message, is_in_guild) + 'attempted to remove a player from Hunger Games instance, not there')
            hg_dict['updated'] = datetime.today()
            return True

        # Allow / disallow bots command.
        elif any([response == 'b', response == 'disallow bots', response == 'allow bots', response == 'allow', response == 'disallow']):
            if hg_dict['uses_bots']:
                # Cancels if not enough non-bots
                hg_players_no_bots = hg_dict['players'].copy()
                while any([player.bot for player in hg_players_no_bots]):
                    for player in hg_players_no_bots:
                        if player.bot:
                            hg_players_no_bots.remove(player)
                while len(hg_players_no_bots) < constants.HG_MIN_GAMESIZE:
                    other_players = util.get_applicable_users(message, is_in_guild, True, hg_players_no_bots)
                    if other_players:
                        hg_players_no_bots.append(random.choice(other_players))
                    else:
                        await message.channel.send('Not enough non-bots to disallow bots.')
                        log.debug(util.get_comm_start(message, is_in_guild) + 'attempted to remove bots from Hunger Games instance, not enough users')
                        hg_dict['updated'] = datetime.today()
                        return True
                # Allows it.
                hg_dict['uses_bots'] = False
                hg_dict['players'] = hg_players_no_bots
                await hunger_games_send_pregame(message, hg_dict['players'], 'Removed bots from the game.', hg_dict['uses_bots'])
                log.debug(util.get_comm_start(message, is_in_guild) + 'removed bots from Hunger Games instance')
            else:
                hg_dict['uses_bots'] = True
                await hunger_games_send_pregame(message, hg_dict['players'], 'Allowed bots into the game.', hg_dict['uses_bots'])
                log.debug(util.get_comm_start(message, is_in_guild) + 'added bots to Hunger Games instance')
            hg_dict['updated'] = datetime.today()
            return True

        # Proceed command.
        elif any([response == 'p', response == 'proceed']):
            await message.channel.send('Generating Hunger Games instance...')
            log.debug(util.get_comm_start(message, is_in_guild) + 'initiated Hunger Games')
            hg_dict['past_pregame'] = True
            hg_dict['generated'] = False
            await hunger_games_generate_full_game(hg_dict, message)
            hg_dict['updated'] = datetime.today()
            return True

        # Cancel command.
        elif any([response == 'c', response == 'cancel']):
            await message.channel.send('Hunger Games canceled.')
            log.debug(util.get_comm_start(message, is_in_guild) + 'canceled Hunger Games')
            del self.curr_hg[str(message.channel.id)]
            hg_dict['updated'] = datetime.today()
            return True


async def hunger_games_start(self, message, argument, is_in_guild):
    """
    Creates a hunger games simulator right inside the bot.
    """
    hg_key = str(message.channel.id)

    # If a game is already in progress, we forward this message.
    if hg_key in self.curr_hg.keys():
        await hunger_games_update(self, message, is_in_guild)

    else:
        # Gets argument for how many users to start hg with.
        if argument:
            try:
                player_count = int(argument)
                if player_count > constants.HG_MAX_GAMESIZE:
                    player_count = constants.HG_MAX_GAMESIZE
                elif player_count < constants.HG_MIN_GAMESIZE:
                    player_count = constants.HG_MIN_GAMESIZE
            except ValueError:
                player_count = 24
        else:
            player_count = 24

        # Get the user list. If user list is < player_count people, we add bots as well.
        user_list = util.get_applicable_users(message, is_in_guild, True)
        uses_bots = False
        if len(user_list) < player_count:
            user_list = util.get_applicable_users(message, is_in_guild, False)
            uses_bots = True
        # If there still aren't enough users, we send error.
        if len(user_list) < constants.HG_MIN_GAMESIZE:
            if len(user_list) == 1:
                await message.channel.send('There was an error accessing userlist.')
                log.error(util.get_comm_start(message, is_in_guild) + ' requested hunger games, bugged userlist')
            else:
                await message.channel.send('Not enough users in server.')
                log.debug(util.get_comm_start(message, is_in_guild) + ' requested hunger games, not enough people')

        # Otherwise, we generate the players and ask if we should proceed.
        else:
            # Get the players.
            hg_players = []
            for i in range(min(player_count, len(user_list))):
                next_player = random.choice(user_list)
                hg_players.append(next_player)
                user_list.remove(next_player)

            # Set in players and actions.
            hg_full_game = {'players': hg_players, 'past_pregame': False, 'uses_bots': uses_bots, 'updated': datetime.today()}
            self.curr_hg.update({hg_key: hg_full_game})

            # Send the initial cast
            await hunger_games_send_pregame(message, hg_players, constants.HG_PREGAME_TITLE, uses_bots)
            log.debug(util.get_comm_start(message, is_in_guild) + 'started Hunger Games instance with {} players'.format(len(hg_players)))

async def thank_you(self, message, argument, is_in_guild):
    """
    Thanks the bot!
    :D
    """
    log.debug(util.get_comm_start(message, is_in_guild) + 'thanked the bot')
    await message.channel.send(random.choice(constants.THANKYOU_RESPONSES))
# =================================================================
#                         FUN COMMANDS
# =================================================================
from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageFilter
from datetime import datetime, timedelta
from src.exceptions import *
from src import constants, util
import wikipedia
import datetime
import discord
import random
import string
import urllib
import json
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
        await message.channel.send('Now copying user ' + (user.nick if user.nick else str(user)))
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
    if not partner_1:
        try:
            # Gets valid users.
            users_choices = util.get_applicable_users(message, is_in_guild, exclude_bots=True)
            # Getting the two users.
            partner_1 = random.choice(users_choices)
            users_choices.remove(partner_1)
            partner_2 = random.choice(users_choices)
        except IndexError:
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

    embed = discord.Embed(title=random.choice(constants.SHIP_MESSAGES).format(partner_1.nick if partner_1.nick else partner_1.name, partner_2.nick if partner_2.nick else partner_2.name), colour=((221 << 16) + (115 << 8) + 215))
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
    character = 'imposter'
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
    await self.ultimate(message, argument, is_in_guild, True)


async def hunger_games(self, message, argument, is_in_guild):
    """
    Creates a hunger games simulator right inside the bot.
    """
    hg_key = str(message.channel)

    # If a game is already in progress, we forward this message.
    if hg_key in self.curr_hg.keys():
        await self.hunger_games_update(hg_key)

    else:
        # Get the user list. If user list is < 24 people, we add bots as well.
        user_list = util.get_applicable_users(message, is_in_guild, True)
        if len(user_list) < 24:
            user_list = util.get_applicable_users(message, is_in_guild, False)
        # If there still aren't enough users, we send error.
        if len(user_list) < 2:
            await message.channel.send('Not enough users in server.')
            log.debug(util.get_comm_start(message, is_in_guild) + ' requested hunger games, not enough people')

        # Otherwise, we generate the entire game.
        else:
            # Get the players.
            hg_players = []
            for i in range(min(24, len(user_list))):
                next_player = random.choice(user_list)
                hg_players.append(next_player)
                user_list.remove(next_player)

            await message.channel.send(str([u.name for u in hg_players]))

            # Set in players and actions.
            hg_full_game = {'players': hg_players, 'generated': False}


async def hunger_games_update(self, channel):
    pass
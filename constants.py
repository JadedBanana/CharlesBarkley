# Constants file
# General use
VERSION = '0.3.3'

# Developer stuff
DEVELOPER_DISCORD_IDS = [
    110194551586570240,   # Jade
    158429528874680320,   # Jabe
    444250440801189891,   # Alex
    620226160328179722    # Megu-Nee
]
ON_WINDOWS_ONLY_RESPOND_TO_DEV = True
IGNORE_DEVELOPER_ONLY_WORKS_ON_LINUX = True
TEMP_DIR = 'temp'

# Crontab shit
CRONTAB_CHECK_FILE = '.croncheck'
CRONTAB_WAIT_INTERVAL = 45
CRONTAB_STR_LENGTH = 24
CRONTAB_STR_CHARS = '1234567890-=_+()*&^%$#@!~`qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFG HJKLZXCVBNM[]{};\':",.<>?/|\\'

# Logging constants
DEFAULT_LEVEL = 0
LOG_TO_CONSOLE = True
LOG_TO_FILE = True
DO_LEVEL_HEADERS = True
DO_TIMESTAMPS = True
LOGS_DIR = 'logs'

# Server, channel, user
COMM_LOG_PREFIX_GUILD = '{} ({}, {}): '
COMM_LOG_PREFIX = '{} ({}): '

# Bot stuff
# Global crap
BOT_TOKEN = 'NzQwNjEwMTc2MDM3NTUyMTc4.Xyrg-Q.33fO34mvKyQmbsGwj54oTiojWp4'
GLOBAL_PREFIX = 'j!'

# YouTube
YOUTUBE_API_KEY = 'AIzaSyAHuBNRF1Ts5VKoqPnln57ojnrUVGUXINU'
YOUTUBE_QUOTA_RESET_HOUR = 3
YOUTUBE_RICKROLL_URL = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
YOUTUBE_RICKROLL_CHANCE = 0.002
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}'
YOUTUBE_SEARCH_COUNT = 100
YOUTUBE_SEARCH_LENGTHS = [1, 2, 3, 4, 5]
YOUTUBE_SEARCH_WEIGHTS = [36, 1296, 46656, 1679616, 60466176]
YOUTUBE_VIDEO_URL_FORMAT = 'https://www.youtube.com/watch?v={}'

# Ultimates
ULTIMATE_BACKGROUND_BOTTOM = 'assets/drbottom.png'
ULTIMATE_BACKGROUND_MIDDLE = 'assets/drmiddle.png'
ULTIMATE_BACKGROUND_TOP = 'assets/drtop.png'
ULTIMATE_CHARACTER_FOLDER = 'assets/danganronpa_chars'
ULTIMATE_CHARACTER_ATTRIBUTES = {
    'akamatsu_kaede': {'colors': {'bottom': (248, 107, 255), 'middle': (255, 230, 255), 'top': (255, 255, 64), 'name': (255, 204, 255)}},
    'amami_rantaro': {'colors': {'bottom': (198, 255, 64), 'middle': (248, 254, 38), 'top': (83, 128, 41), 'name': (229, 255, 59)}},
    'asahina_aoi': {'colors': {'bottom': (255, 77, 80), 'middle': (255, 255, 255), 'top': (128, 27, 27), 'name': (193, 76, 77)}},
    'chabashira_tenko': {'colors': {'bottom': (0, 255, 191), 'middle': (0, 219, 189), 'top': (41, 224, 50), 'name': (0, 223, 133)}},
    'enoshima_junko': {'colors': {'bottom': (128, 101, 124), 'middle': (251, 251, 251), 'top': (128, 28, 40), 'name': (128, 28, 40)}},
    'enoshima_mukuro': {'colors': {'bottom': (251, 251, 251), 'middle': (97, 90, 95), 'top': (178, 47, 46), 'name': (227, 60, 57)}},
    'fujisaki_chihiro': {'colors': {'bottom': (155, 255, 128), 'middle': (137, 251, 173), 'top': (172, 176, 0), 'name': (129, 182, 57)}},
    'fukawa_toko': {'colors': {'bottom': (102, 68, 87), 'middle': (204, 96, 94), 'top': (178, 47, 46), 'name': (227, 60, 57)}},
    'genocider': {'colors': {'bottom': (171, 69, 167), 'middle': (229, 66, 222), 'top': (209, 46, 46), 'name': (145, 18, 18)}},
    'gokuhara_gonta': {'colors': {'bottom': (160, 60, 10), 'middle': (255, 104, 45), 'top': (178, 18, 21), 'name': (239, 115, 0)}},
    'hagakure_yasuhiro': {'colors': {'bottom': (55, 90, 86), 'middle': (56, 153, 143), 'top': (168, 55, 17), 'name': (168, 88, 17)}},
    'hanamura_teruteru': {'colors': {'bottom': (255, 115, 115), 'middle': (200, 200, 200), 'top': (152, 81, 82), 'name': (214, 163, 164)}},
    'harukawa_maki': {'colors': {'bottom': (50, 63, 50), 'middle': (204, 49, 52), 'top': (178, 18, 21), 'name': (255, 24, 0)}},
    'hinata_hajime': {'colors': {'bottom': (154, 160, 108), 'middle': (195, 183, 134), 'top': (128, 128, 0), 'name': (103, 111, 46)}},
    'hoshi_ryoma': {'colors': {'bottom': (27, 27, 34), 'middle': (42, 33, 204), 'top': (92, 113, 168), 'name': (23, 83, 244)}},
    'ikusaba_mukuro': {'colors': {'bottom': (235, 210, 192), 'middle': (106, 88, 66), 'top': (76, 53, 78), 'name': (130, 79, 134)}},
    'imposter': {'colors': {'bottom': (249, 235, 174), 'middle': (222, 175, 35), 'top': (68, 108, 108), 'name': (61, 132, 132)}},
    'iruma_miu': {'colors': {'bottom': (255, 56, 228), 'middle': (245, 222, 242), 'top': (65, 249, 248), 'name': (233, 1, 182)}},
    'ishimaru_kiyotaka': {'colors': {'bottom': (0, 70, 177), 'middle': (3, 26, 59), 'top': (228, 228, 228), 'name': (156, 121, 119)}},
    'kiibo': {'colors': {'bottom': (128, 128, 128), 'middle': (99, 224, 101), 'top': (51, 51, 50), 'name': (34, 250, 54)}},
    'kirigiri_kyoko': {'colors': {'bottom': (157, 107, 160), 'middle': (192, 128, 196), 'top': (89, 73, 90), 'name': (193, 81, 200)}},
    'koizumi_mahiru': {'colors': {'bottom': (227, 89, 30), 'middle': (233, 149, 74), 'top': (236, 142, 109), 'name': (227, 89, 30)}},
    'komaeda_nagito': {'colors': {'bottom': (246, 255, 239), 'middle': (46, 54, 40), 'top': (100, 186, 42), 'name': (94, 143, 61)}},
    'kuwata_leon': {'colors': {'bottom': (213, 75, 26), 'middle': (233, 149, 74), 'top': (206, 100, 63), 'name': (227, 89, 30)}},
    'kuzuryu_fuyuhiko': {'colors': {'bottom': (192, 192, 192), 'middle': (59, 59, 59), 'top': (191, 171, 114), 'name': (137, 137, 137)}},
    'ludenberg_celestia': {'colors': {'bottom': (215, 215, 215), 'middle': (59, 59, 59), 'top': (216, 30, 11), 'name': (199, 49, 34)}},
    'maizono_sayaka': {'colors': {'bottom': (255, 153, 222), 'middle': (243, 121, 183), 'top': (214, 62, 139), 'name': (214, 62, 127)}},
    'mioda_ibuki': {'colors': {'bottom': (207, 240, 255), 'middle': (44, 103, 131), 'top': (206, 95, 199), 'name': (157, 82, 152)}},
    'momota_kaito': {'colors': {'bottom': (92, 91, 92), 'middle': (254, 245, 255), 'top': (206, 95, 199), 'name': (157, 82, 152)}},
    'naegi_makoto': {'colors': {'bottom': (255, 207, 189), 'middle': (254, 245, 255), 'top': (115, 126, 93), 'name': (128, 156, 72)}},
    'nanami_chiaki': {},
    'nevermind_sonia': {},
    'nidai_nekomaru': {},
    'ogami_sakura': {},
    'ouma_kokichi': {},
    'owada_mondo': {},
    'owari_akane': {},
    'pekoyama_peko': {},
    'saihara_shuichi': {},
    'saiyonji_hiyoko': {},
    'shinguji_korekiyo': {},
    'shirogane_tsumugi': {},
    'soda_kazuichi': {},
    'tanaka_gundham': {},
    'togami_byakuya': {'colors': {'bottom': (65, 86, 53), 'middle': (69, 115, 43), 'top': (223, 163, 32), 'name': (194, 120, 39)}},
    'tojo_kirumi': {},
    'tsumiki_mikan': {},
    'yamada_hifumi': {},
    'yonaga_angie': {},
    'yumeno_himiko': {}
}
ULTIMATE_NAME_FONT = 'assets/gill_sans.ttf'
ULTIMATE_NAME_MAX_ORD = 8805
ULTIMATE_PRONOUNS = [
    ['you', 'they'],
    ['your', 'their'],
    ["you're", "they're"],
    ['yourself', 'themselves'],
    ["you've", "they've"],
    ["you'll", "they'll"],
    ['you', 'them'],
    ['You', 'They'],
    ['Your', 'Their'],
    ["You're", "They're"],
    ['Yourself', 'Themselves'],
    ["You've", "They've"],
    ["You'll", "They'll"],
    ['You', 'Them']
]
ULTIMATE_TALENTS = {
    '???': {'desc': '! Guess {0} don\'t remember, huh? Well, better hope it\'s a good one.', 'char': ['hinata_hajime', 'kirigiri_kyoko', 'amami_rantaro']},
    'Actress': {'desc': '! Try as they might, no one could ever hope to emulate the passion {0} put into {1} performances!', 'char': ['enoshima_mukuro']},
    'Adventurer': {'desc': '! Well, who doesn\'t love discovering lands unknown?', 'char': ['amami_rantaro']}, # PLACEHOLDER UNTIL ALEX BEATS DRV3
    'Affluent Progeny': {'desc': '. Heir to the world\'s elite, {0} are destined to rule the world from the shadows.', 'char': ['togami_byakuya', 'imposter'],  'colors': {'bottom': (255, 245, 107), 'middle': (222, 175, 35), 'top': (223, 163, 32), 'name': (194, 120, 39)}},
    'Akido Master': {'desc': '! Hi-yah!', 'char': ['chabashira_tenko']},
    'Analyst': {'desc': '. {7} can dissect any situation and see things most other people can\'t.', 'char': ['kiibo', 'nanami_chiaki', 'saihara_shuichi', 'kirigiri_kyoko']},
    'Angler': {'desc': '. No one really gets how to gut a fish quite like {0}.', 'char': ['yonaga_angie', 'owari_akane']},
    'Animator': {'desc': '! Don\'t forget! Anime is art!', 'char': ['imposter']},
    'Anthropologist': {'desc': '. {7} know more about the Salem Witch Trials than anyone else on Earth.', 'char': ['shinguji_korekiyo']},
    'Archer': {'desc': '! {9} like Hawkeye up in here!', 'char': ['pekoyama_peko']},
    'Architect': {'desc': '. {8} houses are absolutely exquisite.', 'char': ['ludenberg_celestia']},
    'Artist': {'desc': '! Pretty colors and lifelike statues are {1} whole deal!', 'char': ['yonaga_angie']},
    'Assassin': {'desc': '. Here\'s the target. You have 24 hours.', 'char': ['pekoyama_peko', 'ikusaba_mukuro']}, # PLACEHOLDER UNTIL ALEX BEATS DRV3
    'Astronaut': {'desc': '! {7} can reach the stars for sure! If anyone can, it\'s {6}!', 'char': ['momota_kaito']},
    'Baseball Player': {'desc': '! Batter up!', 'char': ['kuwata_leon']},
    'Beatboxer': {'desc': '! Boots and cats and boots and cats...', 'char': ['soda_kazuichi', 'asahina_aoi']},
    'Blacksmith': {'desc': '! Daggers and knives and swords, oh my!', 'char': ['harukawa_maki', 'ikusaba_mukuro']},
    'Biker Gang Leader': {'desc': '! Rev your fucking engines! Let\'s tear up this town!', 'char': ['owada_mondo']},
    'Biologist': {'desc': '. {8} favorite joke is that one about mitosis.', 'char': ['gokuhara_gonta']},
    'Bodyguard': {'desc': '. Are {0} prepared to lay down {1} life?', 'char': ['ogami_sakura', 'nidai_nekomaru', 'imposter']}, # PLACEHOLDER UNTIL ALEX BEATS DRV3
    'Botanist': {'desc': '! Ooh, pretty!', 'char': ['yonaga_angie']},
    'Bounty Hunter': {'desc': '. Feel like hunting down any criminals?', 'char': ['ikusaba_mukuro']}, # PLACEHOLDER UNTIL ALEX BEATS DRV3
    'Boxer': {'desc': '! *DING-DING-DING!* It\'s a TKO!', 'char': ['ogami_sakura']},
    'Breakdancer': {'desc': '! Kick it!', 'char': ['owari_akane']},
    'Breeder': {'desc': '! Use {1} prowess in the dark arts to... potty-train this dog!', 'char': ['tanaka_gundham']},
    'Broadway Singer': {'desc': '. What\'s {1} favorite musical?', 'char': ['nevermind_sonia', 'maizono_sayaka']},
    'CGI Artist': {'desc': '! It looks so *real!*', 'char': ['fujisaki_chihiro']},
    'Cheerleader': {'desc': '! {14}, they\'re the one, if they don\'t win then that\'s no fun!', 'char': ['enoshima_mukuro', 'owari_akane']},
    'Chemist': {'desc': '. Man, that\'s such a boron career. It\'s too basic, if you ask me.', 'char': ['ikusaba_mukuro', 'tsumiki_mikan']},
    'Child Caregiver': {'desc': '. {9} basically like a goblin herder.', 'char': ['harukawa_maki']},
    'Clairvoyant': {'desc': '! {7} and {1} 30% accuracy rate can predict ANY crime that probably won\'t happen!', 'char': ['hagakure_yasuhiro']},
    'Clown': {'desc': '! {9} a clown! Honk honk! :o)', 'char': ['iruma_miu', 'ouma_kokichi', 'yamada_hifumi']},
    'Composer': {'desc': '. Popping out songs one after another ain\'t easy, but it\'s {1} way of life.', 'char': ['akamatsu_kaede']},
    'Con Artist': {'desc': '. {9} a slimy bastard who can convince anyone anything is a good idea.', 'char': ['ouma_kokichi', 'ludenberg_celestia']},
    'Confectioner': {'desc': '! How sweet of {0}!', 'char': ['hanamura_teruteru']},
    'Conspiracy Theorist': {'desc': '. So you think the moon landing was faked, huh? Well, have you heard the MOON is fake, too?', 'char': ['hagakure_yasuhiro']},
    'Cook': {'desc': '! Bon Appetit!', 'char': ['hanamura_teruteru']},
    'Curator': {'desc': '. {8} collection is far more impressive than the Smithsonian.', 'char': ['shinguji_korekiyo']},
    'Despair': {'desc': '. Despair is not a goal, or a set of principles, or a lifestyle, or even an instinct... It\'s what defines {6} as {14}!', 'char': ['enoshima_junko']},
    'Detective': {'desc': '! And the killer is... you!', 'char': ['kirigiri_kyoko', 'shuichi_saihara']},
    'Drug Dealer': {'desc': '. {11} stuck some stuff in some pretty gross places to get to the top, but {0} don\'t regret it.', 'char': ['komaeda_nagito']},
    'Drummer': {'desc': '! Any band is only as good as its drummer!', 'char': ['mioda_ibuki']},
    'DJ': {'desc': '! Lay down some beats, man!', 'char': ['mioda_ibuki']},
    'Entomologist': {'desc': '... so, if I find a spider, do I bring it to you?', 'char': ['gokuhara_gonta']},
    'Entrepreneur': {'desc': '', 'char': ['togami_byakuya', 'imposter']},
    'Exorcist': {'desc': '. The power of Christ compels you!', 'char': ['yonaga_angie']},
    'Fanfic Creator': {'desc': '! So, what next? Maybe a slow-burn coffee shop AU with some self-inserts, a handful of OC\'s, F/F and M/M, a little OOC if necessary, but all in all just fanservice fic for Danganronpa?', 'char': ['yamada_hifumi']},
    'Farmer': {'desc': '! Do {1} have a dog named Bingo? Or... just Ingo? Or Ngo?', 'char': ['owari_akane']},
    'Fashionista': {'desc': '! Looking cool, {14}!', 'char': ['enoshima_mukuro']},
    'Film Director': {'desc': '! When on set, nobody questions {1} judgement.', 'char': ['naegi_makoto', 'kuzuryu_fuyuhiko', 'amami_rantaro', 'akamatsu_kaede', 'shirogane_tsumugi', 'tanaka_gundham']},
    'Forum Admin': {'desc': '. {11} seen some serious shit.', 'char': ['kuzuryu_fuyuhiko']},
    'Gambler': {'desc': '', 'char': ['ludenberg_celestia']},
    'Gamer': {'desc': '', 'char': ['nanami_chiaki']},
    'Golfer': {'desc': '. No one can beat the power of a true Scottish swing.', 'char': ['nevermind_sonia']},
    'Guitarist': {'desc': '', 'char': ['mioda_ibuki']},
    'Gymnast': {'desc': '', 'char': ['owari_akane']},
    'Hacker': {'desc': '. {7} didn\'t actually get {1} title from some school official, {0} got it by hacking into the servers and giving it to {3}.', 'char': ['fujisaki_chihiro']},
    'Hairstylist': {'desc': '', 'char': ['enoshima_mukuro']},
    'Hope': {'desc': '', 'char': ['naegi_makoto']},
    'Housekeeper': {'desc': '! You\'re the ultimate cleaning machine!', 'char': ['tojo_kirumi']},
    'Hypnotist': {'desc': '. People ought to be cautious around {6} -- let down your guard for even a second and you can no longer think for yourself.', 'char': ['hagakure_yasuhiro']},
    'Idol': {'desc': '', 'char': ['maizono_sayaka']},
    'Impostor': {'desc': '. No one truly knows who {0} are beneath the mask... or that {2} even wearing one at all.', 'char': ['pekoyama_peko']}, # PLACEHOLDER UNTIL ALEX BEATS DR2
    'Internet Troll': {'desc': '. {9} really good at pissing people off online.', 'char': ['ouma_kokichi']},
    'Inventor': {'desc': '', 'char': ['iruma_miu']},
    'Lawyer': {'desc': '', 'char': ['kuzuryu_fuyuhiko']},
    'Lucky Student': {'desc': '', 'char': ['komaeda_nagito', 'naegi_makoto']},
    'Magician': {'desc': '! Prepare to be amazed!', 'char': ['yumeno_himiko']},
    'Maid': {'desc': '', 'char': ['tojo_kirumi']},
    'Martial Artist': {'desc': '', 'char': ['ogami_sakura']},
    'Makeup Artist': {'desc': '', 'char': ['enoshima_mukuro']},
    'Matchmaker': {'desc': '', 'char': ['enoshima_mukuro', 'yonaga_angie', 'maizono_sayaka']},
    'Mechanic': {'desc': '. Every tractor {0} work on is sexy.', 'char': ['soda_kazuichi']},
    'Medium': {'desc': '', 'char': ['hagakure_yasuhiro']},
    'Merchant': {'desc': '. No one knows supply and demand better than {6}, and {0} always have just enough stock to match what the public desires.', 'char': ['tanaka_gundham', 'shinguji_korekiyo', 'hagakure_yasuhiro']},
    'Model': {'desc': '', 'char': ['enoshima_mukuro']},
    'Moral Compass': {'desc': '. {7} are the best at telling other people how to act.', 'char': ['ishimaru_kiyotaka']},
    'Musician': {'desc': '', 'char': ['mioda_ibuki']},
    'Neurologist': {'desc': '', 'char': ['tsumiki_mikan']},
    'Ninja': {'desc': '}, lying hidden in the shadows. Watch out.', 'char': ['pekoyama_peko']},
    'Nurse': {'desc': '', 'char': ['tsumiki_mikan']},
    'Pharmacist': {'desc': '. It\'s not totally clear how {0} managed to become one at such a young age, but regardless, {0} are.', 'char': ['tsumiki_mikan']},
    'Photographer': {'desc': '! Say cheese!', 'char': ['koizumi_mahiru']},
    'Poet': {'desc': '. {7} just have a way with words others can only dream of matching.', 'char': ['fukawa_toko']},
    'Prankster': {'desc': '. What devious thing did {0} do to get this title...?', 'char': ['ouma_kokichi']},
    'Prisoner': {'desc': '', 'char': ['hoshi_ryoma']},
    'Puppeteer': {'desc': '. No strings on {1} puppets, no sir!', 'char': ['iruma_miu', 'shinguji_korekiyo']},
    'Psychologist': {'desc': '', 'char': ['tsumiki_mikan']},
    'Pianist': {'desc': '', 'char': ['akamatsu_kaede']},
    'Pilot': {'desc': '. Do a barrel roll!', 'char': ['tanaka_gundham']},
    'Police Officer': {'desc': '', 'char': ['ishimaru_kiyotaka']},
    'Priest': {'desc': '. With just a wave of {1} hand, {0} can enlighten hundreds at a time.', 'char': ['yonaga_angie']},
    'Princess': {'desc': '', 'char': ['nevermind_sonia']},
    'Programmer': {'desc': '! Did you know this bot is written in Python using the discord.py API?', 'char': ['fujisaki_chihiro']},
    'Pyrotechnician': {'desc': '. \'Cause baby, you\'re a firework!', 'char': ['soda_kazuichi', 'kuwata_leon']},
    'Robot': {'desc': '! Beep boop bop beep!', 'char': ['kiibo']},
    'Sailor': {'desc': '', 'char': ['hinata_hajime']},
    'Scout': {'desc': '. Though high adventure may be fun, there is nothing quite like giving back to one\'s community.', 'char': ['ishimaru_kiyotaka']},
    'Secret Agent': {'desc': '. {7} have a license to kill and {0} aren\'t afraid to use it.', 'char': ['kuzuryu_fuyuhiko']},
    'Serial Killer': {'desc': '', 'char': ['genocider']},
    'SFX Artist': {'desc': '. It\'s amazing what sounds you can make with just your mouth.', 'char': ['hinata_hajime', 'momota_kaito']},
    'Skiier': {'desc': '', 'char': ['kuwata_leon']},
    'Soccer Player': {'desc': '', 'char': ['amami_rantaro']},
    'Soldier': {'desc': '. The battlefield is where {0} truly belong.', 'char': ['ikusaba_mukuro']},
    'Sniper': {'desc': '. Headshot.', 'char': ['ikusaba_mukuro']},
    'Snowboarder': {'desc': '. It\'s like being a skiier, but way cooler.', 'char': ['momota_kaito']},
    'Surgeon': {'desc': '', 'char': ['tsumiki_mikan']},
    'Street Fighter': {'desc': '', 'char': ['chabashira_tenko']},
    'Stunt Double': {'desc': '', 'char': ['kuwata_leon', 'hoshi_ryoma']},
    'Superhero': {'desc': '', 'char': ['kiibo']},
    'Supervillain': {'desc': '! What separates a regular villain from a super one? Why, presentation, of course!', 'char': ['ouma_kokichi']},
    'Supreme Leader': {'desc': '', 'char': ['ouma_kokichi']},
    'Survivor': {'desc': '', 'char': ['amami_rantaro']},
    'Swimmer': {'desc': '! {7} swear {0} could swim across the ocean if it was legal!', 'char': ['asahina_aoi']},
    'Swordsman': {'desc': '. While most others spend their time playing video games or watching TV, {0} study the blade.', 'char': ['pekoyama_peko']},
    'Tailor': {'desc': '. Capes aren\'t usually fashionable, but the way {0} make it, anyone can rock that shit.', 'char': ['tojo_kirumi']},
    'Team Manager': {'desc': '', 'char': ['nidai_nekomaru']},
    'Tennis Pro': {'desc': '', 'char': ['hoshi_ryoma']},
    'Test Subject': {'desc': '. The Enrichment Center is committed to the well being of all participants. Cake and grief counseling will be available at the conclusion of the test.', 'char': ['hinata_hajime']},
    'Therapist': {'desc': '. Of course, {0} can\'t talk about it that much, since patient confidentiality is {1} number 1 priority.', 'char': ['fujisaki_chihiro', 'akamatsu_kaede', 'kirigiri_kyoko', 'nanami_chiaki']},
    'Traditional Dancer': {'desc': '', 'char': ['saiyonji_hiyoko']},
    'Translator': {'desc': '. {8} ability to be fluent in so many language baffles scientists.', 'char': ['hinata_hajime']},
    'VFX Artist': {'desc': '. {7} had it better in the 80\'s.', 'char': ['soda_kazuichi', 'imposter', 'momota_kaito', 'tanaka_gundham']},
    'Violinist': {'desc': '', 'char': ['akamatsu_kaede']},
    'Voice Actor': {'desc': '. {9} able to switch voices on a dime, and none of them sound anything alike.', 'char': ['enoshima_junko', 'mioda_ibuki']},
    'Wrestler': {'desc': '! Let\'s settle this in the ring!', 'char': ['ogami_sakura']},
    'Writer': {'desc': '', 'char': ['fukawa_toko']},
    'Yakuza': {'desc': '', 'char': ['kuzuryu_fuyuhiko']},
    'Yoga Guru': {'desc': '. All {1} chakras are open and flowing the sweet nectar of the soul.', 'char': ['hagakure_yasuhiro']}
}
ULTIMATE_TALENT_FONT = 'assets/times_sans_serif.ttf'
ULTIMATE_SPRITE_FILETYPE = '.webp'
ULTIMATE_SPRITE_X = 265

# Hunger Games
# =================DEBUG==================
# 0: nothing
# 3000: 1 - 3 random items
# 4000: 1 weapon, 1 food item, 1 health item
# 8888: make net from rope, give food
# 9999: take away everything and give it to everyone else
# ================WEAPONS================
# 1: mace
# 2: sword
# 3: spear
# 4: explosives
# 5: throwing knives
# 6: hatchet
# 7: slingshot
# 8: rope
# 9: shovel
# 10: net
# 11: molotov cocktail
# 12: bow
# 13: poison
# 14: scissors
# ==================FOOD=================
# 101: clean water
# 102: river water
# 103: loaf of bread
# 104: raw meat
# =================HEALTH================
# 201: bandages
# 202: medicine
# 203: first aid kit
# ==================OTHER================
# 301: shack
# 302: camouflage
# 303: cave
# 304: high ground
HG_WEAPON_ITEMS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
HG_FOOD_ITEMS = [101, 102, 103, 104]
HG_HEALTH_ITEMS = [201, 202, 203]
HG_ALL_ITEMS = HG_WEAPON_ITEMS + HG_FOOD_ITEMS + HG_HEALTH_ITEMS
HG_BLOODBATH_ACTIONS = [
    {'players': 0, 'act': '{0} runs away from the Cornucopia.'},
    {'players': 0, 'act': '{0} runs away from the Cornucopia.'},
    {'players': 0, 'act': '{0} grabs a sword.', 'give': [2]},
    {'players': 0, 'act': '{0} takes a spear from the Cornucopia.', 'give': [3]},
    {'players': 0, 'act': '{0} finds a bag full of explosives.', 'give': [4]},
    {'players': 0, 'act': '{0} grabs a backpack and retreats.', 'give': [4000]},
    {'players': 0, 'act': '{0} takes only a pair of scissors.', 'give': [14]},
    {'players': 0, 'act': '{0} takes a handful of throwing knives.', 'give': [5]},
    {'players': 0, 'act': '{0} accidentally steps on a landmine and explodes.', 'kill': [0]},
    {'players': 0, 'act': '{0} grabs a bottle of alcohol and a rag.', 'give': [11]},
    {'players': 0, 'act': '{0} grabs a first aid kit and runs away.', 'give': [203]},
    {'players': 0, 'act': '{0} grabs a bow and makes a getaway.', 'give': [12]},
    {'players': 0, 'act': '{0} stubs their toe on a grenade. It explodes, killing them.', 'kill': [0]},
    {'players': 0, 'act': '{0} escapes with a lighter and some rope.', 'give': [8]},
    {'players': 1, 'act': '{0} rips a mace out of {1}\'s hands.', 'give': [1, 0]},
    {'players': 1, 'act': '{0} throws a knife into {1}\'s head.', 'kill': [1]},
    {'players': 1, 'act': '{0} strangles {1} after engaging in a fist fight.', 'kill': [1]},
    {'players': 1, 'act': '{0} stabs {1} with a tree branch.', 'kill': [1]},
    {'players': 1, 'act': '{0} breaks {1}\'s nose for a basket of bread.', 'hurt': [1]},
    {'players': 2, 'act': '{0}, {1}, and {2} work together to get as many supplies as possible.', 'give': [3000, 3000, 3000]},
    {'players': 2, 'act': '{0} and {1} work together to drown {2}.', 'kill': [2]},
    {'players': 2, 'act': '{0}, {1}, and {2} get into a fight. {1} triumphantly kills them both.', 'kill': [0, 2]}
]
HG_NORMAL_DAY_ACTIONS = {
    'trigger': [
        {'needs': 302, 'chance': 0.8, 'success': [{'players': 0, 'act': '{0} continues to hide in the bushes.'}, {'players': 1, 'act': '{0} waits until the perfect moment to pop out of the bushes, ambushing {1} and killing them.', 'kill': [1], 'give': [-302, 0]}], 'fail': [{'players': 1, 'act': '{0} is discovered by {1}, who immediately bashes in their skull with a rock.', 'kill': [0]}]},
        {'needs': 304, 'chance': 0.75, 'success': [{'players': 1, 'act': '{0} is attacked by {1}, but {0} has the high ground, so they manage to defeat {1}.', 'give': [-304, 0], 'kill': [1]}], 'fail': [{'players': 0, 'give': [-304]}]},
        {'needs': 1, 'chance': 0.1, 'success': [{'players': 1, 'act': '{0} uses their mace to beat {1} to death.', 'kill':[1]}]},
        {'needs': 2, 'chance': 0.2, 'success': [{'players': 1, 'act': '{0} cuts down {1} with a sword.', 'kill': [1]}, {'players': 1, 'act': '{0} attempts to swing their sword at {1}, but {1} is able to disarm them and use it against them.', 'kill': [0], 'give': [-2, 2]}]},
        {'needs': 3, 'chance': 0.2, 'success': [{'players': 0, 'act': '{0} accidentally impales themselves with a spear.', 'kill': [0]}, {'players': 1, 'act': '{0} impales {1} with a spear.', 'kill': [1], 'give': [-3, 0]}]},
        {'needs': 4, 'chance': 0.2, 'success': [{'players': 1, 'act': '{0} creates a landmine from their explosives. An hour later, {1} steps on it and explodes.', 'kill': [1], 'give': [-4, 0]}, {'players': 0, 'act': '{0} creates a landmine from their explosives.'}, {'players': 0, 'act': '{0} attempts to create a landmine from their explosives, but blows themselves up in the process.', 'kill': [0]}]},
        {'needs': 5, 'chance': 0.2, 'success': [{'players': 1, 'act': '{0} lands a throwing knife right in the middle of {1}\'s chest.', 'kill': [1], 'give': [-5, 0]}, {'players': 1, 'act': '{0} throws a throwing knife through {1}\'s arm. {1} rips it out and throws it back at {0}, killing them.', 'kill': [0], 'give': [-5, 0], 'hurt': [1]}]},
        {'needs': 6, 'chance': 0.2, 'success': [{'players': 1, 'act': '{0} brutally executes {1} with a hatchet.', 'kill': [1]}]},
        {'needs': 7, 'chance': 0.2, 'success': [{'players': 1, 'act': '{0} uses their slingshot to shoot {1} out of a tree, killing them.', 'kill': [1]}]},
        {'needs': 8, 'chance': 0.2, 'success': [{'players': 1, 'act': '{0} creates a net from their rope, which they use to catch food.', 'give': [8888]}]},
        {'needs': 12, 'chance': 0.8, 'success': [{'players': 0, 'act': '{0} practices their archery.'}], 'fail': [{'players': 1, 'act': '{0} successfully shoots an arrow into {1}\'s head.', 'kill': [1]}, {'players': 1, 'act': '{0} shoots an arrow at {1}, but misses, giving away their position. They drop the bow and run.', 'give': [-12, 0]}]},
        {'needs': 13, 'chance': 0.3, 'success': [{'players': 1, 'act': '{0} poisons {1}\'s drink. They drink it and die.', 'give': [-13, 0]}]},
        {'needs': 301, 'chance': 0.9, 'success': [{'players': 4, 'act': '{0} has their camp raided by {1}, {2}, {3}, and {4}.', 'give': [9999, 0, 0, 0, 0]}, {'players': 0, 'act': '{0} defends their stronghold.'}]},
        {'needs': 303, 'chance': 0.9, 'success': [{'players': 4, 'act': '{0} has their camp raided by {1}, {2}, {3}, and {4}.', 'give': [9999, 0, 0, 0, 0]}, {'players': 0, 'act': '{0} defends their stronghold.'}]},
        {'needs': 103, 'chance': 0.1, 'success': [{'players': 2, 'act': '{0} successfully uses food to get {1} to kill {2}.', 'kill': [2], 'give': [-103, 0, 0]}]}
    ],
    'normal': [
        {'players': 0, 'act': '{0} receives clean water from an unknown sponsor.', 'give': [101]},
        {'players': 0, 'act': '{0} receives medical supplies from an unknown sponsor.', 'give': [201]},
        {'players': 0, 'act': '{0} constructs a shack.', 'give': [301]},
        {'players': 0, 'act': '{0} discovers a river.', 'give': [102]},
        {'players': 0, 'act': '{0} travels to higher ground.', 'give': [304]},
        {'players': 0, 'act': '{0} tries to sleep through the day.'},
        {'players': 0, 'act': '{0} discovers a cave.', 'give': [303]},
        {'players': 0, 'act': '{0} finds a hatchet embedded into a tree.', 'give': [6]},
        {'players': 0, 'act': '{0} camouflages themselves in the bushes.', 'give': [302]},
        {'players': 0, 'act': '{0} dies of dysentery.', 'kill': [0]},
        {'players': 0, 'act': '{0} cries to themselves.'},
        {'players': 0, 'act': '{0} wanders around aimlessly.'},
        {'players': 0, 'act': '{0} makes a slingshot.', 'give': [7]},
        {'players': 0, 'act': '{0} eats some berries.'},
        {'players': 0, 'act': '{0} makes a wooden spear.', 'give': [3]},
        {'players': 0, 'act': '{0} picks flowers.'},
        {'players': 0, 'act': '{0} is stung by bees.', 'hurt': [0]},
        {'players': 0, 'act': '{0} is pricked by thorns while picking berries.', 'hurt': [0]},
        {'players': 0, 'act': '{0} finds some rope.', 'give': [8]},
        {'players': 0, 'act': '{0} receives a bottle of poison from an unknown sponsor.', 'give': [13]},
        {'players': 0, 'act': '{0} eats some poisonous berries by accident.', 'kill': [0]},
        {'players': 1, 'act': '{0} uses a rock to break {1}\'s arm.', 'hurt': [1]},
        {'players': 1, 'act': '{0} and {1} split up to look for resources.'},
        {'players': 1, 'act': '{0} sprains their ankle while running away from {1}.', 'hurt': [0]},
        {'players': 1, 'act': '{0} and {1} work together for the day.'},
        {'players': 1, 'act': '{0} tracks down and kills {1}.', 'kill': [1]},
        {'players': 1, 'act': '{0} defeats {1} in a fight, but spares their life.', 'hurt': [1]},
        {'players': 1, 'act': '{0} begs for {1} to kill them. They refuse, keeping {0} alive.'},
        {'players': 1, 'act': '{0} pushes {1} off a cliff.', 'kill': [1]},
        {'players': 1, 'act': '{0} and {1} engage in a fist fight, but accidentally fall off a cliff together.', 'kill': [0, 1]},
        {'players': 1, 'act': '{0} attempts to climb a tree, but falls on {1}, killing them both.', 'kill': [0, 1]},
        {'players': 2, 'act': '{0} pushes a boulder down a hill, which flattens both {1} and {2}.', 'kill': [1, 2]},
        {'players': 2, 'act': '{0} overhears {1} and {2} talking in the distance.'},
        {'players': 3, 'act': '{0} forces {1} to kill either {2} or {3}. They choose {2}.', 'kill': [2]},
        {'players': 3, 'act': '{0} forces {1} to kill either {2} or {3}. They choose {3}.', 'kill': [2]}
    ]
}
HG_NORMAL_NIGHT_ACTIONS = {
    'trigger': [
        {'needs': 302, 'chance': 0.8, 'success': [{'players': 0, 'act': '{0} continues to hide in the bushes.'}, {'players': 1, 'act': '{0} waits until the perfect moment to pop out of the bushes, ambushing {1} and killing them.', 'kill': [1], 'give': [-302, 0]}], 'fail': [{'players': 1, 'act': '{0} is discovered by {1}, who immediately bashes in their skull with a rock.', 'kill': [0]}]},
        {'wounded': True, 'needs': 203, 'success': [{'players': 0, 'act': '{0} tends to their wounds.', 'heal': [0], 'give': [-203]}]},
        {'wounded': True, 'needs': 201, 'chance': 0.9, 'success': [{'players': 0, 'act': '{0} tends to their wounds.', 'heal': [0], 'give': [-201]}]},
        {'wounded': True, 'needs': 202, 'chance': 0.5, 'success': [{'players': 0, 'act': '{0} tends to their wounds.', 'heal': [0], 'give': [-202]}]},
        {'wounded': True, 'chance': 0.2, 'success': [{'players': 0, 'act': '{0} tends to their wounds.', 'heal': [0], 'give': [-202]}], 'fail': [{'players': 0, 'act': '{0} dies from their wounds.', 'kill': [0]}]},
        {'needs': 303, 'chance': 0.2, 'success': [{'players': 0, 'act': '{0} is mauled to death by a bear that was living in the cave they found.', 'kill': [0]}, {'players': 1, 'act': '{0}\'s stronghold is discovered by {1}, who then strangles {0}.', 'kill': [0]}], 'fail': [{'players': 0, 'act': '{0} sleeps peacefully in their cave for the night.', 'give': -301}]},
        {'needs': 9, 'chance': 0.1, 'success': [{'players': 1, 'act': '{0} uses their shovel to bury {1} alive.', 'kill': [1]}]},
        {'needs': 14, 'chance': 0.3, 'success': [{'players': 1, 'act': '{0} stabs a hole right through {1}\'s throat using their scissors.', 'kill': [1]}]},
        {'needs': 104, 'success': [{'players': 0, 'act': '{0} cooks their meat over the fire.', 'give': [-104]}]}
    ],
    'normal': [
        {'players': 0, 'act': '{0} passes out from exhaustion.'},
        {'players': 0, 'act': '{0} screams for help.'},
        {'players': 0, 'act': '{0} questions their sanity.'},
        {'players': 0, 'act': '{0} stays awake all night.'},
        {'players': 0, 'act': '{0} thinks about winning.'},
        {'players': 0, 'act': '{0} dies from hypothermia.', 'kill': [0]},
        {'players': 0, 'act': '{0} prays to every god they can think of.'},
        {'players': 0, 'act': '{0} cannot handle the circumstances and commits suicide.', 'kill': [0]},
        {'players': 0, 'act': '{0} cries themselves to sleep.'},
        {'players': 0, 'act': '{0} thinks about home.'},
        {'players': 0, 'act': '{0} loses sight of where they are.'},
        {'players': 0, 'act': '{0} receives fresh food from an unknown sponsor.', 'give': [103]},
        {'players': 0, 'act': '{0} receives explosives from an unknown sponsor.', 'give': [4]},
        {'players': 1, 'act': '{0} convinces {1} to snuggle.'},
        {'players': 1, 'act': '{0} and {1} hold hands.'},
        {'players': 1, 'act': '{0} pushes {1} into their own fire, burning them alive.', 'kill': [1]},
        {'players': 1, 'act': '{0} and {1} talk about their place in the universe.'},
        {'players': 1, 'act': '{0} and {1} make up stories to entertain themselves.'},
        {'players': 2, 'act': '{0} and {1} team up to ambush {2}.', 'kill': [2]},
        {'players': 3, 'act': '{0} fends {1}, {2}, and {3} away from their fire.'},
        {'players': 5, 'act': '{0}, {1}, and {2} unsuccessfully ambush {3}, {4}, and {5}, who kill them instead.', 'kill': [0, 1, 2]},
        {'players': 5, 'act': '{0}, {1}, and {2} successfully ambush {3}, {4}, and {5}.', 'kill': [3, 4, 5]}
    ]
}
HG_RESTOCK_EVENT = {
    'trigger': [

    ],
    'normal': [
        {'players': 0, 'act': '{0} decides not to go to the feast.'},
        {'players': 0, 'act': '{0} grabs a bundle of dry clothes and runs.'},
        {'players': 1, 'act': '{0} destroys {1}\'s memoirs out of spite.'},
        {'players': 0, 'act': '{0} steps on a landmine near the Cornucopia.', 'kill': [0]},
        {'players': 1, 'act': '{0} and {1} fight over raw meat, but {1} gives up and flees.', 'give': [104, 0]}
    ]
}
HG_FIRE_EVENT = {
    'trigger': [
        {'needs': 10, 'success': [{'players': 1, 'act': '{0} uses their net to capture {1} and toss them into the fire.'}]}
    ],
    'normal': [
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': 'A fireball strikes {0}, killing them.', 'kill': [0]},
        {'players': 0, 'act': '{0} is singed by the flames, but survives.', 'hurt': [0]},
        {'players': 1, 'act': '{0} helps {1} get to higher ground.'},
        {'players': 1, 'act': '{0} pushes {1} into a river, sacrificing themselves.', 'kill': [0]},
        {'players': 1, 'act': '{0} falls to the ground, but kicks {1} hard enough to push them into the fire.', 'kill': [0, 1]},
        {'players': 1, 'act': '{0} kills {1} in order to utilize a body of water safely.', 'kill': [1]},
        {'players': 1, 'act': '{0} and {1} fail to find a safe spot and suffocate.', 'kill': [0, 1]}
    ]
}
HG_FLOOD_EVENT = {
    'trigger': [
        {'needs': 10, 'success': [{'players': 1, 'act': '{0} uses their net to capture {1} and toss them into the water.'}]}
    ],
    'normal': [
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} falls into the water, but miraculously survives.'},
        {'players': 0, 'act': '{0} is swept away by the flood.', 'kill': [0]},
        {'players': 0, 'act': '{0} climbs up a tree, but the waters snap the tree in half, taking the whole thing out.', 'kill': [0]},
        {'players': 1, 'act': '{0} helps {1} get to higher ground.'},
        {'players': 1, 'act': '{0} pushes {1} into the water.', 'kill': [1]},
        {'players': 2, 'act': '{0} throws {1} and {2} to safety, sacrificing themselves.', 'kill': [0]},
    ]
}
HG_TORNADO_EVENT = {
    'trigger': [
        {'needs': 10, 'success': [{'players': 1, 'act': '{0} uses their net to capture {1} and toss them into the storm.'}]}
    ],
    'normal': [
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} survives.'},
        {'players': 0, 'act': '{0} is carried away by the storm.', 'kill': [0]},
        {'players': 1, 'act': '{0} lets {1} into their shelter.'},
        {'players': 1, 'act': '{0} kicks {1} away, letting them be sucked up by the tornado.', 'kill': [1]},
        {'players': 1, 'act': '{0} and {1} run away from the storm together, but as {1} is carried away, they grab {0}, leading them both to their deaths.', 'kill': [0, 1]},
        {'players': 1, 'act': '{0} can\'t handle the circumstances and offers themselves to the storm.', 'kill': [0]},
    ]
}
HG_WINNER_EVENT = 'The winner is {0}!'
HG_TIE_EVENT = 'Since they died at the same time, it\'s a tie between {0} and {1}!'
# Pregame
HG_MIN_GAMESIZE = 2
HG_MAX_GAMESIZE = 48
HG_PREGAME_TITLE = 'The Reaping'
HG_PREGAME_DESCRIPTION = 'Respond one of the following:\nS: Shuffle\t\tR: Replace\nA: Add\t\t\tD: Delete\t\tB: {} bots\nP: Proceed\t\tC: Cancel'
# Graphics
HG_PLAYERSTATUS_WIDTHS = [0, 1, 2, 3, 4, 3, 3, 4, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
HG_PLAYERSTATUS_ROWHEIGHT = 172
HG_PLAYERNAME_FONT = 'assets/arial_bold.ttf'
HG_ACTION_ROWHEIGHT = 175
HG_FONT_SIZE = 16
HG_ICON_SIZE = 128
HG_ICON_BUFFER = 25
HG_TEXT_BUFFER = 6
HG_HEADER_BORDER_BUFFER = 7
HG_BACKGROUND_COLOR = (93, 80, 80)
HG_HEADER_TEXT_COLOR = (255, 207, 39)
HG_ACTION_PLAYER_COLOR = (251, 130, 0)
HG_HEADER_BORDER_COLOR = (255, 255, 255)
HG_HEADER_BACKGROUND_COLOR = (35, 35, 35)
HG_EMBED_COLOR = (251 << 16) + (130 << 8)
# Descriptions
HG_BEGINNING_DESCRIPTION = 'Respond one of the following:\nN: Next Action\nC: Cancel Game'
HG_MIDGAME_DESCRIPTION = 'Respond one of the following:\nN: Next Action\tP: Previous Action\nC: Cancel Game'
HG_POSTGAME_BEGINNING_DESCRIPTION = 'Respond one of the following:\nN: Next Action\nR: Replay (same cast)\tS: New Game\tC: Close'
HG_POSTGAME_MIDGAME_DESCRIPTION = 'Respond one of the following:\nP: Previous Action\tN: Next Action\nR: Replay (same cast)\tS: New Game\tC: Close'
HG_THE_END_DESCRIPTION = 'The end! Respond one of the following:\nP: Previous Action\nR: Replay (same cast)\tS: New Game\tC: Close'
HG_FINALE_DESCRIPTION = 'Respond one of the following:\nP: Previous Action\nR: Replay (same cast)\tS: New Game\tC: Close'
HG_WINNER_TITLE = 'The Winner'
# Events
HG_EVENT_DEFAULT_CHANCE = 0.2
HG_EVENTS = [(HG_FLOOD_EVENT, 'The Flood', 'A vicious flood suddenly appears out of nowhere and sweeps through the Arena.'), (HG_FIRE_EVENT, 'The Fire', 'A sudden bolt of lightning sparks a fire, which explodes into a massive Arena-wide forest fire.'), (HG_TORNADO_EVENT, 'The Tornado', 'Winds in the Arena pick up and a tornado begins to tear its way through the Arena.'), (HG_RESTOCK_EVENT, 'The Replenishing', 'The Cornucopia is restocked with food, weapons, and medical supplies.')]

# Weather constants
WEATHER_API_KEY = 'fbe576aaab00abc563182f75b9725115'
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?appid={}&q={}'
WEATHER_ALT_COUNTRY_CODES = {
    'BO': 'Bolivia', 'FK': 'Falkland Islands', 'FM': 'Micronesia', 'GB': 'United Kingdom', 'IR': 'Iran', 'KP': 'North Korea',
    'KR': 'South Korea', 'LA': 'Laos', 'MD': 'Moldova', 'PS': 'Palestine', 'RU': 'Russia', 'SX': 'Sint Maarten',
    'SY': 'Syria', 'TW': 'Taiwan', 'TZ': 'Tanzania', 'US': 'United States', 'VE': 'Venezuela', 'VN': 'Vietnam'
}
WEATHER_CREDIT_TEXT = 'Powered by OpenWeatherMap'
WEATHER_EMBED_COLOR_DEFAULT = (235 << 16) + (110 << 8) + 75
WEATHER_EMBED_COLORS_BY_ICON = {
    '01d': (235 << 16) + (110 << 8) + 75, '02d': (235 << 16) + (110 << 8) + 75, '10d': (235 << 16) + (110 << 8) + 75, '11d': (235 << 16) + (110 << 8) + 75, '11n': (235 << 16) + (110 << 8) + 75,
    '03d': (242 << 16) + (242 << 8) + 242, '03n': (242 << 16) + (242 << 8) + 242, '04d': (242 << 16) + (242 << 8) + 242, '04n': (242 << 16) + (242 << 8) + 242, '13d': (242 << 16) + (242 << 8) + 242, '13n': (242 << 16) + (242 << 8) + 242, '50d': (242 << 16) + (242 << 8) + 242, '50n': (242 << 16) + (242 << 8) + 242,
    '01n': (72 << 16) + (72 << 8) + 74, '02n': (72 << 16) + (72 << 8) + 74, '09d': (72 << 16) + (72 << 8) + 74, '09n': (72 << 16) + (72 << 8) + 74, '10n': (72 << 16) + (72 << 8) + 74
}
WEATHER_KELVIN_SUB = 273.15
WEATHER_THUMBNAIL_URL = 'http://openweathermap.org/img/wn/{}@4x.png'
WEATHER_WIND_DIRECTIONS = {
    'North': 22.5, 'Northeast': 67.5, 'East': 112.5,
    'Southeast': 157.5, 'South': 202.5, 'Southeast': 247.5,
    'East': 292.5, 'Northeast': 337.5, 'North': 382.5
}

# Globals for the eval function
import math
import util

EVAL_GLOBALS = {
    # Math overall
    'math': math,
    # Math constants
    'pi': math.pi, 'e': math.e, 'tau': math.tau, 'inf': math.inf, 'nan': math.nan,
    # Easy baby shit
    'ceil': math.ceil, 'ncr': util.comb, 'comb': util.comb, 'copysign': math.copysign,
    'fabs': math.fabs, 'abs': math.fabs, 'factorial': math.factorial, 'floor': math.floor,
    'fmod': math.fmod, 'frexp': math.frexp, 'fsum': math.fsum, 'gcd': math.gcd,
    'isclose': math.isclose, 'isfinite': math.isfinite, 'isinf': math.isinf,
    'isinfinite': math.isinf, 'isnan': math.isnan, 'ldexp': math.ldexp,
    'modf': math.modf, 'npr': util.perm, 'perm': util.perm, 'prod': util.prod,
    'product': util.prod, 'remainder': math.remainder, 'trunc': math.trunc,
    'truncate': math.trunc,
    # Power and logarithmic
    'exp': math.exp, 'expm1': math.expm1, 'log': math.log, 'log1p': math.log1p,
    'log2': math.log2, 'log10': math.log10, 'pow': math.pow, 'sqrt': math.sqrt,
    # Trig
    'acos': math.acos, 'asin': math.asin, 'atan': math.atan, 'atan2': math.atan2,
    'cos': math.cos, 'hypot': math.hypot, 'sin': math.sin, 'tan': math.tan,
    # Angles shit
    'deg': math.degrees, 'degrees': math.degrees, 'rad': math.radians,
    'radians': math.radians,
    # Hyperbolas
    'acosh': math.acosh, 'asinh': math.asinh, 'atanh': math.atanh, 'cosh': math.cosh,
    'sinh': math.sinh, 'tanh': math.tanh,
    # Other
    'erf': math.erf, 'erfc': math.erfc, 'gamma': math.gamma, 'lgamma': math.lgamma
}

# Shipping
SHIP_EMBED_COLOR = (221 << 16) + (115 << 8) + 215
SHIP_HEART_IMG = 'assets/heart.png'
SHIP_ICON_SIZE = 128
SHIP_MESSAGES = [
    'I ship {} with {}! Isn\'t it cute?',
    'If you ask me, {} and {} were meant for each other.',
    'OTP: {} and {}.',
    'I ship {} and {}. Cute, right?',
    'I like {} and {}. Enemies to lovers-sorta thing.',
    '{} x {}. No further questions.',
    'Imagine a yandere {} going after {}. Crazy, right?',
    '{} and {}. Both are huge tsunderes.',
    '{} and {}. Bakadere relationships are so cute, IMO.',
    'Say whatever you want. {} and {} is the purest, most amazing ship and I will not stand for any others.'
]

# Uwu
EMOTE_CHARACTERS = '0123456789_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVQXYZ'
UWU_FACES = {
    ':)': 'uwu', ':(': 'umu', ':|': 'u_u', ':-)': 'uwu', ':-(': 'umu', ':-|': 'u_u', '^_^': 'uwu',
    '^w^': 'uwu', 'O_o': 'u_u', 'o_o': 'u_u', 'o_O': 'u_u', 'O_O': 'u_u', '(:': 'uwu', ':D': 'uwu',
    'D:': 'umu', '):': 'umu'
}
OWO_FACES = {
    ':)': 'owo', ':(': 'omo', ':|': 'o_o', ':-)': 'owo', ':-(': 'omo', ':-|': 'o_o', '^_^': 'owo',
    '^w^': 'owo', 'O_o': 'o_o', 'o_o': 'o_o', 'o_O': 'o_o', 'O_O': 'o_o', '(:': 'owo', ':D': 'owo',
    'D:': 'omo', '):': 'omo'
}

# Conversion chars
CONVERT_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+_'
MAX_CONVERT_DEPTH = -16

# Runtime and Uptime
RUNTIME_PREFIX = 'Bot has been running for '
UPTIME_PREFIX = 'Bot has been connected for '

# Ip methods
LINUX_IP_PREFIXES = ['lo', 'eth0']

# Image Manipulation crap
PFP_SIZE_PREFIX = '?size='
PFP_FILETYPE = '.webp'
PFP_DEFAULT_SIZE = 1024

NONDECIMAL_BASES = {
    '0x': [16, 'hexadecimal'],
    '0d': [12, 'duodecimal'],
    '0o': [8, 'octal'],
    '0b': [2, 'binary']
}

# Thank you
THANKYOU_RESPONSES = [
    ':)',
    ':D',
    'You\'re welcome!',
    'It\'s my pleasure.',
    'I aim to please!',
    'Hehe, I\'m just doing my job!',
    ':blush:'
]

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
- calc / eval: Give a math equation and it will be evaluated as one (python eval() function)
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

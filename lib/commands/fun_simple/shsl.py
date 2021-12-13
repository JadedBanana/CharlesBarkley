"""
SHSL / Ultimate command.
Assigns users a(n) SHSL / ultimate talent.
"""
# Local Imports
from lib.util.exceptions import NoUserSpecifiedError, UnableToFindUserError, CannotAccessUserlistError
from lib.util import arguments, assets, discord_info, messaging, parsing
from lib.util.logger import BotLogger as logging

# Package Imports
from PIL import Image, ImageOps, ImageDraw, ImageFilter
import random
import os


# SHSL variables, used for easy bug testing / finnicking.
SHSL_NAME_FONT = 'gill_sans.ttf'
SHSL_NAME_MAX_ORD = 8805
SHSL_TALENT_FONT = 'times_sans_serif.ttf'
SHSL_SPRITE_FILETYPE = '.webp'
SHSL_EMBED_COLOR = (221 << 16) + (115 << 8) + 215

# SHSL Constants
SHSL_CHARACTER_ATTRIBUTES = {
    'akamatsu_kaede': {'colors': {
        'bottom': (248, 107, 255),
        'middle': (255, 230, 255),
        'top': (255, 255, 64),
        'name': (255, 204, 255)
    }},
    'amami_rantaro': {'colors': {
        'bottom': (198, 255, 64),
        'middle': (248, 254, 38),
        'top': (83, 128, 41),
        'name': (229, 255, 59)
    }},
    'asahina_aoi': {'colors': {
        'bottom': (255, 77, 80),
        'middle': (255, 255, 255),
        'top': (128, 27, 27),
        'name': (193, 76, 77)}
    },
    'chabashira_tenko': {'colors': {
        'bottom': (0, 255, 191),
        'middle': (0, 219, 189),
        'top': (41, 224, 50),
        'name': (0, 223, 133)
    }},
    'enoshima_junko': {'colors': {
        'bottom': (128, 101, 124),
        'middle': (251, 251, 251),
        'top': (128, 28, 40),
        'name': (128, 28, 40)
    }},
    'enoshima_mukuro': {'colors': {
        'bottom': (251, 251, 251),
        'middle': (97, 90, 95),
        'top': (178, 47, 46),
        'name': (227, 60, 57)
    }},
    'fujisaki_chihiro': {'colors': {
        'bottom': (155, 255, 128),
        'middle': (137, 251, 173),
        'top': (172, 176, 0),
        'name': (129, 182, 57)
    }},
    'fukawa_toko': {'colors': {
        'bottom': (102, 68, 87),
        'middle': (204, 96, 94),
        'top': (178, 47, 46),
        'name': (227, 60, 57)
    }},
    'genocider': {'colors': {
        'bottom': (171, 69, 167),
        'middle': (229, 66, 222),
        'top': (209, 46, 46),
        'name': (145, 18, 18)
    }},
    'gokuhara_gonta': {'colors': {
        'bottom': (160, 60, 10),
        'middle': (255, 104, 45),
        'top': (178, 18, 21),
        'name': (239, 115, 0)
    }},
    'hagakure_yasuhiro': {'colors': {
        'bottom': (55, 90, 86),
        'middle': (56, 153, 143),
        'top': (168, 55, 17),
        'name': (168, 88, 17)
    }},
    'hanamura_teruteru': {'colors': {
        'bottom': (255, 115, 115),
        'middle': (200, 200, 200),
        'top': (152, 81, 82),
        'name': (214, 163, 164)
    }},
    'harukawa_maki': {'colors': {
        'bottom': (50, 63, 50),
        'middle': (204, 49, 52),
        'top': (178, 18, 21),
        'name': (255, 24, 0)
    }},
    'hinata_hajime': {'colors': {
        'bottom': (154, 160, 108),
        'middle': (195, 183, 134),
        'top': (128, 128, 0),
        'name': (103, 111, 46)
    }},
    'hoshi_ryoma': {'colors': {
        'bottom': (27, 27, 34),
        'middle': (42, 33, 204),
        'top': (92, 113, 168),
        'name': (23, 83, 244)
    }},
    'ikusaba_mukuro': {'colors': {
        'bottom': (235, 210, 192),
        'middle': (106, 88, 66),
        'top': (76, 53, 78),
        'name': (130, 79, 134)
    }},
    'imposter': {'colors': {
        'bottom': (249, 235, 174),
        'middle': (222, 175, 35),
        'top': (68, 108, 108),
        'name': (61, 132, 132)
    }},
    'iruma_miu': {'colors': {
        'bottom': (255, 56, 228),
        'middle': (245, 222, 242),
        'top': (65, 249, 248),
        'name': (233, 1, 182)
    }},
    'ishimaru_kiyotaka': {'colors': {
        'bottom': (0, 70, 177),
        'middle': (3, 26, 59),
        'top': (228, 228, 228),
        'name': (156, 121, 119)
    }},
    'kiibo': {'colors': {
        'bottom': (128, 128, 128),
        'middle': (99, 224, 101),
        'top': (51, 51, 50),
        'name': (34, 250, 54)
    }},
    'kirigiri_kyoko': {'colors': {
        'bottom': (157, 107, 160),
        'middle': (192, 128, 196),
        'top': (89, 73, 90),
        'name': (193, 81, 200)
    }},
    'koizumi_mahiru': {'colors': {
        'bottom': (227, 89, 30),
        'middle': (233, 149, 74),
        'top': (236, 142, 109),
        'name': (227, 89, 30)
    }},
    'komaeda_nagito': {'colors': {
        'bottom': (246, 255, 239),
        'middle': (46, 54, 40),
        'top': (100, 186, 42),
        'name': (94, 143, 61)
    }},
    'kuwata_leon': {'colors': {
        'bottom': (213, 75, 26),
        'middle': (233, 149, 74),
        'top': (206, 100, 63),
        'name': (227, 89, 30)
    }},
    'kuzuryu_fuyuhiko': {'colors': {
        'bottom': (192, 192, 192),
        'middle': (59, 59, 59),
        'top': (191, 171, 114),
        'name': (137, 137, 137)
    }},
    'ludenberg_celestia': {'colors': {
        'bottom': (215, 215, 215),
        'middle': (59, 59, 59),
        'top': (216, 30, 11),
        'name': (199, 49, 34)
    }},
    'maizono_sayaka': {'colors': {
        'bottom': (255, 153, 222),
        'middle': (243, 121, 183),
        'top': (214, 62, 139),
        'name': (214, 62, 127)
    }},
    'mioda_ibuki': {'colors': {
        'bottom': (207, 240, 255),
        'middle': (44, 103, 131),
        'top': (206, 95, 199),
        'name': (157, 82, 152)
    }},
    'momota_kaito': {'colors': {
        'bottom': (92, 91, 92),
        'middle': (254, 245, 255),
        'top': (206, 95, 199),
        'name': (157, 82, 152)
    }},
    'naegi_makoto': {'colors': {
        'bottom': (255, 207, 189),
        'middle': (254, 245, 255),
        'top': (115, 126, 93),
        'name': (128, 156, 72)
    }},
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
    'togami_byakuya': {'colors': {
        'bottom': (65, 86, 53),
        'middle': (69, 115, 43),
        'top': (223, 163, 32),
        'name': (194, 120, 39)
    }},
    'tojo_kirumi': {},
    'tsumiki_mikan': {},
    'yamada_hifumi': {},
    'yonaga_angie': {},
    'yumeno_himiko': {}
}
SHSL_TALENTS = {
    '???': {
        'desc': "! Guess {0} don't remember, huh? Well, better hope it's a good one.",
        'char': ['hinata_hajime', 'kirigiri_kyoko', 'amami_rantaro']
    },
    'Actress': {
        'desc': '! Try as they might, no one could ever hope to emulate the passion {0} put into {1} performances!',
        'char': ['enoshima_mukuro']
    },
    'Adventurer': {
        'desc': "! Well, who doesn't love discovering lands unknown?",
        'char': ['amami_rantaro']
    },
    'Affluent Progeny': {
        'desc': ". Heir to the world's elite, {0} are destined to rule the world from the shadows.",
        'char': ['togami_byakuya', 'imposter'],
        'colors': {
            'bottom': (255, 245, 107),
            'middle': (222, 175, 35),
            'top': (223, 163, 32),
            'name': (194, 120, 39)
        }
    },
    'Akido Master': {
        'desc': '! Hi-yah!',
        'char': ['chabashira_tenko']
    },
    'Analyst': {
        'desc': '. {7} can dissect any situation and see things most other people can\'t.',
        'char': ['kiibo', 'nanami_chiaki', 'saihara_shuichi', 'kirigiri_kyoko']
    },
    'Angler': {
        'desc': '. No one really gets how to gut a fish quite like {0}.',
        'char': ['yonaga_angie', 'owari_akane']
    },
    'Animator': {
        'desc': '! Don\'t forget! Anime is art!',
        'char': ['imposter']
    },
    'Anthropologist': {
        'desc': '. {7} know more about the Salem Witch Trials than anyone else on Earth.',
        'char': ['shinguji_korekiyo']
    },
    'Archer': {
        'desc': '! {9} like Hawkeye up in here!',
        'char': ['pekoyama_peko']
    },
    'Architect': {
        'desc': '. {8} houses are absolutely exquisite.',
        'char': ['ludenberg_celestia']
    },
    'Artist': {
        'desc': '! Pretty colors and lifelike statues are {1} whole deal!',
        'char': ['yonaga_angie']
    },
    'Assassin': {  # PLACEHOLDER UNTIL ALEX BEATS DRV3
        'desc': '. Here\'s the target. You have 24 hours.',
        'char': ['pekoyama_peko', 'ikusaba_mukuro']
    },
    'Astronaut': {
        'desc': '! {7} can reach the stars for sure! If anyone can, it\'s {6}!',
        'char': ['momota_kaito']
    },
    'Baseball Player': {
        'desc': '! Batter up!',
        'char': ['kuwata_leon']
    },
    'Beatboxer': {
        'desc': '! Boots and cats and boots and cats...',
        'char': ['soda_kazuichi', 'asahina_aoi']
    },
    'Blacksmith': {
        'desc': '! Daggers and knives and swords, oh my!',
        'char': ['harukawa_maki', 'ikusaba_mukuro']
    },
    'Biker Gang Leader': {
        'desc': '! Rev your fucking engines! Let\'s tear up this town!',
        'char': ['owada_mondo']
    },
    'Biologist': {
        'desc': '. {8} favorite joke is that one about mitosis.',
        'char': ['gokuhara_gonta']
    },
    'Bodyguard': {  # PLACEHOLDER UNTIL ALEX BEATS DRV3
        'desc': '. Are {0} prepared to lay down {1} life?',
        'char': ['ogami_sakura', 'nidai_nekomaru', 'imposter']
    },
    'Botanist': {
        'desc': '! Ooh, pretty!',
        'char': ['yonaga_angie']
    },
    'Bounty Hunter': {  # PLACEHOLDER UNTIL ALEX BEATS DRV3
        'desc': '. Feel like hunting down any criminals?',
        'char': ['ikusaba_mukuro']
    },
    'Boxer': {
        'desc': '! *DING-DING-DING!* It\'s a TKO!',
        'char': ['ogami_sakura']
    },
    'Breakdancer': {
        'desc': '! Kick it!',
        'char': ['owari_akane']
    },
    'Breeder': {
        'desc': '! Use {1} prowess in the dark arts to... potty-train this dog!',
        'char': ['tanaka_gundham']
    },
    'Broadway Singer': {
        'desc': '. What\'s {1} favorite musical?',
        'char': ['nevermind_sonia', 'maizono_sayaka']
    },
    'CGI Artist': {
        'desc': '! It looks so *real!*',
        'char': ['fujisaki_chihiro']
    },
    'Cheerleader': {
        'desc': '! {14}, they\'re the one, if they don\'t win then that\'s no fun!',
        'char': ['enoshima_mukuro', 'owari_akane']
    },
    'Chemist': {
        'desc': '. Man, that\'s such a boron career. It\'s too basic, if you ask me.',
        'char': ['ikusaba_mukuro', 'tsumiki_mikan']
    },
    'Child Caregiver': {
        'desc': '. {9} basically like a goblin herder.',
        'char': ['harukawa_maki']
    },
    'Clairvoyant': {
        'desc': '! {7} and {1} 30% accuracy rate can predict ANY crime that probably won\'t happen!',
        'char': ['hagakure_yasuhiro']
    },
    'Clown': {
        'desc': '! {9} a clown! Honk honk! :o)',
        'char': ['iruma_miu', 'ouma_kokichi', 'yamada_hifumi']
    },
    'Composer': {
        'desc': '. Popping out songs one after another ain\'t easy, but it\'s {1} way of life.',
        'char': ['akamatsu_kaede']
    },
    'Con Artist': {
        'desc': '. {9} a slimy bastard who can convince anyone anything is a good idea.',
        'char': ['ouma_kokichi', 'ludenberg_celestia']
    },
    'Confectioner': {
        'desc': '! How sweet of {0}!',
        'char': ['hanamura_teruteru']
    },
    'Conspiracy Theorist': {
        'desc': '. So you think the moon landing was faked, huh? Well, have you heard the MOON is fake, too?',
        'char': ['hagakure_yasuhiro']
    },
    'Cook': {
        'desc': '! Bon Appetit!',
        'char': ['hanamura_teruteru']
    },
    'Curator': {
        'desc': '. {8} collection is far more impressive than the Smithsonian.',
        'char': ['shinguji_korekiyo']
    },
    'Despair': {
        'desc': '. Despair is not a goal, or a set of principles, or a lifestyle, or even an instinct... '
                'It\'s what defines {6} as {14}!',
        'char': ['enoshima_junko']
    },
    'Detective': {
        'desc': '! And the killer is... you!',
        'char': ['kirigiri_kyoko', 'shuichi_saihara']
    },
    'Drug Dealer': {
        'desc': '. {11} stuck some stuff in some pretty gross places to get to the top, but {0} don\'t regret it.',
        'char': ['komaeda_nagito']
    },
    'Drummer': {
        'desc': '! Any band is only as good as its drummer!',
        'char': ['mioda_ibuki']
    },
    'DJ': {
        'desc': '! Lay down some beats, man!',
        'char': ['mioda_ibuki']
    },
    'Entomologist': {
        'desc': '... so, if I find a spider, do I bring it to you?',
        'char': ['gokuhara_gonta']
    },
    'Entrepreneur': {
        'desc': '',
        'char': ['togami_byakuya', 'imposter']
    },
    'Exorcist': {
        'desc': '. The power of Christ compels you!',
        'char': ['yonaga_angie']
    },
    'Fanfic Creator': {
        'desc': '! So, what next? Maybe a slow-burn coffee shop AU with some self-inserts, a handful of OC\'s, '
                'F/F and M/M, a little OOC if necessary, but all in all just fanservice fic for Danganronpa?',
        'char': ['yamada_hifumi']
    },
    'Farmer': {
        'desc': '! Do {1} have a dog named Bingo? Or... just Ingo? Or Ngo?',
        'char': ['owari_akane']
    },
    'Fashionista': {
        'desc': '! Looking cool, {14}!',
        'char': ['enoshima_mukuro']
    },
    'Film Director': {
        'desc': '! When on set, nobody questions {1} judgement.',
        'char': ['naegi_makoto', 'kuzuryu_fuyuhiko', 'amami_rantaro', 'akamatsu_kaede', 'shirogane_tsumugi',
                 'tanaka_gundham']
    },
    'Forum Admin': {
        'desc': '. {11} seen some serious shit.',
        'char': ['kuzuryu_fuyuhiko']
    },
    'Gambler': {
        'desc': '',
        'char': ['ludenberg_celestia']
    },
    'Gamer': {
        'desc': '',
        'char': ['nanami_chiaki']
    },
    'Golfer': {
        'desc': '. No one can beat the power of a true Scottish swing.',
        'char': ['nevermind_sonia']
    },
    'Guitarist': {
        'desc': '',
        'char': ['mioda_ibuki']
    },
    'Gymnast': {
        'desc': '',
        'char': ['owari_akane']
    },
    'Hacker': {
        'desc': '. {7} didn\'t actually get {1} title from some school official, '
                '{0} got it by hacking into the servers and giving it to {3}.',
        'char': ['fujisaki_chihiro']
    },
    'Hairstylist': {
        'desc': '',
        'char': ['enoshima_mukuro']
    },
    'Hope': {
        'desc': '',
        'char': ['naegi_makoto']
    },
    'Housekeeper': {
        'desc': '! You\'re the ultimate cleaning machine!',
        'char': ['tojo_kirumi']
    },
    'Hypnotist': {
        'desc': '. People ought to be cautious around {6} -- let down your guard for even a second and you can no '
                'longer think for yourself.',
        'char': ['hagakure_yasuhiro']
    },
    'Idol': {
        'desc': '',
        'char': ['maizono_sayaka']
    },
    'Impostor': {
        'desc': '. No one truly knows who {0} are beneath the mask... or that {2} even wearing one at all.',
        'char': ['pekoyama_peko']
    },  # PLACEHOLDER UNTIL ALEX BEATS DR2
    'Internet Troll': {
        'desc': '. {9} really good at pissing people off online.',
        'char': ['ouma_kokichi']
    },
    'Inventor': {
        'desc': '',
        'char': ['iruma_miu']
    },
    'Lawyer': {
        'desc': '',
        'char': ['kuzuryu_fuyuhiko']
    },
    'Lucky Student': {
        'desc': '',
        'char': ['komaeda_nagito', 'naegi_makoto']
    },
    'Magician': {
        'desc': '! Prepare to be amazed!',
        'char': ['yumeno_himiko']
    },
    'Maid': {
        'desc': '',
        'char': ['tojo_kirumi']
    },
    'Martial Artist': {
        'desc': '',
        'char': ['ogami_sakura']
    },
    'Makeup Artist': {
        'desc': '',
        'char': ['enoshima_mukuro']
    },
    'Matchmaker': {
        'desc': '',
        'char': ['enoshima_mukuro', 'yonaga_angie', 'maizono_sayaka']
    },
    'Mechanic': {
        'desc': '. Every tractor {0} work on is sexy.',
        'char': ['soda_kazuichi']
    },
    'Medium': {
        'desc': '',
        'char': ['hagakure_yasuhiro']
    },
    'Merchant': {
        'desc': '. No one knows supply and demand better than {6}, and {0} always have just enough stock to match what '
                'the public desires.',
        'char': ['tanaka_gundham', 'shinguji_korekiyo', 'hagakure_yasuhiro']
    },
    'Model': {
        'desc': '',
        'char': ['enoshima_mukuro']
    },
    'Moral Compass': {
        'desc': '. {7} are the best at telling other people how to act.',
        'char': ['ishimaru_kiyotaka']
    },
    'Musician': {
        'desc': '',
        'char': ['mioda_ibuki']
    },
    'Neurologist': {
        'desc': '',
        'char': ['tsumiki_mikan']
    },
    'Ninja': {
        'desc': '}, lying hidden in the shadows. Watch out.',
        'char': ['pekoyama_peko']
    },
    'Nurse': {
        'desc': '',
        'char': ['tsumiki_mikan']
    },
    'Pharmacist': {
        'desc': '. It\'s not totally clear how {0} managed to become one at such a young age, but regardless, {0} are.',
        'char': ['tsumiki_mikan']
    },
    'Photographer': {
        'desc': '! Say cheese!',
        'char': ['koizumi_mahiru']
    },
    'Poet': {
        'desc': '. {7} just have a way with words others can only dream of matching.',
        'char': ['fukawa_toko']
    },
    'Prankster': {
        'desc': '. What devious thing did {0} do to get this title...?',
        'char': ['ouma_kokichi']
    },
    'Prisoner': {
        'desc': '',
        'char': ['hoshi_ryoma']
    },
    'Puppeteer': {
        'desc': '. No strings on {1} puppets, no sir!',
        'char': ['iruma_miu', 'shinguji_korekiyo']
    },
    'Psychologist': {
        'desc': '',
        'char': ['tsumiki_mikan']
    },
    'Pianist': {
        'desc': '',
        'char': ['akamatsu_kaede']
    },
    'Pilot': {
        'desc': '. Do a barrel roll!',
        'char': ['tanaka_gundham']
    },
    'Police Officer': {
        'desc': '',
        'char': ['ishimaru_kiyotaka']
    },
    'Priest': {
        'desc': '. With just a wave of {1} hand, {0} can enlighten hundreds at a time.',
        'char': ['yonaga_angie']
    },
    'Princess': {
        'desc': '',
        'char': ['nevermind_sonia']
    },
    'Programmer': {
        'desc': '! Did you know this bot is written in Python using the discord.py API?',
        'char': ['fujisaki_chihiro']
    },
    'Pyrotechnician': {
        'desc': '. \'Cause baby, you\'re a firework!',
        'char': ['soda_kazuichi', 'kuwata_leon']
    },
    'Robot': {
        'desc': '! Beep boop bop beep!',
        'char': ['kiibo']
    },
    'Sailor': {
        'desc': '',
        'char': ['hinata_hajime']
    },
    'Scout': {
        'desc': '. Though high adventure may be fun, there is nothing quite like giving back to one\'s community.',
        'char': ['ishimaru_kiyotaka']
    },
    'Secret Agent': {
        'desc': '. {7} have a license to kill and {0} aren\'t afraid to use it.',
        'char': ['kuzuryu_fuyuhiko']
    },
    'Serial Killer': {
        'desc': '',
        'char': ['genocider']
    },
    'SFX Artist': {
        'desc': '. It\'s amazing what sounds you can make with just your mouth.',
        'char': ['hinata_hajime', 'momota_kaito']
    },
    'Skiier': {
        'desc': '. Cutting through powder, to {6}, is just as easy as riding a bike.',
        'char': ['kuwata_leon']
    },
    'Soccer Player': {
        'desc': '',
        'char': ['amami_rantaro']
    },
    'Soldier': {
        'desc': '. The battlefield is where {0} truly belong.',
        'char': ['ikusaba_mukuro']
    },
    'Sniper': {
        'desc': '. Headshot.',
        'char': ['ikusaba_mukuro']
    },
    'Snowboarder': {
        'desc': '. It\'s like being a skiier, but way cooler.',
        'char': ['momota_kaito']
    },
    'Surgeon': {
        'desc': '',
        'char': ['tsumiki_mikan']
    },
    'Street Fighter': {
        'desc': '',
        'char': ['chabashira_tenko']
    },
    'Stunt Double': {
        'desc': '',
        'char': ['kuwata_leon', 'hoshi_ryoma']
    },
    'Superhero': {
        'desc': '',
        'char': ['kiibo']
    },
    'Supervillain': {
        'desc': '! What separates a regular villain from a super one? Why, presentation, of course!',
        'char': ['ouma_kokichi']
    },
    'Supreme Leader': {
        'desc': '',
        'char': ['ouma_kokichi']
    },
    'Survivor': {
        'desc': '',
        'char': ['amami_rantaro']
    },
    'Swimmer': {
        'desc': '! {7} swear {0} could swim across the ocean if it was legal!',
        'char': ['asahina_aoi']
    },
    'Swordsman': {
        'desc': '. While most others spend their time playing video games or watching TV, {0} study the blade.',
        'char': ['pekoyama_peko']
    },
    'Tailor': {
        'desc': '. Capes aren\'t usually fashionable, but the way {0} make it, anyone can rock that shit.',
        'char': ['tojo_kirumi']
    },
    'Team Manager': {
        'desc': '',
        'char': ['nidai_nekomaru']
    },
    'Tennis Pro': {
        'desc': '',
        'char': ['hoshi_ryoma']
    },
    'Test Subject': {
        'desc': '. The Enrichment Center is committed to the well being of all participants. Cake and grief counseling '
                'will be available at the conclusion of the test.',
        'char': ['hinata_hajime']
    },
    'Therapist': {
        'desc': '. Of course, {0} can\'t talk about it that much, since patient confidentiality is {1} number 1 '
                'priority.',
        'char': ['fujisaki_chihiro', 'akamatsu_kaede', 'kirigiri_kyoko', 'nanami_chiaki']
    },
    'Traditional Dancer': {
        'desc': '',
        'char': ['saiyonji_hiyoko']
    },
    'Translator': {
        'desc': '. {8} ability to be fluent in so many language baffles scientists.',
        'char': ['hinata_hajime']
    },
    'VFX Artist': {
        'desc': '. {7} had it better in the 80\'s.',
        'char': ['soda_kazuichi', 'imposter', 'momota_kaito', 'tanaka_gundham']
    },
    'Violinist': {
        'desc': '',
        'char': ['akamatsu_kaede']
    },
    'Voice Actor': {
        'desc': '. {9} able to switch voices on a dime, and none of them sound anything alike.',
        'char': ['enoshima_junko', 'mioda_ibuki']
    },
    'Wrestler': {
        'desc': '! Let\'s settle this in the ring!',
        'char': ['ogami_sakura']
    },
    'Writer': {
        'desc': '',
        'char': ['fukawa_toko']
    },
    'Yakuza': {
        'desc': '',
        'char': ['kuzuryu_fuyuhiko']
    },
    'Yoga Guru': {
        'desc': '. All {1} chakras are open and flowing the sweet nectar of the soul.',
        'char': ['hagakure_yasuhiro']}
}
SHSL_PRONOUNS = [
    ('you', 'they'),
    ('your', 'their'),
    ("you're", "they're"),
    ('yourself', 'themselves'),
    ("you've", "they've"),
    ("you'll", "they'll"),
    ('you', 'them'),
    ('You', 'They'),
    ('Your', 'Their'),
    ("You're", "They're"),
    ('Yourself', 'Themselves'),
    ("You've", "They've"),
    ("You'll", "They'll"),
    ('You', 'Them')
]


async def ultimate(bot, message, argument):
    """
    Generates an ultimate title for the user, complete with an image.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Call the master function with shsl set to False so that the title says Ultimate instead of SHSL.
    await do_shsl_thing(message, argument, False)


async def shsl(bot, message, argument):
    """
    Generates a SHSL title for the user, complete with an image.

    Arguments:
        bot (lib.bot.JadieClient) : The bot object that called this command.
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
    """
    # Call the master function with shsl set to True so that the title says SHSL instead of Ultimate.
    await do_shsl_thing(message, argument, True)


async def do_shsl_thing(message, argument, use_shsl=True):
    """
    Assigns the user a(n) SHSL / ultimate talent, like in Danganronpa.

    Arguments:
        message (discord.message.Message) : The discord message object that triggered this command.
        argument (str) : The command's argument, if any.
        use_shsl (bool) : Whether to use the SHSL title or the Ultimate title.
    """
    # Tries to get a valid user out of the argument.
    try:
        student = arguments.get_closest_users(message, argument, exclude_bots=False, limit=1)[0]
        uses_author = False

    # On NoUserSpecifiedError, use the message's author.
    except NoUserSpecifiedError:
        student = message.author
        uses_author = True

    # On UnableToFindUserError, tell the user they couldn't find the desired one.
    except UnableToFindUserError:
        logging.info(message, f"requested ultimate/shsl title for user '{argument}', invalid")
        return await messaging.send_text_message(message, f"Could not find user '{argument}'.")

    # On CannotAccessUserlistError, log an error and send an apology message.
    except CannotAccessUserlistError:
        logging.error(message, 'Failed to access the userlist')
        return await messaging.send_text_message(message, 'There was an error accessing the userlist. '
                                                          'Try @ mentioning someone instead.')

    # Gets the talent.
    talent = random.choice([key for key in SHSL_TALENTS])
    talent_dict = SHSL_TALENTS[talent]

    # Gets the character. Valid characters are in the talent_dict.
    character = random.choice(talent_dict['char'])
    character_dict = SHSL_CHARACTER_ATTRIBUTES[character]

    # If the character doesn't have any default colors, then update them with some default values.
    if 'colors' not in character_dict:
        character_dict.update({'colors': {
            'bottom': (255, 255, 255),
            'middle': (255, 255, 255),
            'top': (255, 255, 255),
            'name': (128, 128, 128)
        }})

    # Creates the title string.
    title_str = f'{"You are" if uses_author else discord_info.get_photogenic_username(student) + " is"} the '\
                f'{"SHSL" if use_shsl else "Ultimate"} {talent}{talent_dict["desc"]}'
    # Formats the title string with the proper pronouns.
    for i in range(len(SHSL_PRONOUNS)):
        title_str = title_str.replace('{' + str(i) + '}', SHSL_PRONOUNS[i][0 if uses_author else 1])
    # Replaces the {14} in the title string with the name of the student.
    title_str.replace('{14}', discord_info.get_photogenic_username(student))

    # Creates the background image layers.
    background_bottom = assets.open_image('danganronpa_bg/drbottom.png')
    background_middle = assets.open_image('danganronpa_bg/drmiddle.png')
    background_top = assets.open_image('danganronpa_bg/drtop.png')

    # Opens the student sprite.
    student_sprite = assets.open_image(os.path.join('danganronpa_chars', f'{character}{SHSL_SPRITE_FILETYPE}'))

    # Creates the new images that will be CREATED through this method.
    user_name = Image.new('L', (1280, 720))
    user_colorchar = Image.new('L', (1280, 720))
    user_border = Image.new('L', (1280, 720))
    talent_text = Image.new('L', (1280, 720))
    talent_blur = Image.new('L', (1280, 720))

    # Creates user name without emoji.
    student_name = discord_info.get_photogenic_username(student)
    # Iterate through each character in the name and pull out any characters with ord's greater than the max.
    i = 0
    while i < len(student_name):
        if ord(student_name[i]) > SHSL_NAME_MAX_ORD:
            student_name = student_name.strip(student_name[i])
        else:
            i += 1
    # Now, normalize the string.
    student_name = parsing.normalize_string(student_name)

    # Creates standard user name (white).
    user_writer = ImageDraw.Draw(user_name)
    user_font = assets.open_font(SHSL_NAME_FONT, 100)
    user_writer.text((835 - int(user_font.getsize(student_name)[0] / 2), 0), student_name, font=user_font, fill=255)
    user_name = user_name.rotate(-12.5, center=(-8, 200), resample=Image.BILINEAR, translate=(0, 154))

    # Creates colored user letter.
    user_writer = ImageDraw.Draw(user_colorchar)
    user_writer.text((835 - int(user_font.getsize(student_name)[0] / 2), 0), student_name[0], font=user_font, fill=255)
    user_colorchar = user_colorchar.rotate(-12.5, center=(-8, 200), resample=Image.BILINEAR, translate=(0, 154))

    # Creates user border.
    user_writer = ImageDraw.Draw(user_border)
    user_writer.text((831 - int(user_font.getsize(student_name)[0] / 2), 0), student_name, font=user_font,
                     stroke_width=5, fill=255)
    user_border = user_border.rotate(-12.5, center=(-8, 200), resample=Image.BILINEAR, translate=(0, 150))

    # Creates talent text.
    talent_writer = ImageDraw.Draw(talent_text)
    talent_font = assets.open_font(SHSL_TALENT_FONT, 54)
    talent_writer.text((855 - int(talent_font.getsize(('SHSL ' if use_shsl else 'Ultimate ') + talent)[0] / 2), 0),
                       ('SHSL ' if use_shsl else 'Ultimate ') + talent, font=talent_font, fill=255)
    talent_text = talent_text.rotate(-12.5, center=(0, 205), resample=Image.BILINEAR, translate=(-40, 279))

    # Creates talent blur.
    talent_writer = ImageDraw.Draw(talent_blur)
    talent_writer.text((855 - int(talent_font.getsize(('SHSL ' if use_shsl else 'Ultimate ') + talent)[0] / 2), 0),
                       ('SHSL ' if use_shsl else 'Ultimate ') + talent, font=talent_font, stroke_width=2, fill=255)
    talent_blur = talent_blur.rotate(-12.5, center=(0, 202), resample=Image.BILINEAR, translate=(-40, 279))
    talent_blur = talent_blur.filter(ImageFilter.GaussianBlur(10))

    # Modify the background layer's bottom layer to better fit the talent.
    background_bottom = ImageOps.colorize(
        background_bottom.convert('L'),
        black=(0, 0, 0),
        white=talent_dict['colors']['bottom'] if 'colors' in talent_dict else character_dict['colors']['bottom']
    )

    # Modify the background layer's middle layer to better fit the talent.
    background_middle_2 = ImageOps.colorize(
        background_middle.convert('L'),
        black=(0, 0, 0),
        white=talent_dict['colors']['middle'] if 'colors' in talent_dict else character_dict['colors']['middle']
    ).convert('RGB')

    # Modify the background layer's top layer to better fit the talent.
    background_top_2 = ImageOps.colorize(
        background_top.convert('L'),
        black=(0, 0, 0),
        white=(255, 255, 255),
        mid=talent_dict['colors']['top'] if 'colors' in talent_dict else character_dict['colors']['top']
    )

    # Modify the colored character of the user's name.
    user_colorchar_c = ImageOps.colorize(
        user_colorchar.convert('L'),
        black=(0, 0, 0),
        white=talent_dict['colors']['name'] if 'colors' in talent_dict else character_dict['colors']['name']
    )

    # Modify the color of the talent blur.
    talent_blur_c = ImageOps.colorize(
        talent_blur.convert('L'),
        black=(255, 255, 255),
        white=talent_dict['colors']['name'] if 'colors' in talent_dict else character_dict['colors']['name']
    )

    # Modify the colors of mutliple background elements (just made black).
    user_border_c = ImageOps.colorize(user_border.convert('L'), black=(0, 0, 0), white=(0, 0, 0))
    talent_text_c = ImageOps.colorize(talent_text.convert('L'), black=(0, 0, 0), white=(0, 0, 0))
    student_sprite_black = ImageOps.colorize(student_sprite.convert('L'), black=(0, 0, 0), white=(0, 0, 0))

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
    ultimate_image.paste(student_sprite_black, (265 - int(student_sprite.size[0] / 2) - 75,
                                                ultimate_image.size[1] - student_sprite.size[1]), student_sprite)
    ultimate_image.paste(student_sprite, (265 - int(student_sprite.size[0] / 2),
                                          ultimate_image.size[1] - student_sprite.size[1] + 30), student_sprite)

    # Sends the message.
    logging.info(message, 'requested ultimate/shsl talent')
    await messaging.send_image_based_embed(message, ultimate_image, title_str, SHSL_EMBED_COLOR)


# Command values
DEVELOPER_COMMAND_DICT = {
    'shsl': shsl,
    'ultimate': ultimate
}

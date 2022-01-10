"""
Assets loads assets. Not much else to it, really. Just loads assets.
Checks whether all the assets are present on startup.
"""
# Local Imports
from lib.util.exceptions import InvalidAssetFileDirError

# Package Imports
from PIL import Image, ImageFont
import random
import os

# Assets dir.
ASSETS_DIR = 'assets'

# List of asset files we should expect to see in the asset folder.
EXPECTED_ASSET_FILES = [
    'heart.png', 'Jadi3Pi.png',
    'cards/backgrounds/felt_blue.jpeg', 'cards/backgrounds/felt_green.jpeg', 'cards/backgrounds/felt_red.jpeg',
    'cards/backgrounds/uno_lobby.png',
    'cards/uno/flat/blue_0.png', 'cards/uno/flat/blue_1.png', 'cards/uno/flat/blue_2.png', 'cards/uno/flat/blue_3.png',
    'cards/uno/flat/blue_4.png', 'cards/uno/flat/blue_5.png', 'cards/uno/flat/blue_6.png', 'cards/uno/flat/blue_7.png',
    'cards/uno/flat/blue_8.png', 'cards/uno/flat/blue_9.png',
    'cards/uno/flat/blue_draw2.png', 'cards/uno/flat/blue_reverse.png', 'cards/uno/flat/blue_skip.png',
    'cards/uno/flat/green_0.png', 'cards/uno/flat/green_1.png', 'cards/uno/flat/green_2.png',
    'cards/uno/flat/green_3.png', 'cards/uno/flat/green_4.png', 'cards/uno/flat/green_5.png',
    'cards/uno/flat/green_6.png', 'cards/uno/flat/green_7.png', 'cards/uno/flat/green_8.png',
    'cards/uno/flat/green_9.png',
    'cards/uno/flat/green_draw2.png', 'cards/uno/flat/green_reverse.png', 'cards/uno/flat/green_skip.png',
    'cards/uno/flat/red_0.png', 'cards/uno/flat/red_1.png', 'cards/uno/flat/red_2.png', 'cards/uno/flat/red_3.png',
    'cards/uno/flat/red_4.png', 'cards/uno/flat/red_5.png', 'cards/uno/flat/red_6.png', 'cards/uno/flat/red_7.png',
    'cards/uno/flat/red_8.png', 'cards/uno/flat/red_9.png',
    'cards/uno/flat/red_draw2.png', 'cards/uno/flat/red_reverse.png', 'cards/uno/flat/red_skip.png',
    'cards/uno/flat/yellow_0.png', 'cards/uno/flat/yellow_1.png', 'cards/uno/flat/yellow_2.png',
    'cards/uno/flat/yellow_3.png', 'cards/uno/flat/yellow_4.png', 'cards/uno/flat/yellow_5.png',
    'cards/uno/flat/yellow_6.png', 'cards/uno/flat/yellow_7.png', 'cards/uno/flat/yellow_8.png',
    'cards/uno/flat/yellow_9.png',
    'cards/uno/flat/wild.png', 'cards/uno/flat/wild_draw4.png', 'cards/uno/flat/back.png',
    'cards/uno/lobby/0_blank.png', 'cards/uno/lobby/0_blue.png', 'cards/uno/lobby/0_green.png',
    'cards/uno/lobby/0_red.png', 'cards/uno/lobby/0_yellow.png',
    'cards/uno/lobby/1_blank.png', 'cards/uno/lobby/1_blue.png', 'cards/uno/lobby/1_green.png',
    'cards/uno/lobby/1_red.png', 'cards/uno/lobby/1_yellow.png',
    'cards/uno/lobby/2_blank.png', 'cards/uno/lobby/2_blue.png', 'cards/uno/lobby/2_green.png',
    'cards/uno/lobby/2_red.png', 'cards/uno/lobby/2_yellow.png',
    'cards/uno/lobby/3_blank.png', 'cards/uno/lobby/3_blue.png', 'cards/uno/lobby/3_green.png',
    'cards/uno/lobby/3_red.png', 'cards/uno/lobby/3_yellow.png',
    'cards/uno/lobby/4_blank.png', 'cards/uno/lobby/4_blue.png', 'cards/uno/lobby/4_green.png',
    'cards/uno/lobby/4_red.png', 'cards/uno/lobby/4_yellow.png',
    'cards/uno/lobby/5_blank.png', 'cards/uno/lobby/5_blue.png', 'cards/uno/lobby/5_green.png',
    'cards/uno/lobby/5_red.png', 'cards/uno/lobby/5_yellow.png',
    'cards/uno/lobby/6_blank.png', 'cards/uno/lobby/6_blue.png', 'cards/uno/lobby/6_green.png',
    'cards/uno/lobby/6_red.png', 'cards/uno/lobby/6_yellow.png',
    'cards/uno/lobby/7_blank.png', 'cards/uno/lobby/7_blue.png', 'cards/uno/lobby/7_green.png',
    'cards/uno/lobby/7_red.png', 'cards/uno/lobby/7_yellow.png',
    'cards/uno/lobby/8_blank.png', 'cards/uno/lobby/8_blue.png', 'cards/uno/lobby/8_green.png',
    'cards/uno/lobby/8_red.png', 'cards/uno/lobby/8_yellow.png',
    'cards/uno/lobby/9_blank.png', 'cards/uno/lobby/9_blue.png', 'cards/uno/lobby/9_green.png',
    'cards/uno/lobby/9_red.png', 'cards/uno/lobby/9_yellow.png',
    'danganronpa_bg/drbottom.png', 'danganronpa_bg/drmiddle.png', 'danganronpa_bg/drtop.png',
    'danganronpa_chars/akamatsu_kaede.webp', 'danganronpa_chars/amami_rantaro.webp',
    'danganronpa_chars/asahina_aoi.webp', 'danganronpa_chars/chabashira_tenko.webp',
    'danganronpa_chars/enoshima_junko.webp', 'danganronpa_chars/enoshima_mukuro.webp',
    'danganronpa_chars/fujisaki_chihiro.webp', 'danganronpa_chars/fukawa_toko.webp',
    'danganronpa_chars/genocider.webp', 'danganronpa_chars/gokuhara_gonta.webp',
    'danganronpa_chars/hagakure_yasuhiro.webp', 'danganronpa_chars/hanamura_teruteru.webp',
    'danganronpa_chars/harukawa_maki.webp', 'danganronpa_chars/hinata_hajime.webp',
    'danganronpa_chars/hoshi_ryoma.webp', 'danganronpa_chars/ikusaba_mukuro.webp', 'danganronpa_chars/imposter.webp',
    'danganronpa_chars/iruma_miu.webp', 'danganronpa_chars/ishimaru_kiyotaka.webp', 'danganronpa_chars/kiibo.webp',
    'danganronpa_chars/kirigiri_kyoko.webp', 'danganronpa_chars/koizumi_mahiru.webp',
    'danganronpa_chars/komaeda_nagito.webp', 'danganronpa_chars/kuwata_leon.webp',
    'danganronpa_chars/kuzuryu_fuyuhiko.webp', 'danganronpa_chars/ludenberg_celestia.webp',
    'danganronpa_chars/maizono_sayaka.webp', 'danganronpa_chars/mioda_ibuki.webp',
    'danganronpa_chars/momota_kaito.webp', 'danganronpa_chars/naegi_makoto.webp',
    'danganronpa_chars/nanami_chiaki.webp', 'danganronpa_chars/nevermind_sonia.webp',
    'danganronpa_chars/nidai_nekomaru.webp', 'danganronpa_chars/ogami_sakura.webp',
    'danganronpa_chars/ouma_kokichi.webp', 'danganronpa_chars/owada_mondo.webp',
    'danganronpa_chars/owari_akane.webp', 'danganronpa_chars/pekoyama_peko.webp',
    'danganronpa_chars/saihara_shuichi.webp', 'danganronpa_chars/saiyonji_hiyoko.webp',
    'danganronpa_chars/shinguji_korekiyo.webp', 'danganronpa_chars/shirogane_tsumugi.webp',
    'danganronpa_chars/soda_kazuichi.webp', 'danganronpa_chars/tanaka_gundham.webp',
    'danganronpa_chars/togami_byakuya.webp', 'danganronpa_chars/tojo_kirumi.webp',
    'danganronpa_chars/tsumiki_mikan.webp', 'danganronpa_chars/yamada_hifumi.webp',
    'danganronpa_chars/yonaga_angie.webp', 'danganronpa_chars/yumeno_himiko.webp',
    'fonts/arial.ttf', 'fonts/arial_bold.ttf', 'fonts/gill_sans.ttf', 'fonts/times_sans_serif.ttf'
]
# List of asset directories that should have at least ONE image in them.
EXPECTED_POPULATED_ASSET_DIRS = [
    'feliz/angry/lunes', 'feliz/angry/martes', 'feliz/angry/miercoles', 'feliz/angry/jueves', 'feliz/angry/viernes',
    'feliz/angry/sabado', 'feliz/angry/domingo',
    'feliz/happy/lunes', 'feliz/happy/martes', 'feliz/happy/miercoles', 'feliz/happy/jueves', 'feliz/happy/viernes',
    'feliz/happy/sabado', 'feliz/happy/domingo'
]


def asset_check():
    """
    Makes sure that every expected asset file is accounted for.
    """
    # Required imports
    from lib.util.exceptions import MissingAssetFileError
    import os

    # First, check that the assets folder does exist.
    if not os.path.isdir(ASSETS_DIR):
        raise MissingAssetFileError('Asset folder missing from directory')

    # Detect if any asset files are missing.
    for asset_file in EXPECTED_ASSET_FILES:
        if not os.path.isfile(os.path.join(ASSETS_DIR, asset_file)):
            raise MissingAssetFileError(asset_file)


def open_image(filename):
    """
    Opens the requested image.

    Arguments:
        filename (str) : The image's filename.

    Returns:
        PIL.Image.Image : The opened image.
    """
    return Image.open(get_asset_path(filename)).convert('RGBA')


def open_font(filename, size):
    """
    Opens the requested font.

    Arguments:
        filename (str) : The font's filename.

    Returns:
        PIL.ImageFont : The opened font.
    """
    return ImageFont.truetype(os.path.join(ASSETS_DIR, 'fonts', filename), size=size)


def get_asset_path(filename):
    """
    Gets the filepath for an asset.

    Arguments:
        filename (str) : The asset's path.

    Returns:
        str : The asset's path.
    """
    return os.path.join(ASSETS_DIR, filename)


def get_random_file_from_folder(folder):
    """
    Picks a random file out of the given asset folder.

    Arguments:
        folder (str) : The folder.

    Raises:
        InvalidAssetFileDirError : The folder does not exist, or is not a valid populated asset dir.
    """
    # Assert that it is a directory.
    if not os.path.isdir(get_asset_path(folder)):
        raise InvalidAssetFileDirError(folder)

    # Also assert that it's one we have loaded.
    if folder.replace('\\', '/') not in EXPECTED_POPULATED_ASSET_DIRS:
        raise InvalidAssetFileDirError(folder)

    # Pick a random file from there and join it with the folder.
    chosen_file = random.choice(os.listdir(get_asset_path(folder)))
    chosen_file = os.path.join(get_asset_path(folder), chosen_file)

    # Return.
    return chosen_file

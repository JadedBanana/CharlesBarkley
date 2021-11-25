"""
Assets loads assets. Not much else to it, really. Just loads assets.
Checks whether all the assets are present on startup.
"""
# Assets dir.
ASSETS_DIR = 'assets'

# List of asset files we should expect to see in the asset folder.
EXPECTED_ASSET_FILES = [
    'heart.png',
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
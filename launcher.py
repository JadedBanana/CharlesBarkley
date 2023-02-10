"""
Jadi3Pi launch file.
Uses the lib.cron_checker class to make sure that only one instance of the bot is running at a time.
If the bot isn't running right now, then the bot gets launched.
"""


def launch():
    """
    Launch method.
    Performs some checks, then launches the bot.
    """
    # Parse running parameters.
    parse_running_parameters()

    # Run the primary initializers.
    run_initializers()

    # Now, finally launch the bot.
    from lib import bot
    bot.launch()


def parse_running_parameters():
    """
    Parses running parameters.
    At the moment, only checks for a new working directory.
    """
    # Imports.
    import sys
    import os

    # Iterate through arguments and test for what they start with.
    for arg in sys.argv:
        if arg.startswith('working_dir='):

            # Found a new working dir, switch to there.
            os.chdir(arg[12:])


def run_initializers():
    """
    Runs the initializers.
    """
    # First things first, load up the .env variables.
    from lib.util import environment
    environment.load_dotenv()

    # Then, check the asset files.
    from lib.util import assets
    assets.asset_check()

    # Performing logger setup.
    from lib.util import logger
    logger.basic_setup()

    # Logging message.
    import logging
    logging.info('Passed startup checks, performing basic setup')


# If this is the main thread, launch.
if __name__ == '__main__':
    launch()

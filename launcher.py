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
    # First things first, see if any working directory was provided in the running arguments.
    import sys
    import os

    # Iterate through arguments and test for what they start with.
    for arg in sys.argv:
        if arg.startswith('working_dir='):

            # Found a new working dir, switch to there.
            os.chdir(arg[12:])

    # First things first, load up the .env variables.
    from lib.util import environment
    environment.load_dotenv()

    # Then, check the asset files.
    from lib.util import assets
    assets.asset_check()

    # Next, see if we're supposed to do the croncheck. If so, do that!
    from lib.util import cron
    if environment.get('LAUNCH_RUN_CRONCHECK'):

        # Import cron and get the current cron string.
        from time import sleep
        cron_str_1 = cron.get_cron_string()

        # If there isn't a cron string, we try again a second later.
        if not cron_str_1:
            sleep(1)
            cron_str_1 = cron.get_cron_string()

        # If there STILL isn't a cron string, then we immediately move on to the next part.
        # Otherwise, we test for a second cron string about a minute later.
        if cron_str_1:
            # Wait a little less than a minute, then get the current cron string again.
            sleep(55)
            cron_str_2 = cron.get_cron_string()

            # If the two cron strings are not the same, then we exit.
            if cron_str_1 != cron_str_2:
                exit(0)

    # Performing logger setup.
    from lib.util import logger
    logger.basic_setup()

    # Performing tempfile setup.
    from lib.util import temp_files
    temp_files.initialize()

    # Logging message.
    import logging
    logging.info('Passed startup checks, performing basic setup')

    # Start the cron loop so that any instances of this class after this one don't start while we're running.
    cron_thread = cron.CronThread()
    cron_thread.start()

    # Start the tempfiles loop so that old temp files get deleted.
    temp_files_thread = temp_files.TempFilesThread()
    temp_files_thread.start()

    # Get the current thread.
    import threading
    main_thread = threading.current_thread()

    # Run the watchdog class.
    from lib.util import watchdog
    watchdog = watchdog.Watchdog(main_thread, cron_thread, temp_files_thread)
    watchdog.start()

    # Now, finally launch the bot.
    from lib import bot
    bot.launch()


# If this is the main thread, launch.
if __name__ == '__main__':
    launch()

"""
Jadi3Pi launch file.
Uses the lib.cron_checker class to make sure that only one instance of the bot is running at a time.
If the bot isn't running right now, then the bot gets launched.
"""

if __name__ == '__main__':

    # First things first, load up the .env variables.
    from lib.util import environment
    environment.load_dotenv()

    # Next, see if we're supposed to do the croncheck. If so, do that!
    from lib import cron_checker
    if environment.get('LAUNCH_RUN_CRONCHECK'):

        # Import cron and get the current cron string.
        from time import sleep
        cron_str_1 = cron_checker.get_cronstring()

        # If there isn't a cron string, we try again a second later.
        if not cron_str_1:
            sleep(1)
            cron_str_1 = cron_checker.get_cronstring()

        # If there STILL isn't a cron string, then we immediately move on to the next part.
        # Otherwise, we test for a second cron string about a minute later.
        if cron_str_1:
            # Wait a little less than a minute, then get the current cron string again.
            sleep(55)
            cron_str_2 = cron_checker.get_cronstring()

            # If the two cron strings are not the same, then we exit.
            if cron_str_1 != cron_str_2:
                exit(0)

    # Performing logger setup.
    from lib.util import logger
    logger.basic_setup()

    # Logging message.
    import logging
    logging.info('Passed startup checks, performing basic setup')

    # Start the cron loop so that any instances of this class after this one don't start while we're running.
    cron_checker.start_cron_loop()

    # Now, finally launch the bot.
    from lib import bot
    bot.launch()
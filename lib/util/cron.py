"""
Cron class is used in conjunction with cronjobs to automatically handle reboots and make sure that
only one instance of the bot is running at any given time.
"""
# Package Imports
import os.path as path
import threading
import random


# Constants setting
CRONTAB_CHECK_FILE = '.croncheck'
CRONTAB_WAIT_INTERVAL = 45
CRONTAB_STR_LENGTH = 64
CRONTAB_CHAR_POSSIBILITIES = '1234567890-=_+()*&^%$#@!~`qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFG HJKLZXCVBNM[]{};\':",.<>?/|\\'


def get_cron_string():
    """
    Gets the cron string from the file.
    If the file doesn't exist, it returns None.
    Used often in the launcher.
    """
    # If the crontab check file isn't there, we return None
    if not path.isfile(CRONTAB_CHECK_FILE):
        return None

    # Otherwise, we open the file and return its contents.
    with open(CRONTAB_CHECK_FILE, 'r') as r:
        return r.read()


def write_cron_string():
    """
    Writes a new cron string to the file.
    """
    # Create the new cron string.
    cron_str = ''.join(random.choice(CRONTAB_CHAR_POSSIBILITIES) for i in range(CRONTAB_STR_LENGTH))

    # Open the file and write.
    with open(CRONTAB_CHECK_FILE, 'w') as w:
        w.write(cron_str)


class CronThread(threading.Thread):
    """
    Thread designed to constantly write a random string of characters to the croncheck file.
    This prevents cron jobs from launching two of the bot at once, since the launcher checks the croncheck file twice while booting up.
    """

    def run(self):
        """
        Cron loop updates the cron file with new random strings so that we don't create more than one instance at once thanks to cron.
        """
        # Import time
        import time

        # Infinite loop.
        while True:

            # Write cron string.
            write_cron_string()

            # Wait until next time to write.
            time.sleep(CRONTAB_WAIT_INTERVAL)

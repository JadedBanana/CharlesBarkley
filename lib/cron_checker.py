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
CRONTAB_CHAR_POSSIBILITIES = \
    '1234567890-=_+()*&^%$#@!~`qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFG HJKLZXCVBNM[]{};\':",.<>?/|\\'


# get_cronstring is used for the launcher.
def get_cronstring():
    """
    Gets the cronstring from the file.
    If the file doesn't exist, it returns None.
    """
    # If the crontab check file isn't there, we return None
    if not path.isfile(CRONTAB_CHECK_FILE):
        return None
    # Otherwise, we open the file and return its contents.
    with open(CRONTAB_CHECK_FILE, 'r') as r:
        return r.read()


# This class runs an infinite loop constantly writing new shit to the cron file.
class CronLoop(threading.Thread):

    def run(self):
        """
        Cron loop updates the cron file with new random strings so we don't create more than one instance at once thanks to cron.
        """
        import time
        while True:
            cron_str = ''.join(random.choice(CRONTAB_CHAR_POSSIBILITIES) for i in range(CRONTAB_STR_LENGTH))
            with open(CRONTAB_CHECK_FILE, 'w') as w:
                w.write(cron_str)
            time.sleep(CRONTAB_WAIT_INTERVAL)


# Starts the cron loop. Used to write new shit to the cron file, forever.
def start_cron_loop():
    """
    Starts the cron loop.
    """
    # Just starts a cron loop.
    CronLoop(daemon=True).start()
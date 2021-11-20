"""
Cron class is used in conjunction with cronjobs to automatically handle reboots and make sure that
only one instance of the bot is running at any given time.
"""
# Imports
import os.path as path
import threading
import random
import base64

# Variable setting
CRONTAB_CHECK_FILE = '.croncheck'

# get cronstring is used for the launcher
def get_cronstring():
    """
    Gets the cronstring from the file.
    If the file doesn't exist, it returns None.
    """
    # If the crontab check file isn't there, we return None
    if not path.isfile(constants.CRONTAB_CHECK_FILE):
        return None
    # Otherwise, we open the file and return its contents.
    with open(constants.CRONTAB_CHECK_FILE, 'r') as r:
        return r.read()

# this class runs the loop
class CronLoop(threading.Thread):

    def run(self):
        """
        Cron loop updates the cron file with new random strings so we don't create more than one instance at once thanks to cron.
        """
        import time
        while True:
            cronstr = ''.join([random.choice(constants.CRONTAB_STR_CHARS) for i in range(constants.CRONTAB_STR_LENGTH)])
            with open(constants.CRONTAB_CHECK_FILE, 'w') as w:
                w.write(cronstr)
            time.sleep(constants.CRONTAB_WAIT_INTERVAL)

# starts the cron loop
def start_cron_loop():
    """
    Starts the cron loop.
    """
    # Just starts a cron loop.
    CronLoop().start()
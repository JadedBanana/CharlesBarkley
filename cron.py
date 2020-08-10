import os.path as path
import constants
import threading
import random

# get cronstring is used for the launcher
def get_cronstring():
    # If the crontab check file isn't there, we return None
    if not path.isfile(constants.CRONTAB_CHECK_FILE):
        return None
    # Otherwise, we open the file and return its contents.
    with open(constants.CRONTAB_CHECK_FILE, 'r') as r:
        return r.read()

# this class runs the loop
class CronLoop(threading.Thread):
    def run(self):
        import time
        while True:
            cronstr = ''.join([random.choice(constants.CRONTAB_STR_CHARS) for i in range(constants.CRONTAB_STR_LENGTH)])
            with open(constants.CRONTAB_CHECK_FILE, 'w') as w:
                w.write(cronstr)
            time.sleep(constants.CRONTAB_WAIT_INTERVAL)

# starts the cron loop
def start_cron_loop():
    # Just starts a cron loop.
    CronLoop().start()
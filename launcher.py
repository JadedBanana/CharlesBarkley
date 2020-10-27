# Jadi3Pi launch file
# Meant to be run as part of a crontab that activates once every 2 minutes.

# Set the working directory to what we want so our imports work correctly
# Also checks the OS to make sure we load into the correct working directory
import platform
import os

on_windows = platform.system() == 'Windows'
if on_windows:
    os.chdir('C:/Users/popki/Projects/Python/Jadi3Pi')
else:
    os.chdir('/home/pi/Jadi3Pi')

# Next, import cron and get the current cronstring.
import cron
cronstr_1 = cron.get_cronstring()

# If there isn't a cronstr, we try again a second later.
# If there still isn't one, we skip all this crap and begin.
import time
if not cronstr_1:
    time.sleep(1)
    cronstr_1 = cron.get_cronstring()

if cronstr_1:
    # Wait a little less than a minute.
    time.sleep(55)

    # Get the current cronstring again.
    cronstr_2 = cron.get_cronstring()

    # If the two cronstrings are not the same, then we exit.
    if cronstr_1 != cronstr_2:
        exit(0)

# If it passed, we continue.
import bot

bot.launch(on_windows)
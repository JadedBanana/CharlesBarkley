"""
toggle_ignore_developer command.
Specialized command in that it can be called even when the developer is being ignored.
"""
# Imports
from lib.util import environment
from lib.util import messaging

async def toggle_ignore_dev(bot, message, argument=None):
    """
    Toggles whether or not to ignore the developer.
    The response varies depending on whether or not this is the deployment version.
    """
    # TODO: reimplement logging in this part
    # For deployment client, toggle the ignoring developer status.
    if environment.get("DEPLOYMENT_CLIENT"):
        bot.ignore_developer = not bot.ignore_developer
        await messaging.send_text_message(message, f'Deployment version speaking, now{" " if bot.ignore_developer else "no longer "}ignoring developers')

    # For development client, ignore this message.
    else:
        await messaging.send_text_message(message, f'Development version speaking, ignoring ignore request')

# Command values
COMMAND_NAME = 'toggleignoredev'
COMMAND_NAMES = ['toggleignoredev']
CALL_METHOD = toggle_ignore_dev
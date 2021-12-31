# Local Imports
from lib.util import environment

# Package Imports
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import logging
import sys

# List of tables we should expect to see in the database.
# Functions similar to lib.util.environment's EXPECTED_DOTENV_VARS.
# The dict is keyed by the table name in SQL, and the result is the attribute set in this module.
EXPECTED_DATABASE_TABLES = {
    'reminders': 'REMINDER_TABLE',
    'hg_actions': 'HG_ACTION_TABLE',
    'hg_action_wrappers': 'HG_ACTION_WRAPPER_TABLE',
    'hg_phases': 'HG_PHASES_TABLE',
}

# List of commands that use specific database tables.
COMMANDS_USING_DATABASE_TABLES = {
    'hungergames': ('HG_ACTION_TABLE', 'HG_ACTION_WRAPPER_TABLE', 'HG_PHASES_TABLE'),
    'remindme': ('REMINDER_TABLE',)
}

# Database variables
BASE = None
ENGINE = None
SESSION = None


def initialize():
    """
    Initializes the database and pulls all the required tables.
    """
    # Set the outside values as global, so we can modify them.
    global BASE, ENGINE, SESSION

    # Log.
    logging.info('Attempting to make connection to database...')

    # Wrap with try/catch case to detect ALL exceptions.
    try:

        # Set the base.
        BASE = automap_base()

        # Set the engine.
        ENGINE = create_engine(environment.get('SQLALCHEMY_DATABASE_URL'))

        # Prepare the base and the session with the engine.
        BASE.prepare(ENGINE, reflect=True)
        SESSION = sessionmaker(ENGINE)()

    # On exception, log the error and exit.
    except Exception as e:
        logging.error('Error occurred during database mapping.')
        import traceback
        logging.error(traceback.format_exc().replace('\n\n', '\n').strip('\n'))


        # If we are supposed to exit, exit.
        if environment.get('EXIT_ON_DATABASE_FAILURE'):
            sys.exit(-1)

        # Otherwise, just return.
        return

    # If we've made it this far, then yay! Log our success.
    logging.info('Database connection established successfully.')

    # Variables keeping track of stuff in the loop.
    this_module = sys.modules[__name__]
    missing_tables = False

    # Iterate through the expected database tables.
    for database_table, module_table in EXPECTED_DATABASE_TABLES.items():

        # Check and make sure that the database table exists.
        # If so, set it as the attribute here.
        if hasattr(BASE.classes, database_table):
            setattr(this_module, module_table, getattr(BASE.classes, database_table))

        # Database table does not exist, log warning.
        else:
            missing_tables = True
            logging.warning(f'Expected database table {database_table} in database, not found.')

    # Warn user if missing any tables.
    if missing_tables:
        logging.warning('Related commands may not function correctly as a result of missing database tables.')


def get_disabled_commands_from_missing_tables():
    """
    Gets the disabled table names according to the missing tables.

    Returns:
        str[] : The command names, as they are in COMMANDS_USING_DATABASE_TABLES.
    """
    # First, check if we're supposed to return anything for this, and if not, return an empty dict.
    if not environment.get('DISABLE_COMMANDS_WITH_MISSING_DATABASE_TABLES'):
        return []

    # Second, test if base, engine, or session exist. If not, send back ALL of them.
    if not any([BASE, ENGINE, SESSION]):
        return [command_name for command_name in COMMANDS_USING_DATABASE_TABLES]

    # Otherwise, go through them all individually and add them if they don't have tables here.
    disabled_command_list = []
    for command_name, table_list in COMMANDS_USING_DATABASE_TABLES.items():
        if not all([hasattr(sys.modules[__name__], table_name) for table_name in table_list]):
            disabled_command_list.append(command_name)

    # Return.
    return disabled_command_list

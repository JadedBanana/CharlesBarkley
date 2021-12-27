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
        logging.error(traceback.format_exc().replace('\n\n', '\n'))


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

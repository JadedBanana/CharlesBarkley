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
    'hg_phases': 'HG_PHASES_TABLE',
    'hg_actions': 'HG_ACTIONS_TABLE',
    'hg_action_wrappers': 'HG_ACTION_WRAPPERS_TABLE',
    'hg_current_game_phases': 'HG_CURRENT_GAME_PHASES_TABLE',
    'hg_current_game_actions': 'HG_CURRENT_GAME_ACTIONS_TABLE'
}

# List of commands that use specific database tables.
COMMANDS_USING_DATABASE_TABLES = {
    'hungergames': ('HG_PHASES_TABLE', 'HG_ACTIONS_TABLE', 'HG_ACTION_WRAPPERS_TABLE', 'HG_CURRENT_GAME_PHASES_TABLE',
                    'HG_CURRENT_GAME_ACTIONS_TABLE'),
    'remindme': ('REMINDER_TABLE',)
}

# Database variables
BASE = None
ENGINE = None
SESSION = None


def get_all(table):
    """
    Gets every row from the given table.

    Args:
        database table : Which table to pull from.

    Returns:
        SQLAlchemy.Query : The finalized query.
    """
    # Simple execution.
    return SESSION.query(table)


def get_filtered_by(table, **kwargs):
    """
    Gets a filtered set of rows from the given table according to the kwargs.
    Can only do equal signs, no > or <.

    Args:
        database table : Which table to pull from.
        **kwargs : All variables from which to filter_by.
                   Must refer to database columns equaling something else.

    Returns:
        SQLAlchemy.Query : The finalized query.
    """
    # Simple execution.
    return filter_by(SESSION.query(table), **kwargs)


def get_filtered(table, *args):
    """
    Gets a filtered set of rows from the given table according to the args.
    Can only do equal signs, no > or <.

    Args:
        database table : Which table to pull from.
        *args : All variables from which to filter by.
                Must refer to database columns being less than or equal to or greater than something else.

    Returns:
        SQLAlchemy.Query : The finalized query.
    """
    # Simple execution.
    return filter(SESSION.query(table), *args)


def get_all_joined(base_table, *tables_and_ons):
    """
    Gets every row from the given base_table, combined with the rest of the tables referenced above.

    Args:
        base_table (database table) : The starting table to pull from.
        *tables_and_ons (database table, database column equality)[] : Tuples whose first item is the table to pull
                                                                       from, and whose second item is the equality on
                                                                       which to base the inner join.

    Returns:
        SQLAlchemy.Query : The finalized query.
    """
    # Create the query step-by-step, starting with the base table.
    base_query = join(SESSION.query(base_table), tables_and_ons)

    # Return.
    return base_query


def get_filtered_by_joined(base_table, *tables_and_ons, **kwargs):
    """
    Gets a filtered set of rows from the given base_table, combined with the rest of the tables referenced above,
    according to the provided kwargs.
    Can only do equal signs, no > or <.

    Args:
        base_table (database table) : The starting table to pull from.
        *tables_and_ons (database table, database column equality)[] : Tuples whose first item is the table to pull
                                                                       from, and whose second item is the equality on
                                                                       which to base the inner join.
        **kwargs : All variables from which to filter_by.
                   Must refer to database columns equaling something else.

    Returns:
        SQLAlchemy.Query : The finalized query.
    """
    # Simple return.
    return filter_by(join(SESSION.query(base_table), *tables_and_ons), **kwargs)


def filter_by(base_query, **kwargs):
    """
    Filters the given query according to the kwargs.
    Can only do equal signs, no > or <.

    Args:
        base_query (SQLAlchemy.Query) : The starting query to add onto.
        **kwargs : All variables from which to filter by.
                   Must refer to database columns equaling something else.

    Returns:
        SQLAlchemy.Query : The finalized query.
    """
    # Simple return.
    return base_query.filter_by(**kwargs)


def filter(base_query, *args):
    """
    Filters the given query according to the args.
    Can only do > or < signs, no equalities.

    Args:
        base_query (SQLAlchemy.Query) : The starting query to add onto.
        *args : All variables from which to filter by.
                Must refer to database columns being less than or equal to or greater than something else.

    Returns:
        SQLAlchemy.Query : The finalized query.
    """
    # Simple return.
    return base_query.filter(*args)


def join(base_query, *tables_and_ons):
    """
    Joins the given tables onto the base_query according to the ON statements.

    Args:
        base_query (SQLAlchemy.Query) : The starting query to add onto.
        *tables_and_ons (database table, database column equality)[] : Tuples whose first item is the table to pull
                                                                       from, and whose second item is the equality on
                                                                       which to base the inner join.

    Returns:
        SQLAlchemy.Query : The finalized query.
    """
    # Create new_query from base_query.
    new_query = base_query

    # Iterate through all tables_and_ons and add them slowly.
    for table_and_on in tables_and_ons:
        new_query = new_query.join(table_and_on[0], table_and_on[1])

    # Return.
    return new_query


def insert_into_database(table, **kwargs):
    """
    Creates and inserts a new object into the database.

    Args:
        table (database table) : The starting table to instantiate the object from.
        **kwargs : All the constructor arguments.

    Returns:
        new_object (database table object) : The object that was inserted.
    """
    # Create the object.
    table_object = table(**kwargs)

    # Commit.
    commit_to_database(table_object)

    # Return.
    return table_object


def commit_to_database(new_object):
    """
    Commits a new object to the database.

    Arguments:
        new_object (database table object) : The object to insert into the database.
    """
    # Add and commit.
    SESSION.add(new_object)
    SESSION.commit()


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


def database_available():
    """
    Returns whether the database is available or not.

    Returns:
        bool : Whether the database is available or not.
    """
    # Simple return.
    return all([BASE, ENGINE, SESSION])


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
    if not database_available():
        return [command_name for command_name in COMMANDS_USING_DATABASE_TABLES]

    # Otherwise, go through them all individually and add them if they don't have tables here.
    disabled_command_list = []
    for command_name, table_list in COMMANDS_USING_DATABASE_TABLES.items():
        if not all([hasattr(sys.modules[__name__], table_name) for table_name in table_list]):
            disabled_command_list.append(command_name)

    # Return.
    return disabled_command_list

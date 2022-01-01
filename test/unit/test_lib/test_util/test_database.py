# Package Imports
from unittest import mock, TestCase

# Local Imports
from lib.util import database


class TestDatabase(TestCase):


    def test_database_available_no_base_no_engine_no_session(self):
        """lib.util.database.database_available.no_base.no_engine.no_session"""
        # Set the database module's attributes.
        database.BASE = None
        database.ENGINE = None
        database.SESSION = None

        # Run the method.
        database_available = database.database_available()

        # Run assertions.
        self.assertFalse(database_available)


    def test_database_available_no_base_no_engine_yes_session(self):
        """lib.util.database.database_available.no_base.no_engine.yes_session"""
        # Set the database module's attributes.
        database.BASE = None
        database.ENGINE = None
        database.SESSION = True

        # Run the method.
        database_available = database.database_available()

        # Run assertions.
        self.assertFalse(database_available)


    def test_database_available_no_base_yes_engine_no_session(self):
        """lib.util.database.database_available.no_base.yes_engine.no_session"""
        # Set the database module's attributes.
        database.BASE = None
        database.ENGINE = True
        database.SESSION = None

        # Run the method.
        database_available = database.database_available()

        # Run assertions.
        self.assertFalse(database_available)


    def test_database_available_no_base_yes_engine_yes_session(self):
        """lib.util.database.database_available.no_base.yes_engine.yes_session"""
        # Set the database module's attributes.
        database.BASE = None
        database.ENGINE = True
        database.SESSION = True

        # Run the method.
        database_available = database.database_available()

        # Run assertions.
        self.assertFalse(database_available)


    def test_database_available_yes_base_no_engine_no_session(self):
        """lib.util.database.database_available.yes_base.no_engine.no_session"""
        # Set the database module's attributes.
        database.BASE = True
        database.ENGINE = None
        database.SESSION = None

        # Run the method.
        database_available = database.database_available()

        # Run assertions.
        self.assertFalse(database_available)


    def test_database_available_yes_base_no_engine_yes_session(self):
        """lib.util.database.database_available.yes_base.no_engine.yes_session"""
        # Set the database module's attributes.
        database.BASE = True
        database.ENGINE = None
        database.SESSION = True

        # Run the method.
        database_available = database.database_available()

        # Run assertions.
        self.assertFalse(database_available)


    def test_database_available_yes_base_yes_engine_no_session(self):
        """lib.util.database.database_available.yes_base.yes_engine.no_session"""
        # Set the database module's attributes.
        database.BASE = True
        database.ENGINE = True
        database.SESSION = None

        # Run the method.
        database_available = database.database_available()

        # Run assertions.
        self.assertFalse(database_available)


    def test_database_available_yes_base_yes_engine_yes_session(self):
        """lib.util.database.database_available.yes_base.yes_engine.yes_session"""
        # Set the database module's attributes.
        database.BASE = True
        database.ENGINE = True
        database.SESSION = True

        # Run the method.
        database_available = database.database_available()

        # Run assertions.
        self.assertTrue(database_available)


    @mock.patch('lib.util.environment.get')
    @mock.patch('lib.util.database.database_available')
    def test_get_disabled_commands_from_missing_tables_do_database_available_missing(self, m_da, m_eg):
        """lib.util.database.get_disabled_commands_from_missing_tables.do.database_available.missing"""
        # Set return values.
        m_eg.return_value = True
        m_da.return_value = True

        # Set the database module's attributes.
        database.COMMANDS_USING_DATABASE_TABLES = {
            'comm1': ('TABLE_1', 'TABLE_2'),
            'comm2': ('TABLE_3', 'TABLE_4', 'TABLE_5')
        }

        # Run the method.
        disabled_commands = database.get_disabled_commands_from_missing_tables()

        # Run assertions.
        m_eg.assert_called_once_with('DISABLE_COMMANDS_WITH_MISSING_DATABASE_TABLES')
        m_da.assert_called_once_with()
        self.assertEqual(disabled_commands, ['comm1', 'comm2'])


    @mock.patch('lib.util.environment.get')
    @mock.patch('lib.util.database.database_available')
    def test_get_disabled_commands_from_missing_tables_do_database_available_there(self, m_da, m_eg):
        """lib.util.database.get_disabled_commands_from_missing_tables.do.database_available.missing"""
        # Set return values.
        m_eg.return_value = True
        m_da.return_value = True

        # Set the database module's attributes.
        database.COMMANDS_USING_DATABASE_TABLES = {
            'comm1': ('TABLE_1', 'TABLE_2'),
            'comm2': ('TABLE_3', 'TABLE_4', 'TABLE_5')
        }
        database.TABLE_1 = 'table'
        database.TABLE_2 = 'table'
        database.TABLE_3 = 'table'
        database.TABLE_4 = 'table'
        database.TABLE_5 = 'table'

        # Run the method.
        disabled_commands = database.get_disabled_commands_from_missing_tables()

        # Run assertions.
        m_eg.assert_called_once_with('DISABLE_COMMANDS_WITH_MISSING_DATABASE_TABLES')
        m_da.assert_called_once_with()
        self.assertEqual(disabled_commands, [])

        # Perform cleanup.
        delattr(database, 'TABLE_1')
        delattr(database, 'TABLE_2')
        delattr(database, 'TABLE_3')
        delattr(database, 'TABLE_4')
        delattr(database, 'TABLE_5')


    @mock.patch('lib.util.environment.get')
    @mock.patch('lib.util.database.database_available')
    def test_get_disabled_commands_from_missing_tables_do_database_unavailable_missing(self, m_da, m_eg):
        """lib.util.database.get_disabled_commands_from_missing_tables.do.database_unavailable.missing"""
        # Set return values.
        m_eg.return_value = True
        m_da.return_value = False

        # Set the database module's attributes.
        database.COMMANDS_USING_DATABASE_TABLES = {
            'comm1': ('TABLE_1', 'TABLE_2'),
            'comm2': ('TABLE_3', 'TABLE_4', 'TABLE_5')
        }

        # Run the method.
        disabled_commands = database.get_disabled_commands_from_missing_tables()

        # Run assertions.
        m_da.assert_called_once_with()
        self.assertEqual(disabled_commands, ['comm1', 'comm2'])


    @mock.patch('lib.util.environment.get')
    @mock.patch('lib.util.database.database_available')
    def test_get_disabled_commands_from_missing_tables_do_database_unavailable_there(self, m_da, m_eg):
        """lib.util.database.get_disabled_commands_from_missing_tables.do.database_unavailable.missing"""
        # Set return values.
        m_eg.return_value = True
        m_da.return_value = False

        # Set the database module's attributes.
        database.COMMANDS_USING_DATABASE_TABLES = {
            'comm1': ('TABLE_1', 'TABLE_2'),
            'comm2': ('TABLE_3', 'TABLE_4', 'TABLE_5')
        }
        database.TABLE_1 = 'table'
        database.TABLE_2 = 'table'
        database.TABLE_3 = 'table'
        database.TABLE_4 = 'table'
        database.TABLE_5 = 'table'

        # Run the method.
        disabled_commands = database.get_disabled_commands_from_missing_tables()

        # Run assertions.
        m_da.assert_called_once_with()
        self.assertEqual(disabled_commands, ['comm1', 'comm2'])

        # Perform cleanup.
        delattr(database, 'TABLE_1')
        delattr(database, 'TABLE_2')
        delattr(database, 'TABLE_3')
        delattr(database, 'TABLE_4')
        delattr(database, 'TABLE_5')


    @mock.patch('lib.util.environment.get')
    @mock.patch('lib.util.database.database_available')
    def test_get_disabled_commands_from_missing_tables_dont_database_available_missing(self, m_da, m_eg):
        """lib.util.database.get_disabled_commands_from_missing_tables.dont.database_available.missing"""
        # Set return values.
        m_eg.return_value = False
        m_da.return_value = True

        # Set the database module's attributes.
        database.COMMANDS_USING_DATABASE_TABLES = {
            'comm1': ('TABLE_1', 'TABLE_2'),
            'comm2': ('TABLE_3', 'TABLE_4', 'TABLE_5')
        }

        # Run the method.
        disabled_commands = database.get_disabled_commands_from_missing_tables()

        # Run assertions.
        m_eg.assert_called_once_with('DISABLE_COMMANDS_WITH_MISSING_DATABASE_TABLES')
        self.assertEqual(disabled_commands, [])


    @mock.patch('lib.util.environment.get')
    @mock.patch('lib.util.database.database_available')
    def test_get_disabled_commands_from_missing_tables_dont_database_available_there(self, m_da, m_eg):
        """lib.util.database.get_disabled_commands_from_missing_tables.dont.database_available.missing"""
        # Set return values.
        m_eg.return_value = False
        m_da.return_value = True

        # Set the database module's attributes.
        database.COMMANDS_USING_DATABASE_TABLES = {
            'comm1': ('TABLE_1', 'TABLE_2'),
            'comm2': ('TABLE_3', 'TABLE_4', 'TABLE_5')
        }
        database.TABLE_1 = 'table'
        database.TABLE_2 = 'table'
        database.TABLE_3 = 'table'
        database.TABLE_4 = 'table'
        database.TABLE_5 = 'table'

        # Run the method.
        disabled_commands = database.get_disabled_commands_from_missing_tables()

        # Run assertions.
        m_eg.assert_called_once_with('DISABLE_COMMANDS_WITH_MISSING_DATABASE_TABLES')
        self.assertEqual(disabled_commands, [])

        # Perform cleanup.
        delattr(database, 'TABLE_1')
        delattr(database, 'TABLE_2')
        delattr(database, 'TABLE_3')
        delattr(database, 'TABLE_4')
        delattr(database, 'TABLE_5')


    @mock.patch('lib.util.environment.get')
    @mock.patch('lib.util.database.database_available')
    def test_get_disabled_commands_from_missing_tables_dont_database_unavailable_missing(self, m_da, m_eg):
        """lib.util.database.get_disabled_commands_from_missing_tables.dont.database_unavailable.missing"""
        # Set return values.
        m_eg.return_value = False
        m_da.return_value = False

        # Set the database module's attributes.
        database.COMMANDS_USING_DATABASE_TABLES = {
            'comm1': ('TABLE_1', 'TABLE_2'),
            'comm2': ('TABLE_3', 'TABLE_4', 'TABLE_5')
        }

        # Run the method.
        disabled_commands = database.get_disabled_commands_from_missing_tables()

        # Run assertions.
        m_eg.assert_called_once_with('DISABLE_COMMANDS_WITH_MISSING_DATABASE_TABLES')
        self.assertEqual(disabled_commands, [])


    @mock.patch('lib.util.environment.get')
    @mock.patch('lib.util.database.database_available')
    def test_get_disabled_commands_from_missing_tables_dont_database_unavailable_there(self, m_da, m_eg):
        """lib.util.database.get_disabled_commands_from_missing_tables.dont.database_unavailable.missing"""
        # Set return values.
        m_eg.return_value = False
        m_da.return_value = False

        # Set the database module's attributes.
        database.COMMANDS_USING_DATABASE_TABLES = {
            'comm1': ('TABLE_1', 'TABLE_2'),
            'comm2': ('TABLE_3', 'TABLE_4', 'TABLE_5')
        }
        database.TABLE_1 = 'table'
        database.TABLE_2 = 'table'
        database.TABLE_3 = 'table'
        database.TABLE_4 = 'table'
        database.TABLE_5 = 'table'

        # Run the method.
        disabled_commands = database.get_disabled_commands_from_missing_tables()

        # Run assertions.
        m_eg.assert_called_once_with('DISABLE_COMMANDS_WITH_MISSING_DATABASE_TABLES')
        self.assertEqual(disabled_commands, [])

        # Perform cleanup.
        delattr(database, 'TABLE_1')
        delattr(database, 'TABLE_2')
        delattr(database, 'TABLE_3')
        delattr(database, 'TABLE_4')
        delattr(database, 'TABLE_5')

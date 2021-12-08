from unittest import mock, TestCase, IsolatedAsyncioTestCase
from lib.bot import JadieClient
from lib import bot
from datetime import datetime


class TestBotSynchronous(TestCase):


    @mock.patch('lib.util.environment.get')
    @mock.patch('lib.commands.load_commands')
    @mock.patch('discord.Intents.all')
    @mock.patch('discord.Client.__init__')
    def test_init(self, m_i, m_a, m_lc, m_eg):
        """lib.bot.JadieClient.__init__"""
        # Side effect method for environment.get
        environ_vars = [True, ['12', '31', '50']]
        environ_called_with = []
        def environment_get_side_effect(*args, **kwargs):
            environ_called_with.append(args)
            var = environ_vars[0]
            environ_vars.remove(var)
            return var
        m_eg.side_effect = environment_get_side_effect

        # Return stuff for everything else
        m_i.return_value = None
        m_a.return_value = 'intentional'
        help_init = mock.MagicMock()
        m_lc.return_value = {'fuckyeah': 'bro'}, {'awwyeah': 'babey'}, ['awesome'], {'toggleignoredev': 'snart',
                                                                                     'help_init': help_init}

        # Run the method.
        client = JadieClient()

        # Run assertions.
        self.assertIsInstance(client.bot_start_time, datetime)
        self.assertIsNone(client.bot_uptime)
        self.assertFalse(client.connected_before)
        self.assertFalse(client.reconnected_since)
        self.assertEqual(client.global_prefix, bot.GLOBAL_PREFIX)
        self.assertTrue(len(environ_called_with) == 2)
        self.assertEqual(environ_called_with[0], ('DEPLOYMENT_CLIENT',))
        self.assertEqual(client.deployment_client, True)
        m_lc.assert_called()
        self.assertEqual(client.public_command_dict, {'fuckyeah': 'bro'})
        self.assertEqual(client.developer_command_dict, {'awwyeah': 'babey'})
        self.assertEqual(client.reactive_command_list, ['awesome'])
        self.assertEqual(client.toggle_ignore_developer, 'snart')
        help_init.assert_called_with(bot.VERSION_NUMBER, bot.GLOBAL_PREFIX)
        self.assertFalse(client.ignore_developer)
        self.assertEqual(client.developer_ids, [12, 31, 50])
        m_a.assert_called()
        m_i.assert_called_with(client, intents='intentional')


class TestBotAsynchronous(IsolatedAsyncioTestCase):


    async def test_on_ready_no_guilds(self):
        """lib.bot.JadieClient.on_ready.no_guilds"""
        # Create thing
        client = mock.MagicMock(user='whatever', guilds=[])

        # Run the method.
        await JadieClient.on_ready(client)


    async def test_on_ready_yes_guilds(self):
        """lib.bot.JadieClient.on_ready.yes_guilds"""
        # Create thing
        client = mock.MagicMock(user='whatever', guilds=[mock.MagicMock(name='me', id=20),
                                                         mock.MagicMock(name='alex', id=420),
                                                         mock.MagicMock(name='zach', id=2)])

        # Run the method.
        await JadieClient.on_ready(client)


    @mock.patch('logging.info')
    async def test_on_connect_connected_before(self, m_li):
        """lib.bot.JadieClient.on_connect.connected_before"""
        # Create thing
        client = mock.MagicMock(connected_before=True, reconnected_since=False)

        # Run the method.
        await JadieClient.on_connect(client)

        # Run assertions.
        m_li.assert_called()
        self.assertTrue(client.reconnected_since)


    @mock.patch('logging.info')
    async def test_on_connect_first_connection(self, m_li):
        """lib.bot.JadieClient.on_connect.first_connection"""
        # Create thing
        client = mock.MagicMock(connected_before=False, reconnected_since=False)

        # Run the method.
        await JadieClient.on_connect(client)

        # Run assertions.
        m_li.assert_not_called()
        self.assertTrue(client.reconnected_since)


    @mock.patch('logging.info')
    async def test_on_disconnect_reconnected_since(self, m_li):
        """lib.bot.JadieClient.on_disconnect.reconnected_since"""
        # Create thing
        client = mock.MagicMock(user='me', reconnected_since=True)

        # Run the method.
        await JadieClient.on_disconnect(client)

        # Run assertions.
        m_li.assert_called()
        self.assertFalse(client.reconnected_since)


    @mock.patch('logging.info')
    async def test_on_disconnect_not_reconnected_since(self, m_li):
        """lib.bot.JadieClient.on_disconnect.not_reconnected_since"""
        # Create thing
        client = mock.MagicMock(user='me', reconnected_since=False)

        # Run the method.
        await JadieClient.on_disconnect(client)

        # Run assertions.
        m_li.assert_not_called()
        self.assertFalse(client.reconnected_since)


    @mock.patch('logging.info')
    async def test_on_message_(self, m_li):
        """lib.bot.JadieClient.on_disconnect.not_reconnected_since"""
        # Create thing
        client = mock.MagicMock(user='me', reconnected_since=False)

        # Run the method.
        await JadieClient.on_disconnect(client)

        # Run assertions.
        m_li.assert_not_called()
        self.assertFalse(client.reconnected_since)

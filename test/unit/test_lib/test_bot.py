# Package Imports
from unittest import mock, TestCase, IsolatedAsyncioTestCase
from datetime import datetime
import discord

# Local Imports
from lib.bot import JadieClient
from lib import bot


class TestBotSynchronous(TestCase):


    @mock.patch('lib.util.environment.get')
    @mock.patch('lib.commands.load_all_commands')
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
        command_initialize_method_list = [mock.MagicMock(), mock.MagicMock()]
        m_lc.return_value = {'fuckyeah': 'bro'}, {'awwyeah': 'babey'}, ['awesome'], \
                            {'toggleignoredev': 'snart', 'help_init': help_init}, command_initialize_method_list

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
        for initialize_method in command_initialize_method_list:
            initialize_method.assert_called_once_with()
        self.assertFalse(client.ignore_developer)
        self.assertEqual(client.developer_ids, [12, 31, 50])
        m_a.assert_called()
        m_i.assert_called_with(client, intents='intentional')


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_no_message(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.no_message"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = None

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_message_wrong_type(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.message_wrong_type"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = 20

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_no_author_no_content_no_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.no_author.no_content.no_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author=None, content=None, channel=None, guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_no_author_no_content_no_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.no_author.no_content.no_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author=None, content=None, channel=None, guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_no_author_no_content_guild_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.no_author.no_content.guild_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author=None, content=None, channel=25, guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_no_author_no_content_guild_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.no_author.no_content.guild_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author=None, content=None, channel=25, guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_no_author_no_content_other_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.no_author.no_content.other_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author=None, content=None, channel='other channel', guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_no_author_no_content_other_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.no_author.no_content.other_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author=None, content=None, channel='other channel', guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_no_author_yes_content_no_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.no_author.yes_content.no_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author=None, content='alex cute', channel=None, guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_no_author_yes_content_no_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.no_author.yes_content.no_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author=None, content='alex cute', channel=None, guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_no_author_yes_content_guild_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.no_author.yes_content.guild_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author=None, content='alex cute', channel=25, guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_no_author_yes_content_guild_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.no_author.yes_content.guild_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author=None, content='alex cute', channel=25, guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_no_author_yes_content_other_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.no_author.yes_content.other_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author=None, content='alex cute', channel='other channel', guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_no_author_yes_content_other_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.no_author.yes_content.other_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author=None, content='alex cute', channel='other channel', guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_self_author_no_content_no_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.self_author.no_content.no_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='me', content=None, channel=None, guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_self_author_no_content_no_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.self_author.no_content.no_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='me', content=None, channel=None, guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_self_author_no_content_guild_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.self_author.no_content.guild_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='me', content=None, channel=25, guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_self_author_no_content_guild_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.self_author.no_content.guild_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='me', content=None, channel=25, guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_self_author_no_content_other_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.self_author.no_content.other_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='me', content=None, channel='other channel', guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_self_author_no_content_other_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.self_author.no_content.other_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='me', content=None, channel='other channel', guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_self_author_yes_content_no_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.self_author.yes_content.no_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='me', content='alex cute', channel=None, guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_self_author_yes_content_no_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.self_author.yes_content.no_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='me', content='alex cute', channel=None, guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_self_author_yes_content_guild_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.self_author.yes_content.guild_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='me', content='alex cute', channel=25, guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_self_author_yes_content_guild_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.self_author.yes_content.guild_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='me', content='alex cute', channel=25, guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_self_author_yes_content_other_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.self_author.yes_content.other_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='me', content='alex cute', channel='other channel', guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_self_author_yes_content_other_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.self_author.yes_content.other_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='me', content='alex cute', channel='other channel', guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_user_author_no_content_no_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.user_author.no_content.no_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='user', content=None, channel=None, guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_user_author_no_content_no_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.user_author.no_content.no_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='user', content=None, channel=None, guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_user_author_no_content_guild_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.user_author.no_content.guild_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='user', content=None, channel=25, guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_user_author_no_content_guild_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.user_author.no_content.guild_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='user', content=None, channel=25, guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_user_author_no_content_other_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.user_author.no_content.other_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='user', content=None, channel='other channel', guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_user_author_no_content_other_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.user_author.no_content.other_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='user', content=None, channel='other channel', guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_user_author_yes_content_no_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.user_author.yes_content.no_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='user', content='alex cute', channel=None, guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_user_author_yes_content_no_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.user_author.yes_content.no_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='user', content='alex cute', channel=None, guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_user_author_yes_content_guild_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.user_author.yes_content.guild_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='user', content='alex cute', channel=25, guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertFalse(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_user_author_yes_content_guild_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.user_author.yes_content.guild_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='user', content='alex cute', channel=25, guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertTrue(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_user_author_yes_content_other_channel_no_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.user_author.yes_content.other_channel.no_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='user', content='alex cute', channel='other channel', guild=None)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertTrue(response)


    @mock.patch('logging.error')
    def test_message_object_has_required_attributes_user_author_yes_content_other_channel_yes_guild(self, m_le):
        """lib.bot.JadieClient.message_object_has_required_attributes.user_author.yes_content.other_channel.yes_guild"""
        # Change the value of discord.Message and discord.TextChannel so isinstance() responds correctly
        discord.Message = mock.MagicMock
        discord.TextChannel = int

        # Create the client object.
        client = mock.MagicMock(user='me')

        # Create the message object.
        message = mock.MagicMock(author='user', content='alex cute', channel='other channel', guild=25)

        # Run the method.
        response = JadieClient.message_object_has_required_attributes(client, message)

        # Run assertions.
        self.assertTrue(response)


class TestBotAsynchronous(IsolatedAsyncioTestCase):


    @classmethod
    @mock.patch('lib.bot.JadieClient.__init__')
    def setUpClass(cls, m_i):
        """
        Set up class method.
        Creates a client that is used in MANY places.
        """
        # Setting return value to None to reduce errors and creating the client.
        m_i.return_value = None
        client = JadieClient()
        client.developer_ids = [12, 4843, 20]
        client.global_prefix = 'j!'
        client.public_command_dict = {'public_command': 'hello'}
        client.developer_command_dict = {'developer_command': 'world'}
        client.reactive_command_list = [mock.MagicMock(), mock.MagicMock()]

        # Make this client, the class' client.
        cls.client = client


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


    @mock.patch('lib.bot.JadieClient.is_functional_message')
    @mock.patch('lib.util.parsing.get_command_from_message')
    @mock.patch('lib.commands.run_standard_command')
    @mock.patch('lib.commands.run_reactive_command')
    async def test_on_message_non_functional_author_not_developer_no_command(self, m_rrc, m_rsc, m_gcfm, m_ifm):
        """lib.bot.JadieClient.on_message.non_functional.author_not_developer.no_command"""
        # Set return value for is_functional_message and get_command_from_message
        m_ifm.return_value = False, False
        m_gcfm.return_value = None, None

        # Run the method.
        await self.client.on_message('message')

        # Run assertions.
        m_ifm.assert_called_once_with('message')
        m_gcfm.assert_not_called()
        m_rsc.assert_not_called()
        m_rrc.assert_not_called()


    @mock.patch('lib.bot.JadieClient.is_functional_message')
    @mock.patch('lib.util.parsing.get_command_from_message')
    @mock.patch('lib.commands.run_standard_command')
    @mock.patch('lib.commands.run_reactive_command')
    async def test_on_message_non_functional_author_not_developer_public_command(self, m_rrc, m_rsc, m_gcfm, m_ifm):
        """lib.bot.JadieClient.on_message.non_functional.author_not_developer.public_command"""
        # Set return value for is_functional_message and get_command_from_message
        m_ifm.return_value = False, False
        m_gcfm.return_value = 'public_command', 'argument'

        # Run the method.
        await self.client.on_message('message')

        # Run assertions.
        m_ifm.assert_called_once_with('message')
        m_gcfm.assert_not_called()
        m_rsc.assert_not_called()
        m_rrc.assert_not_called()


    @mock.patch('lib.bot.JadieClient.is_functional_message')
    @mock.patch('lib.util.parsing.get_command_from_message')
    @mock.patch('lib.commands.run_standard_command')
    @mock.patch('lib.commands.run_reactive_command')
    async def test_on_message_non_functional_author_not_developer_developer_command(self, m_rrc, m_rsc, m_gcfm, m_ifm):
        """lib.bot.JadieClient.on_message.non_functional.author_not_developer.developer_command"""
        # Set return value for is_functional_message and get_command_from_message
        m_ifm.return_value = False, False
        m_gcfm.return_value = 'developer_command', 'argument'

        # Run the method.
        await self.client.on_message('message')

        # Run assertions.
        m_ifm.assert_called_once_with('message')
        m_gcfm.assert_not_called()
        m_rsc.assert_not_called()
        m_rrc.assert_not_called()


    @mock.patch('lib.bot.JadieClient.is_functional_message')
    @mock.patch('lib.util.parsing.get_command_from_message')
    @mock.patch('lib.commands.run_standard_command')
    @mock.patch('lib.commands.run_reactive_command')
    async def test_on_message_non_functional_author_not_developer_unknown_command(self, m_rrc, m_rsc, m_gcfm, m_ifm):
        """lib.bot.JadieClient.on_message.non_functional.author_not_developer.unknown_command"""
        # Set return value for is_functional_message and get_command_from_message
        m_ifm.return_value = False, False
        m_gcfm.return_value = 'unknown_command', 'argument'

        # Run the method.
        await self.client.on_message('message')

        # Run assertions.
        m_ifm.assert_called_once_with('message')
        m_gcfm.assert_not_called()
        m_rsc.assert_not_called()
        m_rrc.assert_not_called()


    @mock.patch('lib.bot.JadieClient.is_functional_message')
    @mock.patch('lib.util.parsing.get_command_from_message')
    @mock.patch('lib.commands.run_standard_command')
    @mock.patch('lib.commands.run_reactive_command')
    async def test_on_message_non_functional_author_is_developer_no_command(self, m_rrc, m_rsc, m_gcfm, m_ifm):
        """lib.bot.JadieClient.on_message.non_functional.author_is_developer.no_command"""
        # Set return value for is_functional_message and get_command_from_message
        m_ifm.return_value = False, True
        m_gcfm.return_value = None, None

        # Run the method.
        await self.client.on_message('message')

        # Run assertions.
        m_ifm.assert_called_once_with('message')
        m_gcfm.assert_not_called()
        m_rsc.assert_not_called()
        m_rrc.assert_not_called()


    @mock.patch('lib.bot.JadieClient.is_functional_message')
    @mock.patch('lib.util.parsing.get_command_from_message')
    @mock.patch('lib.commands.run_standard_command')
    @mock.patch('lib.commands.run_reactive_command')
    async def test_on_message_non_functional_author_is_developer_public_command(self, m_rrc, m_rsc, m_gcfm, m_ifm):
        """lib.bot.JadieClient.on_message.non_functional.author_is_developer.public_command"""
        # Set return value for is_functional_message and get_command_from_message
        m_ifm.return_value = False, True
        m_gcfm.return_value = 'public_command', 'argument'

        # Run the method.
        await self.client.on_message('message')

        # Run assertions.
        m_ifm.assert_called_once_with('message')
        m_gcfm.assert_not_called()
        m_rsc.assert_not_called()
        m_rrc.assert_not_called()


    @mock.patch('lib.bot.JadieClient.is_functional_message')
    @mock.patch('lib.util.parsing.get_command_from_message')
    @mock.patch('lib.commands.run_standard_command')
    @mock.patch('lib.commands.run_reactive_command')
    async def test_on_message_non_functional_author_is_developer_developer_command(self, m_rrc, m_rsc, m_gcfm, m_ifm):
        """lib.bot.JadieClient.on_message.non_functional.author_is_developer.developer_command"""
        # Set return value for is_functional_message and get_command_from_message
        m_ifm.return_value = False, True
        m_gcfm.return_value = 'developer_command', 'argument'

        # Run the method.
        await self.client.on_message('message')

        # Run assertions.
        m_ifm.assert_called_once_with('message')
        m_gcfm.assert_not_called()
        m_rsc.assert_not_called()
        m_rrc.assert_not_called()


    @mock.patch('lib.bot.JadieClient.is_functional_message')
    @mock.patch('lib.util.parsing.get_command_from_message')
    @mock.patch('lib.commands.run_standard_command')
    @mock.patch('lib.commands.run_reactive_command')
    async def test_on_message_non_functional_author_is_developer_unknown_command(self, m_rrc, m_rsc, m_gcfm, m_ifm):
        """lib.bot.JadieClient.on_message.non_functional.author_is_developer.unknown_command"""
        # Set return value for is_functional_message and get_command_from_message
        m_ifm.return_value = False, True
        m_gcfm.return_value = 'unknown_command', 'argument'

        # Run the method.
        await self.client.on_message('message')

        # Run assertions.
        m_ifm.assert_called_once_with('message')
        m_gcfm.assert_not_called()
        m_rsc.assert_not_called()
        m_rrc.assert_not_called()


    @mock.patch('lib.bot.JadieClient.is_functional_message')
    @mock.patch('lib.util.parsing.get_command_from_message')
    @mock.patch('lib.commands.run_standard_command')
    @mock.patch('lib.commands.run_reactive_command')
    async def test_on_message_functional_author_not_developer_no_command(self, m_rrc, m_rsc, m_gcfm, m_ifm):
        """lib.bot.JadieClient.on_message.functional.author_not_developer.no_command"""
        # Set return value for is_functional_message and get_command_from_message
        m_ifm.return_value = True, False
        m_gcfm.return_value = None, None

        # Run the method.
        await self.client.on_message('message')

        # Run assertions.
        m_ifm.assert_called_once_with('message')
        m_gcfm.assert_called_once_with('j!', 'message')
        m_rsc.assert_not_called()
        m_rrc.assert_called()


    @mock.patch('lib.bot.JadieClient.is_functional_message')
    @mock.patch('lib.util.parsing.get_command_from_message')
    @mock.patch('lib.commands.run_standard_command')
    @mock.patch('lib.commands.run_reactive_command')
    async def test_on_message_functional_author_not_developer_public_command(self, m_rrc, m_rsc, m_gcfm, m_ifm):
        """lib.bot.JadieClient.on_message.functional.author_not_developer.public_command"""
        # Set return value for is_functional_message and get_command_from_message
        m_ifm.return_value = True, False
        m_gcfm.return_value = 'public_command', 'argument'

        # Run the method.
        await self.client.on_message('message')

        # Run assertions.
        m_ifm.assert_called_once_with('message')
        m_gcfm.assert_called_once_with('j!', 'message')
        m_rsc.assert_called_once_with('public_command', 'hello', self.client, 'message', 'argument')
        m_rrc.assert_not_called()


    @mock.patch('lib.bot.JadieClient.is_functional_message')
    @mock.patch('lib.util.parsing.get_command_from_message')
    @mock.patch('lib.commands.run_standard_command')
    @mock.patch('lib.commands.run_reactive_command')
    async def test_on_message_functional_author_not_developer_developer_command(self, m_rrc, m_rsc, m_gcfm, m_ifm):
        """lib.bot.JadieClient.on_message.functional.author_not_developer.developer_command"""
        # Set return value for is_functional_message and get_command_from_message
        m_ifm.return_value = True, False
        m_gcfm.return_value = 'developer_command', 'argument'

        # Run the method.
        await self.client.on_message('message')

        # Run assertions.
        m_ifm.assert_called_once_with('message')
        m_gcfm.assert_called_once_with('j!', 'message')
        m_rsc.assert_not_called()
        m_rrc.assert_called()


    @mock.patch('lib.bot.JadieClient.is_functional_message')
    @mock.patch('lib.util.parsing.get_command_from_message')
    @mock.patch('lib.commands.run_standard_command')
    @mock.patch('lib.commands.run_reactive_command')
    async def test_on_message_functional_author_not_developer_unknown_command(self, m_rrc, m_rsc, m_gcfm, m_ifm):
        """lib.bot.JadieClient.on_message.functional.author_not_developer.unknown_command"""
        # Set return value for is_functional_message and get_command_from_message
        m_ifm.return_value = True, False
        m_gcfm.return_value = 'unknown_command', 'argument'

        # Run the method.
        await self.client.on_message('message')

        # Run assertions.
        m_ifm.assert_called_once_with('message')
        m_gcfm.assert_called_once_with('j!', 'message')
        m_rsc.assert_not_called()
        m_rrc.assert_called()


    @mock.patch('lib.bot.JadieClient.is_functional_message')
    @mock.patch('lib.util.parsing.get_command_from_message')
    @mock.patch('lib.commands.run_standard_command')
    @mock.patch('lib.commands.run_reactive_command')
    async def test_on_message_functional_author_is_developer_no_command(self, m_rrc, m_rsc, m_gcfm, m_ifm):
        """lib.bot.JadieClient.on_message.functional.author_is_developer.no_command"""
        # Set return value for is_functional_message and get_command_from_message
        m_ifm.return_value = True, True
        m_gcfm.return_value = None, None

        # Run the method.
        await self.client.on_message('message')

        # Run assertions.
        m_ifm.assert_called_once_with('message')
        m_gcfm.assert_called_once_with('j!', 'message')
        m_rsc.assert_not_called()
        m_rrc.assert_called()


    @mock.patch('lib.bot.JadieClient.is_functional_message')
    @mock.patch('lib.util.parsing.get_command_from_message')
    @mock.patch('lib.commands.run_standard_command')
    @mock.patch('lib.commands.run_reactive_command')
    async def test_on_message_functional_author_is_developer_public_command(self, m_rrc, m_rsc, m_gcfm, m_ifm):
        """lib.bot.JadieClient.on_message.functional.author_is_developer.public_command"""
        # Set return value for is_functional_message and get_command_from_message
        m_ifm.return_value = True, True
        m_gcfm.return_value = 'public_command', 'argument'

        # Run the method.
        await self.client.on_message('message')

        # Run assertions.
        m_ifm.assert_called_once_with('message')
        m_gcfm.assert_called_once_with('j!', 'message')
        m_rsc.assert_called_once_with('public_command', 'hello', self.client, 'message', 'argument')
        m_rrc.assert_not_called()


    @mock.patch('lib.bot.JadieClient.is_functional_message')
    @mock.patch('lib.util.parsing.get_command_from_message')
    @mock.patch('lib.commands.run_standard_command')
    @mock.patch('lib.commands.run_reactive_command')
    async def test_on_message_functional_author_is_developer_developer_command(self, m_rrc, m_rsc, m_gcfm, m_ifm):
        """lib.bot.JadieClient.on_message.functional.author_is_developer.developer_command"""
        # Set return value for is_functional_message and get_command_from_message
        m_ifm.return_value = True, True
        m_gcfm.return_value = 'developer_command', 'argument'

        # Run the method.
        await self.client.on_message('message')

        # Run assertions.
        m_ifm.assert_called_once_with('message')
        m_gcfm.assert_called_once_with('j!', 'message')
        m_rsc.assert_called_once_with('developer_command', 'world', self.client, 'message', 'argument')
        m_rrc.assert_not_called()


    @mock.patch('lib.bot.JadieClient.is_functional_message')
    @mock.patch('lib.util.parsing.get_command_from_message')
    @mock.patch('lib.commands.run_standard_command')
    @mock.patch('lib.commands.run_reactive_command')
    async def test_on_message_functional_author_is_developer_unknown_command(self, m_rrc, m_rsc, m_gcfm, m_ifm):
        """lib.bot.JadieClient.on_message.functional.author_is_developer.unknown_command"""
        # Set return value for is_functional_message and get_command_from_message
        m_ifm.return_value = True, True
        m_gcfm.return_value = 'unknown_command', 'argument'

        # Run the method.
        await self.client.on_message('message')

        # Run assertions.
        m_ifm.assert_called_once_with('message')
        m_gcfm.assert_called_once_with('j!', 'message')
        m_rsc.assert_not_called()
        m_rrc.assert_called()


    @mock.patch('lib.bot.JadieClient.message_object_has_required_attributes')
    @mock.patch('lib.bot.JadieClient.ignore_developer_check')
    async def test_is_functional_message_no_attributes(self, m_idc, m_mohra):
        """lib.bot.JadieClient.is_functional_message_no_attributes"""
        # Modify client object
        self.client.deployment_client = True

        # Set return value for message_object_has_required_attributes and ignore_developer_check
        m_mohra.return_value = False
        m_idc.return_value = False

        # Create the message object.
        message = mock.MagicMock(author=mock.MagicMock(id=4843))

        # Run the method.
        functional_message, author_is_developer = await self.client.is_functional_message(message)

        # Run assertions.
        self.assertFalse(functional_message)


    @mock.patch('lib.bot.JadieClient.message_object_has_required_attributes')
    @mock.patch('lib.bot.JadieClient.ignore_developer_check')
    async def test_is_functional_message_ignore_developer_author_is_developer(self, m_idc, m_mohra):
        """lib.bot.JadieClient.is_functional_message.ignore_developer.author_is_developer"""
        # Modify client object
        self.client.deployment_client = True

        # Set return value for message_object_has_required_attributes and ignore_developer_check
        m_mohra.return_value = True
        m_idc.return_value = True

        # Create the message object.
        message = mock.MagicMock(author=mock.MagicMock(id=4843))

        # Run the method.
        functional_message, author_is_developer = await self.client.is_functional_message(message)

        # Run assertions.
        self.assertFalse(functional_message)
        self.assertTrue(author_is_developer)


    @mock.patch('lib.bot.JadieClient.message_object_has_required_attributes')
    @mock.patch('lib.bot.JadieClient.ignore_developer_check')
    async def test_is_functional_message_ignore_developer_author_not_developer(self, m_idc, m_mohra):
        """lib.bot.JadieClient.is_functional_message.ignore_developer.author_not_developer"""
        # Modify client object
        self.client.deployment_client = True

        # Set return value for message_object_has_required_attributes and ignore_developer_check
        m_mohra.return_value = True
        m_idc.return_value = True

        # Create the message object.
        message = mock.MagicMock(author=mock.MagicMock(id=2021))

        # Run the method.
        functional_message, author_is_developer = await self.client.is_functional_message(message)

        # Run assertions.
        self.assertFalse(functional_message)
        self.assertFalse(author_is_developer)


    @mock.patch('lib.bot.JadieClient.message_object_has_required_attributes')
    @mock.patch('lib.bot.JadieClient.ignore_developer_check')
    async def test_is_functional_message_deployment_client_author_is_developer(self, m_idc, m_mohra):
        """lib.bot.JadieClient.is_functional_message.deployment_client.author_is_developer"""
        # Modify client object
        self.client.deployment_client = True

        # Set return value for message_object_has_required_attributes and ignore_developer_check
        m_mohra.return_value = True
        m_idc.return_value = False

        # Create the message object.
        message = mock.MagicMock(author=mock.MagicMock(id=4843))

        # Run the method.
        functional_message, author_is_developer = await self.client.is_functional_message(message)

        # Run assertions.
        self.assertTrue(functional_message)
        self.assertTrue(author_is_developer)


    @mock.patch('lib.bot.JadieClient.message_object_has_required_attributes')
    @mock.patch('lib.bot.JadieClient.ignore_developer_check')
    async def test_is_functional_message_deployment_client_author_not_developer(self, m_idc, m_mohra):
        """lib.bot.JadieClient.is_functional_message.deployment_client.author_not_developer"""
        # Modify client object
        self.client.deployment_client = True

        # Set return value for message_object_has_required_attributes and ignore_developer_check
        m_mohra.return_value = True
        m_idc.return_value = False

        # Create the message object.
        message = mock.MagicMock(author=mock.MagicMock(id=2021))

        # Run the method.
        functional_message, author_is_developer = await self.client.is_functional_message(message)

        # Run assertions.
        self.assertTrue(functional_message)
        self.assertFalse(author_is_developer)


    @mock.patch('lib.bot.JadieClient.message_object_has_required_attributes')
    @mock.patch('lib.bot.JadieClient.ignore_developer_check')
    async def test_is_functional_message_development_client_author_is_developer(self, m_idc, m_mohra):
        """lib.bot.JadieClient.is_functional_message.development_client.author_is_developer"""
        # Modify client object
        self.client.deployment_client = False

        # Set return value for message_object_has_required_attributes and ignore_developer_check
        m_mohra.return_value = True
        m_idc.return_value = False

        # Create the message object.
        message = mock.MagicMock(author=mock.MagicMock(id=4843))

        # Run the method.
        functional_message, author_is_developer = await self.client.is_functional_message(message)

        # Run assertions.
        self.assertTrue(functional_message)
        self.assertTrue(author_is_developer)


    @mock.patch('lib.bot.JadieClient.message_object_has_required_attributes')
    @mock.patch('lib.bot.JadieClient.ignore_developer_check')
    async def test_is_functional_message_development_client_author_not_developer(self, m_idc, m_mohra):
        """lib.bot.JadieClient.is_functional_message.development_client.author_not_developer"""
        # Modify client object
        self.client.deployment_client = False

        # Set return value for message_object_has_required_attributes and ignore_developer_check
        m_mohra.return_value = True
        m_idc.return_value = False

        # Create the message object.
        message = mock.MagicMock(author=mock.MagicMock(id=2021))

        # Run the method.
        functional_message, author_is_developer = await self.client.is_functional_message(message)

        # Run assertions.
        self.assertFalse(functional_message)
        self.assertFalse(author_is_developer)


    async def test_ignore_developer_check_dont_ignore_developer_author_is_developer_toggle(self):
        """lib.bot.JadieClient.ignore_developer_check.dont_ignore_developer.author_is_developer.toggle"""
        # Modify client object
        self.client.ignore_developer = False
        self.client.toggle_ignore_developer = mock.AsyncMock()

        # Create the message object.
        message = mock.MagicMock(content='j!toggleignoredev or whatever')

        # Run the method.
        ignore = await self.client.ignore_developer_check(message, True)

        # Run assertions.
        self.assertFalse(ignore)
        self.client.toggle_ignore_developer.assert_not_called()


    async def test_ignore_developer_check_dont_ignore_developer_author_is_developer_not_toggle(self):
        """lib.bot.JadieClient.ignore_developer_check.dont_ignore_developer.author_is_developer.not_toggle"""
        # Modify client object
        self.client.ignore_developer = False
        self.client.toggle_ignore_developer = mock.AsyncMock()

        # Create the message object.
        message = mock.MagicMock(content='some other message')

        # Run the method.
        ignore = await self.client.ignore_developer_check(message, True)

        # Run assertions.
        self.assertFalse(ignore)
        self.client.toggle_ignore_developer.assert_not_called()


    async def test_ignore_developer_check_dont_ignore_developer_author_not_developer_toggle(self):
        """lib.bot.JadieClient.ignore_developer_check.dont_ignore_developer.author_not_developer.toggle"""
        # Modify client object
        self.client.ignore_developer = False
        self.client.toggle_ignore_developer = mock.AsyncMock()

        # Create the message object.
        message = mock.MagicMock(content='j!toggleignoredev or whatever')

        # Run the method.
        ignore = await self.client.ignore_developer_check(message, False)

        # Run assertions.
        self.assertFalse(ignore)
        self.client.toggle_ignore_developer.assert_not_called()


    async def test_ignore_developer_check_dont_ignore_developer_author_not_developer_not_toggle(self):
        """lib.bot.JadieClient.ignore_developer_check.dont_ignore_developer.author_not_developer.not_toggle"""
        # Modify client object
        self.client.ignore_developer = False
        self.client.toggle_ignore_developer = mock.AsyncMock()

        # Create the message object.
        message = mock.MagicMock(content='some other message')

        # Run the method.
        ignore = await self.client.ignore_developer_check(message, False)

        # Run assertions.
        self.assertFalse(ignore)
        self.client.toggle_ignore_developer.assert_not_called()


    async def test_ignore_developer_check_ignore_developer_author_is_developer_toggle(self):
        """lib.bot.JadieClient.ignore_developer_check.ignore_developer.author_is_developer.toggle"""
        # Modify client object
        self.client.ignore_developer = True
        self.client.toggle_ignore_developer = mock.AsyncMock()

        # Create the message object.
        message = mock.MagicMock(content='j!toggleignoredev or whatever')

        # Run the method.
        ignore = await self.client.ignore_developer_check(message, True)

        # Run assertions.
        self.assertTrue(ignore)
        self.client.toggle_ignore_developer.assert_called_once_with(self.client, message)


    async def test_ignore_developer_check_ignore_developer_author_is_developer_not_toggle(self):
        """lib.bot.JadieClient.ignore_developer_check.ignore_developer.author_is_developer.not_toggle"""
        # Modify client object
        self.client.ignore_developer = True
        self.client.toggle_ignore_developer = mock.AsyncMock()

        # Create the message object.
        message = mock.MagicMock(content='some other message')

        # Run the method.
        ignore = await self.client.ignore_developer_check(message, True)

        # Run assertions.
        self.assertTrue(ignore)
        self.client.toggle_ignore_developer.assert_not_called()


    async def test_ignore_developer_check_ignore_developer_author_not_developer_toggle(self):
        """lib.bot.JadieClient.ignore_developer_check.ignore_developer.author_not_developer.toggle"""
        # Modify client object
        self.client.ignore_developer = True
        self.client.toggle_ignore_developer = mock.AsyncMock()

        # Create the message object.
        message = mock.MagicMock(content='j!toggleignoredev or whatever')

        # Run the method.
        ignore = await self.client.ignore_developer_check(message, False)

        # Run assertions.
        self.assertFalse(ignore)
        self.client.toggle_ignore_developer.assert_not_called()


    async def test_ignore_developer_check_ignore_developer_author_not_developer_not_toggle(self):
        """lib.bot.JadieClient.ignore_developer_check.ignore_developer.author_not_developer.not_toggle"""
        # Modify client object
        self.client.ignore_developer = True
        self.client.toggle_ignore_developer = mock.AsyncMock()

        # Create the message object.
        message = mock.MagicMock(content='some other message')

        # Run the method.
        ignore = await self.client.ignore_developer_check(message, False)

        # Run assertions.
        self.assertFalse(ignore)
        self.client.toggle_ignore_developer.assert_not_called()

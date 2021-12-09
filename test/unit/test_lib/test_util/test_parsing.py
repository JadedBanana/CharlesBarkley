from unittest import TestCase, mock
from lib.util import parsing


class TestParsing(TestCase):


    def test_normalize_string_not_str(self):
        """lib.util.parsing.normalize_string.not_str"""
        # Run the method.
        response = parsing.normalize_string(27)

        # Run assertions.
        self.assertEqual(response, 27)


    def test_normalize_string_newlines(self):
        """lib.util.parsing.normalize_string.newlines"""
        # Run the method.
        response = parsing.normalize_string('beep\nbeep')

        # Run assertions.
        self.assertEqual(response, 'beep beep')


    def test_normalize_string_tabs(self):
        """lib.util.parsing.normalize_string.tabs"""
        # Run the method.
        response = parsing.normalize_string('beep\tbeep')

        # Run assertions.
        self.assertEqual(response, 'beep beep')


    def test_normalize_string_leading_spaces(self):
        """lib.util.parsing.normalize_string.leading_spaces"""
        # Run the method.
        response = parsing.normalize_string('           heck')

        # Run assertions.
        self.assertEqual(response, 'heck')


    def test_normalize_string_trailing_spaces(self):
        """lib.util.parsing.normalize_string.trailing_spaces"""
        # Run the method.
        response = parsing.normalize_string('hell               ')

        # Run assertions.
        self.assertEqual(response, 'hell')


    def test_normalize_string_double_spaces(self):
        """lib.util.parsing.normalize_string.double_spaces"""
        # Run the method.
        response = parsing.normalize_string('alex    is    so      cute')

        # Run assertions.
        self.assertEqual(response, 'alex is so cute')


    def test_normalize_string_keep_others(self):
        """lib.util.parsing.normalize_string.keep_others"""
        # Iterate through unicode characters.
        for i in range(52296):

            # Except the ones we expect to be removed.
            if i in [ord(' '), ord('\n'), ord('\t')]:
                continue

            # Run the method.
            response = parsing.normalize_string(f'{chr(i)}')

            # Run assertions.
            self.assertEqual(response, f'{chr(i)}')


    def test_get_command_from_message_no_command(self):
        """lib.util.parsing.get_command_from_message.no_command.no_argument"""
        # Run the method.
        command, argument = parsing.get_command_from_message('j!', mock.MagicMock(content='just a normal ass message!'))

        # Run assertions.
        self.assertIsNone(command)
        self.assertIsNone(argument)


    def test_get_command_from_message_uppercase_command_no_argument(self):
        """lib.util.parsing.get_command_from_message.uppercase_command.no_argument"""
        # Run the method.
        command, argument = parsing.get_command_from_message('j!', mock.MagicMock(content='J!COMMANDNAME'))

        # Run assertions.
        self.assertEqual(command, 'commandname')
        self.assertIsNone(argument)


    def test_get_command_from_message_lowercase_command_no_argument(self):
        """lib.util.parsing.get_command_from_message.lowercase_command.no_argument"""
        # Run the method.
        command, argument = parsing.get_command_from_message('j!', mock.MagicMock(content='j!commandname'))

        # Run assertions.
        self.assertEqual(command, 'commandname')
        self.assertIsNone(argument)


    def test_get_command_from_message_uppercase_command_single_argument(self):
        """lib.util.parsing.get_command_from_message.uppercase_command.single_argument"""
        # Run the method.
        command, argument = parsing.get_command_from_message('j!', mock.MagicMock(content='J!COMMANDNAME argument'))

        # Run assertions.
        self.assertEqual(command, 'commandname')
        self.assertEqual(argument, 'argument')


    def test_get_command_from_message_lowercase_command_single_argument(self):
        """lib.util.parsing.get_command_from_message.lowercase_command.single_argument"""
        # Run the method.
        command, argument = parsing.get_command_from_message('j!', mock.MagicMock(content='j!commandname argument'))

        # Run assertions.
        self.assertEqual(command, 'commandname')
        self.assertEqual(argument, 'argument')


    def test_get_command_from_message_uppercase_command_multi_argument(self):
        """lib.util.parsing.get_command_from_message.uppercase_command.single_argument"""
        # Run the method.
        command, argument = parsing.get_command_from_message('j!', mock.MagicMock(content='J!COMMANDNAME argument argument argument rah'))

        # Run assertions.
        self.assertEqual(command, 'commandname')
        self.assertEqual(argument, 'argument argument argument rah')


    def test_get_command_from_message_lowercase_command_multi_argument(self):
        """lib.util.parsing.get_command_from_message.lowercase_command.single_argument"""
        # Run the method.
        command, argument = parsing.get_command_from_message('j!', mock.MagicMock(content='j!commandname argument argument argument rah'))

        # Run assertions.
        self.assertEqual(command, 'commandname')
        self.assertEqual(argument, 'argument argument argument rah')

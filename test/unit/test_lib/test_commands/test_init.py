# Package Imports
from unittest import mock, TestCase

# Local Imports
from lib import commands


class TestCommandsSynchronous(TestCase):


    @mock.patch('pkgutil.iter_modules')
    @mock.patch('lib.commands.load_commands_from_package')
    def test_load_all_commands(self, m_lcfp, m_im):
        """lib.commands.load_all_commands"""
        # Set return value for iter_modules
        m_im.return_value = [
            ('importer', 'package1', True),
            ('importer', 'package2', True),
            ('importer', 'package3', True)
        ]

        # Set side effect for load_commands_from_package
        lcfp_called_with = []


        def load_commands_from_package_side_effect(*args, **kwargs):
            lcfp_called_with.append(args)

        m_lcfp.side_effect = load_commands_from_package_side_effect

        # Run the method.
        public_command_dict, developer_command_dict, reactive_command_list, specialized_command_dict, \
            command_initialize_method_list = commands.load_all_commands()

        # Run assertions.
        self.assertTrue(len(lcfp_called_with) == 3)
        self.assertEqual(lcfp_called_with[0], ('package1', {}, {}, [], {}, []))
        self.assertEqual(lcfp_called_with[1], ('package2', {}, {}, [], {}, []))
        self.assertEqual(lcfp_called_with[2], ('package3', {}, {}, [], {}, []))
        self.assertEqual(public_command_dict, {})
        self.assertEqual(developer_command_dict, {})
        self.assertEqual(reactive_command_list, [])
        self.assertEqual(specialized_command_dict, {})
        self.assertEqual(command_initialize_method_list, [])

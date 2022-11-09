# Local Imports
from lib.commands.dev import error_test

# Package Imports
from unittest import mock, IsolatedAsyncioTestCase


class TestErrorTestAsynchronous(IsolatedAsyncioTestCase):


    async def test_error_test(self):
        """lib.commands.test_dev.error_test.error_test"""
        # Run the method.
        with self.assertRaises(Exception):
            await error_test.error_test(mock.MagicMock(), 'message', 'argument')

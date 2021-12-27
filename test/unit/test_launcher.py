# Package Imports
from unittest import mock, TestCase

# Local Imports
import launcher


class TestLauncher(TestCase):


    @mock.patch('launcher.parse_running_parameters')
    @mock.patch('launcher.run_primary_initializers')
    @mock.patch('launcher.cron_check_passed')
    @mock.patch('launcher.run_secondary_initializers')
    @mock.patch('launcher.start_background_threads')
    @mock.patch('lib.bot.launch')
    def test_launch_fail_cron_check(self, m_l, m_sbt, m_rsi, m_ccp, m_rpi, m_prp):
        """launcher.launch.fail_cron_check"""
        # Set the value of the cron check.
        m_ccp.return_value = False

        # Run the method.
        launcher.launch()

        # Run assertions.
        m_prp.assert_called_once_with()
        m_rpi.assert_called_once_with()
        m_ccp.assert_called_once_with()
        m_rsi.assert_not_called()
        m_sbt.assert_not_called()
        m_l.assert_not_called()


    @mock.patch('launcher.parse_running_parameters')
    @mock.patch('launcher.run_primary_initializers')
    @mock.patch('launcher.cron_check_passed')
    @mock.patch('launcher.run_secondary_initializers')
    @mock.patch('launcher.start_background_threads')
    @mock.patch('lib.bot.launch')
    def test_launch_pass_cron_check(self, m_l, m_sbt, m_rsi, m_ccp, m_rpi, m_prp):
        """launcher.launch.pass_cron_check"""
        # Set the value of the cron check.
        m_ccp.return_value = True

        # Run the method.
        launcher.launch()

        # Run assertions.
        m_prp.assert_called_once_with()
        m_rpi.assert_called_once_with()
        m_ccp.assert_called_once_with()
        m_rsi.assert_called_once_with()
        m_sbt.assert_called_once_with()
        m_l.assert_called_once_with()

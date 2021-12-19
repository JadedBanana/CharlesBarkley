# Package Imports
from unittest import mock, TestCase, IsolatedAsyncioTestCase

# Local Imports
from lib.commands.util import weather


class TestWeatherSynchronous(TestCase):


    def test_get_city(self):
        """lib.commands.util.weather.get_city"""
        # Run the method.
        result = weather.get_city({'name': 'why he ourple'})

        # Run assertions
        self.assertEqual(result, 'why he ourple')


    @mock.patch('iso3166.countries.get')
    def test_get_country_alt_code(self, m_g):
        """lib.commands.util.weather.get_country.alt_code"""
        # Set the alternate country codes and mock return values.
        weather.WEATHER_ALT_COUNTRY_CODES = {'BO': 'Bolivia'}
        m_g.name = 'Soviet Union'
        m_g.return_value = m_g

        # Run the method.
        result = weather.get_country({'sys': {'country': 'BO'}})

        # Run assertions
        self.assertEqual(result, 'Bolivia')
        m_g.assert_not_called()


    @mock.patch('iso3166.countries.get')
    def test_get_country_standard_code(self, m_g):
        """lib.commands.util.weather.get_country.standard_code"""
        # Set the alternate country codes and mock return values.
        weather.WEATHER_ALT_COUNTRY_CODES = {'BO': 'Bolivia'}
        m_g.name = 'Soviet Union'
        m_g.return_value = m_g

        # Run the method.
        result = weather.get_country({'sys': {'country': 'SU'}})

        # Run assertions
        self.assertEqual(result, 'Soviet Union')
        m_g.assert_called_once_with('SU')


    @mock.patch('iso3166.countries.get')
    def test_get_country_no_country(self, m_g):
        """lib.commands.util.weather.get_country.no_country"""
        # Set the alternate country codes and mock return values.
        weather.WEATHER_ALT_COUNTRY_CODES = {'BO': 'Bolivia'}
        m_g.name = 'Soviet Union'
        m_g.return_value = m_g

        # Run the method.
        result = weather.get_country({'sys': {}})

        # Run assertions
        self.assertTrue('unknown' in result.lower())
        m_g.assert_not_called()


    @mock.patch('iso3166.countries.get')
    def test_get_country_country_not_str(self, m_g):
        """lib.commands.util.weather.get_country.country_not_str"""
        # Set the alternate country codes and mock return values.
        weather.WEATHER_ALT_COUNTRY_CODES = {'BO': 'Bolivia'}
        m_g.name = 'Soviet Union'
        m_g.return_value = m_g

        # Run the method.
        result = weather.get_country({'sys': {'country': 23}})

        # Run assertions
        self.assertTrue('unknown' in result.lower())
        m_g.assert_not_called()

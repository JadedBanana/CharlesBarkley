# Package Imports
from unittest import mock, IsolatedAsyncioTestCase
from datetime import datetime

# Local Imports
from lib.commands.secret import feliz


class TestFelizAsynchronous(IsolatedAsyncioTestCase):


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_lunes_is_monday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_lunes.is_monday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=3, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_lunes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 0, False)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_lunes_is_tuesday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_lunes.is_tuesday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=4, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_lunes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 0, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_lunes_is_wednesday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_lunes.is_wednesday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=5, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_lunes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 0, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_lunes_is_thursday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_lunes.is_thursday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=6, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_lunes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 0, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_lunes_is_friday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_lunes.is_friday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=7, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_lunes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 0, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_lunes_is_saturday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_lunes.is_saturday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=8, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_lunes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 0, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_lunes_is_sunday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_lunes.is_sunday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=9, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_lunes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 0, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_martes_is_monday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_martes.is_monday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=3, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_martes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 1, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_martes_is_tuesday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_martes.is_tuesday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=4, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_martes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 1, False)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_martes_is_wednesday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_martes.is_wednesday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=5, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_martes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 1, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_martes_is_thursday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_martes.is_thursday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=6, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_martes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 1, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_martes_is_friday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_martes.is_friday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=7, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_martes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 1, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_martes_is_saturday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_martes.is_saturday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=8, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_martes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 1, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_martes_is_sunday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_martes.is_sunday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=9, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_martes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 1, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_miercoles_is_monday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_miercoles.is_monday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=3, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_miercoles('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 2, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_miercoles_is_tuesday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_miercoles.is_tuesday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=4, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_miercoles('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 2, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_miercoles_is_wednesday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_miercoles.is_wednesday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=5, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_miercoles('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 2, False)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_miercoles_is_thursday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_miercoles.is_thursday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=6, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_miercoles('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 2, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_miercoles_is_friday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_miercoles.is_friday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=7, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_miercoles('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 2, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_miercoles_is_saturday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_miercoles.is_saturday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=8, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_miercoles('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 2, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_miercoles_is_sunday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_miercoles.is_sunday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=9, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_miercoles('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 2, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_jueves_is_monday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_jueves.is_monday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=3, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_jueves('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 3, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_jueves_is_tuesday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_jueves.is_tuesday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=4, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_jueves('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 3, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_jueves_is_wednesday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_jueves.is_wednesday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=5, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_jueves('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 3, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_jueves_is_thursday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_jueves.is_thursday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=6, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_jueves('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 3, False)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_jueves_is_friday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_jueves.is_friday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=7, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_jueves('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 3, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_jueves_is_saturday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_jueves.is_saturday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=8, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_jueves('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 3, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_jueves_is_sunday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_jueves.is_sunday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=9, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_jueves('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 3, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_viernes_is_monday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_viernes.is_monday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=3, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_viernes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 4, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_viernes_is_tuesday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_viernes.is_tuesday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=4, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_viernes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 4, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_viernes_is_wednesday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_viernes.is_wednesday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=5, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_viernes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 4, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_viernes_is_thursday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_viernes.is_thursday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=6, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_viernes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 4, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_viernes_is_friday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_viernes.is_friday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=7, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_viernes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 4, False)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_viernes_is_saturday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_viernes.is_saturday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=8, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_viernes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 4, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_viernes_is_sunday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_viernes.is_sunday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=9, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_viernes('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 4, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_sabado_is_monday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_sabado.is_monday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=3, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_sabado('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 5, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_sabado_is_tuesday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_sabado.is_tuesday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=4, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_sabado('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 5, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_sabado_is_wednesday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_sabado.is_wednesday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=5, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_sabado('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 5, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_sabado_is_thursday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_sabado.is_thursday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=6, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_sabado('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 5, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_sabado_is_friday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_sabado.is_friday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=7, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_sabado('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 5, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_sabado_is_saturday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_sabado.is_saturday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=8, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_sabado('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 5, False)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_sabado_is_sunday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_sabado.is_sunday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=9, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_sabado('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 5, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_domingo_is_monday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_domingo.is_monday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=3, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_domingo('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 6, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_domingo_is_tuesday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_domingo.is_tuesday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=4, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_domingo('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 6, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_domingo_is_wednesday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_domingo.is_wednesday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=5, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_domingo('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 6, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_domingo_is_thursday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_domingo.is_thursday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=6, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_domingo('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 6, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_domingo_is_friday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_domingo.is_friday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=7, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_domingo('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 6, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_domingo_is_saturday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_domingo.is_saturday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=8, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_domingo('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 6, True)


    @mock.patch('lib.util.discord_info.get_guild_time')
    @mock.patch('lib.commands.secret.feliz.feliz_send_image')
    async def test_feliz_domingo_is_sunday(self, m_fsi, m_ggt):
        """lib.commands.secret.feliz.feliz_domingo.is_sunday"""
        # Set the return value for m_ggt and create the message.
        m_ggt.return_value = datetime(year=2000, month=1, day=9, hour=12)
        message = mock.MagicMock(channel='channel')

        # Run the method.
        await feliz.feliz_domingo('bot', message, 'argument')

        # Run assertions.
        m_fsi.assert_called_once_with(message, 6, False)

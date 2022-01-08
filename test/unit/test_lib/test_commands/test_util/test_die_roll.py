# Package Imports
from unittest import mock, IsolatedAsyncioTestCase

# Local Imports
from lib.commands.util import die_roll


class TestDieRollAsynchronous(IsolatedAsyncioTestCase):


    @mock.patch('lib.util.parsing.normalize_string')
    @mock.patch('lib.commands.util.die_roll.perform_roll')
    @mock.patch('lib.commands.util.die_roll.argument_valid')
    @mock.patch('lib.commands.util.die_roll.parse_die_roll')
    async def test_die_roll_no_argument_argument_invalid(self, m_pdr, m_av, m_pr, m_ns):
        """lib.commands.util.die_roll.die_roll.no_argument.argument_invalid"""
        # Set return_values.
        m_ns.return_value = None
        m_av.return_value = False

        # Run the method.
        await die_roll.die_roll('message', 'argument')

        # Run assertions.
        m_ns.assert_called_once_with('argument')
        m_pr.assert_called_once_with('message', 1, 6, 0)
        m_av.assert_not_called()
        m_pdr.assert_not_called()


    @mock.patch('lib.util.parsing.normalize_string')
    @mock.patch('lib.commands.util.die_roll.perform_roll')
    @mock.patch('lib.commands.util.die_roll.argument_valid')
    @mock.patch('lib.commands.util.die_roll.parse_die_roll')
    async def test_die_roll_no_argument_argument_valid(self, m_pdr, m_av, m_pr, m_ns):
        """lib.commands.util.die_roll.die_roll.no_argument.argument_valid"""
        # Set return_values.
        m_ns.return_value = None
        m_av.return_value = True

        # Run the method.
        await die_roll.die_roll('message', 'argument')

        # Run assertions.
        m_ns.assert_called_once_with('argument')
        m_pr.assert_called_once_with('message', 1, 6, 0)
        m_av.assert_not_called()
        m_pdr.assert_not_called()


    @mock.patch('lib.util.parsing.normalize_string')
    @mock.patch('lib.commands.util.die_roll.perform_roll')
    @mock.patch('lib.commands.util.die_roll.argument_valid')
    @mock.patch('lib.commands.util.die_roll.parse_die_roll')
    async def test_die_roll_yes_argument_argument_invalid(self, m_pdr, m_av, m_pr, m_ns):
        """lib.commands.util.die_roll.die_roll.yes_argument.argument_invalid"""
        # Set return_values.
        m_ns.return_value = 'argument 2'
        m_av.return_value = False

        # Run the method.
        await die_roll.die_roll('message', 'argument')

        # Run assertions.
        m_ns.assert_called_once_with('argument')
        m_pr.assert_not_called()
        m_av.assert_called_once_with('message', 'argument2')
        m_pdr.assert_not_called()


    @mock.patch('lib.util.parsing.normalize_string')
    @mock.patch('lib.commands.util.die_roll.perform_roll')
    @mock.patch('lib.commands.util.die_roll.argument_valid')
    @mock.patch('lib.commands.util.die_roll.parse_die_roll')
    async def test_die_roll_yes_argument_argument_valid(self, m_pdr, m_av, m_pr, m_ns):
        """lib.commands.util.die_roll.die_roll.yes_argument.argument_valid"""
        # Set return_values.
        m_ns.return_value = 'argument 2'
        m_av.return_value = True

        # Run the method.
        await die_roll.die_roll('message', 'argument')

        # Run assertions.
        m_ns.assert_called_once_with('argument')
        m_pr.assert_not_called()
        m_av.assert_called_once_with('message', 'argument2')
        m_pdr.assert_called_once_with('message', 'argument2')


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_argument_valid_bad_char_multiple_d(self, m_stm, m_i):
        """lib.commands.util.die_roll.argument_valid.bad_char.multiple_d"""
        # Set the VALID_ARGUMENTS_CHARS.
        die_roll.VALID_ARGUMENTS_CHARS = 'argumen'

        # Run the method.
        result = await die_roll.argument_valid('message', 'argumentdd')

        # Run assertions.
        m_i.assert_called_once()
        m_stm.assert_called_once()
        self.assertFalse(result)


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_argument_valid_bad_char_single_d(self, m_stm, m_i):
        """lib.commands.util.die_roll.argument_valid.bad_char.single_d"""
        # Set the VALID_ARGUMENTS_CHARS.
        die_roll.VALID_ARGUMENTS_CHARS = 'argumen'

        # Run the method.
        result = await die_roll.argument_valid('message', 'argumentd')

        # Run assertions.
        m_i.assert_called_once()
        m_stm.assert_called_once()
        self.assertFalse(result)


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_argument_valid_bad_char_no_d(self, m_stm, m_i):
        """lib.commands.util.die_roll.argument_valid.bad_char.no_d"""
        # Set the VALID_ARGUMENTS_CHARS.
        die_roll.VALID_ARGUMENTS_CHARS = 'argumen'

        # Run the method.
        result = await die_roll.argument_valid('message', 'argument')

        # Run assertions.
        m_i.assert_called_once()
        m_stm.assert_called_once()
        self.assertFalse(result)


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_argument_valid_good_char_multiple_d(self, m_stm, m_i):
        """lib.commands.util.die_roll.argument_valid.good_char.multiple_d"""
        # Set the VALID_ARGUMENTS_CHARS.
        die_roll.VALID_ARGUMENTS_CHARS = 'argumentd'

        # Run the method.
        result = await die_roll.argument_valid('message', 'argumentdd')

        # Run assertions.
        m_i.assert_called_once()
        m_stm.assert_called_once()
        self.assertFalse(result)


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_argument_valid_good_char_single_d(self, m_stm, m_i):
        """lib.commands.util.die_roll.argument_valid.good_char.single_d"""
        # Set the VALID_ARGUMENTS_CHARS.
        die_roll.VALID_ARGUMENTS_CHARS = 'argumentd'

        # Run the method.
        result = await die_roll.argument_valid('message', 'argumentd')

        # Run assertions.
        m_i.assert_not_called()
        m_stm.assert_not_called()
        self.assertTrue(result)


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_argument_valid_good_char_no_d(self, m_stm, m_i):
        """lib.commands.util.die_roll.argument_valid.good_char.no_d"""
        # Set the VALID_ARGUMENTS_CHARS.
        die_roll.VALID_ARGUMENTS_CHARS = 'argumentd'

        # Run the method.
        result = await die_roll.argument_valid('message', 'argument')

        # Run assertions.
        m_i.assert_not_called()
        m_stm.assert_not_called()
        self.assertTrue(result)


    @mock.patch('lib.commands.util.die_roll.perform_roll')
    @mock.patch('lib.commands.util.die_roll.parse_count')
    @mock.patch('lib.commands.util.die_roll.parse_addendum')
    @mock.patch('lib.commands.util.die_roll.parse_sides')
    async def test_parse_die_roll_bad_count_bad_addendum_bad_sides(self, m_ps, m_pa, m_pc, m_pr):
        """lib.commands.util.die_roll.parse_die_roll.bad_count.bad_addendum.bad_sides"""
        # Set return_values.
        m_pc.return_value = 2, None
        m_pa.return_value = 4, None
        m_ps.return_value = 8, False

        # Run the method.
        await die_roll.parse_die_roll('message', 'argument')

        # Run assertions.
        m_pr.assert_not_called()


    @mock.patch('lib.commands.util.die_roll.perform_roll')
    @mock.patch('lib.commands.util.die_roll.parse_count')
    @mock.patch('lib.commands.util.die_roll.parse_addendum')
    @mock.patch('lib.commands.util.die_roll.parse_sides')
    async def test_parse_die_roll_valid_count_bad_addendum_bad_sides(self, m_ps, m_pa, m_pc, m_pr):
        """lib.commands.util.die_roll.parse_die_roll.valid_count.bad_addendum.bad_sides"""
        # Set return_values.
        m_pc.return_value = 2, 'post-count argument'
        m_pa.return_value = 4, None
        m_ps.return_value = 8, False

        # Run the method.
        await die_roll.parse_die_roll('message', 'argument')

        # Run assertions.
        m_pr.assert_not_called()


    @mock.patch('lib.commands.util.die_roll.perform_roll')
    @mock.patch('lib.commands.util.die_roll.parse_count')
    @mock.patch('lib.commands.util.die_roll.parse_addendum')
    @mock.patch('lib.commands.util.die_roll.parse_sides')
    async def test_parse_die_roll_bad_count_valid_addendum_bad_sides(self, m_ps, m_pa, m_pc, m_pr):
        """lib.commands.util.die_roll.parse_die_roll.bad_count.valid_addendum.bad_sides"""
        # Set return_values.
        m_pc.return_value = 2, None
        m_pa.return_value = 4, 'post-addendum argument'
        m_ps.return_value = 8, False

        # Run the method.
        await die_roll.parse_die_roll('message', 'argument')

        # Run assertions.
        m_pr.assert_not_called()


    @mock.patch('lib.commands.util.die_roll.perform_roll')
    @mock.patch('lib.commands.util.die_roll.parse_count')
    @mock.patch('lib.commands.util.die_roll.parse_addendum')
    @mock.patch('lib.commands.util.die_roll.parse_sides')
    async def test_parse_die_roll_valid_count_valid_addendum_bad_sides(self, m_ps, m_pa, m_pc, m_pr):
        """lib.commands.util.die_roll.parse_die_roll.valid_count.valid_addendum.bad_sides"""
        # Set return_values.
        m_pc.return_value = 2, 'post-count argument'
        m_pa.return_value = 4, 'post-addendum argument'
        m_ps.return_value = 8, False

        # Run the method.
        await die_roll.parse_die_roll('message', 'argument')

        # Run assertions.
        m_pr.assert_not_called()


    @mock.patch('lib.commands.util.die_roll.perform_roll')
    @mock.patch('lib.commands.util.die_roll.parse_count')
    @mock.patch('lib.commands.util.die_roll.parse_addendum')
    @mock.patch('lib.commands.util.die_roll.parse_sides')
    async def test_parse_die_roll_bad_count_bad_addendum_valid_sides(self, m_ps, m_pa, m_pc, m_pr):
        """lib.commands.util.die_roll.parse_die_roll.bad_count.bad_addendum.valid_sides"""
        # Set return_values.
        m_pc.return_value = 2, None
        m_pa.return_value = 4, None
        m_ps.return_value = 8, True

        # Run the method.
        await die_roll.parse_die_roll('message', 'argument')

        # Run assertions.
        m_pr.assert_not_called()


    @mock.patch('lib.commands.util.die_roll.perform_roll')
    @mock.patch('lib.commands.util.die_roll.parse_count')
    @mock.patch('lib.commands.util.die_roll.parse_addendum')
    @mock.patch('lib.commands.util.die_roll.parse_sides')
    async def test_parse_die_roll_valid_count_bad_addendum_valid_sides(self, m_ps, m_pa, m_pc, m_pr):
        """lib.commands.util.die_roll.parse_die_roll.valid_count.bad_addendum.valid_sides"""
        # Set return_values.
        m_pc.return_value = 2, 'post-count argument'
        m_pa.return_value = 4, None
        m_ps.return_value = 8, True

        # Run the method.
        await die_roll.parse_die_roll('message', 'argument')

        # Run assertions.
        m_pr.assert_not_called()


    @mock.patch('lib.commands.util.die_roll.perform_roll')
    @mock.patch('lib.commands.util.die_roll.parse_count')
    @mock.patch('lib.commands.util.die_roll.parse_addendum')
    @mock.patch('lib.commands.util.die_roll.parse_sides')
    async def test_parse_die_roll_bad_count_valid_addendum_valid_sides(self, m_ps, m_pa, m_pc, m_pr):
        """lib.commands.util.die_roll.parse_die_roll.bad_count.valid_addendum.valid_sides"""
        # Set return_values.
        m_pc.return_value = 2, None
        m_pa.return_value = 4, 'post-addendum argument'
        m_ps.return_value = 8, True

        # Run the method.
        await die_roll.parse_die_roll('message', 'argument')

        # Run assertions.
        m_pr.assert_not_called()


    @mock.patch('lib.commands.util.die_roll.perform_roll')
    @mock.patch('lib.commands.util.die_roll.parse_count')
    @mock.patch('lib.commands.util.die_roll.parse_addendum')
    @mock.patch('lib.commands.util.die_roll.parse_sides')
    async def test_parse_die_roll_valid_count_valid_addendum_valid_sides(self, m_ps, m_pa, m_pc, m_pr):
        """lib.commands.util.die_roll.parse_die_roll.valid_count.valid_addendum.valid_sides"""
        # Set return_values.
        m_pc.return_value = 2, 'post-count argument'
        m_pa.return_value = 4, 'post-addendum argument'
        m_ps.return_value = 8, True

        # Run the method.
        await die_roll.parse_die_roll('message', 'argument')

        # Run assertions.
        m_pc.assert_called_once()
        m_pa.assert_called_once()
        m_ps.assert_called_once()
        m_pr.assert_called_once_with('message', 2, 8, 4)


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_count_no_d(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_count.no_d"""
        # Run the method.
        count, remaining_argument = await die_roll.parse_count('message', 'argument')

        # Run assertions.
        self.assertEqual(count, 1)
        self.assertEqual(remaining_argument, 'argument')
        m_i.assert_not_called()
        m_stm.assert_not_called()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_count_no_count(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_count.no_count"""
        # Run the method.
        count, remaining_argument = await die_roll.parse_count('message', 'd')

        # Run assertions.
        self.assertEqual(remaining_argument, None)
        m_i.assert_called_once()
        m_stm.assert_called_once()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_count_invalid_count(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_count.invalid_count"""
        # Run the method.
        count, remaining_argument = await die_roll.parse_count('message', '+d')

        # Run assertions.
        self.assertEqual(remaining_argument, None)
        m_i.assert_called_once()
        m_stm.assert_called_once()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_count_negative_count(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_count.negative_count"""
        # Run the method.
        count, remaining_argument = await die_roll.parse_count('message', '-20d')

        # Run assertions.
        self.assertEqual(remaining_argument, None)
        m_i.assert_called_once()
        m_stm.assert_called_once()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_count_zero_count(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_count.zero_count"""
        # Run the method.
        count, remaining_argument = await die_roll.parse_count('message', '0d')

        # Run assertions.
        self.assertEqual(remaining_argument, None)
        m_i.assert_called_once()
        m_stm.assert_called_once()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_count_just_count(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_count.just_count"""
        # Run the method.
        count, remaining_argument = await die_roll.parse_count('message', '12d')

        # Run assertions.
        self.assertEqual(count, 12)
        self.assertEqual(remaining_argument, '')
        m_i.assert_not_called()
        m_stm.assert_not_called()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_count_extra_after(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_count.extra_after"""
        # Run the method.
        count, remaining_argument = await die_roll.parse_count('message', '12dwhatever381290-')

        # Run assertions.
        self.assertEqual(count, 12)
        self.assertEqual(remaining_argument, 'whatever381290-')
        m_i.assert_not_called()
        m_stm.assert_not_called()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_addendum_no_signs(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_addendum.no_signs"""
        # Run the method.
        addendum, remaining_argument = await die_roll.parse_addendum('message', 'whatever')

        # Run assertions.
        self.assertEqual(addendum, 0)
        self.assertEqual(remaining_argument, 'whatever')
        m_i.assert_not_called()
        m_stm.assert_not_called()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_addendum_positive_valid(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_addendum.positive.valid"""
        # Run the method.
        addendum, remaining_argument = await die_roll.parse_addendum('message', 'whatever+10')

        # Run assertions.
        self.assertEqual(addendum, 10)
        self.assertEqual(remaining_argument, 'whatever')
        m_i.assert_not_called()
        m_stm.assert_not_called()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_addendum_positive_invalid(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_addendum.positive.invalid"""
        # Run the method.
        addendum, remaining_argument = await die_roll.parse_addendum('message', 'whatever+')

        # Run assertions.
        self.assertIsNone(remaining_argument)
        m_i.assert_called_once()
        m_stm.assert_called_once()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_addendum_negative_valid(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_addendum.negative.valid"""
        # Run the method.
        addendum, remaining_argument = await die_roll.parse_addendum('message', 'whatever-10')

        # Run assertions.
        self.assertEqual(addendum, -10)
        self.assertEqual(remaining_argument, 'whatever')
        m_i.assert_not_called()
        m_stm.assert_not_called()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_addendum_negative_invalid(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_addendum.negative.invalid"""
        # Run the method.
        addendum, remaining_argument = await die_roll.parse_addendum('message', 'whatever-')

        # Run assertions.
        self.assertIsNone(remaining_argument)
        m_i.assert_called_once()
        m_stm.assert_called_once()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_addendum_multiple1_valid(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_addendum.multiple1.valid"""
        # Run the method.
        addendum, remaining_argument = await die_roll.parse_addendum('message', 'whatever-5+8')

        # Run assertions.
        self.assertEqual(addendum, 3)
        self.assertEqual(remaining_argument, 'whatever')
        m_i.assert_not_called()
        m_stm.assert_not_called()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_addendum_multiple1_invalid(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_addendum.multiple1.invalid"""
        # Run the method.
        addendum, remaining_argument = await die_roll.parse_addendum('message', 'whatever-+8')

        # Run assertions.
        self.assertIsNone(remaining_argument)
        m_i.assert_called_once()
        m_stm.assert_called_once()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_addendum_multiple2_valid(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_addendum.multiple2.valid"""
        # Run the method.
        addendum, remaining_argument = await die_roll.parse_addendum('message', 'whatever+5-8')

        # Run assertions.
        self.assertEqual(addendum, -3)
        self.assertEqual(remaining_argument, 'whatever')
        m_i.assert_not_called()
        m_stm.assert_not_called()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_addendum_multiple2_invalid(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_addendum.multiple2.invalid"""
        # Run the method.
        addendum, remaining_argument = await die_roll.parse_addendum('message', 'whatever+-8')

        # Run assertions.
        self.assertIsNone(remaining_argument)
        m_i.assert_called_once()
        m_stm.assert_called_once()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_sides_not_int(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_sides.not_int"""
        # Run the method.
        sides, valid = await die_roll.parse_sides('message', '')

        # Run assertions.
        self.assertEqual(sides, 6)
        self.assertTrue(valid)
        m_i.assert_not_called()
        m_stm.assert_not_called()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_sides_negative(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_sides.negative"""
        # Run the method.
        sides, valid = await die_roll.parse_sides('message', '-10')

        # Run assertions.
        self.assertFalse(valid)
        m_i.assert_called_once()
        m_stm.assert_called_once()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_sides_zero(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_sides.zero"""
        # Run the method.
        sides, valid = await die_roll.parse_sides('message', '0')

        # Run assertions.
        self.assertFalse(valid)
        m_i.assert_called_once()
        m_stm.assert_called_once()


    @mock.patch('lib.util.logger.BotLogger.info')
    @mock.patch('lib.util.messaging.send_text_message')
    async def test_parse_sides_valid(self, m_stm, m_i):
        """lib.commands.util.die_roll.parse_sides.valid"""
        # Run the method.
        sides, valid = await die_roll.parse_sides('message', '20')

        # Run assertions.
        self.assertEqual(sides, 20)
        self.assertTrue(valid)
        m_i.assert_not_called()
        m_stm.assert_not_called()
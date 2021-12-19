# Package Imports
from unittest import mock, TestCase

# Local Imports
from lib.util import misc


class TestMisc(TestCase):


    def test_get_multi_index_str_none(self):
        """lib.util.misc.get_multi_index.str.none"""
        # Run the method.
        indexes = misc.get_multi_index('asdfghjkl', 'p')

        # Run assertions.
        self.assertEqual(indexes, [])


    def test_get_multi_index_str_one(self):
        """lib.util.misc.get_multi_index.str.one"""
        # Run the method.
        indexes = misc.get_multi_index('whatever you say boss', 'bo')

        # Run assertions.
        self.assertEqual(indexes, [17])


    def test_get_multi_index_str_multiple_separate(self):
        """lib.util.misc.get_multi_index.str.multiple.separate"""
        # Run the method.
        indexes = misc.get_multi_index('gang gang', 'gan')

        # Run assertions.
        self.assertEqual(indexes, [0, 5])


    def test_get_multi_index_str_multiple_overlapping(self):
        """lib.util.misc.get_multi_index.str.multiple.overlapping"""
        # Run the method.
        indexes = misc.get_multi_index('ababa', 'aba')

        # Run assertions.
        self.assertEqual(indexes, [0, 2])


    def test_get_multi_index_list_none(self):
        """lib.util.misc.get_multi_index.list.none"""
        # Run the method.
        indexes = misc.get_multi_index([3, 65, 81, 59], 101)

        # Run assertions.
        self.assertEqual(indexes, [])


    def test_get_multi_index_list_one(self):
        """lib.util.misc.get_multi_index.list.one"""
        # Run the method.
        indexes = misc.get_multi_index([49, 13, 88, 'what', 'yes', 30], 'yes')

        # Run assertions.
        self.assertEqual(indexes, [4])


    def test_get_multi_index_list_multiple(self):
        """lib.util.misc.get_multi_index.list.multiple"""
        # Run the method.
        indexes = misc.get_multi_index([32, 54, 32, 848, 68, 'layman'], 32)

        # Run assertions.
        self.assertEqual(indexes, [0, 2])


    def test_upper_per_word_starting(self):
        """lib.util.misc.upper_per_word.starting"""
        # Run the method.
        result = misc.upper_per_word('whatever')

        # Run assertions.
        self.assertEqual(result, 'Whatever')


    def test_upper_per_word_after_space(self):
        """lib.util.misc.upper_per_word.after_space"""
        # Run the method.
        result = misc.upper_per_word('... okay')

        # Run assertions.
        self.assertEqual(result, '... Okay')

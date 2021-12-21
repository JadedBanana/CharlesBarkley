# Package Imports
from unittest import mock, TestCase

# Local Imports
from lib.util import arguments

class TestArguments(TestCase):


    @classmethod
    def setUpClass(cls):
        """
        Set up class method.
        Creates mock users to be used in sort_closest_user_list tests.
        """
        cls.sort_user_1 = mock.MagicMock()
        cls.sort_user_2 = mock.MagicMock()


    def test_sort_closest_user_list_1_wins_percentage_sum1_1_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.1_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_1_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.1_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_1_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.1_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_1_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 0, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_1_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 0, 5),
            (self.sort_user_2, 1, 0, 4, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_1_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 0, 5),
            (self.sort_user_2, 0, 1, 4, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_1_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 0, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_1_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 0, 5),
            (self.sort_user_2, 1, 0, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_1_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 0, 5),
            (self.sort_user_2, 0, 1, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_2_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.2_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_2_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.2_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_2_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.2_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_2_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 5),
            (self.sort_user_2, 0.75, 0.75, 0, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_2_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 5),
            (self.sort_user_2, 1, 0, 0, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_2_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 5),
            (self.sort_user_2, 0, 1, 0, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_2_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 0, 5),
            (self.sort_user_2, 0.75, 0.75, 0, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_2_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 0, 5),
            (self.sort_user_2, 1, 0, 0, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_2_wins_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 0, 5),
            (self.sort_user_2, 0, 1, 0, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_tie_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.tie_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_tie_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.tie_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_tie_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.tie_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_tie_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_tie_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 5),
            (self.sort_user_2, 1, 0, 4, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_tie_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 5),
            (self.sort_user_2, 0, 1, 4, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_tie_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 0, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_tie_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 0, 5),
            (self.sort_user_2, 1, 0, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_tie_nick_index_1_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.1_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 0, 5),
            (self.sort_user_2, 0, 1, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_1_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.1_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_1_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.1_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_1_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.1_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_1_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 0, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_1_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 5),
            (self.sort_user_2, 1, 0, 4, 0, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_1_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 5),
            (self.sort_user_2, 0, 1, 4, 0, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_1_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 0, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_1_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 4, 5),
            (self.sort_user_2, 1, 0, 4, 0, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_1_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 4, 5),
            (self.sort_user_2, 0, 1, 4, 0, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_2_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.2_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 0, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_2_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.2_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 0, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_2_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.2_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 0, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_2_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 0, 0, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_2_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 1, 0, 0, 0, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_2_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 0, 1, 0, 0, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_2_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 0, 0, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_2_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 5),
            (self.sort_user_2, 1, 0, 0, 0, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_2_wins_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 5),
            (self.sort_user_2, 0, 1, 0, 0, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_tie_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.tie_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_tie_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.tie_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_tie_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.tie_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_tie_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 0, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_tie_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 1, 0, 4, 0, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_tie_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 0, 1, 4, 0, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_tie_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 0, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_tie_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 5),
            (self.sort_user_2, 1, 0, 4, 0, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_tie_nick_index_2_wins_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.2_wins_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 5),
            (self.sort_user_2, 0, 1, 4, 0, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_1_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.1_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_1_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.1_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_1_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.1_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_1_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_1_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 5),
            (self.sort_user_2, 1, 0, 4, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_1_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 5),
            (self.sort_user_2, 0, 1, 4, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_1_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_1_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 4, 5),
            (self.sort_user_2, 1, 0, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_1_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 4, 5),
            (self.sort_user_2, 0, 1, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_2_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.2_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_2_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.2_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_2_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.2_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_2_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 0, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_2_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 1, 0, 0, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_2_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 0, 1, 0, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_2_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 0, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_2_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 5),
            (self.sort_user_2, 1, 0, 0, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_2_wins_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 5),
            (self.sort_user_2, 0, 1, 0, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_tie_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.tie_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_tie_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.tie_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_tie_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.tie_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_tie_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_tie_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 1, 0, 4, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_tie_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 0, 1, 4, 4, 1)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_tie_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_tie_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 5),
            (self.sort_user_2, 1, 0, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_tie_nick_index_tie_user_index_1_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.tie_user_index."""
        """1_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 5),
            (self.sort_user_2, 0, 1, 4, 4, 1)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_1_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.1_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 0, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_1_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.1_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 0, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_1_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.1_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 0, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_1_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 0, 1),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_1_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 0, 1),
            (self.sort_user_2, 1, 0, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_1_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 0, 1),
            (self.sort_user_2, 0, 1, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_1_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 0, 1),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_1_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 0, 1),
            (self.sort_user_2, 1, 0, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_1_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 0, 1),
            (self.sort_user_2, 0, 1, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_2_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.2_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 0, 1),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_2_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.2_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 0, 1),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_2_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.2_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 0, 1),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_2_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 1),
            (self.sort_user_2, 0.75, 0.75, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_2_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 1),
            (self.sort_user_2, 1, 0, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_2_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 1),
            (self.sort_user_2, 0, 1, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_2_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 0, 1),
            (self.sort_user_2, 0.75, 0.75, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_2_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 0, 1),
            (self.sort_user_2, 1, 0, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_2_wins_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 0, 1),
            (self.sort_user_2, 0, 1, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_tie_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.tie_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 0, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_tie_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.tie_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 0, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_tie_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.tie_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 0, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_tie_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 1),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_tie_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 1),
            (self.sort_user_2, 1, 0, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_tie_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 1),
            (self.sort_user_2, 0, 1, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_tie_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 0, 1),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_tie_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 0, 1),
            (self.sort_user_2, 1, 0, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_tie_nick_index_1_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.1_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 0, 1),
            (self.sort_user_2, 0, 1, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_1_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.1_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_1_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.1_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_1_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.1_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_1_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 1),
            (self.sort_user_2, 0.75, 0.75, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_1_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 1),
            (self.sort_user_2, 1, 0, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_1_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 1),
            (self.sort_user_2, 0, 1, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_1_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 4, 1),
            (self.sort_user_2, 0.75, 0.75, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_1_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 4, 1),
            (self.sort_user_2, 1, 0, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_1_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 4, 1),
            (self.sort_user_2, 0, 1, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_2_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.2_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 0, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_2_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.2_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 0, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_2_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.2_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 0, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_2_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 1),
            (self.sort_user_2, 0.75, 0.75, 0, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_2_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 1),
            (self.sort_user_2, 1, 0, 0, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_2_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 1),
            (self.sort_user_2, 0, 1, 0, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_2_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 1),
            (self.sort_user_2, 0.75, 0.75, 0, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_2_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 1),
            (self.sort_user_2, 1, 0, 0, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_2_wins_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 1),
            (self.sort_user_2, 0, 1, 0, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_tie_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.tie_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_tie_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.tie_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_tie_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.tie_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_tie_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 1),
            (self.sort_user_2, 0.75, 0.75, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_tie_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 1),
            (self.sort_user_2, 1, 0, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_tie_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 1),
            (self.sort_user_2, 0, 1, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_tie_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 1),
            (self.sort_user_2, 0.75, 0.75, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_tie_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 1),
            (self.sort_user_2, 1, 0, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_tie_nick_index_2_wins_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.2_wins_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 1),
            (self.sort_user_2, 0, 1, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_1_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.1_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_1_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.1_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_1_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.1_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_1_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 1),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_1_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 1),
            (self.sort_user_2, 1, 0, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_1_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 1),
            (self.sort_user_2, 0, 1, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_1_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 4, 1),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_1_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 4, 1),
            (self.sort_user_2, 1, 0, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_1_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 4, 1),
            (self.sort_user_2, 0, 1, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_2_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.2_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_2_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.2_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_2_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.2_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_2_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 1),
            (self.sort_user_2, 0.75, 0.75, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_2_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 1),
            (self.sort_user_2, 1, 0, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_2_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 1),
            (self.sort_user_2, 0, 1, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_2_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 1),
            (self.sort_user_2, 0.75, 0.75, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_2_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 1),
            (self.sort_user_2, 1, 0, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_2_wins_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 1),
            (self.sort_user_2, 0, 1, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_tie_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.tie_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_tie_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.tie_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_tie_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.tie_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 1),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_tie_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 1),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_tie_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 1),
            (self.sort_user_2, 1, 0, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_tie_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 1),
            (self.sort_user_2, 0, 1, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_tie_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 1),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_tie_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 1),
            (self.sort_user_2, 1, 0, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_tie_nick_index_tie_user_index_2_wins_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.tie_user_index."""
        """2_wins_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 1),
            (self.sort_user_2, 0, 1, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_1_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.1_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_1_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.1_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_1_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.1_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_1_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 0, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_1_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 0, 5),
            (self.sort_user_2, 1, 0, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_1_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 0, 5),
            (self.sort_user_2, 0, 1, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_1_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 0, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_1_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 0, 5),
            (self.sort_user_2, 1, 0, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_1_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 0, 5),
            (self.sort_user_2, 0, 1, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_2_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.2_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_2_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.2_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_2_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.2_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_2_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 5),
            (self.sort_user_2, 0.75, 0.75, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_2_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 5),
            (self.sort_user_2, 1, 0, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_2_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 5),
            (self.sort_user_2, 0, 1, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_2_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 0, 5),
            (self.sort_user_2, 0.75, 0.75, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_2_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 0, 5),
            (self.sort_user_2, 1, 0, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_2_wins_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 0, 5),
            (self.sort_user_2, 0, 1, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_tie_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.tie_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_tie_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.tie_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_tie_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.tie_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 0, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_tie_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_tie_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 5),
            (self.sort_user_2, 1, 0, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_tie_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 0, 5),
            (self.sort_user_2, 0, 1, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_tie_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 0, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_tie_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 0, 5),
            (self.sort_user_2, 1, 0, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_tie_nick_index_1_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.1_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 0, 5),
            (self.sort_user_2, 0, 1, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_1_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.1_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_1_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.1_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_1_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.1_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_1_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_1_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 5),
            (self.sort_user_2, 1, 0, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_1_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 5),
            (self.sort_user_2, 0, 1, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_1_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_1_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 4, 5),
            (self.sort_user_2, 1, 0, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_1_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 4, 5),
            (self.sort_user_2, 0, 1, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_2_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.2_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_2_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.2_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_2_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.2_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_2_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 0, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_2_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 1, 0, 0, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_2_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 0, 1, 0, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_2_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 0, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_2_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 5),
            (self.sort_user_2, 1, 0, 0, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_2_wins_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 5),
            (self.sort_user_2, 0, 1, 0, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_tie_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.tie_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_tie_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.tie_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_tie_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.tie_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 0, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_tie_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_tie_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 1, 0, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_tie_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 0, 1, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_tie_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_tie_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 5),
            (self.sort_user_2, 1, 0, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_tie_nick_index_2_wins_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.2_wins_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 5),
            (self.sort_user_2, 0, 1, 4, 0, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_1_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.1_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_1_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.1_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_1_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.1_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_1_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_1_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 5),
            (self.sort_user_2, 1, 0, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_1_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 0, 4, 5),
            (self.sort_user_2, 0, 1, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_1_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.1_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 0, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_1_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.1_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 0, 4, 5),
            (self.sort_user_2, 1, 0, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_1_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.1_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 0, 4, 5),
            (self.sort_user_2, 0, 1, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_2_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.2_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_2_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.2_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_2_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.2_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 0, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_2_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_2_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 1, 0, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_2_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 0, 1, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_2_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.2_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_2_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.2_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 5),
            (self.sort_user_2, 1, 0, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_2_wins_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.2_wins_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 5),
            (self.sort_user_2, 0, 1, 0, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum1_tie_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum1.tie_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum2_tie_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum2.tie_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_1_wins_percentage_sum3_tie_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.1_wins_percentage_sum3.tie_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 5),
            (self.sort_user_2, 0.25, 0.25, 4, 4, 5)
        )

        # Run assertions.
        self.assertLess(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum1_tie_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum2_tie_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 1, 0, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_2_wins_percentage_sum3_tie_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.25, 0.25, 4, 4, 5),
            (self.sort_user_2, 0, 1, 4, 4, 5)
        )

        # Run assertions.
        self.assertGreater(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum1_tie_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum1.tie_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0.75, 0.75, 4, 4, 5),
            (self.sort_user_2, 0.75, 0.75, 4, 4, 5)
        )

        # Run assertions.
        self.assertEqual(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum2_tie_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum2.tie_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 1, 0, 4, 4, 5),
            (self.sort_user_2, 1, 0, 4, 4, 5)
        )

        # Run assertions.
        self.assertEqual(result, 0)


    def test_sort_closest_user_list_tie_percentage_sum3_tie_nick_index_tie_user_index_tie_role_count(self):
        """lib.util.arguments.sort_closest_user_list.2_wins_percentage_sum3.tie_nick_index.tie_user_index."""
        """tie_role_count"""
        # Run the method.
        result = arguments.sort_closest_user_list(
            (self.sort_user_1, 0, 1, 4, 4, 5),
            (self.sort_user_2, 0, 1, 4, 4, 5)
        )

        # Run assertions.
        self.assertEqual(result, 0)

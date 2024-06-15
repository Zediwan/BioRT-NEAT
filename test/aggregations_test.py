from src.functions.aggregation import Aggregation
import unittest

class TestGetRandomActivation(unittest.TestCase):
    def test_get_random(self):
        f = Aggregation.get_random()
        self.assertIsNotNone(f)
        self.assertTrue(callable(f))

    def test_get_random_removed_option(self):
        f = Aggregation.MAX
        new_f = Aggregation.get_random(f)

        self.assertIsNotNone(f)
        self.assertTrue(callable(f))
        self.assertNotEqual(f, new_f)

class TestGetOptions(unittest.TestCase):
    def test_get_options(self):
        options = Aggregation.get_options()
        self.assertIsNotNone(options)
        self.assertTrue(len(options) > 0)
        for option in options:
            self.assertTrue(callable(option))

class TestIsValidActivation(unittest.TestCase):
    def test_is_valid_aggregation_exact_activation(self):
        f = Aggregation.MAX
        self.assertTrue(Aggregation.is_valid_aggregation(f))

    def test_is_valid_aggregation_callable(self):
        f = lambda x: x+1
        self.assertTrue(Aggregation.is_valid_aggregation(f))

    def test_is_valid_aggregation_not_callable(self):
        f = 1
        self.assertFalse(Aggregation.is_valid_aggregation(f))

class TestAsssertActivation(unittest.TestCase):
    def test_assert_aggregation_valid(self):
        f = Aggregation.MAX
        Aggregation.assert_aggregation(f)

    def test_assert_aggregation_raises(self):
        f = 1
        self.assertRaises(ValueError, Aggregation.assert_aggregation, f)

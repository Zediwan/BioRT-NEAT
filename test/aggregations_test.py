from src.functions.aggregations import Aggregations
import unittest

class TestGetRandomActivation(unittest.TestCase):
    def test_get_random(self):
        f = Aggregations.get_random()
        self.assertIsNotNone(f)
        self.assertTrue(callable(f))

class TestGetOptions(unittest.TestCase):
    def test_get_options(self):
        options = Aggregations.get_options()
        self.assertIsNotNone(options)
        self.assertTrue(len(options) > 0)
        for option in options:
            self.assertTrue(callable(option))

class TestIsValidActivation(unittest.TestCase):
    def test_is_valid_aggregation_exact_activation(self):
        f = Aggregations.MAX
        self.assertTrue(Aggregations.is_valid_aggregation(f))

    def test_is_valid_aggregation_callable(self):
        f = lambda x: x+1
        self.assertTrue(Aggregations.is_valid_aggregation(f))

    def test_is_valid_aggregation_not_callable(self):
        f = 1
        self.assertFalse(Aggregations.is_valid_aggregation(f))

class TestAsssertActivation(unittest.TestCase):
    def test_assert_aggregation_valid(self):
        f = Aggregations.MAX
        Aggregations.assert_aggregation(f)

    def test_assert_aggregation_raises(self):
        f = 1
        self.assertRaises(ValueError, Aggregations.assert_aggregation, f)

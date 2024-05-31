from src.functions.aggregations import Aggregations
import unittest

class TestGetRandomActivation(unittest.TestCase):
    def test_get_random_aggregation(self):
        f = Aggregations.get_random_aggregation_function()
        self.assertIsNotNone(f)
        self.assertTrue(callable(f))

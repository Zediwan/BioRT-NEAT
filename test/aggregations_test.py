from src.functions.aggregations import Aggregations
import unittest

class TestGetRandomActivation(unittest.TestCase):
    def test_get_random(self):
        f = Aggregations.get_random()
        self.assertIsNotNone(f)
        self.assertTrue(callable(f))

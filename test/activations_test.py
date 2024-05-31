from src.functions.activations import Activations
import unittest

class TestGetRandomActivation(unittest.TestCase):
    def test_get_random(self):
        f = Activations.get_random()
        self.assertIsNotNone(f)
        self.assertTrue(callable(f))

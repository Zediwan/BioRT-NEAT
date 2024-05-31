from src.functions.activations import Activations
import unittest

class TestGetRandomActivation(unittest.TestCase):
    def test_get_random_activation(self):
        f = Activations.get_random_activation_function()
        self.assertIsNotNone(f)
        self.assertTrue(callable(f))

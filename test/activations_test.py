from src.functions.activations import Activations
import unittest

class TestGetRandomActivation(unittest.TestCase):
    def test_get_random(self):
        f = Activations.get_random()
        self.assertIsNotNone(f)
        self.assertTrue(callable(f))

class TestGetOptions(unittest.TestCase):
    def test_get_options(self):
        options = Activations.get_options()
        self.assertIsNotNone(options)
        self.assertTrue(len(options) > 0)
        for option in options:
            self.assertTrue(callable(option))

class TestIsValidActivation(unittest.TestCase):
    def test_is_valid_activation_exact_activation(self):
        f = Activations.CLAMPED
        self.assertTrue(Activations.is_valid_activation(f))

    def test_is_valid_activation_callable(self):
        f = lambda x: x+1
        self.assertTrue(Activations.is_valid_activation(f))

    def test_is_valid_activation_not_callable(self):
        f = 1
        self.assertFalse(Activations.is_valid_activation(f))

class TestAsssertActivation(unittest.TestCase):
    def test_assert_activation_valid(self):
        f = Activations.CLAMPED
        Activations.assert_activation(f)

    def test_assert_activation_raises(self):
        f = 1
        self.assertRaises(ValueError, Activations.assert_activation, f)

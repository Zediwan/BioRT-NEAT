from src.functions.activation import Activation
import unittest

class TestGetRandomActivation(unittest.TestCase):
    def test_get_random(self):
        f = Activation.get_random()
        self.assertIsNotNone(f)
        self.assertTrue(callable(f))

    def test_get_random_removed_option(self):
        f = Activation.CLAMPED
        new_f = Activation.get_random(f)

        self.assertIsNotNone(f)
        self.assertTrue(callable(f))
        self.assertNotEqual(f, new_f)

class TestGetOptions(unittest.TestCase):
    def test_get_options(self):
        options = Activation.get_options()
        self.assertIsNotNone(options)
        self.assertTrue(len(options) > 0)
        for option in options:
            self.assertTrue(callable(option))

class TestIsValidActivation(unittest.TestCase):
    def test_is_valid_activation_exact_activation(self):
        f = Activation.CLAMPED
        self.assertTrue(Activation.is_valid_activation(f))

    def test_is_valid_activation_callable(self):
        f = lambda x: x+1
        self.assertTrue(Activation.is_valid_activation(f))

    def test_is_valid_activation_not_callable(self):
        f = 1
        self.assertFalse(Activation.is_valid_activation(f))

class TestAsssertActivation(unittest.TestCase):
    def test_assert_activation_valid(self):
        f = Activation.CLAMPED
        Activation.assert_activation(f)

    def test_assert_activation_raises(self):
        f = 1
        self.assertRaises(ValueError, Activation.assert_activation, f)

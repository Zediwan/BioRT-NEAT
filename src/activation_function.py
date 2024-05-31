from __future__ import annotations

from .extended_enum import ExtendedEnum
import random
import math


class ActivationFunction(ExtendedEnum):
    THRESHOLD = lambda x: 1 if x > 0 else 0
    SIGMOID = lambda x: 1 / (1 + math.exp(-x))

    @staticmethod
    def get_random_activation_function() -> ActivationFunction:
        return random.choice(ActivationFunction.get_options())
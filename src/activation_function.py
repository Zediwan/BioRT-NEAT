from __future__ import annotations

from .extended_enum import ExtendedEnum
import random
from neat.activations import *


class ActivationFunction(ExtendedEnum):
    TANH = tanh_activation
    SIGMOID = sigmoid_activation
    SIN = sin_activation
    GAUSS = gauss_activation
    RELU = relu_activation
    EXP = exp_activation
    HAT = hat_activation
    INV = inv_activation
    LOG = log_activation
    CUBE = cube_activation
    SQUARE = square_activation
    CLAMPED = clamped_activation
    ID = identity_activation
    SOFTPLUS = softplus_activation

    @staticmethod
    def get_random_activation_function() -> ActivationFunction:
        return random.choice(ActivationFunction.get_options())
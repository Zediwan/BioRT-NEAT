from __future__ import annotations

from enum import Enum
import random
import math


class Activations(Enum):
    #region functions
    def sigmoid_activation(z: float) -> float:
        z = max(-60.0, min(60.0, 5.0 * z))
        return 1.0 / (1.0 + math.exp(-z))

    def tanh_activation(z: float) -> float:
        z = max(-60.0, min(60.0, 2.5 * z))
        return math.tanh(z)


    def sin_activation(z: float) -> float:
        z = max(-60.0, min(60.0, 5.0 * z))
        return math.sin(z)


    def gauss_activation(z: float) -> float:
        z = max(-3.4, min(3.4, z))
        return math.exp(-5.0 * z ** 2)


    def relu_activation(z: float) -> float:
        return z if z > 0.0 else 0.0


    def elu_activation(z: float) -> float:
        return z if z > 0.0 else math.exp(z) - 1


    def lelu_activation(z: float) -> float:
        leaky = 0.005
        return z if z > 0.0 else leaky * z


    def selu_activation(z: float) -> float:
        lam = 1.0507009873554804934193349852946
        alpha = 1.6732632423543772848170429916717
        return lam * z if z > 0.0 else lam * alpha * (math.exp(z) - 1)


    def softplus_activation(z: float) -> float:
        z = max(-60.0, min(60.0, 5.0 * z))
        return 0.2 * math.log(1 + math.exp(z))


    def identity_activation(z: float) -> float:
        return z


    def clamped_activation(z: float) -> float:
        return max(-1.0, min(1.0, z))


    def inv_activation(z: float) -> float:
        try:
            z = 1.0 / z
        except ArithmeticError:  # handle overflows
            return 0.0
        else:
            return z

    def log_activation(z: float) -> float:
        z = max(1e-7, z)
        return math.log(z)


    def exp_activation(z: float) -> float:
        z = max(-60.0, min(60.0, z))
        return math.exp(z)


    def abs_activation(z: float) -> float:
        return abs(z)


    def hat_activation(z: float) -> float:
        return max(0.0, 1 - abs(z))


    def square_activation(z: float) -> float:
        return z ** 2


    def cube_activation(z: float) -> float:
        return z ** 3
    #endregion

    TANH = tanh_activation
    SIGMOID = sigmoid_activation
    SIN = sin_activation
    GAUSS = gauss_activation
    RELU = relu_activation
    ELU = elu_activation
    SELU = selu_activation
    LELU = lelu_activation
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
    def is_valid(activation: Activations) -> bool:
        return (activation is not None) and (callable(activation))
    
    @staticmethod
    def check_valid_activation(activation: Activations) -> None:
        if not Activations.is_valid(activation):
            raise ValueError(f"Invalid activation function: {activation}.")

    @staticmethod
    def get_random() -> Activations:
        return random.choice([
            Activations.TANH,
            Activations.SIGMOID,
            Activations.SIN,
            Activations.GAUSS,
            Activations.RELU,
            Activations.ELU,
            Activations.SELU,
            Activations.LELU,
            Activations.EXP,
            Activations.HAT,
            Activations.INV,
            Activations.LOG,
            Activations.CUBE,
            Activations.SQUARE,
            Activations.CLAMPED,
            Activations.ID,
            Activations.SOFTPLUS
            ])
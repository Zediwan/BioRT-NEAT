from __future__ import annotations

import random

from .gene import Gene
from ..functions.activation import Activation
from ..functions.aggregation import Aggregation
from ..config import conf


class Node(Gene):
    def __init__(self, af: Activation = None, agg: Aggregation = None, bias: float = 0, response: float = 1) -> None:
        if af is None:
            af = Activation.ID
        Activation.assert_activation(af)
        if agg is None:
            agg = Aggregation.get_random()
        Aggregation.assert_aggregation(agg)
        
        if not isinstance(bias, (float, int)):
            raise TypeError(f"Bias: {bias} must be of type float or int.")
        if not isinstance(response, (float, int)):
            raise TypeError(f"Response {response} must be of type float or int.")

        self.activation = af
        self.aggregation = agg
        self.bias = bias
        self.response = response
    
        self.num_in_connections: int = 0
        from .connection import Connection
        self.out_connections: list[Connection] = []
        self._values: list[float] = []

    def recieve_value(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(f"Value needs to be of type float or int: {value}, {type(value)}.")
        self._values.append(value)

    def get_value(self) -> float:
        return self.activation(self.bias + (self.response * self.aggregation(self._values)))
    
    def mutate(self) -> None:
        if random.random() <= conf.mut.new_af_proba:
            self._mutate_activation_function()
        if random.random() <= conf.mut.new_agg_proba:
            self._mutate_aggregation_function()
        if random.random() <= conf.mut.new_bias_proba:
            self._mutate_bias()
        if random.random() <= conf.mut.new_response_proba:
            self._mutate_response()

    def _mutate_activation_function(self) -> None:
        self.activation = Activation.get_random(self.activation)

    def _mutate_aggregation_function(self) -> None:
        self.aggregation = Aggregation.get_random(self.aggregation)

    def _mutate_bias(self) -> None:
        self.bias += random.gauss(sigma=conf.mut.bias_sigma)

    def _mutate_response(self) -> None:
        self.response += random.gauss(sigma=conf.mut.response_sigma)

    def copy(self) -> Node:
        return Node(af=self.activation, agg=self.aggregation, bias=self.bias, response=self.response)

    def equals(self, node: Node) -> bool:
        return (
            (self.activation == node.activation) and
            (self.aggregation == node.aggregation) and
            (self.bias == node.bias) and
            (self.response == node.bias)
        )

    @staticmethod
    def crossover(g1: Node, g2: Node) -> Node:
        """ Creates a new gene randomly inheriting attributes from its parents."""
        # Note: we use "a if random() > 0.5 else b" instead of choice((a, b))
        # here because `choice` is substantially slower.
        bias = g1.bias if random.random() > 0.5 else g2.bias
        activation = g1.activation if random.random() > 0.5 else g2.activation
        aggregation = g1.aggregation if random.random() > 0.5 else g2.aggregation
        response = g1.response if random.random() > 0.5 else g2.response

        return Node(af=activation, agg=aggregation, bias=bias, response=response)

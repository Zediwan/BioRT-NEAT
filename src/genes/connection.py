from __future__ import annotations

import random

from .gene import Gene
from .node import Node
from ..functions.activation import Activation
from ..functions.aggregation import Aggregation
from ..config import conf

class Connection(Gene):
    def __init__(self, from_node: Node, to_node: Node, weight: float = 1) -> None:
        if not isinstance(from_node, Node):
            raise TypeError(f"From needs to be a Node: {from_node}, {type(from_node)}.")
        if not isinstance(to_node, Node):
            raise TypeError(f"To needs to be a Node: {to_node}, {type(to_node)}.")
        if not isinstance(weight, (float, int)):
            raise TypeError(f"Weight needs to be an integer or float: {weight}, {type(weight)}.")
        if from_node == to_node:
            raise ValueError(f"From node {from_node} and to node {to_node} need to be different.")

        self.FROM_NODE = from_node
        # Append self to out connections of from node
        self.FROM_NODE.out_connections.append(self)
        self.TO_NODE = to_node
        # Increment num of in connections on node
        self.TO_NODE.num_in_connections += 1

        self.weight = weight

    def send_value(self) -> None:
        weighted_value = self.FROM_NODE.get_value() * self.weight
        self.TO_NODE.recieve_value(weighted_value)

    def mutate(self) -> None:
        if random.random() <= conf.mut.new_weight_proba:
            self._mutate_weight()

    def _mutate_weight(self) -> None:
        self.weight += random.gauss(sigma=conf.mut.weight_sigma)

    def copy(self) -> Connection:
        return Connection(self.FROM_NODE, self.TO_NODE, self.weight)

    def similar(self, connection: Connection) -> bool:
        return (
            self.FROM_NODE == connection.FROM_NODE and
            self.TO_NODE == connection.TO_NODE and
            self.weight == connection.weight
        )

    @staticmethod
    def crossover(c1: Connection, c2: Connection) -> Connection:
        pass

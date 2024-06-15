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

        self.from_node = from_node
        # Append self to out connections of from node
        self.from_node.out_connections.append(self)
        self.to_node = to_node
        # Increment num of in connections on node
        self.to_node.num_in_connections += 1

        self.weight = weight

    def send_value(self, value: float) -> None:
        weighted_value = value * self.weight
        self.to_node.recieve_value(weighted_value)

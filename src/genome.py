from __future__ import annotations

import random
import itertools

from .config import conf
from .genes.node import Node
from .genes.connection import Connection


class Genome():
    def __init__(self, inputs: list[Node] = None, outputs: list[Node] = None, num_inputs: int = None, num_outputs: int = None, fully_connect: bool = None, num_starting_connections: int = None) -> None:
        if (inputs is None and num_inputs is None) or (inputs is not None and num_inputs is not None):
            raise ValueError("Cannot have both inputs and num_inputs be None or both defined. (Only one can be given)")
        if (outputs is None and num_outputs is None) or (outputs is not None and num_outputs is not None):
            raise ValueError("Cannot have both outputs and num_outputs be None or both defined. (Only one can be given)")
        if (fully_connect is None and num_starting_connections is None) or (fully_connect is not None and num_starting_connections is not None):
            raise ValueError("Cannot have both fully_connect and num_starting_connections defined, or cannot have both be undefined. (Only one can be given)")

        self.input_nodes: list[Node] = []
        self.output_nodes: list[Node] = []
        self.nodes: list[Node] = []
        self.connections: list[Connection] = []

        # Type checks
        if inputs is not None:
            if not isinstance(inputs, list) or not all(isinstance(node, Node) for node in inputs):
                raise TypeError("Inputs must be a list of Node instances.")
            self.input_nodes = inputs
            self.nodes.extend(inputs)
        if outputs is not None:
            if not isinstance(outputs, list) or not all(isinstance(node, Node) for node in outputs):
                raise TypeError("Outputs must be a list of Node instances.")
            self.output_nodes = outputs
            self.nodes.extend(outputs)
        if num_inputs is not None:
            if not isinstance(num_inputs, int):
                raise TypeError("num_inputs must be an integer.")
            if num_inputs <= 0:
                raise ValueError("num_inputs must be a positive integer.")
            for n in range(num_inputs):
                input_node = Node()
                self.input_nodes.append(input_node)
                self.nodes.append(input_node)
        if num_outputs is not None:
            if not isinstance(num_outputs, int):
                raise TypeError("num_outputs must be an integer.")
            if  num_outputs <= 0:
                raise ValueError("num_outputs must be a positive integer.")
            for n in range(num_outputs):
                output_node = Node()
                self.output_nodes.append(output_node)
                self.nodes.append(output_node)
        if fully_connect is not None:
            if not isinstance(fully_connect, bool):
                raise TypeError("fully_connect must be a boolean.")
        if num_starting_connections is not None:
            if not isinstance(num_starting_connections, int):
                raise TypeError("num_starting_connections must be an integer.")
            if num_starting_connections <= 0:
                raise ValueError("num_starting_connections must be a positive integer.")
            # Num connections cannot exceed the maximum possible connections
            num_starting_connections = max(num_starting_connections, len(self.input_nodes) * len(self.output_nodes))
            # Randomly choose connections to be made
            cons: list[Connection] = random.choices(
                list[itertools.product(self.input_nodes, self.output_nodes)],
                k = num_starting_connections
            )
        elif not fully_connect:
            raise ValueError("Cannot have fully_connect be false and not provide num_starting_connections")
        else:
            self._fully_connect()

    def _fully_connect(self):
        for input_node in self.input_nodes:
            for output_node in self.output_nodes:
                self._add_connection(input_node, output_node)

    def mutate(self) -> None:
        pass
    
    def _mutate_add_new_connection(self) -> None:
        pass
    
    def _mutate_add_new_node(self) -> None:
        pass
    
    def _mutate_delete_connection(self) -> None:
        pass
    
    def _mutate_delete_node(self) -> None:
        pass
    
    def _add_connection(self, from_node: Node, to_node: Node) -> None:
        # TODO typecheck
        # TODO check if connection already exists between the two
        self.connections.append(Connection(from_node=from_node, to_node=to_node))
    
    def _add_node(self, connection: Connection) -> None:
        pass
    
    def _delete_connection(self, connection: Connection) -> None:
        pass
    
    def _delete_node(self, node: Node) -> None:
        pass

    def copy(self) -> Genome:
        pass
    
    def are_nodes_connected(self, n1: Node, n2: Node) -> bool:
        pass

    @staticmethod
    def crossover(g1: Genome, g2: Genome) -> Genome:
        pass

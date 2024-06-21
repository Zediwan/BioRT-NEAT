from __future__ import annotations

import random
import itertools

from .config import conf
from .genes.node import Node
from .genes.connection import Connection

# TODO write a method that gets all nodes that still can be connected to another node

class Genome():
    def __init__(self, inputs: list[Node] = None, outputs: list[Node] = None, num_inputs: int = None, num_outputs: int = None, fully_connect: bool = None, num_starting_connections: int = None) -> None:
        """
        Initialize a Genome object with input and output nodes, optionally creating connections between them.

        Args:
            inputs (list[Node]): List of input Node objects.
            outputs (list[Node]): List of output Node objects.
            num_inputs (int): Number of input nodes.
            num_outputs (int): Number of output nodes.
            fully_connect (bool): Whether to fully connect input and output nodes.
            num_starting_connections (int): Number of initial connections.

        Raises:
            ValueError: If conflicting arguments are provided.
            TypeError: If arguments have incorrect types.
        """
        # Check argument conflicts
        if (inputs is None) == (num_inputs is None):
            raise ValueError("Exactly one of inputs or num_inputs should be provided.")
        if (outputs is None) == (num_outputs is None):
            raise ValueError("Exactly one of outputs or num_outputs should be provided.")
        if (fully_connect is None) == (num_starting_connections is None):
            raise ValueError("Exactly one of fully_connect or num_starting_connections should be provided.")

        self.input_nodes: list[Node] = []
        self.output_nodes: list[Node] = []
        self.nodes: list[Node] = []
        self.connections: list[Connection] = []

        # If inputs are given add them
        if inputs is not None:
            # Type check
            if not all(isinstance(node, Node) for node in inputs):
                raise TypeError("Inputs must be a list of Node instances.")
            self.input_nodes = inputs
            self.nodes.extend(inputs)
        # If outputs are given add them
        if outputs is not None:
            # Type check
            if not all(isinstance(node, Node) for node in outputs):
                raise TypeError("Outputs must be a list of Node instances.")
            self.output_nodes = outputs
            self.nodes.extend(outputs)
        # If num of inputs is given, create and add them
        if num_inputs is not None:
            # Value check
            if num_inputs <= 0:
                raise ValueError("num_inputs must be a positive integer.")
            self.input_nodes.extend(Node() for _ in range(num_inputs))
            self.nodes.extend(self.input_nodes)
        # If num of outputs are given, create and add them
        if num_outputs is not None:
            # Value check
            if num_outputs <= 0:
                raise ValueError("num_outputs must be a positive integer.")
            self.output_nodes.extend(Node() for _ in range(num_outputs))
            self.nodes.extend(self.output_nodes)
        # Check arg conflict
        if fully_connect is not None:
            # Type check
            if not isinstance(fully_connect, bool):
                raise TypeError("fully_connect must be a boolean")
            if num_starting_connections is None and not fully_connect:
                raise ValueError("Cannot have fully_connect as False without providing num_starting_connections.")
        # If num starting connections is give, create and add them
        if num_starting_connections is not None:
            # Value check
            if num_starting_connections <= 0:
                raise ValueError("num_starting_connections must be a positive integer.")
            # Limit the number of starting connections to the possible max
            num_starting_connections = min(num_starting_connections, len(self.input_nodes) * len(self.output_nodes))
            # Randomly choose nodes to connect
            con_tuples: list[tuple[Node, Node]] = random.sample(
                list(itertools.product(self.input_nodes, self.output_nodes)),
                k=num_starting_connections
            )
            # Create the connections
            for con_tuple in con_tuples:
                self._add_connection(from_node=con_tuple[0], to_node=con_tuple[1])
        # Else fully connect the nodes
        elif fully_connect:
            self._fully_connect()

    @property
    def num_inputs(self) -> int:
        return len(self.input_nodes)

    @property
    def num_outputs(self) -> int:
        return len(self.output_nodes)

    @property
    def num_hidden(self) -> int:
        return len(self.nodes) - self.num_inputs - self.num_outputs

    def _fully_connect(self):
        # TODO update this so it can be used when there are already existing connections and it just fills the network up
        for input_node in self.input_nodes:
            for output_node in self.output_nodes:
                self._add_connection(from_node=input_node, to_node=output_node)

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

    def get_connectable_nodes(self) -> tuple[Node, Node, Node]:
        # TODO write tests
        connectable_input_nodes = [input_node for input_node in self.input_nodes if input_node.num_out_connections <= self.num_outputs + self.num_hidden]
        connectable_hidden_nodes = [] # TODO write method to calculate this
        connectable_output_nodes = [output_node for output_node in self.output_nodes if output_node.num_in_connections <= self.num_inputs + self.num_hidden]

        return connectable_input_nodes, connectable_hidden_nodes, connectable_output_nodes

    @staticmethod
    def crossover(g1: Genome, g2: Genome) -> Genome:
        pass

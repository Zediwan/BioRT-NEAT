from __future__ import annotations

from .genes.node import Node
from .genes.connection import Connection


class Genome():
    def __init__(self) -> None:
        self.nodes: list[Node] = []
        self.connections: list[Connection] = []

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
        pass
    
    def _add_node(self, connection: Connection) -> None:
        pass
    
    def _delete_connection(self, connection: Connection) -> None:
        pass
    
    def _delete_node(self, node: Node) -> None:
        pass

    def copy(self) -> Genome:
        pass
    
    @staticmethod
    def crossover(g1: Genome, g2: Genome) -> Genome:
        pass

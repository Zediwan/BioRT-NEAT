from __future__ import annotations

from .gene import NodeGene, ConnectionGene


class NeatNetwork:
    def __init__(self) -> None:
        self.nodes: list[NodeGene]
        self.connections: list[ConnectionGene]
    
    def add_connection(self, src: NodeGene, target: NodeGene) -> None:
        # Check that connection does not exist already
        if self._exists_connection(src, target):
            raise ValueError(f"Connection does already exist! {src} -> {target}")
        new_connection = ConnectionGene(src, target)
        self.connections.append(new_connection)
        
    def add_node(self, old_connection: ConnectionGene) -> None:
        if not old_connection.enabled:
            raise ValueError("Trying do add a node to a disabled connection.")

        # disable old connection
        old_connection.enabled = False
        # add new node
        new_node = NodeGene()
        self.nodes.append(new_node)
        # add connections
        new_connection_in = ConnectionGene(old_connection._in, new_node, weight=1) # The new connection leading into the new node receives a weight of 1
        new_connection_out = ConnectionGene(new_node, old_connection._out, old_connection.weight) # the new connection leading out receives the same weight as the old connection        
        self.connections.append(new_connection_in)
        self.connections.append(new_connection_out)

    def _exists_connection(self, src: NodeGene, target: NodeGene) -> bool:
        for connection in self.connections:
            if connection._in is not src:
                continue
            if connection._out is not target:
                continue
            return True
        return False

    def _disable_connection(self, connection: ConnectionGene) -> None:
        if connection not in self.connections:
            raise ValueError("Connection to disable not in self.connections.")
        
        connection.enabled = False
    
    @classmethod
    def crossover(cls, nn1: NeatNetwork, nn2: NeatNetwork) -> NeatNetwork:
        # check same connections / nodes and choose randomly
        # randomly choose 
        # TODO
        pass
from __future__ import annotations
from .gene import Gene, NodeGene, ConnectionGene
import random
from itertools import count


class NeatNetwork:
    CONNECTION_ADD_PROB: float
    CONNECTION_DEL_PROP: float
    NODE_ADD_PROB: float
    NODE_DEL_PROB: float

    NUM_INPUTS: int
    NUM_OUTPUTS: int

    # By convention, input pins have negative keys, and the output pins have keys 0,1,...
    INPUT_KEYS: list[str] = [-i - 1 for i in range(NUM_INPUTS)]
    OUTPUT_KEYS: list[str] = [i for i in range(NUM_OUTPUTS)]
    
    compatibility_disjoint_coefficient = 1 # The coefficient for the disjoint and excess gene counts’ contribution to the genomic distance.

    def __init__(self, nodes: dict[str, NodeGene] = None, connections: dict[str, ConnectionGene] = None) -> None:
        if not nodes:
            nodes = {}
            for key in NeatNetwork.INPUT_KEYS:
                nodes[key] = NodeGene(self.get_new_node_key(nodes))
            for key in NeatNetwork.OUTPUT_KEYS:
                nodes[key] = NodeGene(self.get_new_node_key(nodes))
        self.nodes = nodes

        if not connections:
            connections = {}
        self.connections = connections

    def feedforward(self) -> list:
        outputs = []

        return outputs

    def distance(self, other: NeatNetwork) -> float:
        """
        Returns the genetic distance between this genome and the other. This distance value
        is used to compute genome compatibility for speciation.
        """

        # Compute node gene distance component.
        node_distance = 0.0
        if self.nodes or other.nodes:
            disjoint_nodes = 0
            for k2 in other.nodes:
                if k2 not in self.nodes:
                    disjoint_nodes += 1

            for k1, n1 in self.nodes.items():
                n2 = other.nodes.get(k1)
                if n2 is None:
                    disjoint_nodes += 1
                else:
                    # Homologous genes compute their own distance value.
                    node_distance += n1.distance(n2)

            max_nodes = max(len(self.nodes), len(other.nodes))
            node_distance += (node_distance +
                             (NeatNetwork.compatibility_disjoint_coefficient *
                              disjoint_nodes)) / max_nodes

        # Compute connection gene differences.
        connection_distance = 0.0
        if self.connections or other.connections:
            disjoint_connections = 0
            for k2 in other.connections:
                if k2 not in self.connections:
                    disjoint_connections += 1

            for k1, c1 in self.connections.items():
                c2 = other.connections.get(k1)
                if c2 is None:
                    disjoint_connections += 1
                else:
                    # Homologous genes compute their own distance value.
                    connection_distance += c1.distance(c2)

            max_conn = max(len(self.connections), len(other.connections))
            connection_distance = (connection_distance +
                                   (NeatNetwork.compatibility_disjoint_coefficient *
                                    disjoint_connections)) / max_conn

        distance = node_distance + connection_distance
        return distance

    def size(self) -> tuple[int, int]:
        """
        Returns genome 'complexity', taken to be
        (number of nodes, number of enabled connections)
        """
        num_enabled_connections = sum([1 for cg in self.connections.values() if cg.enabled])
        return len(self.nodes), num_enabled_connections

    def mutate(self) -> None:
        if random.random() < NeatNetwork.CONNECTION_ADD_PROB:
            self.mutate_add_connection()
        if random.random() < NeatNetwork.CONNECTION_DEL_PROP:
            self.mutate_delete_connection()
        if random.random() < NeatNetwork.NODE_ADD_PROB:
            self.mutate_add_node()
        if random.random() < NeatNetwork.NODE_DEL_PROB:
            self.mutate_delete_node()
        for cg in self.connections.values():
            cg.mutate()
        for ng in self.nodes.values():
            ng.mutate()

    def mutate_add_connection(self) -> None:
        if not self.nodes:
            raise ValueError("No nodes exists yet.")
        possible_outputs = list(self.nodes.values())
        to_node = self.nodes[random.choice(possible_outputs)]

        possible_inputs = possible_outputs + NeatNetwork.INPUT_KEYS
        from_node = self.nodes[random.choice(possible_inputs)]

        self._add_connection(from_node, to_node)

    def mutate_add_node(self) -> None:
        if not self.connections:
            raise ValueError("No Connections exists yet.")
        # Randomly choose a connection
        connection = random.choice(list[self.connections.values()])
        self._add_node(connection)

    def mutate_delete_node(self) -> None:
        avaiable_nodes = [k for k in self.nodes if k not in NeatNetwork.OUTPUT_KEYS]
        if not avaiable_nodes:
            return

        del_key = random.choice(avaiable_nodes)
        connections_to_delete = set()
        for k, v in self.connections.items():
            if del_key in v.key:
                connections_to_delete.add(v.key)

        for key in connections_to_delete:
            del self.connections[key]

        del self.nodes[del_key]

    def mutate_delete_connection(self) -> None:
        if self.connections:
            key = random.choice(list[self.connections.keys()])
            del self.connections[key]

    def _add_connection(self, _from: NodeGene, _to: NodeGene, weight: float = None, enabled: bool = True) -> None:
        # Check that connection does not exist already
        if _from.key in NeatNetwork.OUTPUT_KEYS and _to.key in NeatNetwork.OUTPUT_KEYS:
            return

        key = (_from.key, _to.key)
        if key in self.connections:
            self.connections[key].enabled = True # If the connection exists but is disabled then enable it
        else:
            new_connection = ConnectionGene(_from, _to, weight, enabled)
            self.connections[new_connection.key] = new_connection

    def _add_node(self, old_connection: ConnectionGene) -> None:
        if not self.connections:
            raise ValueError("No Connections exists yet.")
        if not old_connection.enabled:
            raise ValueError("Trying do add a node to a disabled connection.")

        # disable old connection
        old_connection.enabled = False
        # add new node
        new_node = NodeGene(self.get_new_node_key(self.nodes))
        self.nodes[new_node.key] = new_node
        # add connections
        self._add_connection(old_connection._from, new_node, weight=1) # The new connection leading into the new node receives a weight of 1
        self._add_connection(new_node, old_connection._to, weight=old_connection.weight) # the new connection leading out receives the same weight as the old connection

    def get_new_node_key(self, node_dict) -> int:
        if self.node_indexer is None:
            if node_dict:
                self.node_indexer = count(max(list(node_dict)) + 1)
            else:
                self.node_indexer = count(max(list(node_dict)) + 1)

        new_id = next(self.node_indexer)

        assert new_id not in node_dict

        return new_id

    @classmethod
    def crossover(cls, nn1: NeatNetwork, nn2: NeatNetwork) -> NeatNetwork:
        # Inherit connection genes
        connections = {}
        all_keys = set(nn1.connections.keys()) | set(nn2.connections.keys())
        for key in all_keys:
            cg1 = nn1.connections.get(key)
            cg2 = nn2.connections.get(key)
            if cg1 is None:
                # Excess or disjoint gene: random chance to inherit.
                if bool(random.getrandbits(1)):
                    connections[key] = cg2.copy()
            elif cg2 is None:
                # Excess or disjoint gene: random chance to inherit.
                if bool(random.getrandbits(1)):
                    connections[key] = cg1.copy()
            else:
                # Homologous gene: combine genes from both parents.
                connections[key] = ConnectionGene.crossover(cg1, cg2)

        # Inherit node genes
        nodes = {}
        all_keys = set(nn1.nodes.keys()) | set(nn2.nodes.keys())
        for key in all_keys:
            ng1 = nn1.nodes.get(key)
            ng2 = nn2.nodes.get(key)
            if ng1 is None:
                # Excess or disjoint gene: random chance to inherit.
                if bool(random.getrandbits(1)):
                    nodes[key] = ng2.copy()
            elif ng2 is None:
                # Excess or disjoint gene: random chance to inherit.
                if bool(random.getrandbits(1)):
                    nodes[key] = ng1.copy()
            else:
                # Homologous gene: combine genes from both parents.
                nodes[key] = NodeGene.crossover(ng1, ng2)

        return NeatNetwork(nodes, connections)

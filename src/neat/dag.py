class Node:
    def __init__(self, incomming: int = 0, depth: int = 0, out: list[int] = []):
        self.incoming = incomming
        self.depth = depth
        self.out = out
    
    def get_out_connection_count(self) -> int:
        return len(self.out)

class DAG:
    def __init__(self):
        self.nodes: list[Node] = []

    def create_node(self):
        self.nodes.append(Node())

    def create_connection(self, from_node: int, to_node: int) -> bool:
        # Ensure both nodes exist
        if not self.is_valid_index(from_node):
            return False
        if not self.is_valid_index(to_node):
            return False
        # Ensure there is no cycle
        if from_node == to_node:
            return False
        if self.is_ancestor(to_node, from_node):
            return False
        # Ensure the connection doesn't already exist
        if self.is_parent(from_node, to_node):
            return False

        # Add the connection in the parent node
        self.nodes[from_node].out.append(to_node)
        # Increase the incoming connections count of the child node
        self.nodes[to_node].incoming += 1
        return True

    def is_valid_index(self, i: int) -> bool:
        if i < 0:
            raise IndexError(f"Index cannot be negative. {i}.")

        return i < len(self.nodes)

    def is_parent(self, node_1: int, node_2: int) -> bool:
        """
        Checks if node_1 has node_2 in its children list.
        """
        return node_2 in self.nodes[node_1].out

    def is_ancestor(self, node_1: int, node_2: int) -> bool:
        """
        Checks if node_1 is an ancestor of node_2.
        """
        return self.is_parent(node_1, node_2) or any(self.is_ancestor(o, node_2) for o in self.nodes[node_1].out)

    def compute_node_depths(self):
        """
        Computes the depth of each node.
        """
        node_count = len(self.nodes)
        # Nodes with no incoming edge
        start_nodes = [] 
        # Current incoming edge state
        incoming = [n.incoming for n in self.nodes]

        # Initialize incoming state
        for i, node in enumerate(self.nodes):
            # If a connection does not have any incomming nodes then it is an input node
            if node.incoming == 0:
                node.depth = 0
                start_nodes.append(i)

        # Perform the sort
        while start_nodes:
            # Extract a node from the starting set
            idx = start_nodes.pop()
            # Remove incoming connection for all children of this node
            node: Node = self.nodes[idx]
            for o in node.out:
                incoming[o] -= 1
                connected = self.nodes[o]
                connected.depth = max(connected.depth, node.depth + 1)
                # If a child has no incoming edge anymore, add it to the starting set
                if incoming[o] == 0:
                    start_nodes.append(o)

    def get_order(self) -> list[int]:
        """
        Returns nodes indexes sorted topologically
        """
        order = list(range(len(self.nodes)))
        order.sort(key=lambda a: self.nodes[a].depth)
        return order

    def remove_connection(self, from_node: int, to_node: int):
        connections = self.nodes[from_node].out
        found = 0
        for i in range(len(connections)):
            if connections[i] == to_node:
                connections[i], connections[-1] = connections[-1], connections[i]
                connections.pop()
                self.nodes[to_node].incoming -= 1
                found += 1
                break

        if not found:
            print("[WARNING] Connection", from_node, "->", to_node, "not found")
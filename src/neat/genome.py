from dag import DAG
from .functions.activations import Activations
from .network import Network

class Node:
    def __init__(self, bias: float = 0, activation: Activations = None, depth: int = 0):
        if not isinstance(bias, (float, int)):
            raise ValueError(f"Bias {bias} needs to be float or int, but {type(bias)} has been provided.")
        if not Activations.is_valid(activation):
            activation = Activations.get_random()
        if not isinstance(depth, (float, int)):
            raise ValueError(f"Depth {depth} needs to be float or int, but {type(depth)} has been provided.")
        if depth < 0:
            raise ValueError(f"Depth {depth} must be larger than 0.")

        self.bias = bias
        self.activation = activation
        self.depth = depth

class Connection:
    def __init__(self, from_node: int, to_node: int, weight: float = 0):
        if not isinstance(from_node, int):
            raise ValueError(f"From node {from_node} needs to be int, but {type(from_node)} has been provided.")
        if not isinstance(to_node, int):
            raise ValueError(f"To node {to_node} needs to be int, but {type(to_node)} has been provided.")
        if not isinstance(weight, (int, float)):
            raise ValueError(f"Weight {weight} needs to be int or float, but {type(weight)} has been provided.")
        
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight

class Genome:
    def __init__(self):
        self.info: Network.Info = None
        self.nodes: list[Node] = []
        self.connections: list[Connection] = []
        self.graph = DAG()

    def __init__(self, inputs: int, outputs: int) -> None:
        if inputs <= 0:
            raise ValueError(f"Inputs must be bigger than 0. {inputs}.")
        if outputs <= 0:
            raise ValueError(f"Outputs must be bigger than 0. {outputs}.")
        
        self.info = Network.Info(inputs, outputs)
        for _ in range(self.info.inputs):
            self.create_node(activation=Activations.identity_activation, hidden=False)
        for _ in range(self.info.outputs):
            self.create_node(activation=Activations.TANH, hidden=False)

    def create_node(self, activation: Activations, hidden=True) -> int:
        self.nodes.append(Node(activation=activation))
        self.graph.create_node()
        if hidden:
            self.info.hidden += 1
        return len(self.nodes) - 1

    # TODO add Exceptions here
    def try_create_connection(self, from_node: int, to_node, weight: float) -> bool:
        if self.graph.create_connection(from_node, to_node):
            self.connections.append(Connection(from_node, to_node, weight))
            return True
        return False

    # TODO add Exceptions here
    def create_connection(self, from_node: int, to_node, weight: float) -> None:
        self.graph.create_connection(from_node, to_node)
        self.connections.append(Connection(from_node, to_node, weight))

    def split_connection(self, i: int) -> None:
        if i not in range(len(self.connections)):
            raise IndexError(f"Connection index not in valid range: {i} not in [{0}, {len(self.connections)}].")
        
        c: Connection = self.connections[i]
        from_node = c.from_node
        to_node = c.to_node
        weight = c.weight
        self.remove_connection(i)
        
        node_idx = self.create_node(Activations.RELU) # TODO think if we want to use this activation function
        self.create_connection(from_node, node_idx, weight)
        self.create_connection(node_idx, to_node, 1.0)

    def remove_connection(self, i: int) -> None:
        if i not in range(len(self.connections)):
            raise IndexError(f"Connection index not in valid range: {i} not in [{0}, {len(self.connections)}].")
        
        self.graph.remove_connection(self.connections[i].from_node, self.connections[i].to_node)
        self.connections[i], self.connections[-1] = self.connections[-1], self.connections[i] # TODO figure out why this is done
        self.connections.pop()

    def get_order(self) -> list[int]:
        order = list(range(len(self.nodes)))
        order.sort(key=lambda a: self.nodes[a].depth)
        return order

    def compute_depth(self) -> None:
        node_count = len(self.nodes)
        max_depth = 0
        self.graph.compute_node_depths()

        for i in range(node_count):
            self.nodes[i].depth = self.graph.nodes[i].depth
            max_depth = max(self.nodes[i].depth, max_depth)
        output_depth = max(max_depth, 1)
        for i in range(self.info.outputs):
            self.nodes[self.info.inputs + i].depth = output_depth

    def is_input(self, i: int) -> bool:
        if i < 0:
            raise ValueError(f"Index cannot be negative: {i}.")
        
        return i < self.info.inputs

    def is_output(self, i: int) -> bool:
        return self.info.inputs <= i < self.info.inputs + self.info.outputs

    # TODO write a save and load function
    # def write_to_file(self, filename):
    #     writer = BinaryWriter(filename)
    #     writer.write(self.info)
    #     for n in self.nodes:
    #         writer.write(n)
    #     writer.write(len(self.connections))
    #     for c in self.connections:
    #         writer.write(c)

    # def load_from_file(self, filename):
    #     reader = BinaryReader(filename)
    #     if not reader.is_valid():
    #         print("Cannot open file", filename)
    #     self.graph.nodes.clear()
    #     reader.read_into(self.info)
    #     self.nodes = [self.Node() for _ in range(self.info.get_node_count())]
    #     for n in self.nodes:
    #         reader.read_into(n)
    #         self.graph.create_node()
    #     connection_count = reader.read()
    #     for _ in range(connection_count):
    #         c = reader.read()
    #         self.create_connection(c.from_node, c.to_node, c.weight)
    #     print(filename, "loaded")
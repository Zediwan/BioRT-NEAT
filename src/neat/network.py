from .functions.activations import Activations

class Info:
    def __init__(self, inputs: int, outputs: int) -> None:
        self.inputs = inputs
        self.outputs = outputs
        self.hidden = 0

    @property
    def node_count(self) -> int:
        return self.inputs + self.hidden + self.outputs

class Node:
    def __init__(self) -> None:
        self.activation = None
        self.sum = 0.0
        self.bias = 0.0
        self.connection_count = 0
        self.depth = 0

    @property
    def value(self) -> float:
        return self.activation(self.sum + self.bias)

class Connection:
    def __init__(self) -> None:
        self.to = 0
        self.weight = 0.0
        self.value = 0.0

class Slot:
    def __init__(self) -> None:
        self.node = Node()
        self.connection = Connection()

class Network:
    def __init__(self) -> None:
        self.slots: list[Slot] = []
        self.output: list[Node] = []
        self.info: Info = None
        self.max_depth: int = 0
        self.connection_count: int = 0

    def initialize(self, info: Info, connection_count: int) -> None:
        """
        Initializes the slots vector.
        """
        self.info = info
        self.connection_count = connection_count
        self.slots = [Slot() for _ in range(info.node_count + connection_count)]
        self.output = [0.0] * info.outputs

    def set_node(self, i: int, activation: Activations, bias: float, connection_count: int) -> None:
        self.check_slot_index(i)
        Activations.check_valid_activation(activation)
        if connection_count < 0:
            raise ValueError(f"Connection count cannot be negative: {connection_count}.")
        
        self.slots[i].node.activation = activation
        self.slots[i].node.bias = bias
        self.slots[i].node.connection_count = connection_count

    def set_node_depth(self, i: int, depth: int) -> None:
        self.check_slot_index(i)
        self.slots[i].node.depth = depth

    def set_connection(self, i: int, to: int, weight: float) -> None:
        self.check_slot_index(i)
        self.slots[i].connection.to = to
        self.slots[i].connection.weight = weight

    def get_connection(self, i: int) -> Connection:
        self.check_slot_index(i)
        return self.slots[self.info.node_count + i].connection

    def get_node(self, i: int) -> Node:
        self.check_slot_index(i)
        return self.slots[i].node

    def get_output(self, i: int) -> Node:
        self.check_slot_index(i)
        return self.slots[self.info.inputs + self.info.hidden + i].node

    def execute(self, input: list[float]) -> bool:
        if len(input) != self.info.inputs:
            print("Input size mismatch, aborting")
            return False

        for slot in self.slots:
            slot.node.sum = 0.0

        for i in range(self.info.inputs):
            self.slots[i].node.sum = input[i]

        current_connection = 0
        node_count = self.info.node_count
        for i in range(node_count):
            node = self.slots[i].node
            value = node.value
            for o in range(node.connection_count):
                c = self.get_connection(current_connection)
                c.value = value * c.weight
                self.get_node(c.to).sum += c.value
                current_connection += 1

        for i in range(self.info.outputs):
            self.output[i] = self.get_output(i).value

        return True

    def get_result(self) -> list[float]:
        return self.output

    def foreach_node(self, callback):
        node_count = self.info.node_count
        for i in range(node_count):
            callback(self.slots[i].node, i)

    def foreach_connection(self, callback):
        for i in range(self.connection_count):
            callback(self.get_connection(i), i)
            
    def is_valid_slot_index(self, index: int) -> bool:
        return index in range(self.slots)
    
    def check_slot_index(self, index: int) -> None:
        if not self.is_valid_slot_index(index):
            raise IndexError(f"Invalid slot index: {index} not in [{0}, {len(self.slots)}].")

    @property
    def depth(self) -> int:
        return self.max_depth
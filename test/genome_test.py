import unittest
from unittest.mock import patch

from src.genome import Genome
from src.genes.node import Node
from src.functions.activation import Activation
from src.functions.aggregation import Aggregation
from src.config import conf

class TestGenome(unittest.TestCase):
    def setUp(self) -> None:
        self.input_node_1 = Node()
        self.input_node_2 = Node()
        self.input_nodes = [self.input_node_1, self.input_node_2]
        self.num_inputs = len(self.input_nodes)

        self.output_node_1 = Node()
        self.output_nodes = [self.output_node_1]
        self.num_outputs = len(self.output_nodes)

        self.new_node_proba = conf.mut.struct.new_node_proba
        self.new_conn_proba = conf.mut.struct.new_conn_proba
        self.del_node_proba = conf.mut.struct.del_node_proba
        self.del_conn_proba = conf.mut.struct.del_conn_proba
        self.max_hidden_nodes = conf.mut.struct.max_hidden_nodes

    def tearDown(self) -> None:
        conf.mut.struct.new_node_proba = self.new_node_proba
        conf.mut.struct.new_conn_proba = self.new_conn_proba
        conf.mut.struct.del_node_proba = self.del_node_proba
        conf.mut.struct.del_conn_proba = self.del_conn_proba
        conf.mut.struct.max_hidden_nodes = self.max_hidden_nodes

class TestInit_OutputsInputs_FullyConnected(TestGenome):
    def setUp(self) -> None:
        super().setUp()
        self.genome = Genome(inputs=self.input_nodes, outputs=self.output_nodes, fully_connect=True)

    def test_input_nodes_matching(self):
        # Check if the input nodes given are actually in the genome
        for input_node in self.input_nodes:
            self.assertIn(input_node, self.genome.input_nodes, "Input node not in genomes input nodes")
            self.assertIn(input_node, self.genome.nodes, "Input node not in genomes nodes")
        # Check that there are no output nodes in the genome that were not given
        for input_node in self.genome.input_nodes:
            self.assertIn(input_node, self.input_nodes, "Genome input node found that was not expected")

    def test_output_nodes_matching(self):
        # Check if the output nodes given are actually in the genome
        for output_node in self.output_nodes:
            self.assertIn(output_node, self.genome.output_nodes, "Output node not in genomes output nodes")
            self.assertIn(output_node, self.genome.nodes, "Output node not in genomes nodes")
        # Check that there are no output nodes in the genome that weren't given
        for output_node in self.genome.output_nodes:
            self.assertIn(output_node, self.output_nodes, "Genome output node found that was not expected")

    def test_num_nodes(self):
        self.assertEqual(self.num_inputs + self.num_outputs, len(self.genome.nodes), "Number of nodes not as expected")
        self.assertEqual(self.num_inputs, len(self.genome.input_nodes), "Number of inputs not as expected")
        self.assertEqual(self.num_outputs, len(self.genome.output_nodes), "Number of outputs not as expected.")

    def test_connections(self):
        # Check connections
        for input_node in self.genome.input_nodes:
            # Check the input node does not have any input connections
            self.assertEqual(input_node.num_in_connections, 0, "Input node has input connections.")
            # Check that the input node has the expected amount of output connections
            self.assertEqual(len(input_node.out_connections), self.num_outputs, "Input node has more connections than expected.")
            # Go over all the output connections the input node has
            for out_connection in input_node.out_connections:
                # Check that each connection of the input node is towards an output node
                self.assertIn(out_connection.TO_NODE, self.genome.output_nodes, "Input node has a connection to a non-output node.")
            for output_node in self.genome.output_nodes:
                # Check that each output node is connected to the input
                self.assertIn(output_node, [conn.TO_NODE for conn in input_node.out_connections], "Output node is not connected to input.")

        for output_node in self.genome.output_nodes:
            # Check that the number of input connections is equal to the number of inputs (as the genome is fully connected)
            self.assertEqual(output_node.num_in_connections, self.num_inputs, "Output nodes number of connections does not match the expected amount.")
            # Check that the output does not have any output connections
            self.assertEqual(len(output_node.out_connections), 0, "Output node has output connections")

class TestInit_NumOutputsNumInputs_FullyConnected(TestGenome):
    def setUp(self) -> None:
        super().setUp()
        self.genome = Genome(num_inputs=self.num_inputs, num_outputs=self.num_outputs, fully_connect=True)

    def test_num_nodes(self):
        self.assertEqual(self.num_inputs + self.num_outputs, len(self.genome.nodes), "Number of nodes not as expected")
        self.assertEqual(self.num_inputs, len(self.genome.input_nodes), "Number of inputs not as expected")
        self.assertEqual(self.num_outputs, len(self.genome.output_nodes), "Number of outputs not as expected.")

    def test_connections(self):
        # Check connections
        for input_node in self.genome.input_nodes:
            # Check the input node does not have any input connections
            self.assertEqual(input_node.num_in_connections, 0, "Input node has input connections.")
            # Check that the input node has the expected amount of output connections
            self.assertEqual(len(input_node.out_connections), self.num_outputs, "Input nodes number of connections does not match the expected amount.")
            # Go over all the output connections the input node has
            for out_connection in input_node.out_connections:
                # Check that each connection of the input node is towards an output node
                self.assertIn(out_connection.TO_NODE, self.genome.output_nodes, "Input node has a connection to a non-output node.")
            for output_node in self.genome.output_nodes:
                # Check that each output node is connected to the input
                self.assertIn(output_node, [conn.TO_NODE for conn in input_node.out_connections], "Output node is not connected to input.")

        for output_node in self.genome.output_nodes:
            # Check that the number of input connections is equal to the number of inputs (as the genome is fully connected)
            self.assertEqual(output_node.num_in_connections, self.num_inputs, "Output nodes number of connections does not match the expected amount.")
            # Check that the output does not have any output connections
            self.assertEqual(len(output_node.out_connections), 0, "Output node has output connections")

class TestInit_OutputsInputs_NumConnections(TestGenome):
    # TODO write tests

    def test_init_num_connections_exeeds_max(self):
        pass

class TestInit_NumOutputsNumInputs_NumConnections(TestGenome):
    # TODO write tests
    pass

class TestInit_Exceptions(TestGenome):
    def test_init_both_inputs_outputs_and_num_inputs_num_outputs_defined_exception(self):
        self.assertRaises(
            ValueError,
            Genome,
            inputs=self.input_nodes,
            outputs=self.output_nodes,
            num_inputs=self.num_inputs,
            num_outputs=self.num_outputs,
            fully_connect=True
        )

    def test_init_neither_inputs_outputs_and_num_inputs_num_outputs_defined_exception(self):
        self.assertRaises(
            ValueError,
            Genome,
            fully_connect=True
        )

    def test_init_invalid_zero_num_inputs(self):
        self.assertRaises(
            ValueError,
            Genome,
            num_inputs=0,
            num_outputs=self.num_outputs,
            fully_connect=True
        )
    
    def test_init_invalid_negative_num_inputs(self):
        self.assertRaises(
            ValueError,
            Genome,
            num_inputs=-1,
            num_outputs=self.num_outputs,
            fully_connect=True
        )
    
    def test_init_invalid_zero_num_outputs(self):
        self.assertRaises(
            ValueError,
            Genome,
            num_inputs=self.num_inputs,
            num_outputs=0,
            fully_connect=True
        )
    
    def test_init_invalid_negative_num_outputs(self):
        self.assertRaises(
            ValueError,
            Genome,
            num_inputs=self.num_inputs,
            num_outputs=-1,
            fully_connect=True
        )

    def test_init_both_fully_connect_num_connections(self):
        self.assertRaises(
            ValueError,
            Genome,
            num_inputs=self.num_inputs,
            num_outputs=self.num_outputs,
            fully_connect=True,
            num_starting_connections= (self.num_inputs * self.num_outputs)
        )

    def test_init_fully_connect_false_num_connections_none(self):
        self.assertRaises(
            ValueError,
            Genome,
            num_inputs=self.num_inputs,
            num_outputs=self.num_outputs,
            fully_connect=False,
        )

    def test_init_invalid_zero_num_connections(self):
        self.assertRaises(
            ValueError,
            Genome,
            num_inputs=self.num_inputs,
            num_outputs=self.num_outputs,
            num_starting_connections=0
        )
    
    def test_init_invalid_zero_num_connections(self):
        self.assertRaises(
            ValueError,
            Genome,
            num_inputs=self.num_inputs,
            num_outputs=self.num_outputs,
            num_starting_connections=-1
        )

    def test_init_invalid_type_args(self):
        self.assertRaises(
            TypeError,
            Genome,
            inputs="inputs",
            outputs=self.output_nodes,
            fully_connect=True
        )
        self.assertRaises(
            TypeError,
            Genome,
            inputs=self.input_nodes,
            outputs="outputs",
            fully_connect=True
        )
        self.assertRaises(
            TypeError,
            Genome,
            inputs=self.input_nodes,
            outputs=self.output_nodes,
            fully_connect="True"
        )
        self.assertRaises(
            TypeError,
            Genome,
            num_inputs="num_inputs",
            num_outputs=self.num_outputs,
            fully_connect=True
        )
        self.assertRaises(
            TypeError,
            Genome,
            num_inputs=self.num_inputs,
            num_outputs="num_outputs",
            fully_connect=True
        )
        self.assertRaises(
            TypeError,
            Genome,
            num_inputs=self.num_inputs,
            num_outputs=self.num_outputs,
            num_starting_connections = "1"
        )

class TestMutate(TestGenome):
    # TODO write tests
    pass

class TestMutateAddNewConnection(TestGenome):
    # TODO write tests
    pass

class TestMutateAddNewNode(TestGenome):
    # TODO write tests
    pass

class TestMutateDeleteConnection(TestGenome):
    # TODO write tests
    pass

class TestMutateDeleteNode(TestGenome):
    # TODO write tests
    pass

class TestAddConnection(TestGenome):
    # TODO write tests
    pass

class TestAddNode(TestGenome):
    # TODO write tests
    pass

class TestDeleteConnection(TestGenome):
    # TODO write tests
    pass

class TestDeleteNode(TestGenome):
    # TODO write tests
    pass

class TestCopy(TestGenome):
    # TODO write tests
    pass

class TestAreNodesConnected(TestGenome):
    # TODO write tests
    pass

class TestCrossover(TestGenome):
    # TODO write tests
    pass

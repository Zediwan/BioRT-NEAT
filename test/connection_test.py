import unittest

from src.genes.node import Node
from src.genes.connection import Connection
from src.functions.activation import Activation
from src.functions.aggregation import Aggregation
from src.config import conf

class TestConnection(unittest.TestCase):
    def setUp(self) -> None:
        self.from_node = Node()
        self.to_node = Node()

class TestInit(TestConnection):
    def test_init_defaults(self):
        connection = Connection(self.from_node, self.to_node)
        
        self.assertIsNotNone(connection.FROM_NODE)
        self.assertEqual(self.from_node, connection.FROM_NODE)
        self.assertIsNotNone(connection.TO_NODE)
        self.assertEqual(self.to_node, connection.TO_NODE)
        self.assertIsNotNone(connection.weight)
        self.assertEqual(connection.weight, 1)

    def test_init_values(self):
        connection = Connection(self.from_node, self.to_node, 3)

        self.assertIsNotNone(connection.FROM_NODE)
        self.assertEqual(self.from_node, connection.FROM_NODE)
        self.assertIsNotNone(connection.TO_NODE)
        self.assertEqual(self.to_node, connection.TO_NODE)
        self.assertIsNotNone(connection.weight)
        self.assertEqual(connection.weight, 3)

    def test_init_from_to_equal_node_error(self):
        self.assertRaises(ValueError, Connection, self.from_node, self.from_node)

    def test_init_type_error(self):
        self.assertRaises(TypeError, Connection, self.from_node, "test")
        self.assertRaises(TypeError, Connection, "test", self.to_node)
        self.assertRaises(TypeError, Connection, self.from_node, self.to_node, weight = "test")

class TestSendValue(TestConnection):
    def test_send_value_valid_args(self):
        connection = Connection(self.from_node, self.to_node)
        self.from_node._values.append(1)
        connection.send_value()

        self.assertEqual(1, connection.TO_NODE.get_value())

    def test_send_value_weight(self):
        connection = Connection(self.from_node, self.to_node, weight=2)

        self.from_node._values.append(1)
        connection.send_value()

        self.assertEqual(2, connection.TO_NODE.get_value())

class TestMutate(TestConnection):
    def setUp(self) -> None:
        super().setUp()
        self.old_new_weight_proba = conf.mut.new_weight_proba

    def tearDown(self) -> None:
        super().tearDown()
        conf.mut.new_weight_proba = self.old_new_weight_proba

    def test_mutate_zero_probas(self):
        conf.mut.new_weight_proba = 0

        con = Connection(self.from_node, self.to_node)
        pre_mutate_weight = con.weight

        con.mutate()

        self.assertEqual(con.weight, pre_mutate_weight, f"Weight value did change despite 0% mutation chance. Before: {pre_mutate_weight} != after: {con.weight}.")

    def test_mutate_guaranteed(self):
        conf.mut.new_weight_proba = 1

        con = Connection(self.from_node, self.to_node)
        pre_mutate_weight = con.weight

        con.mutate()

        self.assertNotEqual(con.weight, pre_mutate_weight, f"Weight value did not change despite 100% mutation chance. Before: {pre_mutate_weight} == after: {con.weight}.")

class TestMutateWeight(TestConnection):
    def test_mutate_weight(self):
        connection = Connection(self.from_node, self.to_node)
        pre_mut_weight = connection.weight
        connection._mutate_weight()

        self.assertNotEqual(connection.weight, pre_mut_weight, f"Weight value did not change after mutation. Before: {pre_mut_weight} == after: {connection.weight}.")
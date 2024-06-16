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
        
        self.assertIsNotNone(connection.from_node)
        self.assertEqual(self.from_node, connection.from_node)
        self.assertIsNotNone(connection.to_node)
        self.assertEqual(self.to_node, connection.to_node)
        self.assertIsNotNone(connection.weight)
        self.assertEqual(connection.weight, 1)

    def test_init_values(self):
        connection = Connection(self.from_node, self.to_node, 3)

        self.assertIsNotNone(connection.from_node)
        self.assertEqual(self.from_node, connection.from_node)
        self.assertIsNotNone(connection.to_node)
        self.assertEqual(self.to_node, connection.to_node)
        self.assertIsNotNone(connection.weight)
        self.assertEqual(connection.weight, 3)

    def test_init_from_to_equal_node_error(self):
        self.assertRaises(ValueError, Connection, self.from_node, self.from_node)

    def test_init_type_error(self):
        self.assertRaises(TypeError, Connection, self.from_node, "test")
        self.assertRaises(TypeError, Connection, "test", self.to_node)
        self.assertRaises(TypeError, Connection, self.from_node, self.to_node, weight = "test")

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

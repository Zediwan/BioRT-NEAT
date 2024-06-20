import unittest
from unittest.mock import patch

from src.genes.node import Node
from src.genes.connection import Connection
from src.functions.activation import Activation
from src.functions.aggregation import Aggregation
from src.config import conf

# TODO write documentation for all the tests, about what part they are testing

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

        self.assertEqual(con.weight, pre_mutate_weight, f"Weight value did change despite 0% mutation chance.")

    def test_mutate_guaranteed(self):
        conf.mut.new_weight_proba = 1

        con = Connection(self.from_node, self.to_node)
        pre_mutate_weight = con.weight

        con.mutate()

        self.assertNotEqual(con.weight, pre_mutate_weight, f"Weight value did not change despite 100% mutation chance.")

    @patch("random.random")
    def test_mutate_lower_edge(self, mock_random):
        conf.mut.new_weight_proba = 0
        mock_random.return_value = 0

        con = Connection(self.from_node, self.to_node)
        pre_mutate_weight = con.weight

        con.mutate()

        self.assertEqual(con.weight, pre_mutate_weight, f"Weight value did change despite 0% mutation chance.")

class TestMutateWeight(TestConnection):
    def test_mutate_weight(self):
        connection = Connection(self.from_node, self.to_node)
        pre_mut_weight = connection.weight
        connection._mutate_weight()

        self.assertNotEqual(connection.weight, pre_mut_weight, f"Weight value did not change after mutation. Before: {pre_mut_weight} == after: {connection.weight}.")

class TestCopy(TestConnection):
    def test_copy(self):
        con = Connection(self.from_node, self.to_node)
        con_copy = con.copy()

        self.assertEqual(con.FROM_NODE, con_copy.FROM_NODE)
        self.assertEqual(con.TO_NODE, con_copy.TO_NODE)
        self.assertEqual(con.weight, con_copy.weight)

class TestSameConnection(TestConnection):
    def test_same_connection_true(self):
        con1 = Connection(self.from_node, self.to_node, weight=1)
        con2 = Connection(self.from_node, self.to_node, weight=1)

        self.assertTrue(con1.same_connection(con2))

    def test_same_connection_false_from_node(self):
        con1 = Connection(Node(Activation.CLAMPED, agg=Aggregation.MEAN), self.to_node, weight=1)
        con2 = Connection(self.from_node, self.to_node, weight=1)

        self.assertFalse(con1.same_connection(con2))

    def test_same_connection_false_to_node(self):
        con1 = Connection(self.from_node, Node(Activation.CLAMPED, agg=Aggregation.MEAN), weight=1)
        con2 = Connection(self.from_node, self.to_node, weight=1)

        self.assertFalse(con1.same_connection(con2))

class TestSimilar(TestConnection):
    def test_similar_true(self):
        con1 = Connection(self.from_node, self.to_node, weight=1)
        con2 = Connection(self.from_node, self.to_node, weight=1)

        self.assertTrue(con1.similar(con2))

    def test_similar_false_weight(self):
        con1 = Connection(self.from_node, self.to_node, weight=1)
        con2 = Connection(self.from_node, self.to_node, weight=2)

        self.assertFalse(con1.similar(con2))

    def test_similar_false_from_node(self):
        con1 = Connection(Node(Activation.CLAMPED, agg=Aggregation.MEAN), self.to_node, weight=1)
        con2 = Connection(self.from_node, self.to_node, weight=1)

        self.assertFalse(con1.similar(con2))

    def test_similar_false_to_node(self):
        con1 = Connection(self.from_node, Node(Activation.CLAMPED, agg=Aggregation.MEAN), weight=1)
        con2 = Connection(self.from_node, self.to_node, weight=1)

        self.assertFalse(con1.similar(con2))

class TestCrossover(TestConnection):
    def test_crossover_valid(self):
        fn = Node(
            Activation.ID,
            Aggregation.MAX,
            bias=1,
            response=1
        )
        tn = Node(
            Activation.ID,
            Aggregation.MAX,
            bias=1,
            response=1
        )
        w1 = 1
        w2 = 2

        con1 = Connection(fn, tn, weight=w1)
        con2 = Connection(fn, tn, weight=w2)
        con3 = Connection.crossover(con1, con2)

        self.assertIn(con3.weight, [w1, w2])

    @patch("random.random")
    def test_crossover_valid_left(self, mock_random):
        fn = Node(
            Activation.ID,
            Aggregation.MAX,
            bias=1,
            response=1
        )
        tn = Node(
            Activation.ID,
            Aggregation.MAX,
            bias=1,
            response=1
        )
        w1 = 1
        w2 = 2

        mock_random.return_value = 1

        con1 = Connection(fn, tn, weight=w1)
        con2 = Connection(fn, tn, weight=w2)
        con3 = Connection.crossover(con1, con2)

        self.assertEqual(con3.weight, w1)

    @patch("random.random")
    def test_crossover_valid_right(self, mock_random):
        fn = Node(
            Activation.ID,
            Aggregation.MAX,
            bias=1,
            response=1
        )
        tn = Node(
            Activation.ID,
            Aggregation.MAX,
            bias=1,
            response=1
        )
        w1 = 1
        w2 = 2

        mock_random.return_value = 0

        con1 = Connection(fn, tn, weight=w1)
        con2 = Connection(fn, tn, weight=w2)
        con3 = Connection.crossover(con1, con2)

        self.assertEqual(con3.weight, w2)

    @patch("random.random")
    def test_crossover_valid_edge(self, mock_random):
        fn = Node(
            Activation.ID,
            Aggregation.MAX,
            bias=1,
            response=1
        )
        tn = Node(
            Activation.ID,
            Aggregation.MAX,
            bias=1,
            response=1
        )
        w1 = 1
        w2 = 2

        mock_random.return_value = 0.5

        con1 = Connection(fn, tn, weight=w1)
        con2 = Connection(fn, tn, weight=w2)
        con3 = Connection.crossover(con1, con2)

        self.assertEqual(con3.weight, w2)

    def test_crossover_invalid(self):
        fn1 = Node(
            Activation.ID,
            Aggregation.MAX,
            bias=1,
            response=1
        )
        fn2 = Node(
            Activation.CLAMPED,
            Aggregation.MIN,
            bias=2,
            response=2
        )
        tn1 = Node(
            Activation.ID,
            Aggregation.MAX,
            bias=1,
            response=1
        )
        tn2 = Node(
            Activation.CLAMPED,
            Aggregation.MIN,
            bias=2,
            response=2
        )
        w1 = 1
        w2 = 2

        con1 = Connection(fn1, tn1, weight=w1)
        con2 = Connection(fn2, tn2, weight=w2)

        self.assertRaises(ValueError, Connection.crossover, con1, con2)

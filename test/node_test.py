import unittest

from src.genes.node import Node
from src.functions.activation import Activation
from src.functions.aggregation import Aggregation
from src.config import conf

class TestNode(unittest.TestCase):
    def setUp(self) -> None:
        self._af = Activation.ID
        self._agg = Aggregation.MAX
        self._bias = 1
        self._response = 1

class TestInit(TestNode):
    def test_init_no_args(self):
        node = Node()
        
        self.assertIsNotNone(node)
        self.assertIsNotNone(node.activation)
        self.assertTrue(Activation.is_valid_activation(node.activation))
        self.assertIsNotNone(node.aggregation)
        self.assertTrue(Aggregation.is_valid_aggregation(node.aggregation))
        self.assertIsNotNone(node.bias)
        self.assertEqual(node.bias, 0)
        self.assertIsNotNone(node.response)
        self.assertEqual(node.response, 1)
    
    def test_init_valid_args(self):
        node = Node(af=self._af, agg=self._agg, bias=self._bias, response=self._response)

        self.assertEqual(node.activation, self._af)
        self.assertEqual(node.aggregation, self._agg)
        self.assertEqual(node.bias, self._bias)
        self.assertEqual(node.response, self._response)
    
    def test_init_invalid_af_arg(self):
        self.assertRaises(ValueError, Node, af="test", agg=self._agg, bias=self._bias, response=self._response)

    def test_init_invalid_agg_arg(self):
        self.assertRaises(ValueError, Node, af=self._af, agg="test", bias=self._bias, response=self._response)

    def test_init_invalid_bias_arg(self):
        self.assertRaises(TypeError, Node, af=self._af, agg=self._agg, bias="test", response=self._response)

    def test_init_invalid_response_arg(self):
        self.assertRaises(TypeError, Node, af=self._af, agg=self._agg, bias=self._bias, response="test")

class TestRecieveCalue(TestNode):
    def test_reciev_value_valid(self):
        node = Node(af=Activation.get_random(), agg=Aggregation.get_random())
        node.recieve_value(1)

    def test_recieve_value_invalid(self):
        node = Node(af=Activation.get_random(), agg=Aggregation.get_random())
        self.assertRaises(TypeError, node.recieve_value, "test")

class TestGetValueSingle(TestNode):
    def test_get_value_valid_single_input_zero(self):
        node = Node(af=Activation.ID, agg=Aggregation.get_random(), bias=0, response=0)
        node.recieve_value(1)
        result = node.get_value()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, 0)
    
    def test_get_value_valid_single_input_no_change(self):
        node = Node(af=Activation.ID, agg=Aggregation.get_random(), bias=0, response=1)
        node.recieve_value(1)
        result = node.get_value()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, 1)
    
    def test_get_value_valid_single_input_bias(self):
        node = Node(af=Activation.ID, agg=Aggregation.get_random(), bias=1, response=1)
        node.recieve_value(1)
        result = node.get_value()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, 2)
    
    def test_get_value_valid_single_input_response(self):
        node = Node(af=Activation.ID, agg=Aggregation.get_random(), bias=0, response=2)
        node.recieve_value(1)
        result = node.get_value()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, 2)
    
    def test_get_value_valid_single_input_response_and_bias(self):
        node = Node(af=Activation.ID, agg=Aggregation.get_random(), bias=1, response=2)
        node.recieve_value(1)
        result = node.get_value()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, 3)

class TestGetValueMultiple(TestNode):
    def test_get_value_valid_multiple_inputs_zero(self):
        node = Node(af=Activation.ID, agg=Aggregation.MEAN, bias=0, response=0)
        node.recieve_value(1)
        node.recieve_value(2)
        result = node.get_value()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, 0)

    def test_get_value_valid_multiple_inputs_no_change(self):
        node = Node(af=Activation.ID, agg=Aggregation.MEAN, bias=0, response=1)
        node.recieve_value(1)
        node.recieve_value(2)
        result = node.get_value()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, 1.5)

    def test_get_value_valid_multiple_inputs_bias(self):
        node = Node(af=Activation.ID, agg=Aggregation.MEAN, bias=1, response=1)
        node.recieve_value(1)
        node.recieve_value(2)
        result = node.get_value()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, 2.5)

    def test_get_value_valid_multiple_inputs_response(self):
        node = Node(af=Activation.ID, agg=Aggregation.MEAN, bias=0, response=2)
        node.recieve_value(1)
        node.recieve_value(2)
        result = node.get_value()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, 3)

    def test_get_value_valid_multiple_inputs_response_and_bias(self):
        node = Node(af=Activation.ID, agg=Aggregation.MEAN, bias=1, response=2)
        node.recieve_value(1)
        node.recieve_value(2)
        result = node.get_value()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, 4)

class TestMutate(TestNode):
    def setUp(self) -> None:
        super().setUp()
        self.old_new_af_proba = conf.mut.new_af_proba
        self.old_new_agg_proba = conf.mut.new_agg_proba
        self.old_new_bias_proba = conf.mut.new_bias_proba
        self.old_new_response_proba = conf.mut.new_response_proba

    def tearDown(self) -> None:
        super().tearDown()
        conf.mut.new_af_proba = self.old_new_af_proba
        conf.mut.new_agg_proba = self.old_new_agg_proba
        conf.mut.new_bias_proba = self.old_new_bias_proba
        conf.mut.new_response_proba = self.old_new_response_proba

    def test_mutate_zero_probas(self):
        conf.mut.new_af_proba = 0
        conf.mut.new_agg_proba = 0
        conf.mut.new_bias_proba = 0
        conf.mut.new_response_proba = 0

        node_pure = Node(self._af, self._agg, self._bias, self._response)
        node_mutated = Node(self._af, self._agg, self._bias, self._response)

        node_mutated.mutate()

        self.assertEqual(node_pure.activation, node_mutated.activation)
        self.assertEqual(node_pure.aggregation, node_mutated.aggregation)
        self.assertEqual(node_pure.bias, node_mutated.bias)
        self.assertEqual(node_pure.response, node_mutated.response)

    def test_mutate_guaranteed(self):
        conf.mut.new_af_proba = 1
        conf.mut.new_agg_proba = 1
        conf.mut.new_bias_proba = 1
        conf.mut.new_response_proba = 1

        node_pure = Node(self._af, self._agg, self._bias, self._response)
        node_mutated = Node(self._af, self._agg, self._bias, self._response)

        node_mutated.mutate()

        self.assertNotEqual(node_pure.activation, node_mutated.activation)
        self.assertNotEqual(node_pure.aggregation, node_mutated.aggregation)
        self.assertNotEqual(node_pure.bias, node_mutated.bias)
        self.assertNotEqual(node_pure.response, node_mutated.response)

class TestMutateActivationFunction(TestNode):
    def test_mutate_activation_function(self):
        node_pure = Node(self._af, self._agg, self._bias, self._response)
        node_mutated = Node(self._af, self._agg, self._bias, self._response)

        node_mutated._mutate_activation_function()

        self.assertNotEqual(node_pure.activation, node_mutated.activation)

class TestMutateAggregationFunction(TestNode):
    def test_mutate_aggregation_function(self):
        node_pure = Node(self._af, self._agg, self._bias, self._response)
        node_mutated = Node(self._af, self._agg, self._bias, self._response)

        node_mutated._mutate_aggregation_function()

        self.assertNotEqual(node_pure.aggregation, node_mutated.aggregation)

class TestMutateBias(TestNode):
    def test_mutate_bias(self):
        node_pure = Node(self._af, self._agg, self._bias, self._response)
        node_mutated = Node(self._af, self._agg, self._bias, self._response)

        node_mutated._mutate_bias()

        self.assertNotEqual(node_pure.bias, node_mutated.bias)

class TestMutateResponse(TestNode):
    def test_mutate_response(self):
        node_pure = Node(self._af, self._agg, self._bias, self._response)
        node_mutated = Node(self._af, self._agg, self._bias, self._response)

        node_mutated._mutate_response()

        self.assertNotEqual(node_pure.response, node_mutated.response)

class TestCopy(TestNode):
    def test_copy(self):
        node = Node(self._af, self._agg, self._bias, self._response)
        node_copy = node.copy()

        self.assertEqual(node.activation, node_copy.activation)
        self.assertEqual(node.aggregation, node_copy.aggregation)
        self.assertEqual(node.bias, node_copy.bias)
        self.assertEqual(node.response, node_copy.response)

class TestEquals(TestNode):
    def test_equals_true(self):
        node1 = Node(self._af, self._agg, self._bias, self._response)
        node2 = Node(self._af, self._agg, self._bias, self._response)

        self.assertTrue(node1.equals(node2))

    def test_equals_false(self):
        node1 = Node(self._af, self._agg, self._bias, self._response)
        node2 = Node(self._af, self._agg, self._bias + 1, self._response)

        self.assertFalse(node1.equals(node2))

class TestCrossover(TestNode):
    def test_crossover(self):
        node1 = Node(self._af, self._agg, self._bias, self._response)
        node2 = Node(Activation.get_random(self._af), Aggregation.get_random(self._agg), self._bias + 1, self._response + 1)

        child_node = Node.crossover(node1, node2)

        self.assertIn(child_node.activation, (node1.activation, node2.activation))
        self.assertIn(child_node.aggregation, (node1.aggregation, node2.aggregation))
        self.assertIn(child_node.bias, (node1.bias, node2.bias))
        self.assertIn(child_node.response, (node1.response, node2.response))

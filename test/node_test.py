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

class TestGetValueSingle(TestNode):
    def test_get_value_valid_single_input_zero(self):
        node = Node(af=Activation.ID, agg=Aggregation.get_random(), bias=0, response=0)
        inputs = [1]
        result = node.get_value(inputs)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, 0)
    
    def test_get_value_valid_single_input_no_change(self):
        node = Node(af=Activation.ID, agg=Aggregation.get_random(), bias=0, response=1)
        inputs = [1]
        result = node.get_value(inputs)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, inputs[0])
    
    def test_get_value_valid_single_input_bias(self):
        node = Node(af=Activation.ID, agg=Aggregation.get_random(), bias=1, response=1)
        inputs = [1]
        result = node.get_value(inputs)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, inputs[0] + 1)
    
    def test_get_value_valid_single_input_response(self):
        node = Node(af=Activation.ID, agg=Aggregation.get_random(), bias=0, response=2)
        inputs = [1]
        result = node.get_value(inputs)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, inputs[0] * 2)
    
    def test_get_value_valid_single_input_response_and_bias(self):
        node = Node(af=Activation.ID, agg=Aggregation.get_random(), bias=1, response=2)
        inputs = [1]
        result = node.get_value(inputs)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, inputs[0] * 2 + 1)
        
    def test_get_value_invalid_single_input(self):
        node = Node(af=Activation.ID, agg=Aggregation.get_random(), bias=0, response=0)
        inputs = ["invalid input"]
        
        self.assertRaises((ValueError, TypeError), node.get_value, inputs)

class TestGetValueMultiple(TestNode):
    def test_get_value_valid_multiple_inputs_zero(self):
        node = Node(af=Activation.ID, agg=Aggregation.MEAN, bias=0, response=0)
        inputs = [1, 2]
        result = node.get_value(inputs)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, 0)

    def test_get_value_valid_multiple_inputs_no_change(self):
        node = Node(af=Activation.ID, agg=Aggregation.MEAN, bias=0, response=1)
        inputs = [1, 2]
        result = node.get_value(inputs)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, (inputs[0] + inputs[1])/2)

    def test_get_value_valid_multiple_inputs_bias(self):
        node = Node(af=Activation.ID, agg=Aggregation.MEAN, bias=1, response=1)
        inputs = [1, 2]
        result = node.get_value(inputs)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, (inputs[0] + inputs[1])/2 + 1)

    def test_get_value_valid_multiple_inputs_response(self):
        node = Node(af=Activation.ID, agg=Aggregation.MEAN, bias=0, response=2)
        inputs = [1, 2]
        result = node.get_value(inputs)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, (inputs[0] + inputs[1])/2 * 2)

    def test_get_value_valid_multiple_inputs_response_and_bias(self):
        node = Node(af=Activation.ID, agg=Aggregation.MEAN, bias=1, response=2)
        inputs = [1, 2]
        result = node.get_value(inputs)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, (float, int))
        self.assertEqual(result, (inputs[0] + inputs[1])/2 * 2 + 1)

    def test_get_value_invalid_multiple_inputs(self):
        node = Node(af=Activation.ID, agg=Aggregation.get_random(), bias=0, response=0)
        inputs = ["invalid input"]

        self.assertRaises((ValueError, TypeError), node.get_value, inputs)

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
    pass

class TestMutateAggregationFunction(TestNode):
    pass

class TestMutateBias(TestNode):
    pass

class TestMutateResponse(TestNode):
    pass

class TestCopy(TestNode):
    pass

class TestEquals(TestNode):
    pass

class TestCrossover(TestNode):
    pass

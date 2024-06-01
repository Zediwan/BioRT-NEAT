
from src.gene import Gene, NodeGene
from src.functions.activations import Activations
from src.functions.aggregations import Aggregations
import unittest

class TestNodeGene(unittest.TestCase):
    def setUp(self) -> None:
        self.key = 1
        self.node_gene = NodeGene(key=self.key)
        # Save class variables to reset them after tests have been completed
        self.starting_BIAS_MUTATION_CHANCE = NodeGene.BIAS_MUTATION_CHANCE
        self.starting_ACTIVATION_FUNCTION_MUTATION_CHANCE = NodeGene.ACTIVATION_FUNCTION_MUTATION_CHANCE
        self.starting_AGGREGATION_FUNCTION_MUTATION_CHANCE = NodeGene.AGGREGATION_FUNCTION_MUTATION_CHANCE
        self.starting_RESPONSE_FUNCTION_MUTATION_CHANCE = NodeGene.RESPONSE_FUNCTION_MUTATION_CHANCE
    
    def tearDown(self) -> None:
        # Reset class variables back to starting values
        NodeGene.BIAS_MUTATION_CHANCE = self.starting_BIAS_MUTATION_CHANCE
        NodeGene.ACTIVATION_FUNCTION_MUTATION_CHANCE = self.starting_ACTIVATION_FUNCTION_MUTATION_CHANCE
        NodeGene.AGGREGATION_FUNCTION_MUTATION_CHANCE = self.starting_AGGREGATION_FUNCTION_MUTATION_CHANCE
        NodeGene.RESPONSE_FUNCTION_MUTATION_CHANCE = self.starting_RESPONSE_FUNCTION_MUTATION_CHANCE

class TestNodeGene(TestNodeGene):
    def test_initialises_with_default_values(self):
        """
        NodeGene initializes with default values when no parameters are provided
        """
        self.node_gene = NodeGene(key=1)
        self.assertEqual(self.node_gene.bias, 1)
        self.assertIsNotNone(self.node_gene.activation)
        self.assertTrue(callable(self.node_gene.activation))
        self.assertIsNotNone(self.node_gene.aggregation)
        self.assertTrue(callable(self.node_gene.aggregation))
        self.assertEqual(self.node_gene.response, 1)
    
    def test_mutate_no_changes_when_chances_not_met(self):
        """
        Mutate method handles cases when random chance conditions are not met
        """
        original_bias = self.node_gene.bias
        original_activation = self.node_gene.activation
        original_aggregation = self.node_gene.aggregation
        original_response = self.node_gene.response

        NodeGene.BIAS_MUTATION_CHANCE = 0
        NodeGene.ACTIVATION_FUNCTION_MUTATION_CHANCE = 0
        NodeGene.AGGREGATION_FUNCTION_MUTATION_CHANCE = 0
        NodeGene.RESPONSE_FUNCTION_MUTATION_CHANCE = 0

        self.node_gene.mutate()

        self.assertEqual(self.node_gene.bias, original_bias)
        self.assertEqual(self.node_gene.activation, original_activation)
        self.assertEqual(self.node_gene.aggregation, original_aggregation)
        self.assertEqual(self.node_gene.response, original_response)

    def test_node_gene_initializes_with_specified_values(self):
        """
        NodeGene initializes with specified values for bias, activation, aggregation, and response
        """
        bias = 0.5
        activation = Activations.SIGMOID
        aggregation = Aggregations.SUM
        response = 1

        node_gene = NodeGene(self.key, bias, activation, aggregation, response)

        self.assertEqual(node_gene.bias, bias)
        self.assertEqual(node_gene.activation, activation)
        self.assertEqual(node_gene.aggregation, aggregation)
        self.assertEqual(node_gene.response, response)

    def test_mutate_method_mutates_bias(self):
        """
        Mutate method correctly mutates bias when random chance condition is met
        """
        initial_bias = self.node_gene.bias
        NodeGene.BIAS_MUTATION_CHANCE = 1  # Set mutation chance to 100% for testing
        self.node_gene.mutate()
        self.assertNotEqual(self.node_gene.bias, initial_bias)

    def test_mutate_activation_function(self):
        """
        Mutate method correctly mutates activation function when random chance condition is met
        """
        initial_activation = self.node_gene.activation
        NodeGene.ACTIVATION_FUNCTION_MUTATION_CHANCE = 1  # Set mutation chance to 100% for testing
        self.node_gene.mutate()
        self.assertNotEqual(self.node_gene.activation, initial_activation)

    def test_mutate_aggregation_function(self):
        """
        Mutate method correctly mutates aggregation function when random chance condition is met
        """
        original_aggregation = self.node_gene.aggregation
        NodeGene.AGGREGATION_FUNCTION_MUTATION_CHANCE = 1  # Set mutation chance to 100% for testing
        self.node_gene.mutate()
        self.assertNotEqual(self.node_gene.aggregation, original_aggregation)

    def test_mutate_response_function(self):
        """
        Mutate method correctly mutates response function when random chance condition is met
        """
        response_before = self.node_gene.response
        NodeGene.RESPONSE_FUNCTION_MUTATION_CHANCE = 1  # Set mutation chance to 100%
        self.node_gene.mutate()
        response_after = self.node_gene.response
        self.assertNotEqual(response_before, response_after)

    def test_copy_method_creates_exact_copy(self):
        """
        Copy method creates an exact copy of the NodeGene instance
        """
        copied_node_gene = self.node_gene.copy()
    
        self.assertEqual(self.node_gene.bias, copied_node_gene.bias)
        self.assertEqual(self.node_gene.activation, copied_node_gene.activation)
        self.assertEqual(self.node_gene.aggregation, copied_node_gene.aggregation)
        self.assertEqual(self.node_gene.response, copied_node_gene.response)

    def test_node_gene_inherits_and_implements_abstract_methods(self):
        """
        NodeGene inherits from Gene and implements all abstract methods
        """
        self.assertIsInstance(self.node_gene, Gene)
        self.assertTrue(hasattr(self.node_gene, 'mutate'))
        self.assertTrue(hasattr(self.node_gene, 'copy'))
        self.assertTrue(hasattr(self.node_gene, 'equals'))
        self.assertTrue(hasattr(self.node_gene, 'distance'))
        self.assertTrue(hasattr(NodeGene, 'crossover'))

    def test_distance_calculation(self):
        """
        Distance method calculates correct distance between two NodeGene instances
        """
        node_gene1 = NodeGene(self.key, bias=0.5, af=Activations.SIGMOID, aggregation=Aggregations.SUM, response=1)
        node_gene2 = NodeGene(self.key+1, bias=0.8, af=Activations.RELU, aggregation=Aggregations.MEAN, response=2)
        expected_distance = abs(0.5 - 0.8) + abs(2 - (1)) + 1.0 + 1.0
        self.assertEqual(node_gene1.distance(node_gene2), expected_distance)

    def test_distance_handles_none_functions(self):
        """
        Distance method handles cases when activation or aggregation functions are None
        """
        node_gene1 = self.node_gene
        node_gene2 = node_gene1.copy()
        node_gene1.activation = None
        node_gene2.activation = None
        node_gene1.aggregation = None
        node_gene2.aggregation = None

        distance = node_gene1.distance(node_gene2)

        self.assertEqual(distance, 0)

    def test_crossover_inherits_attributes(self):
        """
        Crossover method creates a new NodeGene inheriting attributes from both parents
        """
        parent1 = NodeGene(key=self.key, bias=0.5, af=Activations.SIGMOID, aggregation=Aggregations.SUM, response=1)
        parent2 = NodeGene(key=self.key, bias=-0.5, af=Activations.RELU, aggregation=Aggregations.MAX, response=2)
    
        child = NodeGene.crossover(parent1, parent2)
    
        self.assertIn(child.bias, [0.5, -0.5])
        self.assertIn(child.activation, [Activations.SIGMOID, Activations.RELU])
        self.assertIn(child.aggregation, [Aggregations.SUM, Aggregations.MAX])
        self.assertIn(child.response, [1, 2])

    def test_mutate_bias_extreme_values(self):
        """
        _mutate_bias method handles extreme values for bias mutation
        """
        initial_bias = self.node_gene.bias
        self.node_gene._mutate_bias()
        self.assertNotEqual(self.node_gene.bias, initial_bias)  # Check if bias has changed

    def test_crossover_handles_different_keys(self):
        """
        Crossover method handles cases when parent NodeGenes have different keys
        """
        g1 = NodeGene(self.key, bias=0.5, af=Activations.SIGMOID, aggregation=Aggregations.SUM, response=1)
        g2 = NodeGene(self.key+1, bias=0.8, af=Activations.RELU, aggregation=Aggregations.MAX, response=2)

        self.assertRaises(AssertionError, NodeGene.crossover, g1, g2)

    def test_handle_invalid_types(self):
        """
        NodeGene should handle invalid types for bias, activation, aggregation, and response
        """
        self.assertRaises(TypeError, NodeGene, None)
        self.assertRaises(TypeError, NodeGene, 1, "invalid_bias_type", Activations.SIGMOID, Aggregations.SUM, 1)
        self.assertRaises(TypeError, NodeGene, 1, 1, "invalid_bias_type", Aggregations.SUM, 1)
        self.assertRaises(TypeError, NodeGene, 1, 1, Activations.SIGMOID, "invalid_bias_type", 1)
        self.assertRaises(TypeError, NodeGene, 1, 1, Activations.SIGMOID, Aggregations.SUM, "invalid_bias_type")

    # Test the performance of the mutate method under high mutation chances
    def test_mutate_method_high_mutation_chances(self):
        NodeGene.BIAS_MUTATION_CHANCE = 1.0
        NodeGene.ACTIVATION_FUNCTION_MUTATION_CHANCE = 1.0
        NodeGene.AGGREGATION_FUNCTION_MUTATION_CHANCE = 1.0
        NodeGene.RESPONSE_FUNCTION_MUTATION_CHANCE = 1.0

        initial_bias = self.node_gene.bias
        initial_activation = self.node_gene.activation
        initial_aggregation = self.node_gene.aggregation
        initial_response = self.node_gene.response

        self.node_gene.mutate()

        self.assertNotEqual(self.node_gene.bias, initial_bias)
        self.assertNotEqual(self.node_gene.activation, initial_activation)
        self.assertNotEqual(self.node_gene.aggregation, initial_aggregation)
        self.assertNotEqual(self.node_gene.response, initial_response)

    def test_large_number_of_instances_efficiency(self):
        """
        Ensure NodeGene's methods handle large numbers of instances efficiently
        """
        # Create a large number of NodeGene instances
        num_instances = 1000
        instances = [NodeGene(i) for i in range(num_instances)]
    
        # Test that all instances were created successfully
        self.assertEqual(len(instances), num_instances)

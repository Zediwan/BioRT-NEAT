from __future__ import annotations
from abc import ABC, abstractmethod
import random
from .extended_enum import ExtendedEnum
from .functions.activations import Activations
from .functions.aggregations import Aggregations

class Gene(ABC):
    # The coefficient for each weight, bias, or response multiplier difference’s contribution to
    # the genomic distance (for homologous nodes or connections).
    # This is also used as the value to add for differences in
    # activation functions, aggregation functions, or enabled/disabled status.
    compatibility_weight_coefficient = 1

    def __init__(self, key) -> None:
        self.key = key
    
    @abstractmethod
    def mutate(self) -> None:
        pass

    @abstractmethod
    def copy(self) -> None:
        pass

    @abstractmethod
    def equals(self, gene: Gene) -> bool:
        pass

    @abstractmethod
    def distance(self, gene: Gene) -> float:
        pass

    @staticmethod
    @abstractmethod
    def crossover(g1: Gene, g2: Gene) -> Gene:
        pass

class NodeGeneType(ExtendedEnum):
    # Sensor and input are the same
    SENSOR = 1
    INPUT = 1
    HIDDEN = 2
    OUTPUT = 3
        
class NodeGene(Gene):
    BIAS_MUTATION_CHANCE = 0
    ACTIVATION_FUNCTION_MUTATION_CHANCE = 0
    AGGREGATION_FUNCTION_MUTATION_CHANCE = 0
    RESPONSE_FUNCTION_MUTATION_CHANCE = 0

    def __init__(self, bias: float = 1, af: Activations = None, aggregation = None, response: Activations = None) -> None:
        super().__init__()
        self.bias = bias
        if af is None:
            af = Activations.get_random_activation_function()
        self.activation = af
        self.aggregation = aggregation
        if response is None:
            response = Activations.get_random_activation_function()
        self.response = response
    
    def mutate(self) -> None:
        super().mutate()
        if random.random() <= NodeGene.BIAS_MUTATION_CHANCE:
            self._mutate_bias()
        if random.random() <= NodeGene.ACTIVATION_FUNCTION_MUTATION_CHANCE:
            self._mutate_activation_function()
        if random.random() <= NodeGene.AGGREGATION_FUNCTION_MUTATION_CHANCE:
            self._mutate_activation_function()
        if random.random() <= NodeGene.RESPONSE_FUNCTION_MUTATION_CHANCE:
            self._mutate_activation_function()
    
    def _mutate_bias(self) -> None:
        self.bias += random.gauss()
    
    def _mutate_activation_function(self) -> None:
        self.activation = Activations.get_random_activation_function()

    def _mutate_aggregation_function(self) -> None:
        self.aggregation = Aggregations.get_random_aggregation_function

    def _mutate_response_function(self) -> None:
        self.response = Activations.get_random_activation_function()

    def copy(self) -> NodeGene:
        return NodeGene(self.bias, self.activation, self.aggregation, self.response)

    def equals(self, gene: Gene) -> bool:
        raise NotImplementedError()

    def distance(self, other: NodeGene) -> float:
        d = abs(self.bias - other.bias) + abs(self.response - other.response)
        if self.activation != other.activation:
            d += 1.0
        if self.aggregation != other.aggregation:
            d += 1.0
        return d * Gene.compatibility_weight_coefficient

    @staticmethod
    def crossover(g1: NodeGene, g2: NodeGene) -> NodeGene:
        """ Creates a new gene randomly inheriting attributes from its parents."""
        assert g1.key == g2.key # TODO why is this needed?

        # Note: we use "a if random() > 0.5 else b" instead of choice((a, b))
        # here because `choice` is substantially slower.
        bias = g1.bias if random.random > 0.5 else g2.bias
        activation = g1.activation if random.random > 0.5 else g2.activation
        aggregation = g1.aggregation if random.random > 0.5 else g2.aggregation
        response = g1.response if random.random > 0.5 else g2.response

        return NodeGene(bias, activation, aggregation, response)
        
class ConnectionGene(Gene):
    WEIGHT_MUTATION_CHANCE = 0
    ENABLED_MUTATION_CHANCE = 0

    def __init__(self, _from: NodeGene, _to: NodeGene, weight = None, enabled: bool = True) -> None:
        super().__init__((_from.key, _to.key))
        self._from: NodeGene = _from
        self._to: NodeGene = _to
        if weight is None:
            weight = random.uniform()
        self.weight = weight
        self.enabled = enabled
        #self.recurrent = False
    
    def mutate(self) -> None:
        super().mutate()
        if random.random() <= ConnectionGene.WEIGHT_MUTATION_CHANCE:
            self._mutate_weight()
        if random.random() <= ConnectionGene.ENABLED_MUTATION_CHANCE:
            self.enabled = not self.enabled

    def _mutate_weight(self) -> None:
        self.weight += random.gauss()

    def _mutate_enabled(self) -> None:
        self.enabled = not self.enabled

    def copy(self) -> ConnectionGene:
        return ConnectionGene(self._from, self._to, self.weight, self.enabled)

    def equals(self, connection: ConnectionGene) -> bool:
        return self._from.equals(connection._from) and self._to.equals(connection._to)

    def distance(self, other: ConnectionGene) -> float:
        d = abs(self.weight - other.weight)
        if self.enabled != other.enabled:
            d += 1.0
        return d * Gene.compatibility_weight_coefficient

    @staticmethod
    def crossover(g1: ConnectionGene, g2: ConnectionGene) -> ConnectionGene:
        """ Creates a new gene randomly inheriting attributes from its parents."""
        assert g1.key == g2.key # TODO why is this needed?

        # Note: we use "a if random() > 0.5 else b" instead of choice((a, b))
        # here because `choice` is substantially slower.
        weight = g1.weight if random.random > 0.5 else g2.weight
        enabled = g1.enabled if random.random > 0.5 else g2.enabled

        return ConnectionGene(g1._from, g1._to, weight, enabled)

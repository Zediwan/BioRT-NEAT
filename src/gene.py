from __future__ import annotations
from abc import ABC, abstractmethod
import random
from itertools import count
from .extended_enum import ExtendedEnum
from .activation_function import ActivationFunction


class NodeGeneType(ExtendedEnum):
    # Sensor and input are the same
    SENSOR = 1 
    INPUT = 1
    HIDDEN = 2
    OUTPUT = 3

class Gene(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def mutate(self) -> None:
        pass

    @abstractmethod
    def copy(self) -> None:
        pass
        
class NodeGene(Gene):
    BIAS_MUTATION_CHANCE = 0
    ACTIVATION_FUNCTION_MUTATION_CHANCE = 0
    
    def __init__(self) -> None:
        super().__init__()
        self.bias: float
        self.activation_function: ActivationFunction
        self.type = None
    
    def mutate(self) -> None:
        super().mutate()
        if random.random() <= NodeGene.BIAS_MUTATION_CHANCE:
            self._mutate_bias()
        if random.random() <= NodeGene.ACTIVATION_FUNCTION_MUTATION_CHANCE:
            self._mutate_activation_function()
    
    def _mutate_bias(self) -> None:
        self.bias += random.gauss()
    
    def _mutate_activation_function(self) -> None:
        self.activation_function = ActivationFunction.get_random_activation_function()
        
class ConnectionGene(Gene):
    connection_archive: dict[tuple[int, int], int] = {}
    innovation_number_index = count()

    def __init__(self, _from: NodeGene, _to: NodeGene, weight = None) -> None:
        super().__init__()
        self._from: NodeGene = _from
        self._to: NodeGene = _to
        if weight is None:
            weight = random.uniform()
        self.weight = weight
        self.enabled = True
        #self.recurrent = False
        self.INNOVATION_NUMBER: int = ConnectionGene.get_innovation_number(_from, _to)
    
    def equals(self, connection: ConnectionGene) -> bool:
        return self._from.__eq__(connection._from) and self._to.__eq__(connection._to)

    @staticmethod
    def get_innovation_number(_from: NodeGene, _to: NodeGene) -> int:
        key = (_from, _to)

        if key not in ConnectionGene.connection_archive:
            ConnectionGene.connection_archive[key] = next(ConnectionGene.innovation_number_index)

        return ConnectionGene.connection_archive[key]

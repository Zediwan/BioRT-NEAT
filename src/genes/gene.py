from __future__ import annotations

from abc import ABC, abstractmethod

class Gene(ABC):
    @abstractmethod
    def mutate(self) -> None:
        pass

    @abstractmethod
    def copy(self) -> None:
        pass

    @abstractmethod
    def equals(self, gene: Gene) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def crossover(g1: Gene, g2: Gene) -> Gene:
        pass
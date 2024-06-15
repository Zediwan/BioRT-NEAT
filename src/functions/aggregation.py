from __future__ import annotations

from enum import Enum
import random
from functools import reduce
from operator import mul
from neat.math_util import mean, median2

def product_aggregation(x: list[float]) -> float:  # note: `x` is a list or other iterable
        return reduce(mul, x, 1.0)

def sum_aggregation(x: list[float]) -> float:
    return sum(x)


def max_aggregation(x: list[float]) -> float:
    return max(x)


def min_aggregation(x: list[float]) -> float:
    return min(x)


def maxabs_aggregation(x: list[float]) -> float:
    return max(x, key=abs)


def median_aggregation(x: list[float]) -> float:
    return median2(x)


def mean_aggregation(x: list[float]) -> float:
    return mean(x)

class Aggregation(Enum):
    PRODUCT = product_aggregation
    SUM = sum_aggregation
    MAX = max_aggregation
    MIN = min_aggregation
    MAX_ABS = maxabs_aggregation
    MEDIAN = median_aggregation
    MEAN = mean_aggregation

    @staticmethod
    def get_options() -> list[Aggregation]:
        return [
            Aggregation.MAX,
            Aggregation.MAX_ABS,
            Aggregation.MEAN,
            Aggregation.MEDIAN,
            Aggregation.MIN,
            Aggregation.PRODUCT,
            Aggregation.MIN
        ]

    @staticmethod
    def is_valid_aggregation(aggregation: Aggregation) -> bool:
        return aggregation in Aggregation.get_options() or callable(aggregation)

    @staticmethod
    def assert_aggregation(aggregation: Aggregation) -> None:
        if not Aggregation.is_valid_aggregation(aggregation):
            raise ValueError(f"Provided function is not a valid aggregation function: {aggregation}.")


    @staticmethod
    def get_random(old_agg: Aggregation = None) -> Aggregation:
        options = Aggregation.get_options().copy()
        if Aggregation.is_valid_aggregation(old_agg):
            options.remove(old_agg)
        return random.choice(options)
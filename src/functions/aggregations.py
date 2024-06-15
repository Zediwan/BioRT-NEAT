from __future__ import annotations
import random
from functools import reduce
from operator import mul
from neat.math_util import mean, median2

class Aggregations():
    #region functions
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
    #endregion

    PRODUCT = product_aggregation
    SUM = sum_aggregation
    MAX = max_aggregation
    MIN = min_aggregation
    MAX_ABS = maxabs_aggregation
    MEDIAN = median_aggregation
    MEAN = mean_aggregation

    aggregations = {
        MAX,
        MAX_ABS,
        MEAN,
        MEDIAN,
        MIN,
        PRODUCT,
        MIN
    }

    @staticmethod
    def is_valid_aggregation(aggregation: Aggregations) -> bool:
        return aggregation in Aggregations.aggregations

    @staticmethod
    def assert_aggregation(aggregation: Aggregations) -> None:
        if not Aggregations.is_valid_aggregation(aggregation):
            raise ValueError(f"Provided function is not a valid aggregation function: {aggregation}.")


    @staticmethod
    def get_random() -> Aggregations:
        return random.choice(Aggregations.aggregations)
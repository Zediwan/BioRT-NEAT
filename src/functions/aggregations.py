from __future__ import annotations
import random
from ..extended_enum import ExtendedEnum
from functools import reduce
from operator import mul
from neat.math_util import mean, median2

class Aggregations(ExtendedEnum):
    def product_aggregation(x):  # note: `x` is a list or other iterable
        return reduce(mul, x, 1.0)

    def sum_aggregation(x):
        return sum(x)


    def max_aggregation(x):
        return max(x)


    def min_aggregation(x):
        return min(x)


    def maxabs_aggregation(x):
        return max(x, key=abs)


    def median_aggregation(x):
        return median2(x)


    def mean_aggregation(x):
        return mean(x)
    
    PRODUCT = product_aggregation
    SUM = sum_aggregation
    MAX = max_aggregation
    MIN = min_aggregation
    MAX_ABS = maxabs_aggregation
    MEDIAN = median_aggregation
    MEAN = mean_aggregation

    @staticmethod
    def get_random_aggregation_function() -> Aggregations:
        return random.choice(Aggregations.get_options())
import unittest
from unittest.mock import patch

from src.genome import Genome
from src.genes.node import Node
from src.functions.activation import Activation
from src.functions.aggregation import Aggregation
from src.config import conf

class TestGenome(unittest.TestCase):
    def setUp(self) -> None:
        pass

class TestInit(TestGenome):
    def test_init_defaults(self):
        pass
    
    def test_init_valid_args(self):
        pass
    
    def test_init_fully_connect(self):
        pass
    
    def test_init_num_connections(self):
        pass
    
    def test_init_invalid_type_args(self):
        pass

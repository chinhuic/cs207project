from pytest import raises
import numpy as np
import math
import unittest
from SimulatedTimeSeries import SimulatedTimeSeries

class TestSimulatedTimeSeries(unittest.TestCase):
    
    # Produce
    # Test produce with chunk size 1
    def test_produce_chunk_1(self):
        sts = SimulatedTimeSeries(iter(zip(range(3), range(1, 4))))
        self.assertEqual(next(sts.produce()), [(0, 1)])
        self.assertEqual(next(sts.produce()), [(1, 2)])
        self.assertEqual(next(sts.produce()), [(2, 3)])
        
    # Test produce with chunk size 3
    def test_produce_chunk_3(self):
        sts = SimulatedTimeSeries(iter(zip(range(3), range(1, 4))))
        self.assertEqual(next(sts.produce(3)), [(0, 1), (1, 2), (2, 3)])
        
    # Test produce with various chunk sizes
    def test_produce_chunk_various(self):
        sts = SimulatedTimeSeries(iter(zip(range(10), range(1, 11))))
        self.assertEqual(next(sts.produce(2)), [(0, 1), (1, 2)])
        self.assertEqual(next(sts.produce(3)), [(2, 3), (3, 4), (4, 5)])
        self.assertEqual(next(sts.produce(5)), 
                         [(5, 6), (6, 7), (7, 8), (8, 9), (9, 10)])
        
    # __iter__ 
    # Test iterating over STS with empty values
    def test_iter_empty(self):
        sts_empty = SimulatedTimeSeries(iter(zip([], [])))
        with self.assertRaises(StopIteration): 
            next(iter(sts_empty))
            
            
    # Test iterating over a STS with evenly spaced integer values
    def test_iter_integer_spaced_1(self):
        sts = SimulatedTimeSeries(iter(zip(range(1, 16), range(15))))
        sts_iter = iter(sts)
        
        self.assertEqual(0, next(sts_iter))
        self.assertEqual(1, next(sts_iter))
        self.assertEqual(2, next(sts_iter))
        
    def test_iter_integer_spaced_3(self):
        sts = SimulatedTimeSeries(iter(zip(range(8), range(-5, 17, 3))))
        
        sts_iter = iter(sts)
        
        self.assertEqual(-5, next(sts_iter))
        self.assertEqual(-2, next(sts_iter))
        self.assertEqual(1, next(sts_iter))
    
            

    # Test iterating over a STS with values of type float
    def test_iter_float_values(self):
        sts = SimulatedTimeSeries(iter(zip(range(3), [3.14159, 42., -0.207])))
        
        sts_iter = iter(sts)
        
        self.assertEqual(3.14159, next(sts_iter))
        self.assertEqual(42., next(sts_iter))
        self.assertEqual(-0.207, next(sts_iter))
        
    # itervalues
    # Test itervalues method over STS with empty values
    def test_itervalues_empty(self):
        sts_empty = SimulatedTimeSeries(iter(zip([],[])))
        with self.assertRaises(StopIteration):
            next(sts_empty.itervalues())

    # Test itervalues method over a STS with one value
    def test_itervalues_simple(self):
        sts_simple = SimulatedTimeSeries(iter(zip([0],[42])))
        sts_simple_itervalues = sts_simple.itervalues()
        self.assertEqual(42, next(sts_simple_itervalues))
        with self.assertRaises(StopIteration):
            next(sts_simple_itervalues)
            
    # itertimes
    # Test itertimes method over STS with empty values
    def test_itertimes_empty(self):
        sts_empty = SimulatedTimeSeries(iter(zip([], [])))
        with self.assertRaises(StopIteration): 
            next(sts_empty.itertimes())
            
    # Test itertimes method over a STS with one value
    def test_itertimes_simple(self):
        sts_simple = SimulatedTimeSeries(iter(zip([0], [42])))
        sts_simple_itertimes = sts_simple.itertimes()
        self.assertEqual(0, next(sts_simple_itertimes))
        with self.assertRaises(StopIteration): 
            next(sts_simple_itertimes)
            
    # Test iterating over a STS with integer times
    def test_itertimes_integer(self):
        sts = SimulatedTimeSeries(iter(zip([3, 4, 5, 6], [1, 5, 3, 6])))
        
        sts_itertimes = sts.itertimes()
        
        self.assertEqual(3, next(sts_itertimes))
        self.assertEqual(4, next(sts_itertimes))
        self.assertEqual(5, next(sts_itertimes))
        self.assertEqual(6, next(sts_itertimes))
        
    # Test iterating over a STS with floating point times
    def test_itertimes_float(self):
        sts = SimulatedTimeSeries(iter(zip([0.1, 0.3, 0.6, 8.5], [1, 5, 3, 6])))
        
        sts_itertimes = sts.itertimes()
        
        self.assertEqual(0.1, next(sts_itertimes))
        self.assertEqual(0.3, next(sts_itertimes))
        self.assertEqual(0.6, next(sts_itertimes))
        self.assertEqual(8.5, next(sts_itertimes))
        
    # iteritems
    # Test iteritems method over STS with empty values
    def test_iteritems_empty(self):
        sts_empty = SimulatedTimeSeries(iter(zip([], [])))
        with self.assertRaises(StopIteration): 
            next(sts_empty.iteritems())
            
    # Test itertimes method over a STS with one value
    def test_iteritems_simple(self):
        sts_simple = SimulatedTimeSeries(iter(zip([1], [42])))
        sts_simple_iteritems = sts_simple.iteritems()
        self.assertEqual((1, 42), next(sts_simple_iteritems))
        with self.assertRaises(StopIteration): 
            next(sts_simple_iteritems)
            
    # Test iteritems over a STS with integer times and values
    # Check both the types of results and answers expected
    def test_iteritems_integer(self):
        sts = SimulatedTimeSeries(iter(zip([15, 20, 25, 30], [1, 5, 3, 6])))
            
        sts_iteritems = sts.iteritems()
        
        self.assertEqual((15, 1), next(sts_iteritems))
        self.assertEqual((20, 5), next(sts_iteritems))
        self.assertEqual((25, 3), next(sts_iteritems))
        self.assertEqual((30, 6), next(sts_iteritems))
        
    # Test iterating over a STS with float times and values
    # Check both the types of results and answers expected
    def test_iteritems_float(self):
        sts = SimulatedTimeSeries(iter(zip([1.2, 1.21, 1.41, 1.7], [1.5, 5.2, 3.21, 6.3])))
        
            
        sts_iteritems = sts.iteritems()
        
        self.assertEqual((1.2, 1.5), next(sts_iteritems))
        self.assertEqual((1.21, 5.2), next(sts_iteritems))
        self.assertEqual((1.41, 3.21), next(sts_iteritems))
        self.assertEqual((1.7, 6.3 ), next(sts_iteritems))
        
    
if __name__ == '__main__':
    unittest.main()
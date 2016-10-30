
from pytest import raises
import numpy as np
import unittest
from TimeSeries_Week2 import TimeSeries

class TestTimeSeries_Week2(unittest.TestCase):
    
    # __iter__ 
    # Test iterating over TS with empty values
    def test_iter_empty(self):
        ts_empty = TimeSeries([])
        with self.assertRaises(StopIteration): 
            next(iter(ts_empty))
            
    # Test iterating over a TS with one value
    def test_iter_simple(self):
        ts_simple = TimeSeries([1])
        ts_simple_iter = iter(ts_simple)
        self.assertEqual(ts_simple.value[0], next(ts_simple_iter))
        with self.assertRaises(StopIteration): 
            next(ts_simple_iter)
            
    # Test iterating over a TS with evenly spaced integer values
    # Check both the types of results and answers expected
    def test_iter_integer_spaced_1(self):
        ts = TimeSeries(range(15))
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, int) for n in iter_list))
        
        # Check results
        self.assertEqual(ts.value, iter_list)
        
    def test_iter_integer_spaced_3(self):
        ts = TimeSeries(range(-5, 17, 3))
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, int) for n in iter_list))
        
        # Check results
        self.assertEqual(ts.value, iter_list)
        
    def test_iter_integer_spaced_7(self):
        ts = TimeSeries(range(-14, 701, 7))
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, int) for n in iter_list))
        
        # Check results
        self.assertEqual(ts.value, iter_list)
        
    # Test iterating over a TS with values of type string
    # Check both the types of results and answers expected
    def test_iter_string_values(self):
        ts = TimeSeries(['1', '2', '5', '15'])
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, str) for n in iter_list))
        
        # Check results
        self.assertEqual(ts.value, iter_list)
        
    # Test iterating over a TS with values of type float
    # Check both the types of results and answers expected
    def test_iter_float_values(self):
        ts = TimeSeries([3.14159, 42., -0.207])
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
        
        # Check type
        self.assertTrue(all(isinstance(n, float) for n in iter_list))
        
        # Check results
        self.assertEqual(ts.value, iter_list)
        
    # Test iterating over a TS with values of type bool
    # Check both the types of results and answers expected
    def test_iter_bool_values(self):
        ts = TimeSeries([True, False, False, True, True])
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
        
        # Check type
        self.assertTrue(all(isinstance(n, bool) for n in iter_list))
        
        # Check results    
        self.assertEqual(ts.value, iter_list)
        
    # Test iterating over a TS with values of different types
    def test_iter_heterogeneous_values(self):
        ts = TimeSeries([True, 3, 'hello', 0.07, ('cs', 207)])
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
            
        self.assertEqual(ts.value, iter_list)
        
    # Test iterating over TS with different sequence types for input
    def test_iter_string_input(self):
        ts = TimeSeries('123456789abcde')
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
            
        self.assertEqual(ts.value, iter_list)
    
    def test_iter_tuple_input(self):
        ts = TimeSeries((0, 3.1, 5.2, 100, 9.77))
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
            
        self.assertEqual(ts.value, iter_list)
        
    # itertimes
    # Test itertimes method over TS with empty values
    def test_itertimes_empty(self):
        ts_empty = TimeSeries([])
        with self.assertRaises(StopIteration): 
            next(ts_empty.itertimes())
            
    # Test itertimes method over a TS with one value
    def test_itertimes_simple(self):
        ts_simple = TimeSeries([42])
        ts_simple_itertimes = ts_simple.itertimes()
        self.assertEqual(0, next(ts_simple_itertimes))
        with self.assertRaises(StopIteration): 
            next(ts_simple_itertimes)
            
    # Test iterating over a TS with integers
    # Check both the types of results and answers expected
    def test_itertimes_integer(self):
        ts = TimeSeries([1, 5, 3, 6])
        
        iter_list = []
        for val in ts.itertimes():
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, int) for n in iter_list))
        
        # Check results
        self.assertEqual([0, 1, 2, 3], iter_list)
        
    def test_itertimes_string(self):
        ts = TimeSeries('hellocs207')
        
        iter_list = []
        for val in ts.itertimes():
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, int) for n in iter_list))
        
        # Check results
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], iter_list)
            
    # iteritems
    # Test iteritems method over TS with empty values
    def test_iteritems_empty(self):
        ts_empty = TimeSeries([])
        with self.assertRaises(StopIteration): 
            next(ts_empty.iteritems())
            
    # Test itertimes method over a TS with one value
    def test_iteritems_simple(self):
        ts_simple = TimeSeries([42])
        ts_simple_iteritems = ts_simple.iteritems()
        self.assertEqual((0, 42), next(ts_simple_iteritems))
        with self.assertRaises(StopIteration): 
            next(ts_simple_iteritems)
            
    # Test iterating over a TS with integers
    # Check both the types of results and answers expected
    def test_iteritems_integer(self):
        ts = TimeSeries([1, 5, 3, 6])
        
        iter_list = []
        for val in ts.iteritems():
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, tuple) for n in iter_list))
        
        # Check results
        self.assertEqual([(0, 1), (1, 5), (2, 3), (3, 6)], iter_list)
        
    def test_iteritems_string(self):
        ts = TimeSeries('hello')
        
        iter_list = []
        for val in ts.iteritems():
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, tuple) for n in iter_list))
        
        # Check results
        self.assertEqual([(0, 'h'), (1, 'e'), (2, 'l'), (3, 'l'), (4, 'o')], 
                         iter_list)
    
if __name__ == '__main__':
    unittest.main()
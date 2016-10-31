
from pytest import raises
import numpy as np
import unittest
from TimeSeries_Class import TimeSeries

class TestTimeSeries_Week3(unittest.TestCase):
    
    # __init__
    # types of sequences
    def test_arg_type_range(self):
        self.assertEqual(TimeSeries(range(0,3), range(0,3)).value, [0,1,2])
        self.assertEqual(TimeSeries(range(0,3), range(0,3)).time, [0,1,2])
    
    def test_arg_type_tuple(self):
        self.assertEqual(TimeSeries(range(0,4), (1,42,3,10)).value, [1,42,3,10])
        self.assertEqual(TimeSeries(range(0,4), (1,42,3,10)).time, [0,1,2,3])
        
    # number of arguments
    def test_omitted_arg(self):
        with self.assertRaises(TypeError):
            x = TimeSeries()
    
    
    def test_multiple_args(self):
        with self.assertRaises(TypeError):
            x = TimeSeries(1,2,3)
            
    # series length
    def test_no_data_value(self):
        self.assertEqual(TimeSeries([], []).value, [])
        self.assertEqual(TimeSeries([], []).time, [])

    def test_one_data_value(self):
        self.assertEqual(TimeSeries([5], [1]).value, [1])
        self.assertEqual(TimeSeries([5], [1]).time, [5])

    def test_multiple_data_values(self):
        self.assertEqual(TimeSeries([0,1,2], [1,2,3]).value, [1,2,3])
        self.assertEqual(TimeSeries([0,1,2], [1,2,3]).time, [0,1,2])
        
    # __len__
    def test_length_zero(self):
        self.assertEqual(len(TimeSeries([], [])), 0)

    def test_length_nonzero(self):
        self.assertEqual(len(TimeSeries([0,1,2], [8,12,42])), 3)
        
    # __getitem__
    def test_getitem_index_in_series(self):
        x = TimeSeries(range(0,6), [2,4,6,8,10,12])
        self.assertEqual(x[3], 8)

    def test_getitem_large_index_outside_boundary(self):
        x = TimeSeries(range(0,6), [2,4,6,8,10,12])
        with self.assertRaises(IndexError):
            x[10]

    def test_getitem_negative_index(self):
        x = TimeSeries(range(0,6), [2,4,6,8,10,12])
        self.assertEqual(x[-1], 12)
        
    # __setitem__
    def test_setitem(self):
        x = TimeSeries([1,2,3,4,5,6], [2,4,6,8,10,12])
        x[2] = 7
        self.assertEqual(x.value, [2,4,7,8,10,12])
        # Check that time is unchanged
        self.assertEqual(x.time, [1,2,3,4,5,6])
        
    #### __repr__ and __str__ ?
        
    # __iter__ 
    # Test iterating over TS with empty values
    def test_iter_empty(self):
        ts_empty = TimeSeries([], [])
        with self.assertRaises(StopIteration): 
            next(iter(ts_empty))
            
    # Test iterating over a TS with one value
    def test_iter_simple(self):
        ts_simple = TimeSeries([0], [1])
        ts_simple_iter = iter(ts_simple)
        self.assertEqual(ts_simple.value[0], next(ts_simple_iter))
        with self.assertRaises(StopIteration): 
            next(ts_simple_iter)
            
    # Test iterating over a TS with evenly spaced integer values
    # Check both the types of results and answers expected
    def test_iter_integer_spaced_1(self):
        ts = TimeSeries(range(1, 16), range(15))
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, int) for n in iter_list))
        
        # Check results
        self.assertEqual(ts.value, iter_list)
        
    def test_iter_integer_spaced_3(self):
        ts = TimeSeries(range(8), range(-5, 17, 3))
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, int) for n in iter_list))
        
        # Check results
        self.assertEqual(ts.value, iter_list)
        
    def test_iter_integer_spaced_7(self):
        ts = TimeSeries(range(715, 7), range(-14, 701, 7))
        
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
        ts = TimeSeries(range(4), ['1', '2', '5', '15'])
        
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
        ts = TimeSeries(range(3), [3.14159, 42., -0.207])
        
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
        ts = TimeSeries(range(5), [True, False, False, True, True])
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
        
        # Check type
        self.assertTrue(all(isinstance(n, bool) for n in iter_list))
        
        # Check results    
        self.assertEqual(ts.value, iter_list)
        
    # Test iterating over a TS with values of different types
    def test_iter_heterogeneous_values(self):
        ts = TimeSeries(range(5), [True, 3, 'hello', 0.07, ('cs', 207)])
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
            
        self.assertEqual(ts.value, iter_list)
        
    # Test iterating over TS with different sequence types for input
    def test_iter_string_input(self):
        ts = TimeSeries(range(14), '123456789abcde')
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
            
        self.assertEqual(ts.value, iter_list)
    
    def test_iter_tuple_input(self):
        ts = TimeSeries(range(5), (0, 3.1, 5.2, 100, 9.77))
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
            
        self.assertEqual(ts.value, iter_list)
        
    # itertimes
    # Test itertimes method over TS with empty values
    def test_itertimes_empty(self):
        ts_empty = TimeSeries([], [])
        with self.assertRaises(StopIteration): 
            next(ts_empty.itertimes())
            
    # Test itertimes method over a TS with one value
    def test_itertimes_simple(self):
        ts_simple = TimeSeries([0], [42])
        ts_simple_itertimes = ts_simple.itertimes()
        self.assertEqual(0, next(ts_simple_itertimes))
        with self.assertRaises(StopIteration): 
            next(ts_simple_itertimes)
            
    # Test iterating over a TS with integer times
    # Check both the types of results and answers expected
    def test_itertimes_integer(self):
        ts = TimeSeries([3, 4, 5, 6], [1, 5, 3, 6])
        
        iter_list = []
        for val in ts.itertimes():
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, int) for n in iter_list))
        
        # Check results
        self.assertEqual([3, 4, 5, 6], iter_list)
        
    # Test iterating over a TS with floating point times
    # Check both the types of results and answers expected
    def test_itertimes_float(self):
        ts = TimeSeries([0.1, 0.3, 0.6, 8.5], [1, 5, 3, 6])
        
        iter_list = []
        for val in ts.itertimes():
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, float) for n in iter_list))
        
        # Check results
        self.assertEqual([0.1, 0.3, 0.6, 8.5], iter_list)
        
    # iteritems
    # Test iteritems method over TS with empty values
    def test_iteritems_empty(self):
        ts_empty = TimeSeries([], [])
        with self.assertRaises(StopIteration): 
            next(ts_empty.iteritems())
            
    # Test itertimes method over a TS with one value
    def test_iteritems_simple(self):
        ts_simple = TimeSeries([1], [42])
        ts_simple_iteritems = ts_simple.iteritems()
        self.assertEqual((1, 42), next(ts_simple_iteritems))
        with self.assertRaises(StopIteration): 
            next(ts_simple_iteritems)
            
    # Test iterating over a TS with integer times and values
    # Check both the types of results and answers expected
    def test_iteritems_integer(self):
        ts = TimeSeries([15, 20, 25, 30], [1, 5, 3, 6])
        
        iter_list = []
        for val in ts.iteritems():
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, tuple) for n in iter_list))
        
        # Check results
        self.assertEqual([(15, 1), (20, 5), (25, 3), (30, 6)], iter_list)
        
    # Test iterating over a TS with float times and values
    # Check both the types of results and answers expected
    def test_iteritems_float(self):
        ts = TimeSeries([1.2, 1.21, 1.41, 1.7], [1.5, 5.2, 3.21, 6.3])
        
        iter_list = []
        for val in ts.iteritems():
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, tuple) for n in iter_list))
        
        # Check results
        self.assertEqual([(1.2, 1.5), (1.21, 5.2), (1.41, 3.21), (1.7, 6.3)], iter_list)
        
    # interpolate
    # Test interpolation method with empty input
    def test_interpolate_empty_input(self):
        a = TimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([])
        
        self.assertEqual(b.value, [])
        self.assertEqual(b.time, [])
        self.assertTrue(isinstance(b, TimeSeries))
        
    # Test interpolation method with single new time that is already in TS
    def test_interpolate_in_array_single(self):
        a = TimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([5])
        self.assertEqual(b.value, [2])
        self.assertEqual(b.time, [5])
        self.assertTrue(isinstance(b, TimeSeries))
        
    # Test interpolation method with multiple new times that are already in TS
    def test_interpolate_in_array_multiple(self):
        a = TimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([0, 5, 10])
        self.assertEqual(b.value, [1, 2, 3])
        self.assertEqual(b.time, [0, 5, 10])
        self.assertTrue(isinstance(b, TimeSeries))
        
    # Test interpolation for stationary boundary conditions
    def test_interpolate_stationary_min(self):
        a = TimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([-0.1])
        self.assertEqual(b.value, [1])
        self.assertEqual(b.time, [-0.1])
        self.assertTrue(isinstance(b, TimeSeries))
        
    def test_interpolate_stationary_max(self):
        a = TimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([15])
        self.assertEqual(b.value, [3])
        self.assertEqual(b.time, [15])
        self.assertTrue(isinstance(b, TimeSeries))
        
    def test_interpolate_stationary_min_max(self):
        a = TimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([-5, 42])
        self.assertEqual(b.value, [1, 3])
        self.assertEqual(b.time, [-5, 42])
        self.assertTrue(isinstance(b, TimeSeries))
                
    # Test interpolation method with simple cases provided in Week 3 handout
    def test_interpolate_simple_1(self):
        a = TimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([1])
        self.assertEqual(b.value, [1.2])
        self.assertEqual(b.time, [1])
        self.assertTrue(isinstance(b, TimeSeries))
        
    def test_interpolate_simple_2(self):
        a = TimeSeries([0, 5, 10], [1, 2, 3])
        b = TimeSeries([2.5, 7.5], [100, -100])
        c = a.interpolate(b.time)
        self.assertEqual(c.value, [1.5, 2.5])
        self.assertEqual(c.time, [2.5, 7.5])
        self.assertTrue(isinstance(c, TimeSeries))
        
    # Test interpolation with float values
    def test_interpolate_simple_2(self):
        a = TimeSeries([0.5, 3.2], [1.96, 3.14])
        b = a.interpolate([0.4, 2.0])
        self.assertEqual(b.value[0], 1.96)
        self.assertTrue(b.value[1] < 2.616 and b.value[1] > 2.615) # avoid roundoff ambiguities
        self.assertEqual(b.time, [0.4, 2.0])
        self.assertTrue(isinstance(b, TimeSeries))
        
    # Test interpolation method with mixture of cases above
    def test_interpolate_mixture(self):
        a = TimeSeries([3, 6, 7, 8, 15, 20], [0, 5, 2, 3, 10, -3])
        b = a.interpolate([0, 1, 6.5, 10, 22, 500])
        self.assertEqual(b.value, [0, 0, 3.5, 5, -3, -3])
        self.assertEqual(b.time, [0, 1, 6.5, 10, 22, 500])
        self.assertTrue(isinstance(b, TimeSeries))
    
    
if __name__ == '__main__':
    unittest.main()
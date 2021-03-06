from pytest import raises
import numpy as np
import math
import unittest
from TimeSeries import TimeSeries
from lazy import LazyOperation, lazy_add, lazy_mul, lazy

class TestTimeSeries(unittest.TestCase):
    
    # __init__
    # types of sequences
    def test_arg_type_range(self):
        self.assertEqual(TimeSeries(range(0,3), range(0,3))._value, [0,1,2])
        self.assertEqual(TimeSeries(range(0,3), range(0,3))._time, [0,1,2])
    
    def test_arg_type_tuple(self):
        self.assertEqual(TimeSeries(range(0,4), (1,42,3,10))._value, [1,42,3,10])
        self.assertEqual(TimeSeries(range(0,4), (1,42,3,10))._time, [0,1,2,3])
        
    # Faulty arguments
    # Times and Values have different lengths
    def test_invalid_array_lengths(self):
        with self.assertRaises(ValueError):
            x = TimeSeries([1, 2, 3], [4, 5])
            
    # Values non numeric
    def test_non_numeric_values(self):
        with self.assertRaises(TypeError):
            x = TimeSeries([1, 2, 3], ['hello', 'world', '!'])
        
    # Times non numeric
    def test_non_numeric_times(self):
        with self.assertRaises(TypeError):
            x = TimeSeries(['hello', 'world', '!'], [1, 2, 3])

    # Both times and values non numeric
    def test_non_numeric_data(self):
        with self.assertRaises(TypeError):
            x = TimeSeries(['hello'], ['world'])
            
    # Duplicate times present
    def test_non_distinct_times(self):
        with self.assertRaises(ValueError):
            x = TimeSeries([1.1, 1.1, 1.2], [3, 4, 5])       
        
    # Input data not of type sequence
    def test_non_sequence_data1(self):
        with self.assertRaises(TypeError):
            x = TimeSeries([3], 4)
            
    def test_non_sequence_data2(self):
        with self.assertRaises(TypeError):
            x = TimeSeries(53, (4))
        
    # number of arguments
    def test_omitted_arg(self):
        with self.assertRaises(TypeError):
            x = TimeSeries()
    
    
    def test_multiple_args(self):
        with self.assertRaises(TypeError):
            x = TimeSeries(1,2,3)
            
    # series length
    def test_no_data_value(self):
        self.assertEqual(TimeSeries([], [])._value, [])
        self.assertEqual(TimeSeries([], [])._time, [])

    def test_one_data_value(self):
        self.assertEqual(TimeSeries([5], [1])._value, [1])
        self.assertEqual(TimeSeries([5], [1])._time, [5])

    def test_multiple_data_values(self):
        self.assertEqual(TimeSeries([0,1,2], [1,2,3])._value, [1,2,3])
        self.assertEqual(TimeSeries([0,1,2], [1,2,3])._time, [0,1,2])
        
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
        self.assertEqual(x._value, [2,4,7,8,10,12])
        # Check that time is unchanged
        self.assertEqual(x._time, [1,2,3,4,5,6])

    # __contains__
    def test_contains_in_series(self):
        x = TimeSeries([1,2,3,4,5,6], [2,4,6,8,10,12])
        self.assertTrue(8 in x)

    def test_contains_not_in_series(self):
        x = TimeSeries([1,2,3,4,5,6], [2,4,6,8,10,12])
        self.assertFalse(42 in x)

    def test_contains_checks_only_values_not_times(self):
        x = TimeSeries([1,2,3,4,5,6], [2,4,6,8,10,12])
        self.assertFalse(1 in x)
        
 
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
        self.assertEqual(ts_simple._value[0], next(ts_simple_iter))
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
        self.assertEqual(ts._value, iter_list)
        
    def test_iter_integer_spaced_3(self):
        ts = TimeSeries(range(8), range(-5, 17, 3))
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, int) for n in iter_list))
        
        # Check results
        self.assertEqual(ts._value, iter_list)
        
        

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
        self.assertEqual(ts._value, iter_list)
        
 
    
    def test_iter_tuple_input(self):
        ts = TimeSeries(range(5), (0, 3.1, 5.2, 100, 9.77))
        
        iter_list = []
        for val in ts:
            iter_list.append(val)
            
        self.assertEqual(ts._value, iter_list)


    # values
    def test_values_empty(self):
        ts = TimeSeries([],[])
        x = np.array([])
        self.assertTrue(np.array_equal(ts.values(),x))

    def test_values_nonempty(self):
        ts = TimeSeries(range(5),(2,4,6,8,10))
        x = np.array([2,4,6,8,10])
        self.assertTrue(np.array_equal(ts.values(),x))

    def test_values_output_type(self):
        ts = TimeSeries(range(5),(2,4,6,8,10))
        x = np.array([])
        self.assertEqual(type(ts.values()),type(x))



    # itervalues
    def test_itervalues_empty(self):
        ts_empty = TimeSeries([],[])
        with self.assertRaises(StopIteration):
            next(ts_empty.itervalues())

    def test_itervalues_simple(self):
        ts_simple = TimeSeries([0],[42])
        ts_simple_itervalues = ts_simple.itervalues()
        self.assertEqual(42, next(ts_simple_itervalues))
        with self.assertRaises(StopIteration):
            next(ts_simple_itervalues)



    # times
    def test_times_empty(self):
        ts = TimeSeries([],[])
        x = np.array([])
        self.assertTrue(np.array_equal(ts.times(),x))

    def test_times_nonempty(self):
        ts = TimeSeries(range(5),(2,4,6,8,10))
        x = np.array([0,1,2,3,4])
        self.assertTrue(np.array_equal(ts.times(),x))

    def test_times_output_type(self):
        ts = TimeSeries(range(5),(2,4,6,8,10))
        x = np.array([])
        self.assertEqual(type(ts.times()),type(x))

        
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
    

    # items
    def test_items_empty(self):
        ts = TimeSeries([],[])
        self.assertEqual([], ts.items())

    def test_items_nonempty(self):
        ts = TimeSeries([1,2,3,4,5],[2,4,6,8,10])
        self.assertEqual([(1,2),(2,4),(3,6),(4,8),(5,10)],ts.items())


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
        
        self.assertEqual(b._value, [])
        self.assertEqual(b._time, [])
        self.assertTrue(isinstance(b, TimeSeries))
        
    # Test interpolation method with single new time that is already in TS
    def test_interpolate_in_array_single(self):
        a = TimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([5])
        self.assertEqual(b._value, [2])
        self.assertEqual(b._time, [5])
        self.assertTrue(isinstance(b, TimeSeries))
        
    # Test interpolation method with multiple new times that are already in TS
    def test_interpolate_in_array_multiple(self):
        a = TimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([0, 5, 10])
        self.assertEqual(b._value, [1, 2, 3])
        self.assertEqual(b._time, [0, 5, 10])
        self.assertTrue(isinstance(b, TimeSeries))
        
    # Test interpolation for stationary boundary conditions
    def test_interpolate_stationary_min(self):
        a = TimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([-0.1])
        self.assertEqual(b._value, [1])
        self.assertEqual(b._time, [-0.1])
        self.assertTrue(isinstance(b, TimeSeries))
        
    def test_interpolate_stationary_max(self):
        a = TimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([15])
        self.assertEqual(b._value, [3])
        self.assertEqual(b._time, [15])
        self.assertTrue(isinstance(b, TimeSeries))
        
    def test_interpolate_stationary_min_max(self):
        a = TimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([-5, 42])
        self.assertEqual(b._value, [1, 3])
        self.assertEqual(b._time, [-5, 42])
        self.assertTrue(isinstance(b, TimeSeries))
                
    # Test interpolation method with simple cases provided in Week 3 handout
    def test_interpolate_simple_1(self):
        a = TimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([1])
        self.assertEqual(b._value, [1.2])
        self.assertEqual(b._time, [1])
        self.assertTrue(isinstance(b, TimeSeries))
        
    def test_interpolate_simple_2(self):
        a = TimeSeries([0, 5, 10], [1, 2, 3])
        b = TimeSeries([2.5, 7.5], [100, -100])
        c = a.interpolate(b._time)
        self.assertEqual(c._value, [1.5, 2.5])
        self.assertEqual(c._time, [2.5, 7.5])
        self.assertTrue(isinstance(c, TimeSeries))
        
    # Test interpolation with float values
    def test_interpolate_simple_2(self):
        a = TimeSeries([0.5, 3.2], [1.96, 3.14])
        b = a.interpolate([0.4, 2.0])
        self.assertEqual(b._value[0], 1.96)
        self.assertTrue(b._value[1] < 2.616 and b._value[1] > 2.615) # avoid roundoff ambiguities
        self.assertEqual(b._time, [0.4, 2.0])
        self.assertTrue(isinstance(b, TimeSeries))
        
    # Test interpolation method with mixture of cases above
    def test_interpolate_mixture(self):
        a = TimeSeries([3, 6, 7, 8, 15, 20], [0, 5, 2, 3, 10, -3])
        b = a.interpolate([0, 1, 6.5, 10, 22, 500])
        self.assertEqual(b._value, [0, 0, 3.5, 5, -3, -3])
        self.assertEqual(b._time, [0, 1, 6.5, 10, 22, 500])
        self.assertTrue(isinstance(b, TimeSeries))
        
    @lazy
    def check_length(self, a,b):
        return len(a)==len(b)
    
    def test_lazy_length_check_with_normal_construction(self):
        thunk = self.check_length(TimeSeries(range(0,4),range(1,5)), TimeSeries(range(1,5),range(2,6)))
        self.assertTrue(thunk.eval() == True)

    def test_lazy_length_check_with_lazy_construction(self):
        thunk = self.check_length(TimeSeries(range(0,4),range(1,5)).lazy, TimeSeries(range(1,5),range(2,6)).lazy)
        self.assertTrue(thunk.eval() == True)
    
    def test_same_output_normal_v_lazy(self):
        x = TimeSeries([1,2,3,4],[1, 9, 4, 16])
        ans = x.lazy.eval()
        self.assertEqual(x._time,ans._time)
        self.assertEqual(x._value,ans._value)


    # __add__
    # test infix addition
    def test_add_valid_int(self):
        ts = TimeSeries(range(5),[1,2,3,4,5])
        ts2 = TimeSeries(range(5),[1,1,1,1,1])
        
        ans = ts+ts2
        real_ans = TimeSeries(range(5),[2,3,4,5,6])

        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)


    def test_add_unequal_times(self):
        ts = TimeSeries(range(5),[1,2,3,4,5])
        ts2 = TimeSeries(range(1,6),[1,1,1,1,1])
        with self.assertRaises(ValueError):
            result = ts+ts2

    def test_add_unequal_lengths(self):
        ts = TimeSeries(range(5),[1,2,3,4,5])
        ts2 = TimeSeries(range(8),[1,1,1,1,1,2,3,4])
        with self.assertRaises(ValueError):
            result = ts+ts2

    def test_add_positive_int(self):
        ts = TimeSeries(range(5),[1,2,3,4,5])
        ans = ts + 2
        real_ans = TimeSeries(range(5),[3,4,5,6,7])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)

    def test_add_negative_int(self):
        ts = TimeSeries(range(5),[1,2,3,4,5])
        ans = ts + (-2)
        real_ans = TimeSeries(range(5),[-1,0,1,2,3])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)

    def test_add_float(self):
        ts = TimeSeries(range(5),[1,2,3,4,5])
        ans = ts + 0.5
        real_ans = TimeSeries(range(5),[1.5,2.5,3.5,4.5,5.5])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)

    def test_add_lhs_int(self):
        ts = TimeSeries(range(5),[1,2,3,4,5])
        ans = 2+ts
        real_ans = TimeSeries(range(5),[3,4,5,6,7])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)

    # __sub__
    def test_sub_valid_int(self):
        ts = TimeSeries(range(3),[10,10,10])
        ts2 = TimeSeries(range(3),[1,2,3])

        ans = ts-ts2
        real_ans = TimeSeries(range(3),[9,8,7])

        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)

    def test_sub_unequal_times(self):
        ts = TimeSeries(range(5),[1,2,3,4,5])
        ts2 = TimeSeries(range(1,6),[1,1,1,1,1])
        with self.assertRaises(ValueError):
            result = ts-ts2

    def test_sub_unequal_lengths(self):
        ts = TimeSeries(range(5),[1,2,3,4,5])
        ts2 = TimeSeries(range(8),[1,1,1,1,1,2,3,4])
        with self.assertRaises(ValueError):
            result = ts-ts2

    def test_sub_int(self):
        ts = TimeSeries(range(5),[1,2,3,4,5])
        ans = ts-1
        real_ans = TimeSeries(range(5),[0,1,2,3,4])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)

    def test_sub_float(self):
        ts = TimeSeries(range(5),[1,2,3,4,5])
        ans = ts-0.5
        real_ans = TimeSeries(range(5),[0.5,1.5,2.5,3.5,4.5])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)

    def test_sub_int_lhs(self):
        ts = TimeSeries(range(5),[1,2,3,4,5])
        ans = 10-ts
        real_ans = TimeSeries(range(5),[9,8,7,6,5])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)


    # __eq__
    def test_eq_all_equal(self):
        ts = TimeSeries(range(3),[1,2,3])
        ts2 = TimeSeries(range(3),[1,2,3])
        real_ans = np.array([True,True,True])
        self.assertTrue(np.array_equal(ts==ts2,real_ans))
        

    def test_eq_all_unequal(self):
        ts = TimeSeries(range(3),[1,2,3])
        ts2 = TimeSeries(range(3),[4,5,6])
        real_ans = np.array([False,False,False])
        self.assertTrue(np.array_equal(ts==ts2,real_ans))

    def test_eq_mixed(self):
        ts = TimeSeries(range(3),[1,2,3])
        ts2 = TimeSeries(range(3),[1,5,3])
        real_ans = np.array([True,False,True])
        self.assertTrue(np.array_equal(ts==ts2,real_ans))

    def test_eq_unequal_times(self):
        ts = TimeSeries(range(5),[1,2,3,4,5])
        ts2 = TimeSeries(range(1,6),[1,1,1,1,1])
        with self.assertRaises(ValueError):
            ts == ts2

    def test_eq_unequal_lengths(self):
        ts = TimeSeries(range(5),[1,2,3,4,5])
        ts2 = TimeSeries(range(8),[1,1,1,1,1,2,3,4])
        with self.assertRaises(ValueError):
            ts == ts2

    # __mul__
    def test_mul_ints(self):
        ts = TimeSeries(range(3),[10,10,10])
        ts2 = TimeSeries(range(3),[1,2,3])
        ans = ts*ts2

        real_ans = TimeSeries(range(3),[10,20,30])

        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)

    def test_mul_unequal_times(self):
        ts = TimeSeries(range(5),[1,2,3,4,5])
        ts2 = TimeSeries(range(1,6),[1,1,1,1,1])
        with self.assertRaises(ValueError):
            ts * ts2

    def test_mul_unequal_lengths(self):
        ts = TimeSeries(range(5),[1,2,3,4,5])
        ts2 = TimeSeries(range(8),[1,1,1,1,1,2,3,4])
        with self.assertRaises(ValueError):
            ts * ts2

    def test_mul_int(self):
        ts = TimeSeries(range(3),[1,2,3])
        ans = ts*10
        real_ans = TimeSeries(range(3),[10,20,30])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)

    def test_mul_int_lhs(self):
        ts = TimeSeries(range(3),[1,2,3])
        ans = 10*ts
        real_ans = TimeSeries(range(3),[10,20,30])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)

    def test_mul_neg_int(self):
        ts = TimeSeries(range(3),[1,2,3])
        ans = -10*ts
        real_ans = TimeSeries(range(3),[-10,-20,-30])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)

    def test_mul_zero(self):
        ts = TimeSeries(range(3),[1,2,3])
        ans = ts*0
        real_ans = TimeSeries(range(3),[0,0,0])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)


    # __neg__
    def test_neg_positive_ints(self):
        ts = TimeSeries(range(3),[1,2,3])
        ans = -ts
        real_ans = TimeSeries(range(3),[-1,-2,-3])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)

    def test_neg_negative_ints(self):
        ts = TimeSeries(range(3),[-1,-2,-3])
        ans = -ts
        real_ans = TimeSeries(range(3),[1,2,3])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)

    def test_neg_mixed_ints(self):
        ts = TimeSeries(range(3),[1,-2,3])
        ans = -ts
        real_ans = TimeSeries(range(3),[-1,2,-3])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)


    # __pos__
    def test_pos_positive_ints(self):
        ts = TimeSeries(range(3),[1,2,3])
        ans = +ts
        real_ans = TimeSeries(range(3),[1,2,3])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)
        

    def test_pos_negative_ints(self):
        ts = TimeSeries(range(3),[-1,-2,-3])
        ans = +ts
        real_ans = TimeSeries(range(3),[-1,-2,-3])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)

    def test_pos_mixed_ints(self):
        ts = TimeSeries(range(3),[-1,2,-3])
        ans = +ts
        real_ans = TimeSeries(range(3),[-1,2,-3])
        self.assertEqual(ans._time,real_ans._time)
        self.assertEqual(ans._value,real_ans._value)


    # __abs__
    def test_abs_int_result(self):
        ts = TimeSeries(range(4),[1,1,1,1])
        self.assertEqual(abs(ts),2)

    def test_abs_nonint_result(self):
        ts = TimeSeries(range(3),[1,2,3])
        self.assertEqual(abs(ts),math.sqrt(1+4+9))

    # __bool__
    def test_bool_true(self):
        ts = TimeSeries(range(4),[1,1,1,1])
        self.assertTrue(abs(ts))

    def test_bool_false(self):
        ts = TimeSeries(range(1),[0])
        self.assertFalse(abs(ts))
    
    def test_bool_empty(self):
        ts = TimeSeries([],[])
        self.assertFalse(abs(ts))


    # test against numpy array input
    def test_numpy_array_value(self):
        with self.assertRaises(NotImplementedError):
            ts = TimeSeries(range(3),np.array([1,2,3]))

    def test_numpy_array_time(self):
        with self.assertRaises(NotImplementedError):
            ts = TimeSeries(np.array([1,2,3]),[4,5,6])
            
    # mean
    # test mean of single valued TS
    def test_mean_single_val(self):
        ts = TimeSeries([4], [42])
        self.assertEqual(ts.mean(), 42)
        
    # test mean for larger TS
    def test_mean_larger(self):
        ts = TimeSeries(range(20), range(20))
        self.assertEqual(ts.mean(), 9.5)
       

    # test mean for some chunk input
    def test_mean_chunk(self):
        ts = TimeSeries(range(20), range(20))
        self.assertEqual(ts.mean(chunk = 1), 0)
        self.assertEqual(ts.mean(chunk = 3), 1)
        self.assertEqual(ts.mean(chunk = 20), 9.5)
    
    # std
    # test std of single valued TS
    def test_std_single_val(self):
        ts = TimeSeries([4], [42])
        self.assertEqual(ts.std(), 0)
        
    # test std for equal valued TS
    def test_std_equal_val(self):
        ts = TimeSeries([4, 5, 6, 7, 8], [1, 1, 1, 1, 1])
        self.assertEqual(ts.std(), 0)
        
    # test std for larger TS
    def test_std_larger(self):
        ts = TimeSeries(range(20), range(20))
        self.assertEqual(ts.std(), np.std(np.array(range(20))))
        
    # test std for some chunk input
    def test_std_chunk(self):
        ts = TimeSeries(range(20), range(20))
        self.assertEqual(ts.std(chunk = 1), np.std(np.array([0])))
        self.assertEqual(ts.std(chunk = 3), np.std(np.array([0, 1, 2])))
        self.assertEqual(ts.std(chunk = 20), np.std(np.array(range(20))))

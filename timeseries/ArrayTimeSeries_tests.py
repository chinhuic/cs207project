
from pytest import raises
import numpy as np
import unittest
import math
from ArrayTimeSeries import ArrayTimeSeries
from lazy import LazyOperation, lazy_add, lazy_mul, lazy

class TestArrayTimeSeries(unittest.TestCase):
    
    # __init__
    # types of sequences
    def test_arg_type_range(self):
        self.assertTrue((ArrayTimeSeries(range(0,3), range(0,3))._value ==
                         np.array([0, 1, 2])).all())

    def test_arg_type_tuple(self):
        self.assertTrue((ArrayTimeSeries((0, 1, 2, 4), (1,42,3,10))._value ==
                         np.array([1,42,3,10])).all())
        
    # number of arguments
    def test_omitted_arg(self):
        with self.assertRaises(TypeError):
            x = ArrayTimeSeries()

    def test_multiple_args(self):
        with self.assertRaises(TypeError):
            x = ArrayTimeSeries(1,2,3)
        
    # non-distinct times
    def test_time_non_distinct(self):
        with self.assertRaises(ValueError):
            x = ArrayTimeSeries((1, 1, 2, 3), range(4))
            
    # times and values different length
    def test_time_value_different_length(self):
        with self.assertRaises(ValueError):
            x = ArrayTimeSeries((1, 1, 2, 3), range(5))
            
    # simple arguments
    def test_no_data_value(self):
        self.assertTrue((ArrayTimeSeries([], [])._value == np.array([])).all())
        self.assertTrue((ArrayTimeSeries([], [])._time == np.array([])).all())

    def test_one_data_value(self):
        self.assertTrue((ArrayTimeSeries([0], [1])._value == np.array([1])).all())
        self.assertTrue((ArrayTimeSeries([0], [1])._time == np.array([0])).all())

    def test_multiple_data_values(self):
        self.assertTrue((ArrayTimeSeries([0,1,2], [1,2,3])._value == np.array([1,2,3])).all())
        self.assertTrue((ArrayTimeSeries([0,1,2], [1,2,3])._time == np.array([0,1,2])).all())


    # __len__
    def test_length_zero(self):
        self.assertEqual(len(ArrayTimeSeries([],[])), 0)

    def test_length_nonzero(self):
        self.assertEqual(len(ArrayTimeSeries(range(3), [8,12,42])), 3)
    
    # __getitem__
    def test_getitem_index_in_series(self):
        x = ArrayTimeSeries(range(6), [2,4,6,8,10,12])
        self.assertEqual(x[3], 8)

    def test_getitem_large_index_outside_boundary(self):
        x = ArrayTimeSeries(range(6), [2,4,6,8,10,12])
        with self.assertRaises(IndexError):
            x[10]

    def test_getitem_negative_index(self):
        x = ArrayTimeSeries(range(6), [2,4,6,8,10,12])
        self.assertEqual(x[-1], 12)
        
    # __setitem__
    def test_setitem(self):
        x = ArrayTimeSeries(range(6), [2,4,6,8,10,12])
        x[2] = 7
        self.assertTrue((x._value == np.array([2,4,7,8,10,12])).all())
        self.assertTrue((x._time == np.array(range(6))).all())
        
    # __contains__
    def test_contains_in_series(self):
        x = ArrayTimeSeries([1,2,3,4,5,6], [2,4,6,8,10,12])
        self.assertTrue(8 in x)

    def test_contains_not_in_series(self):
        x = ArrayTimeSeries([1,2,3,4,5,6], [2,4,6,8,10,12])
        self.assertFalse(42 in x)

    def test_contains_checks_only_values_not_times(self):
        x = ArrayTimeSeries([1,2,3,4,5,6], [2,4,6,8,10,12])
        self.assertFalse(1 in x)

        
    # __iter__ 
    # Test iterating over ATS (ArrayTimeSeries) with empty values
    def test_iter_empty(self):
        ats_empty = ArrayTimeSeries([], [])
        with self.assertRaises(StopIteration): 
            next(iter(ats_empty))
            
    # Test iterating over ATS with one value
    def test_iter_simple(self):
        ats_simple = ArrayTimeSeries([0], [1])
        ats_simple_iter = iter(ats_simple)
        self.assertEqual(ats_simple._value[0], next(ats_simple_iter))
        with self.assertRaises(StopIteration): 
            next(ats_simple_iter)
            
    # Test iterating over ATS with evenly spaced integer values
    # Check both the types of results and answers expected
    def test_iter_integer_spaced_1(self):
        ats = ArrayTimeSeries(range(15), range(15))
        
        iter_list = []
        for val in ats:
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, np.integer) for n in iter_list))
        
        # Check results
        self.assertTrue((iter_list == ats._value).all())
        
    def test_iter_integer_spaced_3(self):
        ats = ArrayTimeSeries(range(-5, 17, 3), range(-5, 17, 3))
        
        iter_list = []
        for val in ats:
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, np.integer) for n in iter_list))
        
        # Check results
        self.assertTrue((iter_list == ats._value).all())
        
    def test_iter_integer_spaced_7(self):
        ats = ArrayTimeSeries(range(-14, 701, 7), range(-14, 701, 7))
        
        iter_list = []
        for val in ats:
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, np.integer) for n in iter_list))
        
        # Check results
        self.assertTrue((iter_list == ats._value).all())
        
    # Test iterating over a ATS with values of type float
    # Check both the types of results and answers expected
    def test_iter_float_values(self):
        ats = ArrayTimeSeries((0.01, 0.5, 5.3), (3.14159, 42., -0.207))
        
        iter_list = []
        for val in ats:
            iter_list.append(val)
        
        # Check type
        self.assertTrue(all(isinstance(n, np.float) for n in iter_list))
        
        # Check results
        self.assertTrue((iter_list == ats._value).all())
        
        
    # times
    def test_times_empty(self):
        ts = ArrayTimeSeries([],[])
        x = np.array([])
        self.assertTrue(np.array_equal(ts.times(),x))

    def test_times_nonempty(self):
        ts = ArrayTimeSeries(range(5),(2,4,6,8,10))
        x = np.array([0,1,2,3,4])
        self.assertTrue(np.array_equal(ts.times(),x))

    def test_times_output_type(self):
        ts = ArrayTimeSeries(range(5),(2,4,6,8,10))
        x = np.array([])
        self.assertEqual(type(ts.times()),type(x))
        
    # itervalues
    def test_itervalues_empty(self):
        ts_empty = ArrayTimeSeries([],[])
        with self.assertRaises(StopIteration):
            next(ts_empty.itervalues())

    def test_itervalues_simple(self):
        ts_simple = ArrayTimeSeries([0],[42])
        ts_simple_itervalues = ts_simple.itervalues()
        self.assertEqual(42, next(ts_simple_itervalues))
        with self.assertRaises(StopIteration):
            next(ts_simple_itervalues)
        
    # itertimes
    # Test itertimes method over ATS with empty values
    def test_itertimes_empty(self):
        ats_empty = ArrayTimeSeries([], [])
        with self.assertRaises(StopIteration): 
            next(ats_empty.itertimes())
            
    # Test itertimes method over ATS with one value
    def test_itertimes_simple(self):
        ats_simple = ArrayTimeSeries([3], [42])
        ats_simple_itertimes = ats_simple.itertimes()
        self.assertEqual(3, next(ats_simple_itertimes))
        with self.assertRaises(StopIteration): 
            next(ats_simple_itertimes)
            
    # Test iterating over ATS with integers
    # Check both the types of results and answers expected
    def test_itertimes_integer(self):
        ats = ArrayTimeSeries(range(4), [1, 5, 3, 6])
        
        iter_list = []
        for val in ats.itertimes():
            iter_list.append(val)
        
        # Check results
        self.assertEqual([0, 1, 2, 3], iter_list)

    # iteritems
    # Test iteritems method over ATS with empty values
    def test_iteritems_empty(self):
        ats_empty = ArrayTimeSeries([], [])
        with self.assertRaises(StopIteration): 
            next(ats_empty.iteritems())
            
    # Test itertimes method over ATS with one value
    def test_iteritems_simple(self):
        ats_simple = ArrayTimeSeries([3], [42])
        ats_simple_iteritems = ats_simple.iteritems()
        self.assertEqual((3, 42), next(ats_simple_iteritems))
        with self.assertRaises(StopIteration): 
            next(ats_simple_iteritems)
            
    # Test iterating over a ATS with integers
    # Check both the types of results and answers expected
    def test_iteritems_integer(self):
        ats = ArrayTimeSeries(range(4), [1, 5, 3, 6])
        
        iter_list = []
        for val in ats.iteritems():
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, tuple) for n in iter_list))
        
        # Check results
        self.assertEqual([(0, 1), (1, 5), (2, 3), (3, 6)], iter_list)
        
        
    # items
    def test_items_empty(self):
        ts = ArrayTimeSeries([],[])
        self.assertEqual([], ts.items())

    def test_items_nonempty(self):
        ts = ArrayTimeSeries([1,2,3,4,5],[2,4,6,8,10])
        self.assertEqual([(1,2),(2,4),(3,6),(4,8),(5,10)],ts.items())

    def test_items_string(self):
        ts = ArrayTimeSeries(range(3),'abc')
        self.assertEqual([(0,'a'), (1,'b'), (2,'c')],ts.items())

    def test_items_output_type(self):
        ts = ArrayTimeSeries(range(3),'abc')
        self.assertEqual(type(ts.items()), list)
        
    # interpolate
    # Test interpolation method with empty input
    def test_interpolate_empty_input(self):
        a = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([])
        
        self.assertTrue(np.array_equal(b._value, np.array([])))
        self.assertTrue(np.array_equal(b._time, np.array([])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
        
    # Test interpolation method with single new time that is already in TS
    def test_interpolate_in_array_single(self):
        a = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([5])
        self.assertTrue(np.array_equal(b._value, np.array([2])))
        self.assertTrue(np.array_equal(b._time, np.array([5])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
        
    # Test interpolation method with multiple new times that are already in TS
    def test_interpolate_in_array_multiple(self):
        a = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([0, 5, 10])
        self.assertTrue(np.array_equal(b._value, np.array([1, 2, 3])))
        self.assertTrue(np.array_equal(b._time, np.array([0, 5, 10])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
    
    # Test interpolation for stationary boundary conditions
    def test_interpolate_stationary_min(self):
        a = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([-0.1])
        self.assertTrue(np.array_equal(b._value, np.array([1])))
        self.assertTrue(np.array_equal(b._time, np.array([-0.1])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
        
    def test_interpolate_stationary_max(self):
        a = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([15])
        self.assertTrue(np.array_equal(b._value, np.array([3])))
        self.assertTrue(np.array_equal(b._time, np.array([15])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
        
    def test_interpolate_stationary_min_max(self):
        a = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([-5, 42])
        self.assertTrue(np.array_equal(b._value, np.array([1, 3])))
        self.assertTrue(np.array_equal(b._time, np.array([-5, 42])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
    
    # Test interpolation method with simple cases provided in Week 3 handout
    def test_interpolate_simple_1(self):
        a = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([1])
        self.assertTrue(np.array_equal(b._value, np.array([1.2])))
        self.assertTrue(np.array_equal(b._time, np.array([1])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
        
    def test_interpolate_simple_2(self):
        a = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        b = ArrayTimeSeries([2.5, 7.5], [100, -100])
        c = a.interpolate(b.time)
        self.assertTrue(np.array_equal(b._value, np.array([1.5, 2.5])))
        self.assertTrue(np.array_equal(b._time, np.array([2.5, 7.5])))
        self.assertTrue(isinstance(c, ArrayTimeSeries))
        
    # Test interpolation with float values
    def test_interpolate_simple_2(self):
        a = ArrayTimeSeries([0.5, 3.2], [1.96, 3.14])
        b = a.interpolate([0.4, 2.0])
        self.assertEqual(b._value[0], 1.96)
        self.assertTrue(b._value[1] < 2.616 and b._value[1] > 2.615) # avoid roundoff ambiguities
        self.assertTrue(np.array_equal(b._time, np.array([0.4, 2.0])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
        
    # Test interpolation method with mixture of cases above
    def test_interpolate_mixture(self):
        a = ArrayTimeSeries([3, 6, 7, 8, 15, 20], [0, 5, 2, 3, 10, -3])
        b = a.interpolate([0, 1, 6.5, 10, 22, 500])
        self.assertTrue(np.array_equal(b._value, np.array([0, 0, 3.5, 5, -3, -3])))
        self.assertTrue(np.array_equal(b._time, np.array([0, 1, 6.5, 10, 22, 500])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
        
    @lazy
    def check_length(self, a,b):
        return len(a)==len(b)
    
    def test_lazy_length_check_with_normal_construction(self):
        thunk = self.check_length(ArrayTimeSeries(range(0,4),range(1,5)), 
                                  ArrayTimeSeries(range(1,5),range(2,6)))
        self.assertTrue(thunk.eval() == True)

    def test_lazy_length_check_with_lazy_construction(self):
        thunk = self.check_length(ArrayTimeSeries(range(0,4),range(1,5)).lazy, 
                                  ArrayTimeSeries(range(1,5),range(2,6)).lazy)
        self.assertTrue(thunk.eval() == True)
    
    # __add__
    # test infix addition
    def test_add_valid_int(self):
        ts = ArrayTimeSeries(range(5),[1,2,3,4,5])
        ts2 = ArrayTimeSeries(range(5),[1,1,1,1,1])
        
        ans = ts+ts2
        real_ans = ArrayTimeSeries(range(5),[2,3,4,5,6])
        self.assertTrue(np.array_equal(real_ans._value, ans._value))
        self.assertTrue(np.array_equal(real_ans._time, ans._time))


    def test_add_unequal_times(self):
        ts = ArrayTimeSeries(range(5),[1,2,3,4,5])
        ts2 = ArrayTimeSeries(range(1,6),[1,1,1,1,1])
        with self.assertRaises(ValueError):
            result = ts+ts2

    def test_add_unequal_lengths(self):
        ts = ArrayTimeSeries(range(5),[1,2,3,4,5])
        ts2 = ArrayTimeSeries(range(6),[1,1,1,1,1,2])
        with self.assertRaises(ValueError):
            result = ts+ts2
            
    def test_add_positive_int(self):
        ts = ArrayTimeSeries(range(5),[1,2,3,4,5])
        ans = ts + 2
        real_ans = ArrayTimeSeries(range(5),[3,4,5,6,7])
        self.assertTrue(np.array_equal(real_ans._value, ans._value))
        self.assertTrue(np.array_equal(real_ans._time, ans._time))

    def test_add_negative_int(self):
        ts = ArrayTimeSeries(range(5),[1,2,3,4,5])
        ans = ts + (-2)
        real_ans = ArrayTimeSeries(range(5),[-1,0,1,2,3])
        self.assertTrue(np.array_equal(real_ans._value, ans._value))
        self.assertTrue(np.array_equal(real_ans._time, ans._time))

    def test_add_float(self):
        ts = ArrayTimeSeries(range(5),[1,2,3,4,5])
        ans = ts + 0.5
        real_ans = ArrayTimeSeries(range(5),[1.5,2.5,3.5,4.5,5.5])
        self.assertTrue(np.array_equal(real_ans._value, ans._value))
        self.assertTrue(np.array_equal(real_ans._time, ans._time))

    def test_add_lhs_int(self):
        ts = ArrayTimeSeries(range(5),[1,2,3,4,5])
        ans = 2+ts
        real_ans = ArrayTimeSeries(range(5),[3,4,5,6,7])
        self.assertTrue(np.array_equal(real_ans._value, ans._value))
        self.assertTrue(np.array_equal(real_ans._time, ans._time))

    # __sub__
    def test_sub_valid_int(self):
        ts = ArrayTimeSeries(range(3),[10,10,10])
        ts2 = ArrayTimeSeries(range(3),[1,2,3])

        ans = ts-ts2
        real_ans = ArrayTimeSeries(range(3),[9,8,7])
        self.assertTrue(np.array_equal(real_ans._value, ans._value))
        self.assertTrue(np.array_equal(real_ans._time, ans._time))


    def test_sub_unequal_times(self):
        ts = ArrayTimeSeries(range(5),[1,2,3,4,5])
        ts2 = ArrayTimeSeries(range(1,6),[1,1,1,1,1])
        with self.assertRaises(ValueError):
            result = ts-ts2

    def test_sub_unequal_lengths(self):
        ts = ArrayTimeSeries(range(5),[1,2,3,4,5])
        ts2 = ArrayTimeSeries(range(8),[1,1,1,1,1,2,3,4])
        with self.assertRaises(ValueError):
            result = ts-ts2

    def test_sub_int(self):
        ts = ArrayTimeSeries(range(5),[1,2,3,4,5])
        ans = ts-1
        real_ans = ArrayTimeSeries(range(5),[0,1,2,3,4])
        self.assertTrue(np.array_equal(real_ans._value, ans._value))
        self.assertTrue(np.array_equal(real_ans._time, ans._time))
        
    def test_sub_float(self):
        ts = ArrayTimeSeries(range(5),[1,2,3,4,5])
        ans = ts-0.5
        real_ans = ArrayTimeSeries(range(5),[0.5,1.5,2.5,3.5,4.5])
        self.assertTrue(np.array_equal(real_ans._value, ans._value))
        self.assertTrue(np.array_equal(real_ans._time, ans._time))

    def test_sub_int_lhs(self):
        ts = ArrayTimeSeries(range(5),[1,2,3,4,5])
        ans = 10-ts
        real_ans = ArrayTimeSeries(range(5),[9,8,7,6,5])
        self.assertTrue(np.array_equal(real_ans._value, ans._value))
        self.assertTrue(np.array_equal(real_ans._time, ans._time))
        
    # __eq__
    def test_eq_all_equal(self):
        ts = ArrayTimeSeries(range(3),[1,2,3])
        ts2 = ArrayTimeSeries(range(3),[1,2,3])
        real_ans = np.array([True,True,True])
        self.assertTrue(np.array_equal(ts==ts2,real_ans))
        

    def test_eq_all_unequal(self):
        ts = ArrayTimeSeries(range(3),[1,2,3])
        ts2 = ArrayTimeSeries(range(3),[4,5,6])
        real_ans = np.array([False,False,False])
        self.assertTrue(np.array_equal(ts==ts2,real_ans))

    def test_eq_mixed(self):
        ts = ArrayTimeSeries(range(3),[1,2,3])
        ts2 = ArrayTimeSeries(range(3),[1,5,3])
        real_ans = np.array([True,False,True])
        self.assertTrue(np.array_equal(ts==ts2,real_ans))

    def test_eq_unequal_times(self):
        ts = ArrayTimeSeries(range(5),[1,2,3,4,5])
        ts2 = ArrayTimeSeries(range(1,6),[1,1,1,1,1])
        with self.assertRaises(ValueError):
            ts == ts2

    def test_eq_unequal_lengths(self):
        ts = ArrayTimeSeries(range(5),[1,2,3,4,5])
        ts2 = ArrayTimeSeries(range(8),[1,1,1,1,1,2,3,4])
        with self.assertRaises(ValueError):
            ts == ts2

    # __mul__
    def test_mul_ints(self):
        ts = ArrayTimeSeries(range(3),[10,10,10])
        ts2 = ArrayTimeSeries(range(3),[1,2,3])
        ans = ts*ts2

        real_ans = ArrayTimeSeries(range(3),[10,20,30])

        self.assertTrue(np.array_equal(real_ans._value, ans._value))
        self.assertTrue(np.array_equal(real_ans._time, ans._time))

    def test_mul_unequal_times(self):
        ts = ArrayTimeSeries(range(5),[1,2,3,4,5])
        ts2 = ArrayTimeSeries(range(1,6),[1,1,1,1,1])
        with self.assertRaises(ValueError):
            ts * ts2

    def test_mul_unequal_lengths(self):
        ts = ArrayTimeSeries(range(5),[1,2,3,4,5])
        ts2 = ArrayTimeSeries(range(8),[1,1,1,1,1,2,3,4])
        with self.assertRaises(ValueError):
            ts * ts2

    def test_mul_int(self):
        ts = ArrayTimeSeries(range(3),[1,2,3])
        ans = ts*10
        real_ans = ArrayTimeSeries(range(3),[10,20,30])
        self.assertTrue(np.array_equal(real_ans._value, ans._value))
        self.assertTrue(np.array_equal(real_ans._time, ans._time))

    def test_mul_int_lhs(self):
        ts = ArrayTimeSeries(range(3),[1,2,3])
        ans = 10*ts
        real_ans = ArrayTimeSeries(range(3),[10,20,30])
        self.assertTrue(np.array_equal(real_ans._value, ans._value))
        self.assertTrue(np.array_equal(real_ans._time, ans._time))

    def test_mul_neg_int(self):
        ts = ArrayTimeSeries(range(3),[1,2,3])
        ans = -10*ts
        real_ans = ArrayTimeSeries(range(3),[-10,-20,-30])
        self.assertTrue(np.array_equal(real_ans._value, ans._value))
        self.assertTrue(np.array_equal(real_ans._time, ans._time))

    def test_mul_zero(self):
        ts = ArrayTimeSeries(range(3),[1,2,3])
        ans = ts*0
        real_ans = ArrayTimeSeries(range(3),[0,0,0])
        self.assertTrue(np.array_equal(real_ans._value, ans._value))
        self.assertTrue(np.array_equal(real_ans._time, ans._time))
        
    # __abs__
    def test_abs_int_result(self):
        ts = ArrayTimeSeries(range(4),[1,1,1,1])
        self.assertEqual(abs(ts),2)

    def test_abs_nonint_result(self):
        ts = ArrayTimeSeries(range(3),[1,2,3])
        self.assertEqual(abs(ts),math.sqrt(1+4+9))

    # __bool__
    def test_bool_true(self):
        ts = ArrayTimeSeries(range(4),[1,1,1,1])
        self.assertTrue(abs(ts))

    def test_bool_false(self):
        ts = ArrayTimeSeries(range(1),[0])
        self.assertFalse(abs(ts))
    
    def test_bool_empty(self):
        ts = ArrayTimeSeries([],[])
        self.assertFalse(abs(ts))

        
if __name__ == '__main__':
    unittest.main()
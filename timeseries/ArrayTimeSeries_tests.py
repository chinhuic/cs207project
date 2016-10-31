from pytest import raises
import numpy as np
import unittest
from ArrayTimeSeries import ArrayTimeSeries
from lazy import LazyOperation, lazy_add, lazy_mul, lazy

class TestArrayTimeSeries(unittest.TestCase):
    
    # __init__
    # types of sequences
    def test_arg_type_range(self):
        self.assertTrue((ArrayTimeSeries(range(0,3), range(0,3)).value ==
                         np.array([0, 1, 2])).all())

    def test_arg_type_tuple(self):
        self.assertTrue((ArrayTimeSeries((0, 1, 2, 4), (1,42,3,10)).value ==
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
        self.assertTrue((ArrayTimeSeries([], []).value == np.array([])).all())
        self.assertTrue((ArrayTimeSeries([], []).time == np.array([])).all())

    def test_one_data_value(self):
        self.assertTrue((ArrayTimeSeries([0], [1]).value == np.array([1])).all())
        self.assertTrue((ArrayTimeSeries([0], [1]).time == np.array([0])).all())

    def test_multiple_data_values(self):
        self.assertTrue((ArrayTimeSeries([0,1,2], [1,2,3]).value == np.array([1,2,3])).all())
        self.assertTrue((ArrayTimeSeries([0,1,2], [1,2,3]).time == np.array([0,1,2])).all())


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
        self.assertTrue((x.value == np.array([2,4,7,8,10,12])).all())
        self.assertTrue((x.time == np.array(range(6))).all())
        
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
        self.assertEqual(ats_simple.value[0], next(ats_simple_iter))
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
        self.assertTrue((iter_list == ats.value).all())
        
    def test_iter_integer_spaced_3(self):
        ats = ArrayTimeSeries(range(-5, 17, 3), range(-5, 17, 3))
        
        iter_list = []
        for val in ats:
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, np.integer) for n in iter_list))
        
        # Check results
        self.assertTrue((iter_list == ats.value).all())
        
    def test_iter_integer_spaced_7(self):
        ats = ArrayTimeSeries(range(-14, 701, 7), range(-14, 701, 7))
        
        iter_list = []
        for val in ats:
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, np.integer) for n in iter_list))
        
        # Check results
        self.assertTrue((iter_list == ats.value).all())
        
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
        self.assertTrue((iter_list == ats.value).all())
        
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
        
    # interpolate
    # Test interpolation method with empty input
    def test_interpolate_empty_input(self):
        a = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([])
        
        self.assertTrue(np.array_equal(b.value, np.array([])))
        self.assertTrue(np.array_equal(b.time, np.array([])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
        
    # Test interpolation method with single new time that is already in TS
    def test_interpolate_in_array_single(self):
        a = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([5])
        self.assertTrue(np.array_equal(b.value, np.array([2])))
        self.assertTrue(np.array_equal(b.time, np.array([5])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
        
    # Test interpolation method with multiple new times that are already in TS
    def test_interpolate_in_array_multiple(self):
        a = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([0, 5, 10])
        self.assertTrue(np.array_equal(b.value, np.array([1, 2, 3])))
        self.assertTrue(np.array_equal(b.time, np.array([0, 5, 10])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
    
    # Test interpolation for stationary boundary conditions
    def test_interpolate_stationary_min(self):
        a = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([-0.1])
        self.assertTrue(np.array_equal(b.value, np.array([1])))
        self.assertTrue(np.array_equal(b.time, np.array([-0.1])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
        
    def test_interpolate_stationary_max(self):
        a = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([15])
        self.assertTrue(np.array_equal(b.value, np.array([3])))
        self.assertTrue(np.array_equal(b.time, np.array([15])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
        
    def test_interpolate_stationary_min_max(self):
        a = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([-5, 42])
        self.assertTrue(np.array_equal(b.value, np.array([1, 3])))
        self.assertTrue(np.array_equal(b.time, np.array([-5, 42])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
    
    # Test interpolation method with simple cases provided in Week 3 handout
    def test_interpolate_simple_1(self):
        a = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        b = a.interpolate([1])
        self.assertTrue(np.array_equal(b.value, np.array([1.2])))
        self.assertTrue(np.array_equal(b.time, np.array([1])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
        
    def test_interpolate_simple_2(self):
        a = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        b = ArrayTimeSeries([2.5, 7.5], [100, -100])
        c = a.interpolate(b.time)
        self.assertTrue(np.array_equal(b.value, np.array([1.5, 2.5])))
        self.assertTrue(np.array_equal(b.time, np.array([2.5, 7.5])))
        self.assertTrue(isinstance(c, ArrayTimeSeries))
        
    # Test interpolation with float values
    def test_interpolate_simple_2(self):
        a = ArrayTimeSeries([0.5, 3.2], [1.96, 3.14])
        b = a.interpolate([0.4, 2.0])
        self.assertEqual(b.value[0], 1.96)
        self.assertTrue(b.value[1] < 2.616 and b.value[1] > 2.615) # avoid roundoff ambiguities
        self.assertTrue(np.array_equal(b.time, np.array([0.4, 2.0])))
        self.assertTrue(isinstance(b, ArrayTimeSeries))
        
    # Test interpolation method with mixture of cases above
    def test_interpolate_mixture(self):
        a = ArrayTimeSeries([3, 6, 7, 8, 15, 20], [0, 5, 2, 3, 10, -3])
        b = a.interpolate([0, 1, 6.5, 10, 22, 500])
        self.assertTrue(np.array_equal(b.value, np.array([0, 0, 3.5, 5, -3, -3])))
        self.assertTrue(np.array_equal(b.time, np.array([0, 1, 6.5, 10, 22, 500])))
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
    
    def test_same_output_normal_v_lazy(self):
        x = ArrayTimeSeries([1,2,3,4],[1, 9, 4, 16])
        self.assertEqual(x, x.lazy.eval())
   
        
if __name__ == '__main__':
    unittest.main()
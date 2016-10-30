
from pytest import raises
import numpy as np
import unittest
from ArrayTimeSeries import ArrayTimeSeries

class TestArrayTimeSeries(unittest.TestCase):
    
    # __init__
    # types of sequences
    def test_arg_type_range(self):
        self.assertTrue((ArrayTimeSeries(range(0,3)).value ==
                         np.array([0, 1, 2])).all())

    def test_arg_type_string(self):
        self.assertTrue((ArrayTimeSeries('time').value ==
                         np.array(['t','i','m','e'])).all())

    def test_arg_type_tuple(self):
        self.assertTrue((ArrayTimeSeries((1,42,3,10)).value ==
                         np.array([1,42,3,10])).all())
        
    

    def test_arg_type_list_of_tuples(self):
        self.assertTrue((ArrayTimeSeries([(1,2),(3,4),(5,6)]).value ==
                         np.array([(1,2),(3,4),(5,6)])).all())
        
    # number of arguments
    def test_omitted_arg(self):
        with self.assertRaises(TypeError):
            x = ArrayTimeSeries()

    def test_multiple_args(self):
        with self.assertRaises(TypeError):
            x = ArrayTimeSeries(1,2,3)

    # simple arguments
    def test_no_data_value(self):
        self.assertTrue((ArrayTimeSeries([]).value == np.array([])).all())

    def test_one_data_value(self):
        self.assertTrue((ArrayTimeSeries([1]).value == np.array([1])).all())

    def test_multiple_data_values(self):
        self.assertTrue((ArrayTimeSeries([1,2,3]).value == np.array([1,2,3])).all())


    # __len__

    def test_length_zero(self):
        self.assertEqual(len(ArrayTimeSeries([])), 0)

    def test_length_nonzero(self):
        self.assertEqual(len(ArrayTimeSeries([8,12,42])), 3)



    # __getitem__

    def test_getitem_index_in_series(self):
        x = ArrayTimeSeries([2,4,6,8,10,12])
        self.assertEqual(x[3], 8)

    def test_getitem_large_index_outside_boundary(self):
        x = ArrayTimeSeries([2,4,6,8,10,12])
        with self.assertRaises(IndexError):
            x[10]

    def test_getitem_negative_index(self):
        x = ArrayTimeSeries([2,4,6,8,10,12])
        self.assertEqual(x[-1], 12)




    # __setitem__
    def test_setitem(self):
        x = ArrayTimeSeries([2,4,6,8,10,12])
        x[2] = 7
        self.assertTrue((x.value == np.array([2,4,7,8,10,12])).all())
    
    # __iter__ 
    # Test iterating over ATS (ArrayTimeSeries) with empty values
    def test_iter_empty(self):
        ats_empty = ArrayTimeSeries([])
        with self.assertRaises(StopIteration): 
            next(iter(ats_empty))
            
    # Test iterating over ATS with one value
    def test_iter_simple(self):
        ats_simple = ArrayTimeSeries([1])
        ats_simple_iter = iter(ats_simple)
        self.assertEqual(ats_simple.value[0], next(ats_simple_iter))
        with self.assertRaises(StopIteration): 
            next(ats_simple_iter)
            
    # Test iterating over ATS with evenly spaced integer values
    # Check both the types of results and answers expected
    def test_iter_integer_spaced_1(self):
        ats = ArrayTimeSeries(range(15))
        
        iter_list = []
        for val in ats:
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, np.integer) for n in iter_list))
        
        # Check results
        self.assertTrue((iter_list == ats.value).all())
        
    def test_iter_integer_spaced_3(self):
        ats = ArrayTimeSeries(range(-5, 17, 3))
        
        iter_list = []
        for val in ats:
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, np.integer) for n in iter_list))
        
        # Check results
        self.assertTrue((iter_list == ats.value).all())
        
    def test_iter_integer_spaced_7(self):
        ats = ArrayTimeSeries(range(-14, 701, 7))
        
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
        ats = ArrayTimeSeries((3.14159, 42., -0.207))
        
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
        ats_empty = ArrayTimeSeries([])
        with self.assertRaises(StopIteration): 
            next(ats_empty.itertimes())
            
    # Test itertimes method over ATS with one value
    def test_itertimes_simple(self):
        ats_simple = ArrayTimeSeries([42])
        ats_simple_itertimes = ats_simple.itertimes()
        self.assertEqual(0, next(ats_simple_itertimes))
        with self.assertRaises(StopIteration): 
            next(ats_simple_itertimes)
            
    # Test iterating over ATS with integers
    # Check both the types of results and answers expected
    def test_itertimes_integer(self):
        ats = ArrayTimeSeries([1, 5, 3, 6])
        
        iter_list = []
        for val in ats.itertimes():
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, int) for n in iter_list))
        
        # Check results
        self.assertEqual([0, 1, 2, 3], iter_list)

    # iteritems
    # Test iteritems method over ATS with empty values
    def test_iteritems_empty(self):
        ats_empty = ArrayTimeSeries([])
        with self.assertRaises(StopIteration): 
            next(ats_empty.iteritems())
            
    # Test itertimes method over ATS with one value
    def test_iteritems_simple(self):
        ats_simple = ArrayTimeSeries([42])
        ats_simple_iteritems = ats_simple.iteritems()
        self.assertEqual((0, 42), next(ats_simple_iteritems))
        with self.assertRaises(StopIteration): 
            next(ats_simple_iteritems)
            
    # Test iterating over a ATS with integers
    # Check both the types of results and answers expected
    def test_iteritems_integer(self):
        ats = ArrayTimeSeries([1, 5, 3, 6])
        
        iter_list = []
        for val in ats.iteritems():
            iter_list.append(val)
            
        # Check type
        self.assertTrue(all(isinstance(n, tuple) for n in iter_list))
        
        # Check results
        self.assertEqual([(0, 1), (1, 5), (2, 3), (3, 6)], iter_list)
        
if __name__ == '__main__':
    unittest.main()
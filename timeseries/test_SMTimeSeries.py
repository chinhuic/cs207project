from pytest import raises
import numpy as np
import math
import shutil
from ArrayTimeSeries import ArrayTimeSeries
from SMTimeSeries import SMTimeSeries
from FileStorageManager import FSM_global
from lazy import LazyOperation, lazy_add, lazy_mul, lazy

# NOTE: We use pytest here instead of our typical unittest, since we had 
#       difficulty using the latter to delete test data after running tests

    
# __init__

def test_str_id():
    # Store some time series data
    t1 = SMTimeSeries([1, 2, 3], [4, 5, 6], 'hi')
    t2 = SMTimeSeries([0], [0], 'bye')
    
    assert t1._id == 'hi'
    assert t2._id == 'bye'
    
    assert((np.array([4, 5, 6]) == FSM_global.get('hi').values()).all())
    assert((np.array([0]) == FSM_global.get('bye').values()).all())

    
def test_int_id():
    # Store some time series data
    t1 = SMTimeSeries([1, 2, 3], [4, 5, 6], 1)
    t2 = SMTimeSeries([0], [0], 2)
    
    assert t1._id == '1'
    assert t2._id == '2'
    
    assert((np.array([4, 5, 6]) == FSM_global.get(1).values()).all())
    assert((np.array([0]) == FSM_global.get(2).values()).all())
    
           

def test_no_id():
    t1 = SMTimeSeries([10, 20], [3, 4])
    
    t1_stored = FSM_global.get(t1._id)
    
    assert((t1.values() == t1_stored.values()).all())
    assert((t1.times() == t1_stored.times()).all())
    
    
def test_time_value_diff_length():
    with raises(ValueError):
        SMTimeSeries([1, 2, 3], [1, 2])
        
def test_time_input_numeric():
    with raises(TypeError):
        SMTimeSeries(['a', 'b'], [1, 2])
        
def test_value_input_numeric():
    with raises(TypeError):
        SMTimeSeries([1, 2], ['a', 'b'])
        
def test_time_input_sequence():
    with raises(TypeError):
        SMTimeSeries(12, [1, 2])
        
def test_value_input_sequence():
    with raises(TypeError):
        SMTimeSeries([1, 2], 12)


# __from_db__

def test_from_db():
    t1 = SMTimeSeries([1, 2, 3], [1, 2, 3], 3)
    
    t_from_db = t1.from_db('hi')
    assert((np.array([4, 5, 6]) == t_from_db.values()).all())
    
def test_from_db_no_id():
    t1 = SMTimeSeries([1, 2, 3], [1, 2, 3], 3)
    
    with raises(KeyError):
        t1.from_db('hey')
        
# __len__
def test_len():
    t1 = SMTimeSeries([1, 2, 3], [1, 2, 3], 3)
    
    assert(len(t1) == 3)
    
def test_len_empty():
    t1 = SMTimeSeries([], [], 3)
    
    assert(len(t1) == 0)

# interpolate
def test_interpolate():
    a = SMTimeSeries([0, 5, 10], [1, 2, 3], 4)
    b = a.interpolate([])
    
    assert(np.array_equal(FSM_global.get(b._id).values(), np.array([])))
    assert(np.array_equal(FSM_global.get(b._id).times(), np.array([])))
    
    
def test_interpolate_2():
    a = SMTimeSeries([0, 5, 10], [1, 2, 3], 4)
    b = a.interpolate([0, 5, 10])

    assert(np.array_equal(FSM_global.get(b._id).values(),  np.array([1, 2, 3])))
    assert(np.array_equal(FSM_global.get(b._id).times(),  np.array([0, 5, 10])))

# __iter__
def test_iter_1():
    t = SMTimeSeries([], [], 5)
    with raises(StopIteration): 
        next(iter(t))
    
def test_iter_2():
    t = SMTimeSeries(range(-14, 701, 7), range(-14, 701, 7))
        
    iter_list = []
    for val in t:
        iter_list.append(val)
            
    assert((iter_list == t.values()).all())
    
# itervalues
def test_itervalues():
    t = SMTimeSeries(range(4), [1, 5, 3, 6])
        
    iter_list = []
    for val in t.values():
        iter_list.append(val)
        
    # Check results
    assert([1, 5, 3, 6] == iter_list)


# itertimes
def test_itertimes():
    t = SMTimeSeries(range(4), [1, 5, 3, 6])
        
    iter_list = []
    for val in t.times():
        iter_list.append(val)
        
    # Check results
    assert([0, 1, 2, 3] == iter_list)
    
# iteritems
def test_iteritems():
    t = SMTimeSeries(range(4), [1, 5, 3, 6])
        
    iter_list = []
    for val in t.iteritems():
        iter_list.append(val)
            
    assert([(0, 1), (1, 5), (2, 3), (3, 6)] == iter_list)
    
    
# __getitem__
def test_getitem_index_in_series():
    t = SMTimeSeries(range(6), [2,4,6,8,10,12])
    assert(t[3] == 8)

def test_getitem_large_index_outside_boundary():
    t = SMTimeSeries(range(6), [2,4,6,8,10,12])
    with raises(IndexError):
        t[10]

def test_getitem_negative_index():
    t = SMTimeSeries(range(6), [2,4,6,8,10,12])
    assert(t[-1] == 12)
    
    
# __setitem__
def test_setitem():
    t = SMTimeSeries(range(6), [2,4,6,8,10,12])
    t[2] = 7
    assert((t.values() == np.array([2,4,7,8,10,12])).all())
    assert((t.times() == np.array(range(6))).all())
    
    
# __contains__
def test_contains_in_series():
    t = SMTimeSeries([1,2,3,4,5,6], [2,4,6,8,10,12])
    assert(8 in t)

def test_contains_not_in_series():
    t = SMTimeSeries([1,2,3,4,5,6], [2,4,6,8,10,12])
    assert(42 not in t)

def test_contains_checks_only_values_not_times():
    t = SMTimeSeries([1,2,3,4,5,6], [2,4,6,8,10,12])
    assert(1 not in t)
    
# times
def test_times_empty():
    t = SMTimeSeries([],[])
    x = np.array([])
    assert(np.array_equal(t.times(), x))

def test_times_nonempty():
    t = SMTimeSeries(range(5),(2,4,6,8,10))
    x = np.array([0,1,2,3,4])
    assert(np.array_equal(t.times(),x))
    
# values
def test_values_empty():
    t = SMTimeSeries([],[])
    x = np.array([])
    assert(np.array_equal(t.values(), x))
    
def test_values_nonempty():
    t = SMTimeSeries(range(5),(2,4,6,8,10))
    x = np.array([2,4,6,8,10])
    assert(np.array_equal(t.values(),x))
    
# items
def test_items_empty():
    t = SMTimeSeries([],[])
    assert(t.items() == [])
    
def test_items_nonempty():
    t = SMTimeSeries(range(5),(2,4,6,8,10))
    x = [(0, 2), (1, 4), (2, 6), (3, 8), (4, 10)]
    assert(t.items() == x)
   

@lazy
def check_length(a,b):
    return len(a)==len(b)
    
def test_lazy_length_check_with_normal_construction():
    thunk = check_length(SMTimeSeries(range(0,4),range(1,5)), 
                         SMTimeSeries(range(1,5),range(2,6)))
    assert(thunk.eval() == True)

def test_lazy_length_check_with_lazy_construction():
    thunk = check_length(SMTimeSeries(range(0,4),range(1,5)).lazy, 
                         SMTimeSeries(range(1,5),range(2,6)).lazy)
    assert(thunk.eval() == True)
    
# __add__
def test_add_valid_int():
    t1 = SMTimeSeries(range(5),[1,2,3,4,5])
    t2 = SMTimeSeries(range(5),[1,1,1,1,1])
        
    ans = t1 + t2
    real_ans = SMTimeSeries(range(5),[2,3,4,5,6])
    assert(np.array_equal(real_ans.values(), ans.values()))
    assert(np.array_equal(real_ans.times(), ans.times()))


def test_add_unequal_times():
    t1 = SMTimeSeries(range(5),[1,2,3,4,5])
    t2 = SMTimeSeries(range(1,6),[1,1,1,1,1])
    with raises(ValueError):
        result = t1+t2
        
# __sub__
def test_sub_valid_int():
    t1 = SMTimeSeries(range(3),[10,10,10])
    t2 = SMTimeSeries(range(3),[1,2,3])

    ans = t1-t2
    real_ans = SMTimeSeries(range(3),[9,8,7])
    assert(np.array_equal(real_ans.values(), ans.values()))
    assert(np.array_equal(real_ans.times(), ans.times()))


def test_sub_unequal_times():
    t1 = SMTimeSeries(range(5),[1,2,3,4,5])
    t2 = SMTimeSeries(range(1,6),[1,1,1,1,1])
    with raises(ValueError):
        result = t1 - t2
        
# __mul__
def test_mul_ints():
    t1 = SMTimeSeries(range(3),[10,10,10])
    t2 = SMTimeSeries(range(3),[1,2,3])
    ans = t1*t2

    real_ans = SMTimeSeries(range(3),[10,20,30])

    assert(np.array_equal(real_ans.values(), ans.values()))
    assert(np.array_equal(real_ans.times(), ans.times()))

def test_mul_unequal_times():
    t1 = SMTimeSeries(range(5),[1,2,3,4,5])
    t2 = SMTimeSeries(range(1,6),[1,1,1,1,1])
    with raises(ValueError):
        t1 * t2
        
# __neg__
def test_neg_pos_vals():
    t = SMTimeSeries(range(5), [1, 2, 3, 4, 5])
    assert((-t == SMTimeSeries(range(5), [-1, -2, -3, -4, -5])).all())
    
def test_neg_neg_vals():
    t = SMTimeSeries(range(5), [-1, -2, -3, -4, -5])
    assert((-t == SMTimeSeries(range(5), [1, 2, 3, 4, 5])).all())
    

    
# __pos__
def test_pos_pos_vals():
    t = SMTimeSeries(range(5), [1, 2, 3, 4, 5])
    assert((+t == SMTimeSeries(range(5), [1, 2, 3, 4, 5])).all())
    
def test_pos_neg_vals():
    t = SMTimeSeries(range(5), [-1, -2, -3, -4, -5])
    assert((+t == SMTimeSeries(range(5), [-1, -2, -3, -4, -5])).all())
    
def test_pos_mixed_vals():
    t = SMTimeSeries(range(5), [1, -2, 3, 4, -5])
    assert((+t == SMTimeSeries(range(5), [1, -2, 3, 4, -5])).all())


# __eq__
def test_eq_all_equal():
    t1 = SMTimeSeries(range(3),[1,2,3])
    t2 = SMTimeSeries(range(3),[1,2,3])
    real_ans = np.array([True,True,True])
    assert(np.array_equal(t1==t2,real_ans))
    
def test_eq_all_unequal():
    t1 = SMTimeSeries(range(3),[1,2,3])
    t2 = SMTimeSeries(range(3),[4,5,6])
    real_ans = np.array([False,False,False])
    assert(np.array_equal(t1==t2,real_ans))

def test_eq_mixed():
    t1 = SMTimeSeries(range(3),[1,2,3])
    t2 = SMTimeSeries(range(3),[1,5,3])
    real_ans = np.array([True,False,True])
    assert(np.array_equal(t1==t2,real_ans))
        

# __abs__
def test_abs_int_result():
    t = SMTimeSeries(range(4),[1,1,1,1])
    assert(abs(t),2)

def test_abs_nonint_result():
    t = SMTimeSeries(range(3),[1,2,3])
    assert(abs(t),math.sqrt(1+4+9))

# __bool__
def test_bool_true():
    t = SMTimeSeries(range(4),[1,1,1,1])
    assert(abs(t))

def test_bool_false():
    t = SMTimeSeries(range(1),[0])
    assert(not abs(t))
    
def test_bool_empty():
    t = SMTimeSeries([],[])
    assert(not abs(t))


# __mean__

# test mean of single valued SM_TS
def test_mean_single_val():
    t = SMTimeSeries([4], [42])
    assert(t.mean() == 42)
        
# test mean for larger ATS
def test_mean_larger():
    t = SMTimeSeries(range(20), range(20))
    assert(t.mean() == 9.5)
       

# test mean for some chunk input
def test_mean_chunk():
    t = SMTimeSeries(range(20), range(20))
    assert(t.mean(chunk = 1) == 0)
    assert(t.mean(chunk = 3) == 1)
    assert(t.mean(chunk = 20) == 9.5)
    
# std
# test std of single valued ATS
def test_std_single_val():
    t = SMTimeSeries([4], [42])
    assert(t.std() == 0)
        
# test std for equal valued ATS
def test_std_equal_val():
    t = SMTimeSeries([4, 5, 6, 7, 8], [1, 1, 1, 1, 1])
    assert(t.std() == 0)
        
# test std for larger ATS
def test_std_larger():
    t = SMTimeSeries(range(20), range(20))
    assert(t.std() == np.std(np.array(range(20))))
        
# test std for some chunk input
def test_std_chunk():
    t = SMTimeSeries(range(20), range(20))
    assert(t.std(chunk = 1) == np.std(np.array([0])))
    assert(t.std(chunk = 3) == np.std(np.array([0, 1, 2])))
    assert(t.std(chunk = 20) == np.std(np.array(range(20))))
    
    delete_test_data()

# remove test files
def delete_test_data():
    shutil.rmtree("./SM_TS_data")
    
    
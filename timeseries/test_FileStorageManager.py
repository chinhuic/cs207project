from pytest import raises
import numpy as np
import math
import shutil
from ArrayTimeSeries import ArrayTimeSeries
from FileStorageManager import FileStorageManager

# NOTE: We use pytest here instead of our typical unittest, since we had 
#       difficulty using the latter to delete test data after running tests

storage_manager = FileStorageManager()
    
# store
# id's represented as ints
def test_store_int_id():
    # Store some time series data
    t1 = ArrayTimeSeries([1, 2, 3, 4], [1, 1.5, 2, 2.5])
    t2 = ArrayTimeSeries([1], [2])
    t3 = ArrayTimeSeries([0, 1, 5, 6], [-5, 3, 1, 6])
    
    storage_manager.store(1, t1)
    storage_manager.store(2, t2)
    storage_manager.store(3, t3)
        
# id's represented as strings
def test_store_str_id():
    # Store some time series data
    t4 = ArrayTimeSeries([1, 2, 3, 4], [1, 1.5, 2, 2.5])
    t5 = ArrayTimeSeries([1], [2])
    t6 = ArrayTimeSeries([0, 1, 5, 6], [-5, 3, 1, 6])
    
    storage_manager.store('4', t4)
    storage_manager.store('5', t5)
    storage_manager.store('6', t6)
        
# get
# valid id's represented as ints
def test_get_valid_int_id():
    t1 = storage_manager.get(1)
    t2 = storage_manager.get(2)
    assert((t1 == ArrayTimeSeries([1, 2, 3, 4], [1, 1.5, 2, 2.5])).all())
    assert((t2 == ArrayTimeSeries([1], [2])).all())
        
# valid id's represented as strings
def test_get_valid_str_id():
    t1 = storage_manager.get('1')
    t2 = storage_manager.get('2')
    assert((t1 == ArrayTimeSeries([1, 2, 3, 4], [1, 1.5, 2, 2.5])).all())
    assert((t2 == ArrayTimeSeries([1], [2])).all())
        
def test_get_invalid_id():
    with raises(KeyError):
        x = storage_manager.get('7')
            
# overwriting disk
def test_overwrite():
    t1 = storage_manager.get(1)
    assert((t1 == ArrayTimeSeries([1, 2, 3, 4], [1, 1.5, 2, 2.5])).all())
        
    t1_new = ArrayTimeSeries([42], [207])
    storage_manager.store(1, t1_new)
        
    t1_new_from_disk = storage_manager.get('1')
    assert((t1_new_from_disk == t1_new))
        
# size
# valid id's represented as strings
def test_size_valid_str():
    assert(storage_manager.size('1') == 1)
    assert(storage_manager.size('2') == 1)
    assert(storage_manager.size('3') == 4)
    assert(storage_manager.size('4') == 4)
    assert(storage_manager.size('5') == 1)
    assert(storage_manager.size('6') == 4)
        
# valid id's represented as ints
def test_size_valid_int():
    assert(storage_manager.size(1) == 1)
    assert(storage_manager.size(2) == 1)
    assert(storage_manager.size(3) == 4)
    assert(storage_manager.size(4) == 4)
    assert(storage_manager.size(5) == 1)
    assert(storage_manager.size(6) == 4)
        
    
def test_size_invalid_id():
    with raises(KeyError):
        x = storage_manager.size('7')
            
# _autogenerate_id
    
# difficult to test this -- we just create a (relatively) large collection
# of id's and see if the _autogenerate_id function returns a unique id
def test_autogenerate_id():
    t1 = ArrayTimeSeries([1], [0])
        
    # We could do this by directly comparing to storage_manager._index
    # rather than storing a bunch of time series, but the latter more
    # closely resembles the functionality of the storage manager.
    for i in range(10, 1000, 50):
        storage_manager.store(i, t1)

    new_id = storage_manager._autogenerate_id()
        
    # check if new_id is unique
    assert(new_id not in storage_manager._index)
    
    delete_test_data()
    
# remove test files
def delete_test_data():
    shutil.rmtree("./SM_TS_data")
        
from TimeSeries_Class import TimeSeries # Change library name later
import numpy as np

class ArrayTimeSeries(TimeSeries):
    """
    A subclass of TimeSeries that stores ordered time series values in
    a numpy array
    
    Parameters
    ----------
    times : sequence
        A sequence containing the ordered time points
    values : sequence
        A sequence containing the values corresponding to the time data. 
        
    Notes
    -----
    PRE:
      - `times` must be in sorted (monotonically increasing) order
      - `times` and `values` must be of the same length
      - data in `values` are ordered with their corresponding time, i.e.
        1st element in `values` corresponds to 1st time point, 2nd element
        in `values` corresponds to 2nd time point, etc.
        
    WARNINGS:
      - if `times` is not sorted then indexing will be unreliable
          
    Examples
    --------
    >>> at1 = ArrayTimeSeries([0, 1, 2], [1, 2, 3])
    >>> at1.value
    array([1, 2, 3])
    >>> at1.time
    array([0, 1, 2])
    >>> len(at1)
    3
    
    >>> at2 = ArrayTimeSeries((0, 2, 4, 7, 10), [4, 1, 10, 2, 100])
    >>> at2.value
    array([  4,   1,  10,   2, 100])
    >>> at2.time
    array([ 0,  2,  4,  7, 10])
    >>> len(at2)
    5
    
    """
    
    def __init__(self, times, values):
        # Check length
        if len(times) != len(values):
            raise ValueError('Input times and values must have the same length')
            
        # Check that all times are distinct 
        # (we don't check sortedness due to time complexity)
        if len(times) != len(set(times)):
            raise ValueError('Input times and values must have the same length')
        
        self.length = len([x for x in values])
        self.value = np.array([x for x in values])
        self.time = np.array([t for t in times])
    
    def __len__(self):
        return self.length
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
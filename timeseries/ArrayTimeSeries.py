from TimeSeries_Week2 import TimeSeries # Change library name later
import numpy as np

class ArrayTimeSeries(TimeSeries):
    """
    A subclass of TimeSeries that stores ordered time series values in
    a numpy array
    
    Parameters
    ----------
    values : sequence
        A sequence containing the values corresponding to the time data. 
        
    Notes
    -----
    PRE:  data in `values` are ordered with their corresponding time, i.e.
          1st element in `values` corresponds to 1st time point, 2nd element
          in `values` corresponds to 2nd time point, etc.
          
    Examples
    --------
    >>> ArrayTimeSeries([1,2,3]).value
    array([1, 2, 3])
    
    >>> ArrayTimeSeries(range(0,10,2)).value
    array([0, 2, 4, 6, 8])
    
    >>> a1 = ArrayTimeSeries((5.1, 6.2, 3.2))
    >>> len(a1)
    3
    """
    
    def __init__(self, values):
        self.length = len([x for x in values])
        self.value = np.array([x for x in values])
    
    def __len__(self):
        return self.length
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
import numpy as np

class TimeSeries:
    """
    TimeSeries class
    
    Represents a series of ordered numerical tuples, representing (time, value), possibly empty
    Construction:  ts = TimeSeries(<a sequence of times>, <a sequence of values>)
    
    Parameters
    ----------
    times : sequence
        A sequence containing the ordered time points
    values : sequence
        A sequence containing the values corresponding to the time data. 
        
    Notes
    -----
    PRE: 
      - timeseries data MUST be in sorted time order
      - both sequences of times and values must be of the same length
      
    Examples
    --------
    >>> t1 = TimeSeries([1, 2, 3], [5, 10, 6])
    >>> t1.value
    [5, 10, 6]
    >>> t1.time
    [1, 2, 3]
    
    >>> t2 = TimeSeries((0, 2, 4, 7, 10), [4, 1, 10, 2, 100])
    >>> t2.value
    [4, 1, 10, 2, 100]
    >>> t2.time
    [0, 2, 4, 7, 10]
    """

    # ASSUMING THAT TIMES IS NOW REQUIRED
    #constructor for TimeSeries
    #attributes are 
    #  times: contains the ordered time points of the time series
    #  value: contains the time series ordered data
    def __init__(self, times, values):
        self.time = [t for t in times]
        self.value = [x for x in values]
        
    # Method len(ts), returns length of timeseries
    def __len__(self):
        return len(self.value)
    
    # Method to return item val in timeseries given the index
    # use as ts[index]
    def __getitem__(self, index):
        return self.value[index]
    
    # Method to set val as ts(index) = val
    # Return nothing
    def __setitem__(self, index, val):
        self.value[index] = val
    
    
    # for length < 3, need to clean up repr
    def __repr__(self):
        class_name = type(self).__name__
        s = class_name + '['
        for i in range(len(self)):
            if (i >2):
                break
            
            s = s + str(self.value[i])
            if (i < len(self)-1):
                s = s + ', '
            
        if (len(self) > 3):
            s = s + '... '
        
        s = s + ']'
        return s
    
    def __str__(self):
        # Ernest: Reimplemented a more general form to work with class inheritance        
        class_name = type(self).__name__
        s = 'The ' + class_name + ' of length ' + str(len(self.value)) + ' is ['
        
        for i in range(len(self)):
            if (i >2):
                break
            
            s = s + str(self.value[i])
            if (i < len(self)-1):
                s = s + ', '
            
        if (len(self) > 3):
            s = s + '... '
        
        s = s + ']'
        return s
    
    def __iter__(self):
        for val in self.value:
            yield val
    
    def itertimes(self):
        for time in self.time:
            yield time
            
    def iteritems(self):
        for item in zip(self.time, self.value):
            yield item
            
if __name__ == "__main__":
    import doctest
    doctest.testmod()
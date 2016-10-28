import numpy as np

class TimeSeries:
    """
    TimeSeries class 
    Represents a series of ordered numerical values, possibly empty
    Construction:  ts = TimeSeries(<any sequence of numerical values>)
    PRE: timeseries data MUST  be in order
    >>> TimeSeries([1,2,3]).value
    [1, 2, 3]
    
    >>> TimeSeries(range(0,10,2)).value
    [0, 2, 4, 6, 8]
    """
    
    #constructor for TimeSeries
    #attributes are 
    #  value: contains the time series ordered data
    def __init__(self, data):
        self.value = [x for x in data]
    
    #Method len(ts), returns length of timeseries
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
        # Reimplemented a more general form
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
    
    # Week 2
    def __iter__(self):
        for val in self.value:
            yield val
            
    def itertimes(self):
        for time in range(len(self)):
            yield time
            
    def iteritems(self):
        for item in enumerate(self):
            yield item
            
            

class ArrayTimeSeries(TimeSeries):
    def __init__(self, data):
        self.value = np.array(data)
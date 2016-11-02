import abc
from TimeSeriesInterface import TimeSeriesInterface


class SizedContainerTimeSeriesInterface(TimeSeriesInterface, abc.ABC):
    """
    
    """

    # Method to return the length of  the timeseries

    @abc.abstractmethod
    def __len__(self):
        """
        implemented differently in both the classes
        """
       
    
    # Method that should return item value given the index
    # use as ts[index]
    
    def __getitem__(self, index):
        return self._value[index]
    
    # Method that should set the value at the given index as val, ts(index) = val
    # Returns nothing
    def __setitem__(self, index, val):
        self._value[index] = val
    
    # Method that should return True when the value is in the timeseries values
    def __contains__(self, value):
        return value in self.value
    
    # Method that returns the numpy array of values
    def values(self):
        return np.array(self.value)

    # Method that returns the numpy array of times
    def times(self):
        return np.array(self.time)

    # Method that returns the list of time-value tuple pairs
    def items(self):
        return [(t, v) for t, v in zip(self.time, self.value)]


    def __repr__(self):
        class_name = type(self).__name__
        s = class_name + '['
        for i in range(len(self)):
            if (i >9):
                break
            
            s = s + str(self._value[i])
            if (i < len(self)-1):
                s = s + ', '
            
        if (len(self) > 10):
            s = s + '... '
        
        s = s + ']'
        return s

    def __str__(self):
        """
        Method to print a representation of the TimeSeries in a concise manner.
        
        Prints the length of the time series and the corresponding values if the
        time series has 10 or fewer items. If the time series has more than 10 items,
        then we print the length of the time series and the first ten items.
        """     
        class_name = type(self).__name__
        s = 'The ' + class_name + ' of length ' + str(len(self._value)) + ' is ['
        
        for i in range(len(self)):
            if (i >9):
                break
            
            s = s + str(self._value[i])
            if (i < len(self)-1):
                s = s + ', '
            
        if (len(self) > 10):
            s = s + '... '
        
        s = s + ']'
        return s

    @property
    def lazy(self):
        def identfn(x):
            return x
        return LazyOperation(identfn, self)
    

            

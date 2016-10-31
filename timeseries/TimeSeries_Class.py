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
            
    @staticmethod
    def binsearch_helper(seq, val):
        """ 
        A helper function for interpolate that retrieves the index of the smallest element
        in a sorted sequence that is larger than val in O(lg(n)) time.
        
        (Adapted from 'Software Design' Lecture)
        
        Parameters
        ----------
        seq : sequence
            a monotonically increasing sequence of numeric objects with length at least 2
        val : numeric
            a numeric object that is NOT in `seq`, and must be strictly less than the
            largest element in `seq` and strictly greater than the smallest element in `seq`
            
        Returns
        ----------
        rangemin: int
            an integer representing the index of the smallest element in `seq` that
            is strictly greater than `val`
            
        Notes
        -----
        PRE: 
            - `seq` is sorted in monotonically increasing order (hence, no duplicates) 
            -  objects in seq are numeric (and hence comparable)
            - `seq` has length greater than or equal to 2
            - `val` is not an element of `seq`
            - `val` is strictly less than the largest element of `seq`, and strictly greater
              than the smallest element of `seq`.
        POST: 
            - `seq` is not changed by this function (immutable)
            - returns the index of the smallest element in `seq` that
              is strictly greater than `val`

        WARNINGS: If `seq` is not sorted, the function is not guaranteed to terminate
  
        Examples
        --------
        >>> ts = TimeSeries([], [])
        >>> input = list(range(10))
        >>> ts.binsearch_helper(input, 5.1)
        6
        >>> ts.binsearch_helper(input, 4.5)
        5
        >>> ts.binsearch_helper(input, 8.9)
        9
        """
        rangemin = 0
        rangemax = len(seq) - 1
        while True:
            if rangemin >= rangemax:
                return rangemin
            midpoint = rangemin + (rangemax - rangemin) // 2
            if seq[midpoint] > val:
                rangemax = midpoint
            elif seq[midpoint] < val:
                rangemin = midpoint + 1
            else:
                raise ValueError("Precondition violated: val should not already be in seq")
            
    def interpolate(self, times):
        """
        A method that takes in a sequence of new time points and computes corresponding 
        values for these times as follows:
        
          - If the new time point is less than the smallest time in the TimeSeries 
            instance, then the new value is the value associated with the smallest time.
          - If the new time point is greater than the largest time in the TimeSeries 
            instance, then the new value is the value associated with the largest time.
          - If the new time point is equal to any of the time points in the TimeSeries, then
            the new value is the value associated with the equal time point.
          - Else, the new value is linearly interpolated from the two values corresponding to
            the two nearest time points.
        
        Parameters
        ----------
        times: sequence
           A sequence of new time points 
        
        
        PRECONDITION: 
        
        Returns
        ----------
        ts: TimeSeries instance
            a new TimeSeries instance consisting of the new time points and their interpolated
            values.
            
        Notes
        -----
        PRE: the TimeSeries instance has at least 2 data points
        POST: 
            - the TimeSeries instance is not changed by this function 
            - returns a new TimeSeries instance consisting of the new time points and their 
              interpolated values.

        WARNINGS: If the TimeSeries instance has fewer than 2 data points, you may access invalid
                  sequence indices.
  
        Examples
        --------
        >>> ts = TimeSeries([0, 5, 10], [1, 2, 3])
        >>> ts.interpolate([0])
        TimeSeries[1]
        >>> ts.interpolate([5])
        TimeSeries[2]
        >>> ts.interpolate([0, 5, 10])
        TimeSeries[1, 2, 3]
        >>> ts.interpolate([1])
        TimeSeries[1.2]
        
        """
        # Empty array which will be used to store interpolated values
        interpolated_vals = []
        
        # Sequentially compute interpolated values for each time point
        for t in times:
            # If time point already exists, then just use the corresponding value
            if t in self.time:      
                interpolated_vals.append(self.value[self.time.index(t)])
                
            # If time is less than lower stationary boundary
            elif t < self.time[0]:
                interpolated_vals.append(self.value[0])
      
            # If time is greater than upper stationary boundary
            elif t > self.time[-1]:    
                interpolated_vals.append(self.value[-1]) 
 
            # Search for indices of two nearest time points using binary search
            # and compute the linear interpolation from the values of these nearest points
            else:       
                next_index = self.binsearch_helper(self.time, t)
                prev_index = next_index - 1
                
                # Interpolate using the following formula:
                # v' = v_0 + (t - t_0) * (v_1 - v_0) / (t_1 - t_0)
                #   t'  - new time point
                #   v'  - value to be interpolated for new time point
                #   t_0 - time at lower point
                #   t_1 - time at upper point
                #   v_0 - value at lower point
                #   v_1 - value at upper point
            
                # Obtain the quantities above
                v_0, v_1 = self.value[prev_index], self.value[next_index]
                t_0, t_1 = self.time[prev_index], self.time[next_index]
                 
                # Compute interpolation
                v_interpolated = v_0 + ((t - t_0) * (v_1 - v_0) / (t_1 - t_0))
                
                interpolated_vals.append(v_interpolated)

        return self.__class__(times, interpolated_vals)
            
if __name__ == "__main__":
    import doctest
    doctest.testmod()
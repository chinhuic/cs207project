
from lazy import LazyOperation, lazy_add, lazy_mul, lazy
import numpy as np
import numbers
import math

class TimeSeries:
    """
    TimeSeries class
    
    Represents a series of ordered numerical tuples, representing (time, value), possibly empty
    Construction:  ts = TimeSeries(<a sequence of times>, <a sequence of values>)
    
    Parameters
    ----------
    times : sequence (numerical)
        A sequence containing the ordered time points
    values : sequence (numerical)
        A sequence containing the values corresponding to the time data. 
        
    Notes
    -----
    PRE:
      - `times` must be in sorted (monotonically increasing) order
      - `times` and `values` must be of the same length
      - `times` and `values` data must be numeric
      - `times` and `values` must be sequence-like objects
      - data in `values` are ordered with their corresponding time, i.e.
        1st element in `values` corresponds to 1st time point, 2nd element
        in `values` corresponds to 2nd time point, etc.
        
    WARNINGS:
      - if `times` is not sorted then indexing will be unreliable
          
    Examples
    --------
    >>> t = TimeSeries([0, 1, 2], [1, 2, 3])
    >>> len(t)
    3
    >>> t[1]
    2
    >>> t[2]
    3
    """

    def __init__(self, times, values):
        """
        Constructor for TimeSeries class. Initializes TimeSeries with 
        time values given in `times` and corresponding values given in `values`
        
        Checks that:
          - `times` and `values` are of equal length
          - times in `times` are all distinct
          - data in `times` and `values` are numeric
          - `times` and `values` are sequences
          
        Parameters
        ----------
        times : sequence (numerical)
            A sequence containing the ordered time points
        values : sequence (numerical)
            A sequence containing the values corresponding to the time data. 
        """
        # Check length
        if len(times) != len(values):
            raise ValueError('Input times and values must have the same length')
            
        # Check that all times are distinct 
        # (we don't check sortedness due to time complexity)
        if len(times) != len(set(times)):
            raise ValueError('Input times and values must have the same length')
            
        # Check if input data is numeric
        if not all(isinstance(x, numbers.Number) for x in values):
            raise TypeError('Data must be numerical!')
            
        if not all(isinstance(t, numbers.Number) for t in times):
            raise TypeError('Time values must be numerical!')
            
        # Check if input data is sequence-like
        try:
            iter(values)
            iter(times)
        except:
            raise TypeError('Data must be a sequence!')
            
        if type(times) == type(np.array([])) or type(values) == type(np.array([])):
            raise NotImplementedError
        else:
            self._time = [t for t in times]
            self._value = [x for x in values]
        
        
        
    # Method len(ts), returns length of timeseries
    def __len__(self):
        return len(self._value)
    
    # Method to return item val in timeseries given the index
    # use as ts[index]
    def __getitem__(self, index):
        return self._value[index]
    
    # Method to set val as ts(index) = val
    # Return nothing
    def __setitem__(self, index, val):
        self._value[index] = val
    
    # Method returns True when value is in timeseries values
    def __contains__(self, value):
        return value in self._value

    
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
    
    def __iter__(self):
        for val in self._value:
            yield val

    def values(self):
        return np.array(self._value)
    
    def itervalues(self):
        for value in self._value:
            yield value

    def times(self):
        return np.array(self._time)

    def itertimes(self):
        for time in self._time:
            yield time

    def items(self):
        return [(t, v) for t, v in zip(self._time, self._value)]
            
    def iteritems(self):
        for item in zip(self._time, self._value):
            yield item
            
    @property
    def lazy(self):
        def identfn(x):
            return x
        return LazyOperation(identfn, self)
            
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
            if t in self._time:      
                interpolated_vals.append(self._value[self._time.index(t)])
                
            # If time is less than lower stationary boundary
            elif t < self._time[0]:
                interpolated_vals.append(self._value[0])
      
            # If time is greater than upper stationary boundary
            elif t > self._time[-1]:    
                interpolated_vals.append(self._value[-1]) 
 
            # Search for indices of two nearest time points using binary search
            # and compute the linear interpolation from the values of these nearest points
            else:       
                next_index = self.binsearch_helper(self._time, t)
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
                v_0, v_1 = self._value[prev_index], self._value[next_index]
                t_0, t_1 = self._time[prev_index], self._time[next_index]
                 
                # Compute interpolation
                v_interpolated = v_0 + ((t - t_0) * (v_1 - v_0) / (t_1 - t_0))
                
                interpolated_vals.append(v_interpolated)

        return TimeSeries(times, interpolated_vals)




    # operator overloading

    def _check_length_helper(self , rhs):
        if not len(self)==len(rhs):
            raise ValueError(str(self)+' and '+str(rhs)+' must have the same length')

    def _check_timedomains_helper(self, rhs):
        if not np.array_equal(self.times(), rhs.times()):
            raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')

    # addition
    def __add__(self,rhs):
        # check lengths are equal and time domains are same
        try:
            # handling case of a constant
            if isinstance(rhs, numbers.Real):
                newvals = [i+rhs for i in self._value]
            else:
                self._check_length_helper(rhs)
                self._check_timedomains_helper(rhs)
                newvals = [i+j for i,j in zip(self._value,rhs._value)]
            return self.__class__(self._time,newvals)
        except TypeError:
            return NotImplemented

    def __radd__(self,other):
        return self + other

    # subtraction
    def __sub__(self,rhs):
        # check lengths are equal and time domains are same
        try:
            # handling case of a constant
            if isinstance(rhs, numbers.Real):
                newvals = [i-rhs for i in self._value]
            else:
                self._check_length_helper(rhs)
                self._check_timedomains_helper(rhs)
                newvals = [i-j for i,j in zip(self._value,rhs._value)]
            return self.__class__(self._time,newvals)
        except TypeError:
            return NotImplemented
    
    def __rsub__(self,other):
        if isinstance(other,numbers.Real):
            newvals = [other-i for i in self._value]
            return self.__class__(self._time,newvals)
        else:
            return self-other

    # equality
    def __eq__(self,rhs):
        # check lengths are equal and time domains are same
        try:
            self._check_length_helper(rhs)
            self._check_timedomains_helper(rhs)
            #return all(i==j for i,j in zip(self._value,rhs._value))
            truths = [i==j for i,j in zip(self._value,rhs._value)]
            return np.array(truths)

        except TypeError:
            return NotImplemented

    # multiplication
    def __mul__(self,rhs):
        # check lengths are equal and time domains are same
        try:
            # handling case of a constant
            if isinstance(rhs,numbers.Real):
                newvals = [i*rhs for i in self._value]
            else:
                self._check_length_helper(rhs)
                self._check_timedomains_helper(rhs)
                newvals = [i*j for i,j in zip(self._value,rhs._value)]
            return self.__class__(self._time,newvals)

        except TypeError:
            return NotImplemented

    def __rmul__(self,other):
        return self * other

    #signs
    def __neg__(self):
        newvals = [-i for i in self._value]
        return self.__class__(self._time,newvals)

    def __pos__(self):
        return self.__class__(self._time,self._value)

    # square root of the sum of the squares of values
    def __abs__(self):
        return math.sqrt(sum(x*x for x in self._value))

    def __bool__(self): 
        return bool(abs(self))


            
if __name__ == "__main__":
    import doctest
    doctest.testmod()
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
        
          - If the new time point is less than the smallest time in the ArrayTimeSeries 
            instance, then the new value is the value associated with the smallest time.
          - If the new time point is greater than the largest time in the ArrayTimeSeries 
            instance, then the new value is the value associated with the largest time.
          - If the new time point is equal to any of the time points in the ArrayTimeSeries, then
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
        ts: ArrayTimeSeries instance
            a new ArrayTimeSeries instance consisting of the new time points and their 
            interpolated values.
            
        Notes
        -----
        PRE: the ArrayTimeSeries instance has at least 2 data points
        POST: 
            - the ArrayTimeSeries instance is not changed by this function 
            - returns a new ArrayTimeSeries instance consisting of the new time points and their 
              interpolated values.

        WARNINGS: If the ArrayTimeSeries instance has fewer than 2 data points, you may access invalid
                  sequence indices.
  
        Examples
        --------
        >>> ts = ArrayTimeSeries([0, 5, 10], [1, 2, 3])
        >>> ts.interpolate([0])
        ArrayTimeSeries[1]
        >>> ts.interpolate([5])
        ArrayTimeSeries[2]
        >>> ts.interpolate([0, 5, 10])
        ArrayTimeSeries[1, 2, 3]
        >>> ts.interpolate([1])
        ArrayTimeSeries[1.2]
        
        """
        # Empty array which will be used to store interpolated values
        interpolated_vals = []
        
        # Sequentially compute interpolated values for each time point
        for t in times:
            # If time point already exists, then just use the corresponding value
            if t in self.time:      
                interpolated_vals.append(self.value[np.where(self.time == t)][0])
                
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

        return ArrayTimeSeries(times, interpolated_vals)
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
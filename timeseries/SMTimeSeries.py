
from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
from FileStorageManager import FSM_global
from ArrayTimeSeries import ArrayTimeSeries
import numbers
import numpy as np

class SMTimeSeries(SizedContainerTimeSeriesInterface):
    """
    A subclass of SizedContainerTimeSeriesInterface that stores ordered time series 
    values persistently on disk, with storage managed by a storage manager.
    
    ASSUMES THAT A GLOBAL FileStorageManager (`FSM_global`) EXISTS
    
    Parameters
    ----------
    times : sequence (numerical)
        A sequence containing the ordered time points
    values : sequence (numerical)
        A sequence containing the values corresponding to the time data. 
    id : int/string (optional)
        id associated with the time series to be initialized. If no id provided,
        then a unique one is generated
        
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
    >>> t1 = SMTimeSeries([0, 1, 2], [1, 2, 3])
    >>> len(t1)
    3
    >>> t1[1]
    2.0
    >>> t1[2] = 4
    >>> t1[2]
    4.0
    """
    
    def __init__(self, times, values, id = None):
        """
        Constructor for SMTimeSeries class. Initializes SMTimeSeries with 
        time values given in `times` and corresponding values given in `values`.
        Also stores an `id` for the purposes of identifying the SMTimeSeries
        instance from storage.
        
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
        id : int/string (optional)
            id associated with the time series to be initialized. If no id provided,
            then a unique one is generated
        
        """
        
        # Check length
        if len(times) != len(values):
            raise ValueError('Input times and values must have the same length')
            
        # Check that all times are distinct 
        # (we don't check sortedness due to time complexity)
        if len(times) != len(set(times)):
            raise ValueError('Input times must be distinct!')
            
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
        
        if id is None:
            # Generate id if unspecified
            # Typecast to string just in case
            self._id = str(FSM_global._autogenerate_id())
        else:
            self._id = str(id)
            
        FSM_global.store(self._id, ArrayTimeSeries(times, values))
        
    @classmethod
    def from_db(cls, id):
        """
        Class method with an id to look up and fetch a time series 
        from the global storage manager. 
        
        Parameters
        ----------
        id : int/string
          id associated with the time series we wish to obtain from disk
            
        Returns
        -------
        t : SMTimeSeries
          the time series corresponding to given id
            
        Notes
        -----
        PRE:
            `id` should exist in the storage manager
        
        WARNINGS:
            If given `id` does not exist, then KeyError is raised
            
        """
        if id not in FSM_global._index:
            raise KeyError('Input ID does not exist on disk!')
        else:
            return FSM_global.get(id)
    
    def __len__(self):
        """
        Obtain the length of the SMTimeSeries instance
         
        Returns
        -------
        l : int
          Length of the SMTimeSeries instance
        
        """
        return FSM_global.size(self._id)
        
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
        ts: SMTimeSeries instance
            a new SMTimeSeries instance consisting of the new time points and their interpolated
            values.
            
        Notes
        -----
        PRE: the SMTimeSeries instance has at least 2 data points
        POST: 
            - the SMTimeSeries instance is not changed by this function 
            - returns a new SMTimeSeries instance consisting of the new time points and their 
              interpolated values.
        WARNINGS: If the SMTimeSeries instance has fewer than 2 data points, you may access invalid
                  sequence indices.
        """
        
        t = FSM_global.get(self._id)
        t_interpolated = t.interpolate(times)
        return SMTimeSeries(t_interpolated.times(), t_interpolated.values())
        
    def __iter__(self):
        """
        Returns an iterator over values of the SMTimeSeries instance
         
        Returns
        -------
        it : iter
          iterator over values of the SMTimeSeries instance
        
        """
        t = FSM_global.get(self._id)
        return iter(t)
            
    def itervalues(self):
        """
        Returns an iterator over values of the SMTimeSeries instance
         
        Returns
        -------
        it : iter
          iterator over values of the SMTimeSeries instance
        
        """
        t = FSM_global.get(self._id)
        return t.itervalues()

    def itertimes(self):
        """
        Returns an iterator over times of the SMTimeSeries instance
         
        Returns
        -------
        it : iter
          iterator over times of the SMTimeSeries instance
        
        """
        t = FSM_global.get(self._id)
        return t.itertimes()

    def iteritems(self):
        """
        Returns an iterator over items (time, value) pairs of the SMTimeSeries 
        instance
         
        Returns
        -------
        it : iter
          iterator over items of the SMTimeSeries instance
        
        """
        t = FSM_global.get(self._id)
        return t.iteritems()
    
    def __getitem__(self, index):
        """
        Returns the value in the SMTimeSeries instance corresponding to 
        `index`
        
        Parameters
        ----------
        index : int
          index of interest
         
        Returns
        -------
        val : numeric
          value in the SMTimeSeries instance corresponding to `index`
        
        """
        t = FSM_global.get(self._id)
        return t[index]
    
    def __setitem__(self, index, val):
        """
        Sets the value in the SMTimeSeries instance corresponding to 
        `index` to new value `val`
        
        Parameters
        ----------
        index : int
          index of interest
        val : numeric
          value to update
        
        """
        t = FSM_global.get(self._id)
        t[index] = val
        FSM_global.store(self._id, t)
    
    def __contains__(self, value):
        """
        Method that should return True when the value is in the SMTimeSeries 
        instance.
        
        Parameters
        ----------
        value : numeric
          value of interest

        Returns
        -------
        L : bool
          returns True if value is in time series, false otherwise
        
        """
        t = FSM_global.get(self._id)
        return value in t._value
    
    def values(self):
        """
        Method that returns the numpy array of values of the time series 
        instance.
        
        Returns
        -------
        vals : numpy array
          values of the time series instance.  
        """
        t = FSM_global.get(self._id)
        return t.values()

    def times(self):
        """
        Method that returns the numpy array of times of the time series 
        instance.
        
        Returns
        -------
        times : numpy array
          times of the time series instance.  
        """
        t = FSM_global.get(self._id)
        return t.times()

    
    def items(self):
        """
        Method that returns the list of time-value tuple pairs of the time
        series instance.
        
        Returns
        -------
        items : tuple list
          list of time-value pairs of the time series instance.
        """
        t = FSM_global.get(self._id)
        return t.items()


    def __repr__(self):
        """
        Method that abbreviates string representation of the time series and returns 
        it. The goal of __repr__ is to be unambiguous, and is typically intended for 
        developers. 
    
        """
        t = FSM_global.get(self._id)
        return repr(t)


    def __str__(self):
        """
        Method to print a representation of the SMTimeSeries in a concise manner.
        
        Prints the length of the time series and the corresponding values if the
        time series has 10 or fewer items. If the time series has more than 10 items,
        then we print the length of the time series and the first ten items.
        """     
        t = FSM_global.get(self._id)
        return str(t)
    
            
   
    def __add__(self,rhs):
        """
        Method to perform infix addition after checking the lengths are equal, and time 
        domains are the same for operations on an SMTimeSeries  
        
        Parameters
        ----------
        rhs : SMTimeSeries
          a second SMTimeSeries instance whose values we wish to add to the 
          SMTimeSeries instance
          
        Notes
        -----
        PRE: 
         - time domains of the two time series instances are the same
         - number of values of the two time series instances are the same 
           (implied by first precondition)

        Returns
        -------
        t_added : SMTimeSeries
          A new SMTimeSeries instance with updated values
        
        """
        t = FSM_global.get(self._id) + FSM_global.get(rhs._id)
        return SMTimeSeries(t.times(), t.values())

        
    def __radd__(self,other):
        """
        Method that implements the binary arithmetic operation of addition with reflected (swapped) operands
        
        Parameters
        ----------
        other : numeric
          numeric value to be added to each value in time series instance
          

        Returns
        -------
        t_new : SMTimeSeries
          A new SMTimeSeries instance with updated values
        
        """
        t = FSM_global.get(self._id)
        t_added = t + other
        return SMTimeSeries(t_added.times(), t_added.values())


    def __sub__(self,rhs):
        """
        Method to perform infix subtraction after checking the lengths are equal, and time 
        domains are the same for operations on an SMTimeSeries  
        
        Parameters
        ----------
        rhs : SMTimeSeries
          a second SMTimeSeries instance whose values we wish to subtract from the 
          SMTimeSeries instance
          
        Notes
        -----
        PRE: 
         - time domains of the two time series instances are the same
         - number of values of the two time series instances are the same 
           (implied by first precondition)

        Returns
        -------
        t_subtracted : SMTimeSeries
          A new SMTimeSeries instance with updated values
        
        """
        t = FSM_global.get(self._id) - FSM_global.get(rhs._id)
        return SMTimeSeries(t.times(), t.values())

    def __rsub__(self,other):
        """
        Method that implements the binary arithmetic operation of subtraction with reflected (swapped) 
        operands
        
        Parameters
        ----------
        other : numeric
          numeric value to be subtracted from each value in time series instance
          

        Returns
        -------
        t_new : SMTimeSeries
          A new SMTimeSeries instance with updated values
        """
        
        t = FSM_global.get(self._id)
        t_subbed = t - other
        return SMTimeSeries(t_subbed.times(), t_subbed.values())
    
 
    def __mul__(self,rhs):
        """
        Method to perform infix multiplication after checking the lengths are equal, and time 
        domains are the same for operations on an SMTimeSeries  
        
        Parameters
        ----------
        rhs : SMTimeSeries
          a second SMTimeSeries instance whose values we wish to multiply with the 
          SMTimeSeries instance values
          
        Notes
        -----
        PRE: 
         - time domains of the two time series instances are the same
         - number of values of the two time series instances are the same 
           (implied by first precondition)

        Returns
        -------
        t_multiplied : SMTimeSeries
          A new SMTimeSeries instance with updated values
        
        """
        t = FSM_global.get(self._id) * FSM_global.get(rhs._id)
        return SMTimeSeries(t.times(), t.values())

    def __rmul__(self,other):
        """
        Method that implements the binary arithmetic operation of multiplication with 
        reflected (swapped) operands
        
        Parameters
        ----------
        other : numeric
          numeric value to be multiplied element-wise with each value in time series instance   

        Returns
        -------
        t_new : SMTimeSeries
          A new SMTimeSeries instance with updated values
        """
        
        t = FSM_global.get(self._id)
        t_mul = t * other
        return SMTimeSeries(t_mul.times(), t_mul.values())

    
    def __eq__(self,rhs):
        """
        Method to perform infix equality after checking the lengths are equal, and 
        time domains are the same for operations on an SMTimeSeries   
        
        Parameters
        ----------
        rhs : SMTimeSeries
          a second SMTimeSeries instance whose values we wish to multiply with the 
          SMTimeSeries instance values

        Returns
        -------
        L : bool
          True if the two time series are equal as defined above, False otherwise
        """
        t1 = FSM_global.get(self._id)
        t2 = FSM_global.get(rhs._id)
        
        return t1 == t2
    
    def __neg__(self):
        """
        Method that performs negation on a value
        
        Returns
        -------
        t_new : SMTimeSeries
          A new SMTimeSeries instance with updated values 
        """
        t = FSM_global.get(self._id)
        t_neg = -t
        return SMTimeSeries(t_neg.times(), t_neg.values())

    def __pos__(self):
        """
        Method that returns the value, as positive of a positive value is still 
        positive, and positive of a negative value is still negative
        
        Returns
        -------
        t_new : SMTimeSeries
          A new SMTimeSeries instance with updated values 
        """
        t = FSM_global.get(self._id)
        return SMTimeSeries(t.times(), t.values())

    
    def __abs__(self):
        """
        Method that returns the positive square root of the sum of the squares of values
        of the time series.
        
        Returns
        -------
        val : int
          the positive square root of the sum of the squares of values of the time series
        """
        t = FSM_global.get(self._id)
        return abs(t)
    
    def __bool__(self): 
        """
        Method that returns 'true' for everything that is not zero, and 'false' for zero
        
        Returns
        -------
        l : bool
          'true' for everything that is not zero, and 'false' for zero
        """
        t = FSM_global.get(self._id)
        return bool(abs(t))
    
    def mean(self, chunk = None):
        """
        Calculates the mean.
        
        Parameters
        ----------
        chunk: int
           a positive integer that specifies how many values from the beginning
           of the time series to consider for calculting the mean; default value is None.
           It is an optional argument. If chunk is not specified, then the mean of all
           the values of the time series is calculated
        PRE: The time series must have at least one value
        
        
        Returns
        -------
        the_mean: float
           a floating point number, which is the mean of the specified values of the timeseries 
        """
        
        t = FSM_global.get(self._id)

        if ( chunk == None ):  
            val = t.values()
            the_mean = np.mean(val)
            
        else:
            val = t.values()
            intermediate = val[:chunk]
            the_mean = np.mean(intermediate)
            
        return the_mean               
                


    def std(self, chunk = None):
        """
        Calculates the standard deviation.
        
        Parameters
        ----------
        chunk: int
           a positive integer that specifies how many values from the beginning
           of the time series to consider for calculting the standard deviation; default value is None.
           It is an optional argument. If chunk is not specified, the standard deviation of all the
           values of the time series is calculated
        PRE: The time series must have at least one value
        
        Returns
        -------
        the_std: float
           a floating point number, which is the standard deviation of the specified values of the timeseries 
        """

        t = FSM_global.get(self._id)
        
        if ( chunk == None ):
            val = t.values()
            the_std = np.std(val)

        else:
            val = t.values()
            intermediate = val[:chunk]
            the_std = np.std(intermediate)

        return the_std
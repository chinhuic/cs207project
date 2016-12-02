
from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
from FileStorageManager import FileStorageManager
from ArrayTimeSeries import ArrayTimeSeries


class SMTimeSeries(SizedContainerTimeSeriesInterface):
    """
    StorageManager Time Series Class
    """
    
    storage_manager = FileStorageManager()
    
    def __init__(self, times, values, id = None):
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
            self._id = str(storage_manager.autogenerate_id())
        else:
            self._id = str(id)
            
        storage_manager.store(self._id, ArrayTimeSeries(times, values))
        
    @classmethod
    def from_db(self, id):
        """
        (Class)method with an id to look up and fetch from the storage manager. The 
        storage manager allocates the time series in memory.
        """
        raise storage_manager.get(id)
    
    def __len__(self):
        t = storage_manager.size(self._id)
        
    def interpolate(self, times):
        t = StorageManager.get(self._id)
        t_interpolated = t.interpolate(times)
        return SMTimeSeries(t_interpolated.times(), t_interpolated.values())
        
    # Method to iterate over values
    def __iter__(self):
        t = storage_manager.get(self._id)
        return iter(t)
            
    # Method that returns an iterator over the values 
    def itervalues(self):
        t = storage_manager.get(self._id)
        return t.itervalues()

    # Method that returns an iterator over the times
    def itertimes(self):
        t = storage_manager.get(self._id)
        return t.itertimes()

    # Method that returns an iterator over the items
    def iteritems(self):
        t = storage_manager.get(self._id)
        return t.iteritems()
    
    # Method that should return item value given the index
    # use as ts[index]    
    def __getitem__(self, index):
        t = storage_manager.get(self._id)
        return t[index]
    
    # Method that should set the value at the given index as val, ts(index) = val
    # Returns nothing
    def __setitem__(self, index, val):
        t = storage_manager.get(self._id)
        t[index] = val
        storage_manager.store(self._id, t)
    
    # Method that should return True when the value is in the timeseries values
    def __contains__(self, value):
        t = storage_manager.get(self._id)
        return value in t._value
    
    # Method that returns the numpy array of values
    def values(self):
        t = storage_manager.get(self._id)
        return t.values()

    # Method that returns the numpy array of times
    def times(self):
        t = storage_manager.get(self._id)
        return t.times()

    # Method that returns the list of time-value tuple pairs
    def items(self):
        t = storage_manager.get(self._id)
        return t.items()

    # Method that abbreviates string representation and returns it
    # the goal of __repr__ is to be unambiguous, and is typically intended for developers 
    def __repr__(self):
        t = storage_manager.get(self._id)
        return repr(t)

    # Method that returns a representation of a TimeSeries in a concise, unambiguous manner 
    # the goal of __str__ is to be readable, and is typically intended for users 
    def __str__(self):
        """
        Method to print a representation of the TimeSeries in a concise manner.
        
        Prints the length of the time series and the corresponding values if the
        time series has 10 or fewer items. If the time series has more than 10 items,
        then we print the length of the time series and the first ten items.
        """     
        t = storage_manager.get(self._id)
        return str(t)
    
    # Helper method for methods that perform calculations (like __add__, __sub__, for instance),
    # to check whether the lengths are the same
    def _check_length_helper(self , rhs):
        t1 = storage_manager.get(self._id)
        t2 = storage_manager.get(rhs._id)
        if not len(t1)==len(t2):
            raise ValueError(str(t1)+' and '+str(t2)+' must have the same length')

    # Helper method for methods that perform calculations (like __add__, __sub__, for instance),
    # to check whether the time domains of the TimeSeries are the same
    def _check_timedomains_helper(self, rhs):
        t1 = storage_manager.get(self._id)
        t2 = storage_manager.get(rhs._id)
        if not np.array_equal(t1.times(), t2.times()):
            raise ValueError(str(t1)+' and '+str(t2)+' must have the same time points')
            
    # Method to perform infix addition after checking the lengths are equal, and time domains are the same
    # for operations on a TimeSeries   
    def __add__(self,rhs):
        t = storage_manager.get(self._id) + storage_manager.get(rhs._id)
        return SMTimeSeries(t.times(), t.values())

        
    # Method that implements the binary arithmetic operation of addition with reflected (swapped) operands
    def __radd__(self,other):
        t = storage_manager.get(self._id)
        t_added = t + other
        return SMTimeSeries(t_added.times(), t_added.values())

    # Method to perform infix subtraction after checking the lengths are equal, and time domains are the same
    # for operations on a TimeSeries   
    def __sub__(self,rhs):
        t = storage_manager.get(self._id) - storage_manager.get(rhs._id)
        return SMTimeSeries(t.times(), t.values())

    # Method that implements the binary arithmetic operation of subtraction with reflected (swapped) operands
    def __rsub__(self,other):
        t = storage_manager.get(self._id)
        t_subbed = t - other
        return SMTimeSeries(t_subbed.times(), t_subbed.values())
    
    # Method to perform infix multiplication after checking the lengths are equal, and time domains are the same
    # for operations on a TimeSeries   
    def __mul__(self,rhs):
        t = storage_manager.get(self._id) * storage_manager.get(rhs._id)
        return SMTimeSeries(t.times(), t.values())

    # Method that implements the binary arithmetic operation of multiplication with reflected (swapped) operands
    def __rmul__(self,other):
        t = storage_manager.get(self._id)
        t_mul = t * other
        return SMTimeSeries(t_mul.times(), t_mul.values())

    
    # Method to perform infix equality after checking the lengths are equal, and time domains are the same
    # for operations on a TimeSeries   
    def __eq__(self,rhs):
        t1 = storage_manager.get(self._id)
        t2 = storage_manager.get(rhs._id)
        
        return t1 == t2
    
    # Method that performs negation on a value
    # signs
    def __neg__(self):
        t = storage_manager.get(self._id)
        t_neg = -t
        return SMTimeSeries(t_neg.times(), t_neg.values())

    # Method that returns the value, as positive of a positive value is still positive,
    # and positive of a negative value is still negative
    def __pos__(self):
        t = storage_manager.get(self._id)
        return SMTimeSeries(t.times(), t.values())

    # Method that returns the positive square root of the sum of the squares of values
    def __abs__(self):
        t = storage_manager.get(self._id)
        return abs(t)
    
    # Method that returns 'true' for everything that is not zero, and 'false' for zero
    def __bool__(self): 
        t = storage_manager.get(self._id)
        return bool(abs(t))
    
     def mean(self, chunk = None):
        """
        Calculates the mean.
        PARAMETERS
        ------------
        chunk: int
           a positive integer that specifies how many values from the beginning
           of the time series to consider for calculting the mean; default value is None.
           It is an optional argument. If chunk is not specified, then the mean of all
           the values of the time series is calculated
        PRE: The time series must have at least one value
        
        
        RETURNS
        -------
        the_mean: float
           a floating point number, which is the mean of the specified values of the timeseries 
        """
        
        t = storage_manager.get(self._id)

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
        PARAMENTERS
        ------------
        chunk: int
           a positive integer that specifies how many values from the beginning
           of the time series to consider for calculting the standard deviation; default value is None.
           It is an optional argument. If chunk is not specified, the standard deviation of all the
           values of the time series is calculated
        PRE: The time series must have at least one value
        
        RETURNS
        -------
        the_std: float
           a floating point number, which is the standard deviation of the specified values of the timeseries 
        """

        t = storage_manager.get(self._id)
        
        if ( chunk == None ):
            val = t.values()
            the_std = np.std(val)

        else:
            val = t.values()
            intermediate = val[:chunk]
            the_std = np.std(intermediate)

        return the_std
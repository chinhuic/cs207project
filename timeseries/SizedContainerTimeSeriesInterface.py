import abc
from TimeSeriesInterface import TimeSeriesInterface
from lazy import LazyOperation, lazy_add, lazy_mul, lazy
import numpy as np
import numbers
import math

class SizedContainerTimeSeriesInterface(TimeSeriesInterface, abc.ABC):
    """
       An ABC (abstract base class) or interface that inherits from the TimeSeriesInterface 
       ABC.
       This has the methods which pertain to the "containerness" of the timeseries: the 
       notions of indexing, length, and returning arrays in addition to iterators
    """

    # Method to return the length of the timeseries
    @abc.abstractmethod
    def __len__(self):
        """
        Returns the length of the timeseries. It is an abstract method, and must
        necessarily be implemented by any class that inherits from SizedContainerTimeSeriesInterface.
        Implemented slightly differently in the classes TimeSeries and ArrayTimeSeries
        """
        pass

    # Method that computes corresponding values for a given sequence of time points by linear
    # interpolation of existing values    
    @abc.abstractmethod
    def interpolate(self, times):
        """
        A method that takes in a sequence of new time points and computes corresponding 
        values by linear interpolation of existing values. It is an abstract method, and must
        necessarily be implemented by any class that inherits from SizedContainerTimeSeriesInterface.
        Implemented slightly differently in TimeSeries and ArrayTimeSeries classes
        """
        pass

    # Method to iterate over values 
    def __iter__(self):
        for val in self._value:
            yield val

    # Method that returns an iterator over the values 
    def itervalues(self):
        return iter(self._value)

    # Method that returns an iterator over the times
    def itertimes(self):
        return iter(self._time)

    # Method that returns an iterator over the items
    def iteritems(self):
        return iter(zip(self._time, self._value))

        
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
        return value in self._value
    
    # Method that returns the numpy array of values
    def values(self):
        return np.array(self._value)

    # Method that returns the numpy array of times
    def times(self):
        return np.array(self._time)

    # Method that returns the list of time-value tuple pairs
    def items(self):
        return [(t, v) for t, v in zip(self._time, self._value)]

    # Method that abbreviates string representation and returns it
    # the goal of __repr__ is to be unambiguous, and is typically intended for developers 
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

    # Method that returns a representation of a TimeSeries in a concise, unambiguous manner 
    # the goal of __str__ is to be readable, and is typically intended for users 
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

    # Method to return a new LazyOperation instance using an identity function
    @property
    def lazy(self):
        def identfn(x):
            return x
        return LazyOperation(identfn, self)

    # Helper method for methods that perform calculations (like __add__, __sub__, for instance),
    # to check whether the lengths are the same
    def _check_length_helper(self , rhs):
        if not len(self)==len(rhs):
            raise ValueError(str(self)+' and '+str(rhs)+' must have the same length')

    # Helper method for methods that perform calculations (like __add__, __sub__, for instance),
    # to check whether the time domains of the TimeSeries are the same
    def _check_timedomains_helper(self, rhs):
        if not np.array_equal(self.times(), rhs.times()):
            raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')

    # Method to perform infix addition after checking the lengths are equal, and time domains are the same
    # for operations on a TimeSeries   
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

        
    # Method that implements the binary arithmetic operation of addition with reflected (swapped) operands
    def __radd__(self,other):
        return self + other

    # Method to perform infix subtraction after checking the lengths are equal, and time domains are the same
    # for operations on a TimeSeries   
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

    # Method that implements the binary arithmetic operation of subtraction with reflected (swapped) operands
    def __rsub__(self,other):
        if isinstance(other,numbers.Real):
            newvals = [other-i for i in self._value]
            return self.__class__(self._time,newvals)
        else:
            return self-other

    # Method to perform infix equality after checking the lengths are equal, and time domains are the same
    # for operations on a TimeSeries   
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

    # Method to perform infix multiplication after checking the lengths are equal, and time domains are the same
    # for operations on a TimeSeries   
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

    # Method that implements the binary arithmetic operation of multiplication with reflected (swapped) operands
    def __rmul__(self,other):
        return self * other

    # Method that performs negation on a value
    # signs
    def __neg__(self):
        newvals = [-i for i in self._value]
        return self.__class__(self._time, newvals)

    # Method that returns the value, as positive of a positive value is still positive,
    # and positive of a negative value is still negative
    def __pos__(self):
        return self.__class__(self._time, self._value)

    # Method that returns the positive square root of the sum of the squares of values
    def __abs__(self):
        return math.sqrt(sum(x*x for x in self._value))
    
    # Method that returns 'true' for everything that is not zero, and 'false' for zero
    def __bool__(self): 
        return bool(abs(self))





    ## NEW STUFF ##
    ## EVERYTHING ABOVE THIS IS THE SAME AS BEFORE ##

    def mean(self, chunk = None)
        """
        Calculates the mean.

        PARAMETERS
        ------------
        chunk: int
           a positive integer that specifies how many values from the beginning
           of the time series to consider for calcultiong the mean; default value is None.
           It is an optional argument.

        RETURNS
        -------
        the_mean: float
           a floating point number, which is the mean of the specified values of the timeseries 

        """

        if ( chunk == None ):  
            val = self.values()
            the_mean = np.mean(val)
            
        else:
            val = self.values()
            intermediate = val[:chunk]
            the_mean = np.mean(intermediate)
            
         return the_mean               
                


    def std(self, chunk = None)
        """
        Calculates the standard deviation.

        PARAMENTERS
        ------------
        chunk: int
           a positive integer that specifies how many values from the beginning
           of the time series to consider for calcultiong the mean; default value is None.
           It is an optional argument.

        RETURNS
        -------
        the_std: float
           a floating point number, which is the standard deviation of the specified values of the timeseries 

        """

        if ( chunk == None ):
            val = self.values()
            the_std = np.std(val)

        else:
            val = self.values()
            intermediate = val[:chunk]
            the_std = np.std(intermediate)

        return the_std
        
    


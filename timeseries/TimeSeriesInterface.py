import abc

class TimeSeriesInterface(abc.ABC):
    """
    An ABC (abstract base class) or interface that defines the common methods that may
    be used in both  sized-container based time series as well as stream based and simulated 
    time series.
    """
    @abc.abstractmethod
    def __iter__(self):
        """Method to iterate over values in time series""" 

    @abc.abstractmethod
    def itervalues(self):
        """Returns an interator over values"""
        
    @abc.abstractmethod
    def itertimes(self):
        """Returns an interator over times"""

    @abc.abstractmethod
    def iteritems(self):
        """Returns an iterator over time-value pairs"""


            

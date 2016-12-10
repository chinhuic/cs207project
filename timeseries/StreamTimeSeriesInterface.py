from TimeSeriesInterface import TimeSeriesInterface
import abc

class StreamTimeSeriesInterface(TimeSeriesInterface, abc.ABC):

    """
    An ABC (abstract base class) or interface to handle those timeseries that do not
    have an underlying array (or storage). 
    
    """
    @abc.abstractmethod
    def produce(self, chunk = 1):
        """
        A method that yields a 'chunk' sized bunch of new elements whenever it is called.
        MUST be a generator method.
        """


        
        


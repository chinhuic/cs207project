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
        An method that generates a chunk sized bunch of new elements into the timeseries 
        whenever it is called
        """


        
        


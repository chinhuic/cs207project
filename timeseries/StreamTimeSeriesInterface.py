import abc

class StreamTimeSeriesInterface(abc.ABC):

    """
    An ABC (abstract base class) or interface to handle those timeseries that do not
    have an underlying array (or storage). 
    
    """
    @abc.abstractmethod
    def produce(self, chunk = 1):
        """
        An abstract (generator) method that generates a chunk sized bunch
        of new elements into the timeseries whenever it is called

        PARAMETER
        ----------
        chunk: int
            the chunk argument must be an integer; default value is 1

        YIELDS
        -------
        the chunk-sized list of values.  
        """
        #yield random.sample(range(1, 10000000), chunk)
        
        


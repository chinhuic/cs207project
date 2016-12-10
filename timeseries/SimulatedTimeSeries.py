from StreamTimeSeriesInterface import StreamTimeSeriesInterface

class SimulatedTimeSeries(StreamTimeSeriesInterface):
    """
    SimulatedTimeSeries class
     
    Construction:  ts = SimulatedTimeSeries(gen)
                     where `gen` is a generator of (time, value) pairs 
    
    Parameters
    ----------
    gen: generator (tuple)
        generator of (time, value) pairs for the time series
        
    Notes
    -----
    PRE:
      - time values in `gen` must be in sorted (monotonically increasing) order
          
    """

    def __init__(self, generator_method):
        """
        Constructor for SimulatedTimeSeries. Argument is generator_method: a generator 
        method, which is then bound to self._gmethod
        """
        self._gmethod = iter(generator_method)
        
        
    def produce(self, chunk = 1):
        """
        Uses the generator method passed as an argument to the constructor (which was then bound
        to self._gmethod in the constructor) to generate a sequence with `chunk` number of
        (time, value) pairs.  

        A method that yields a 'chunk' sized bunch of new elements whenever it is called
       
        PARAMETER
        ----------
        chunk: int
            the chunk argument must be an integer; default value is 1

        YIELDS
        -------
        the chunk-sized list of (time, value) pairs  
        """
        generated_list = []
        
        g = self._gmethod
         
        for i in range(chunk): 
            generated_list.append(next(g))

        yield generated_list

       
    def __iter__(self):
        """Method to iterate over values in the time series""" 
        for time, val in self._gmethod:
            yield val
    
    def itertimes(self):
        """interator over times"""
        for time, val in self._gmethod:
            yield time
    
    def itervalues(self):
        """iterator over values"""
        for time, val in self._gmethod:
            yield val
        
    def iteritems(self):
        """iterator over time-value pairs"""
        for time, val in self._gmethod:
            yield (time, val)
        
            
         
         
    

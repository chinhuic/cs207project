from StreamTimeSeriesInterface import StreamTimeSeriesInterface

class SimulatedTimeSeries(StreamTimeSeriesInterface):
    """
    SimulatedTimeSeries class
     
    Construction:  ts = SimulatedTimeSeries(<any generator function>)

    PRE: argument passed to constructor must be a generator
    
    """

    def __init__(self, generator_method):
        """
        Constructor for SimulatedTimeSeries. Argument is generator_method: a generator 
        method, which is then bound to self._gmethod
        """
        self._gmethod = iter(generator_method)
        
        
    def produce(self, chunk = 1):
        """
        Uses the generator method passed as an argument to the constructor to generate a 
        sequence with `chunk` number of (time, value) pairs.  

        An method that generates a chunk sized bunch of new elements into the timeseries 
        whenever it is called
       
        PARAMETER
        ----------
        chunk: int
            the chunk argument must be an integer; default value is 1

        YIELDS
        -------
        the chunk-sized list of values.  
        """
        generated_list = []
        
        g = self._gmethod
         
        for i in range(chunk): 
            generated_list.append(next(g))

        yield generated_list

        
    def __iter__(self):
        return self
    
    def itertimes(self):
        yield self.produce(chunk = 1)[0][0]
    
    def itervalues(self):
        return self.produce(chunk = 1)[0][1]
        
    def iteritems(self):
        return self.produce(chunk = 1)[0]
        
            
         
         
    

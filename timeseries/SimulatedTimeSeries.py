from StreamTimeSeriesInterface import StreamTimeSeriesInterface

class SimulatedTimeSeries(StreamTimeSeriesInterface):
    """
    SimulatedTimeSeries class
     
    Construction:  ts = SimulatedTimeSeries(<any generator function>)

    PRE: argument passed to constructor must be a generator
    
    """


     def __init__(self, generator_method):
         """
         Constructor for SimulatedTimeSeries. Argument is generator_method: a generator method, which
         is then bound to self._gmethod
         """
         
         self._gmethod = generator_method()
         
          

    
     def produce(self, chunk = 1):
         """
         Inherited from StreamTimeSeriesInterface. Uses the generator method passed as an argument to the
         constructor, which was bound to self._gmethod, to generate a sequence with chunk number of values. It then
         yields that sequence. 

        
         """
         a_list = []

         g = self._gmethod
         
         for i in range(chunk):
             a_list.append(next(g))

         yield a_list

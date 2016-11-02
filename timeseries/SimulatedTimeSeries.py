from StreamTimeSeriesInterface import StreamTimeSeriesInterface

class SimulatedTimeSeries(StreamTimeSeriesInterface):

     def __init__(self, generator_method):
         
         self._gmethod = generator_method
         
          

    
     def produce(self, chunk = 1):
         a_list = []

         g = self._gmethod
         
         for i in range(chunk):
             a_list.append(next(g))

         yield a_list
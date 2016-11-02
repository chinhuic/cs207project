import abc
import random
import collections.abc
class StreamTimeSeriesInterface(abc.ABC):

    @abc.abstractmethod
    def produce(self, chunk = 1):
        """
        """
        #yield random.sample(range(1, 10000000), chunk)
        
        
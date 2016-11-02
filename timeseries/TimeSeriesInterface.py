import abc

class TimeSeriesInterface(abc.ABC):
    """
    An ABC (abstract base class) or interface that defines the common methods that may
    be used in both  sized-container based time series as well as stream based and simulated time series.
    """

    def __iter__(self):
        for val in self.value:
            yield val


    def itervalues(self):
        for value in self.value:
            yield value

    def itertimes(self):
        for time in self.time:
            yield time


    def iteritems(self):
        for item in zip(self.time, self.value):
            yield item



            

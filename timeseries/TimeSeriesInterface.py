import abc

class TimeSeriesInterface(abc.ABC):
    """
    An ABC (abstract base class) or interface that defines the common methods that may
    be used in both  sized-container based time series as well as stream based and simulated time series.
    """

    def __iter__(self):
        for val in self._value:
            yield val


    def itervalues(self):
        for value in self._value:
            yield value

    def itertimes(self):
        for time in self._time:
            yield time


    def iteritems(self):
        for item in zip(self._time, self._value):
            yield item



            

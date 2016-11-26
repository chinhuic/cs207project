
from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface

class SMTimeSeries(SizedContainerTimeSeriesInterface):
    """
    StorageManager Time Series Class
    """
    def __init__(self, times, values, id = None):
        raise NotImplementedError
        
    def from_db(self, id):
        """
        (Class)method with an id to look up and fetch from the storage manager. The 
        storage manager allocates the time series in memory.
        """
        raise NotImplementedError
    

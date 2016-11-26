
import abc

class StorageManagerInterface(abc.ABC):
    """
    Interface for the Storage Manager class
    """
    
    @abc.abstractmethod
    def store(self, id, t):
        """
        Method to store an instance of a SizedContainerTimeSeriesInterface
        """
    
    @abc.abstractmethod
    def size(self, id):
        """
        Method to obtain the size of a SizedContainerTimeSeriesInterface by id
        """
        
    @abc.abstractmethod
    def get(self, id):
        """
        Method to obtain a SizedContainerTimeSeries instance.
        """
        
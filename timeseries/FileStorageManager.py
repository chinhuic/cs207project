
from StorageManagerInterface import StorageManagerInterface

class FileStorageManager(StorageManagerInterface):
    
    def __init__(self, file):
        raise NotImplementedError
        
    def store(self, id, t):
        """
        Method to store an instance of a SizedContainerTimeSeriesInterface
        """
        raise NotImplementedError
        
    def size(self, id):
        """
        Method to obtain the size of a SizedContainerTimeSeriesInterface by id
        """
        raise NotImplementedError
        
    def get(self, id):
        """
        Method to obtain a SizedContainerTimeSeries instance
        """
        raise NotImplementedError
       
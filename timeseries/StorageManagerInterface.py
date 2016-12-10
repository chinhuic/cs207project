
import abc

class StorageManagerInterface(abc.ABC):
    """
    Interface for a file storage manager of our time series
    
    Methods
    -------
    store:
        Stores a given time series `t` into the storage manager by index
        
    size:
        Returns the length of the time series in storage by index
    
    get:
        Returns a time series instance by index
    """
    
    @abc.abstractmethod
    def store(self, id, t):
        """
        Stores a given time series `t` into the storage manager, indexed by `id`
        
        Parameters
        ----------
        id : int / string
            id to which the given time series `t` is assigned
        t : SizedContainerTimeSeriesInterface
            The time series to be stored
            
        Returns
        -------
        t : SizedContainerTimeSeriesInterface
            The input time series
            
        Notes
        -----
        - if the `id` already exists in storage, then we overwrite the previous 
          time series corresponding with the given id with `t`.
          
        """
    
    @abc.abstractmethod
    def size(self, id):
        """
        Returns the length of the time series in storage indexed by `id`
        
        Parameters
        ----------
        id: int / string
            id of the time series of interest
            
        Returns
        -------
        l : int
            Length of the time series in storage corresponding to `id`
            
        Notes
        -----
        PRE:
            `id` should exist in the storage manager
        
        WARNINGS:
            If given `id` does not exist, then KeyError is raised
        """
        
    @abc.abstractmethod
    def get(self, id):
        """
        Returns a time series instance by given `id`
        
        Parameters
        ----------
        id: int / string
            id of the time series of interest
            
        Returns
        -------
        t : SizedContainerTimeSeriesInterface
            The time series corresponding to the given `id`
            
        Notes
        -----
        PRE:
            `id` should exist in the storage manager
        
        WARNINGS:
            If given `id` does not exist, then KeyError is raised
        """
        
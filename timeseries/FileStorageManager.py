
from StorageManagerInterface import StorageManagerInterface
from ArrayTimeSeries import ArrayTimeSeries
from random import randint
import os, sys
import numpy as np
import pickle

class FileStorageManager(StorageManagerInterface):
    """
    A file storage manager class that manages the persistent storage of our
    individual time series.
    
    Parameters
    ----------
    filename: string (optional)
        Name of pickle file to stores the id and length of each time series. 
        Default is 'ts_index.pkl'.
        
    directory: string (optional)
        Path to directory to which index file and time series data files are
        to be stored. 
    
    Examples
    --------
    >>> sm = FileStorageManager()
    >>> t1 = ArrayTimeSeries([1, 2, 3, 4], [1, 1.5, 2, 2.5])
    >>> sm.store(1, t1)
    ArrayTimeSeries[1.0, 1.5, 2.0, 2.5]
    >>> sm.get(1)
    ArrayTimeSeries[1.0, 1.5, 2.0, 2.5]
    >>> sm.size(1)
    4
    """
    
    
    def __init__(self, filename = 'ts_index.pkl', directory = './SM_TS_data'):
        """
        Constructor for FileStorageManager. Initializes FileStorageManager with 
        a pointer to a filename that stores the id and length of each time series, 
        and to a directory containing the aforesaid file as well as data files
        of stored time series
          
        Parameters
        ----------
        filename: string (optional)
            Name of pickle file to stores the id and length of each time series. 
            Default is 'ts_index.pkl'.
        
        directory: string (optional)
            Path to directory to which index file and time series data files are
            to be stored. 
        """
        # Check if directory already exists. If not, create it
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        # Check if file storing id and length of each time series (index_file)
        # exists. If so, store its contents in a variable. If not, create a new
        # dictionary to store (future) id - length mappings
        try:
            with open(directory + '/' + filename, 'rb') as index_file:
                self._index = pickle.load(index_file)
        except:
            self._index = dict()
            
        self._filename = filename
        self._directory = directory
            
        
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
        - stores the time series as a 2-d numpy array with 64-bit floats for both times 
          and values
          
        """
        # Convert time series to 2D numpy arrays with 64-bit floats for both
        # times and values
        t_64bit_arr = np.vstack((t.times(), t.values())).astype(np.float64)
        
        # Store/Update the time series data into a .npy file indexed by the series' id
        np.save(self._directory + '/' + 'ts_' + str(id), t_64bit_arr)
        
        # Store/Update the id - length mapping corresponding to the time series
        self._index[str(id)] = len(t)
        
        # Update the index_file
        with open(self._directory + '/' + self._filename, 'wb') as index_file:
            pickle.dump(self._index, index_file, protocol=pickle.HIGHEST_PROTOCOL)
        
        return t
        
        
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

        # Check if `id` exists in our storage. If not, raise KeyError
        if str(id) in self._index:
            return self._index[str(id)]
        
        else:
            raise KeyError('Input ID does not exist on disk!')
        
        
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
        
        # Check if `id` exists in our storage. If so, retrieve stored time 
        # series with given id. If not, raise KeyError 
        if str(id) in self._index:
            t = np.load(self._directory + '/' + 'ts_' + str(id) + '.npy')
            
            return ArrayTimeSeries(t[0], t[1])
        
        else:
            raise KeyError('Input ID does not exist on disk!')
        
    
    def _autogenerate_id(self):     
        """
        Method to generate a new id for when user does not specify id
                   
        Returns
        -------
        id : int
            An id that does not already exist in storage
            
        """
        
        # Generate a random id and check if it already exists in storage.
        # If so, repeat. If not, return this id.
        
        # FUTURE WORK: make the id's less 'messy' in that they don't 
        #              become hideously large while still giving user
        #              a sufficient set of id's to work with
        
        while True:
            proposed_id = randint(1, sys.maxsize)
            
            if proposed_id not in self._index:
                return proposed_id

            

# Create a global instance of FileStorageManager
FSM_global = FileStorageManager()

from StorageManagerInterface import StorageManagerInterface
from ArrayTimeSeries import ArrayTimeSeries
from random import randint
import os, sys
import numpy as np
import pickle

class FileStorageManager(StorageManagerInterface):
    
    def __init__(self, filename = 'ts_index.pkl', directory = './SM_TS_data'):
        
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        try:
            with open(directory + '/' + filename, 'rb') as index_file:
                self._index = pickle.load(index_file)
        except:
            self._index = dict()
            
        self._filename = filename
        self._directory = directory
            
        
    def store(self, id, t):
        """
        Method to store an instance of a SizedContainerTimeSeriesInterface
        """
        # Convert time series to 2D numpy arrays with 64-bit floats for both
        # times and values
        t_64bit_arr = np.vstack((t.times(), t.values())).astype(np.float64)
        
        np.save(self._directory + '/' + 'ts_' + str(id), t_64bit_arr)
        
        self._index[str(id)] = len(t)
        
        with open(self._directory + '/' + self._filename, 'wb') as index_file:
            pickle.dump(self._index, index_file, protocol=pickle.HIGHEST_PROTOCOL)
        
        return t
        
        
    def size(self, id):
        """
        Method to obtain the size of a SizedContainerTimeSeriesInterface by id
        """
        if str(id) in self._index:
            return self._index[str(id)]
        
        else:
            raise KeyError('Input ID does not exist on disk!')
        
        
    def get(self, id):
        """
        Method to obtain a SizedContainerTimeSeries instance
        """
        # Retrieve stored time series with given id
        if str(id) in self._index:
            t = np.load(self._directory + '/' + 'ts_' + str(id) + '.npy')
            
            return ArrayTimeSeries(t[0], t[1])
        
        else:
            raise KeyError('Input ID does not exist on disk!')
        
    
    def _autogenerate_id(self):
        """
        Method to generate a new id for when user does not specify id
        """
        while True:
            proposed_id = randint(1, sys.maxsize)
            
            if proposed_id not in self._index:
                return proposed_id
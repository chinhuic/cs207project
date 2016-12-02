
from StorageManagerInterface import StorageManagerInterface
from ArrayTimeSeries import ArrayTimeSeries
from random import randint
import sys
import numpy as np
import json

class FileStorageManager(StorageManagerInterface):
    
    # Might add id_file to argument
    def __init__(self):
        try:
            id_file = open('id.json', 'r')
            self._id = json.load(id_file)
        except IOError:
            self._id = set()
            
        self._filename = 'id.json'
            
        
    def store(self, id, t):
        """
        Method to store an instance of a SizedContainerTimeSeriesInterface
        """
        # Convert time series to 2D numpy arrays with 64-bit floats for both
        # times and values
        t_64bit_arr = np.vstack((t.times(), t.values())).astype(np.float64)
        
        np.save('ts_data/'+str(id), t_64_bit_arr)
        
        self._id.add(id)
        
        np.save('id.json', self._id)
        
        # or return t_64bit_arr?
        return t
        
        
    def size(self, id):
        """
        Method to obtain the size of a SizedContainerTimeSeriesInterface by id
        """
        
        # Retrieve stored time series with given id
        t = np.load('data/'+str(id)+'.npz')
        
        return len(t)
        
        
    def get(self, id):
        """
        Method to obtain a SizedContainerTimeSeries instance
        """
        # Retrieve stored time series with given id
        t = np.load('data/'+str(id)+'.npy')
        
        return ArrayTimeSeries(t[0], t[1])
    
    def autogenerate_id(self):
        """
        Method to generate a new id for when user does not specify id
        """
        return str(randint(1, sys.maxsize))
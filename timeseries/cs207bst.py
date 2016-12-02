# unbalanced binary search tree
# based off lab 10
import pickle
import os
import struct
import portalocker


class ValueRef(object):
    """
    Reference to a string value on disk

    Parameters
    ----------
    referent : optional
        The value to store (default is None)

    address : int, optional
        Address of the referent (default is 0)

    Attributes
    ----------
    _referent
    _address
        
    Notes
    -----
    WARNINGS:
        - referent values converted to utf-8 encoded bytes of string 
        of referent when stored to account for different key, value types
        - return type of get for a value will always be a string type

    Examples
    --------

    """

    def __init__(self, referent=None, address=0):
        """
        Constructor for ValueRef.  Initializes with a value given by `referent`
        at the address given by `address`

        Parameters
        ----------
        referent : int/float/string, optional
            The value to store (default is None)

        address : int, optional
            Address of the referent (default is 0)

        """
        self._referent = referent #value to store
        self._address = address #address to store at
        
    @property
    def address(self):
        """returns the address of the value"""
        return self._address
    
    def prepare_to_store(self, storage):
        """acts as placeholder for BinaryNodRef method which stores refs"""
        pass

    @staticmethod
    def referent_to_bytes(referent):
        """
        converts string of referent value to bytes

        NOTE: changed original code to account for other referent types, so forced
        referent into string type to encode into utf-8
        """
        return str(referent).encode('utf-8')

    @staticmethod
    def bytes_to_referent(bytes):
        """converts bytes back to the string of the referent value"""
        return bytes.decode('utf-8')

    
    def get(self, storage):
        """read bytes for value from disk"""
        # read from the address if there is an address but no _referent value
        if self._referent is None and self._address:
            self._referent = self.bytes_to_referent(storage.read(self._address))
        return self._referent

    def store(self, storage):
        """"store bytes for value to disk"""
        #called by BinaryNode.store_refs
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_bytes(self._referent))


class BinaryNodeRef(ValueRef):
    """"
    A reference to a btree node on disk. It is a specialized subclass of ValueRef to 
    serialize/deserialize a BinaryNode

    Parameters
    ----------
    referent : optional
        The value to store (default is None)

    address : int, optional
        Address of the referent (default is 0)
        
    Notes
    -----
    WARNINGS:
        - referent values converted to utf-8 encoded bytes of string 
        of referent when stored to account for different referent types

    Examples
    --------

    """
    
    #calls the BinaryNode's store_refs
    def prepare_to_store(self, storage):
        """have a node store its refs"""
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_bytes(referent):
        """"use pickle to convert node to bytes"""
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
        })

    @staticmethod
    def bytes_to_referent(string):
        """unpickle bytes to get a node object"""
        d = pickle.loads(string)
        return BinaryNode(
            BinaryNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            BinaryNodeRef(address=d['right']),
        )
    
class BinaryNode(object):
    """
    Implements a node in the binary tree
    
    Parameters
    ----------
    left_ref : BinaryNodeRef
        A reference to the left child

    key
        The key component in a key value pair

    value_ref: ValueRef
        A reference to the value that corresponds to key

    right_ref: BinaryNodeRef
        A reference to the right child
    
    Attributes
    ----------
    left_ref
    key
    value_ref
    right_ref

        
    Notes
    -----
          
    Examples
    --------

    """
    @classmethod
    def from_node(cls, node, **kwargs):
        """clone a node with some changes from another one"""
        return cls(
            left_ref=kwargs.get('left_ref', node.left_ref),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=kwargs.get('right_ref', node.right_ref),
        )

    def __init__(self, left_ref, key, value_ref, right_ref):
        """
        Constructor for BinaryNode. Initializes with a `key`, a reference to the value
        given by `value_ref`, a reference to the left child `left_ref`, and a
        reference to the right child `right_ref`.
        """
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref

    def store_refs(self, storage):
        """method for a node to store all of its stuff"""
        self.value_ref.store(storage)
        #calls BinaryNodeRef.store. which calls
        #BinaryNodeRef.prepate_to_store
        #which calls this again and recursively stores
        #the whole tree
        self.left_ref.store(storage)
        self.right_ref.store(storage)

class BinaryTree(object):
    """"
    Immutable Binary Tree class. Constructs new tree on changes

    Parameters
    ----------
    storage : Storage
        A Storage object to manage storage of Binary Tree

    Attributes
    ----------
    _storage : Storage
        a storage object to manage read/write

    _tree_ref : BinaryNodeRef
        refrence to unbalanced bst, created when `self_refresh_tree_ref()` called in constructor

    Notes
    -----
        
    WARNINGS:
        - return type of get for a value will always be a string type
          
    Examples
    --------
    """
    def __init__(self, storage):
        """
        Constructor for BinaryTree class.  Initialized with an instance of Storage 
        given by `storage`. The _refresh_tree_ref method initializes the value `_tree_ref`,
        a reference to the tree root node or root address, which is itself a BinaryNodeRef.
        """
        self._storage = storage
        self._refresh_tree_ref()

    def commit(self):
        """changes are final only when committed"""
        #triggers BinaryNodeRef.store
        self._tree_ref.store(self._storage)
        #make sure address of new tree is stored
        self._storage.commit_root_address(self._tree_ref.address)

    def _refresh_tree_ref(self):
        """get reference to new tree if it has changed"""
        self._tree_ref = BinaryNodeRef(
            address=self._storage.get_root_address())

    def get(self, key):
        """get value for given `key`"""
        #your code here
        #if tree is not locked by another writer
        #refresh the references and get new tree if needed
        if not self._storage.locked:
            self._refresh_tree_ref()
        #get the top level node
        node = self._follow(self._tree_ref)
        #traverse until you find appropriate node
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif key > node.key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def set(self, key, value):
        """set a new value in the tree. will cause a new tree"""

        #try to lock the tree. If we succeed make sure
        #we dont lose updates from any other process
        if self._storage.lock():
            self._refresh_tree_ref()
        #get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        #insert and get new tree ref
        self._tree_ref = self._insert(node, key, value_ref)
        
    
    def _insert(self, node, key, value_ref):
        """insert a new node creating a new path from root"""
        #create a tree ifnthere was none so far
        if node is None:
            new_node = BinaryNode(
                BinaryNodeRef(), key, value_ref, BinaryNodeRef())
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node,
                left_ref=self._insert(
                    self._follow(node.left_ref), key, value_ref))
        elif key > node.key:
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._insert(
                    self._follow(node.right_ref), key, value_ref))
        else: #create a new node to represent this data
            new_node = BinaryNode.from_node(node, value_ref=value_ref)
        return BinaryNodeRef(referent=new_node)

    def delete(self, key):
        """delete node with key given by `key`, creating new tree and path"""
        if self._storage.lock():
            self._refresh_tree_ref()
        node = self._follow(self._tree_ref)
        self._tree_ref = self._delete(node, key)
        
    def _delete(self, node, key):
        """underlying delete implementation. removes the node given by `node` when `key` matches.
        traverses tree until it reaches the matching key."""
        if node is None:
            raise KeyError
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node,
                left_ref=self._delete(
                    self._follow(node.left_ref), key))
        elif key > node.key:
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._delete(
                    self._follow(node.right_ref), key))
        else:
            left = self._follow(node.left_ref)
            right = self._follow(node.right_ref)
            if left and right:
                replacement = self._find_max(left)
                left_ref = self._delete(
                    self._follow(node.left_ref), replacement.key)
                new_node = BinaryNode(
                    left_ref,
                    replacement.key,
                    replacement.value_ref,
                    node.right_ref,
                )
            elif left:
                return node.left_ref
            else:
                return node.right_ref
        return BinaryNodeRef(referent=new_node)

    def _follow(self, ref):
        """get a node from a reference given by `ref`"""
        #calls BinaryNodeRef.get
        return ref.get(self._storage)
    
    def _find_max(self, node):
        """returns the right most node, the maximum"""
        while True:
            next_node = self._follow(node.right_ref)
            if next_node is None:
                return node
            node = next_node


class Storage(object):
    """
    Stoarge class manages access to storage, controlling the reads and writes 
    as well as locking of the storage

    Parameters
    ----------
    f : file name (string)
        Database filename to store the binary tree

    Attributes
    ----------
    _f : string
        filename of the file to store to
    
    locked: bool
        indicator for status of storage lock
        
    Notes
    -----
    WARNINGS:
        - referent values converted to utf-8 encoded bytes of string 
        of referent when stored to account for different referent types
        - return type of get for a value will always be a string type
          
    Examples
    --------

    """
    SUPERBLOCK_SIZE = 4096
    INTEGER_FORMAT = "!Q"
    INTEGER_LENGTH = 8

    def __init__(self, f):
        """
        Constructor for Storage class. Initializes with storage in file `f`,
        initial storage being unlocked, and calls _ensure_superblock method
        to ensure the first write starts on sector boundary.
        """
        self._f = f
        self.locked = False
        #we ensure that we start in a sector boundary
        self._ensure_superblock()

    def _ensure_superblock(self):
        """"guarantee that the next write will start on a sector boundary"""
        self.lock()
        self._seek_end()
        end_address = self._f.tell()
        if end_address < self.SUPERBLOCK_SIZE:
            self._f.write(b'\x00' * (self.SUPERBLOCK_SIZE - end_address))
        self.unlock()

    def lock(self):
        """if not locked, lock the file for writing"""
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False

    def unlock(self):
        """if locked, unlock"""
        if self.locked:
            self._f.flush()
            portalocker.unlock(self._f)
            self.locked = False

    def _seek_end(self):
        """find the end of the storage file"""
        self._f.seek(0, os.SEEK_END)

    def _seek_superblock(self):
        """"go to beginning of file which is on sector boundary"""
        self._f.seek(0)

    def _bytes_to_integer(self, integer_bytes):
        """
        unpacks the string `integer_bytes` to format given by `INTEGER_FORMAT`
        returns corresponding integer value
        """
        return struct.unpack(self.INTEGER_FORMAT, integer_bytes)[0]

    def _integer_to_bytes(self, integer):
        """returns a string with value given by `integer` packed according to format given by `INTEGER_FORMAT`"""
        return struct.pack(self.INTEGER_FORMAT, integer)

    def _read_integer(self):
        """reads next `INTEGER_LENGTH` positions in file and returns its integer value"""
        return self._bytes_to_integer(self._f.read(self.INTEGER_LENGTH))

    def _write_integer(self, integer):
        """writes to storage file value of `integer` in bytes"""
        self.lock()
        self._f.write(self._integer_to_bytes(integer))


    # ?????
    def write(self, data):
        """write data to disk, returning the adress at which you wrote it"""
        #first lock, get to end, get address to return, write size
        #write data, unlock <==WRONG, dont want to unlock here
        #your code here
        self.lock()
        self._seek_end()
        object_address = self._f.tell()
        self._write_integer(len(data))
        self._f.write(data)
        return object_address

    def read(self, address):
        """returns data at the location given by `address`"""
        self._f.seek(address)
        length = self._read_integer()
        data = self._f.read(length)
        return data

    def commit_root_address(self, root_address):
        """write the integer given by `root_address` into storage"""
        self.lock()
        self._f.flush()
        #make sure you write root address at position 0
        self._seek_superblock()
        #write is atomic because we store the address on a sector boundary.
        self._write_integer(root_address)
        self._f.flush()
        self.unlock()

    def get_root_address(self):
        """reads the first integer in the superblock"""
        #your code here
        self._seek_superblock()
        root_address = self._read_integer()
        return root_address

    def close(self):
        """closees the storage file"""
        self.unlock()
        self._f.close()

    @property
    def closed(self):
        """checks if the storage file and returns True if closed"""
        return self._f.closed



class DBDB(object):
    """
    The DBDB class acts as a database, holding the binary tree of all key, value 
    pairs as well as its storage manager

    Parameters
    ----------
    f : string
        Database filename to store the binary tree

    Attributes
    ----------
    _storage : Storage
        storage to be used with `_tree`

    _tree : BinaryTree
        unbalanced binary tree initialized with storage `_storage`
        
    Notes
    -----
    PRE:
        - `key` and `value` must both be of type int, float, or str
        
    WARNINGS:
        - referent values converted to utf-8 encoded bytes of string 
        of referent when stored to account for different referent types
        - return type of `self._tree.get` for will always be a string type
        - `DBDB.get` will always try to convert output to an int or float if possible,
        otherwise it will be left as a string

          
    Examples
    --------

    """

    def __init__(self, f):
        """
        Constructor for DBDB. Initiallizes with storage in file `f` (opened 
        by connect function) and a binary tree created with the initialized storage
        
        Parameters
        ----------
        f : file name (string)
            Database filename to store the binary tree
        """
        self._storage = Storage(f)
        self._tree = BinaryTree(self._storage)

    def _assert_not_closed(self):
        """checks that the database is open, raises error if not"""
        if self._storage.closed:
            raise ValueError('Database closed.')

    def close(self):
        """closes the storage"""
        self._storage.close()

    def commit(self):
        """
        saves the final changes
        calls BinaryTree commit to save
        """
        self._assert_not_closed()
        self._tree.commit()

    def get(self, key):
        """
        returns the final value stored with under key
        calls BinaryTree get to traverse the tree's branches

        if possible, returns an int or a float, but returns 
        a string otherwise.
        """
        self._assert_not_closed()
        result = self._tree.get(key)


        try:
            return int(result)
        except ValueError:
            try:
                return float(result)
            except ValueError:
                return result


    def set(self, key, value):
        """
        assigns a new value to key
        calls BinaryTree set to set the key, value
        """

        # raise an Error of the key or value is not an int/float/string
        if type(key) not in [int,float,str]:
            raise TypeError('Precondition violated: key must be int, float, or str')

        if type(value) not in [int,float,str]:
            raise TypeError('Precondition violated: value must be int, float, or str')

        self._assert_not_closed()
        return self._tree.set(key, value)

    def delete(self, key):
        """
        deletes node with key and its value
        calls BinaryTree delete to delete the node
        """
        self._assert_not_closed()
        return self._tree.delete(key)



def connect(dbname):
    """"
    Opens an existing database file, creating a new one if it 
    does not yet exist, under the name `dbname` and returns instance of DBDB

    Parameters
    ----------
    dbname : string
        name of the database to access, will create if does not exist already
        
    Notes
    -----

    Examples
    --------
    """

    # open database file
    try:
        f = open(dbname, 'r+b')
    # create new one if it does not already exist
    except IOError:
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')

    # return DBDB instance
    return DBDB(f)

if __name__ == "__main__":
    db = connect("/tmp/test.dbdb")
    db.set(1,10)
    db.commit()
    db.close()
    db = connect("/tmp/test.dbdb")
    print(db.get(1))
    print(type(db.get(1)))
    os.remove("/tmp/test.dbdb")

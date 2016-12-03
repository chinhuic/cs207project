# red-black tree
# based off lab 10
# based off Scott Lobdell's implementation of Red-Black trees, given on 
# on http://scottlobdell.me/2016/02/purely-functional-red-black-trees-python/

import pickle
import os
import struct
import portalocker

class Color(object):
    """
    Used to denote the color attribute of a node in the red-black tree
    Attributes
    ----------
    RED
    BLACK
    """
    RED = 0
    BLACK = 1

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
        """
        acts as placeholder for BinaryNodRef method which stores references
        Parameters
        ----------
        storage : Storage
            The storage manager through which we can read, write, lock etc to the file
        
        """
        pass

    @staticmethod
    def referent_to_bytes(referent):
        """
        converts string of referent value to bytes
        
        Parameters
        ----------
        referent : int/float/string, optional
            The value to convert to bytes (default is None)
            
        NOTE: changed original code to account for other referent types, so forced
        referent into string type to encode into utf-8
        """
        return str(referent).encode('utf-8')

    @staticmethod
    def bytes_to_referent(bytes):
        """
        converts bytes back to the string of the referent value
        Parameters
        ----------
        bytes : bytes
            The byte value to be converted to the string of the referent value  
        
        """
        return bytes.decode('utf-8')

    
    def get(self, storage):
        """
        read bytes for value from disk
        Parameters
        ----------
        storage : Storage
            The storage manager through which we can read, write, lock etc to the file
        
        """
        # read from the address if there is an address but no _referent value
        if self._referent is None and self._address:
            self._referent = self.bytes_to_referent(storage.read(self._address))
        return self._referent

    def store(self, storage):
        """
        store bytes for value to disk
        Parameters
        ----------
        storage : Storage
            The storage manager through which we can read, write, lock etc to the file
            
        """
        #called by BinaryNode.store_refs
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_bytes(self._referent))


class BinaryNodeRef(ValueRef):
    """"
    A reference to a rbtree node on disk. It is a specialized subclass of ValueRef to 
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
    """
    
    #calls the BinaryNode's store_refs
    def prepare_to_store(self, storage):
        """
        stores the references of a node
        Parameters
        ----------
        storage : Storage
            The storage manager through which we can read, write, lock etc to the file
        """
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_bytes(referent):
        """
        uses pickle to convert from node to bytes
        Parameters
        ----------
        referent : int/float/string, optional
            The value to convert to bytes 
        """
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
            'color': referent.color
        })

    @staticmethod
    def bytes_to_referent(string):
        """
        unpickle bytes to get a node object
        Parameters
        ----------
        string : bytes
            The byte value to be unpickled to get a node object
        
        """
        d = pickle.loads(string)
        return BinaryNode(
            BinaryNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            BinaryNodeRef(address=d['right']),
            d['color'] 
        )
    
class BinaryNode(object):
    """
    Implements a node in the binary tree
    
    Parameters
    ----------
    left_ref : BinaryNodeRef
        A reference to the left child
    key : int, float, or str
        The key component in a key value pair
    value_ref: ValueRef
        A reference to the value that corresponds to key
    right_ref: BinaryNodeRef
        A reference to the right child
    color : Color
        The color of the node
    
    Attributes
    ----------
    left_ref
    key
    value_ref
    right_ref
    color
    """
    @classmethod
    def from_node(cls, node, **kwargs):
        """
        clone a node with some changes from another one
        Parameters
        ----------
        node : Binary Node
            The node to be cloned with some changes
        kwargs: Keyword argument
            The changes that need to be incorporated into the cloned node
        """
        return cls(
            left_ref=kwargs.get('left_ref', node.left_ref),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=kwargs.get('right_ref', node.right_ref),
            color=kwargs.get('color', node.color)
        )

    def __init__(self, left_ref, key, value_ref, right_ref, color=Color.RED):
        """
        Constructor for BinaryNode. Initializes with a `key`, a reference to the value
        given by `value_ref`, a reference to the left child `left_ref`, a
        reference to the right child `right_ref`, and 'color' which denotes the color of the node.
        Parameters
        ----------
        left_ref : BinaryNodeRef
            A reference to the left child
        key : int, float, or str
            The key component in a key value pair
        value_ref: ValueRef
            A reference to the value that corresponds to key
        right_ref: BinaryNodeRef
            A reference to the right child
        color : Color
            The color of the node, default is RED   
        
        """
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref
        self.color = color

    def blacken(self):
        """makes the color of the node black if it was red, no change otherwise"""
        if self.color == Color.RED:
            self.color = Color.BLACK

    def redden(self):
        """makes the color of the node red if it was black, no change otherwise"""
        if self.color == Color.BLACK:
            self.color = Color.RED

    def is_black(self):
        """
        checks whether the color of the node is black or not.
        Returns 'True' if the node is black, otherwise 'False'
        """
        if self.color == Color.BLACK:
            return True
        else:
            return False

    def is_red(self):
        """
        checks whether the color of the node is red or not.
        Returns 'True' if the color is red, otherwise 'False'
        """
        if self.color == Color.RED:
            return True
        else:
            return False

    def store_refs(self, storage):
        """
        method for a node to store the references to its value and children to the storage denoted by 'storage'
        Parameters
        -----------
        storage : Storage
            The storage manager through which we can read, write, lock etc to the file
        
        """
        self.value_ref.store(storage)
        #calls BinaryNodeRef.store. which calls
        #BinaryNodeRef.prepate_to_store
        #which calls this again and recursively stores
        #the whole tree
        self.left_ref.store(storage)
        self.right_ref.store(storage)


class BinaryTree(object):
    """"
    Immutable Red-Black Binary Tree class. Constructs new tree when any changes are made
    
    Parameters
    ----------
    storage : Storage
        The storage manager through which we can read, write, lock etc to the file
        
    Attributes
    ----------
    _storage : Storage
        a storage object to manage read/write
    _tree_ref : BinaryNodeRef
        refrence to unbalanced bst, created when `self._refresh_tree_ref()` called in constructor
        
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
        Parameters
        ----------
        storage : Storage
            The storage manager through which we can read, write, lock etc to the file
        """
        self._storage = storage
        self._refresh_tree_ref()

    def commit(self):
        """
        Stores the changes that have been made. Any
        changes will be final only when they are committed.
        """
        #triggers BinaryNodeRef.store
        self._tree_ref.store(self._storage)
        #make sure address of new tree is stored
        self._storage.commit_root_address(self._tree_ref.address)

    def _refresh_tree_ref(self):
        """gets reference to the new root of the tree if the structure has changed"""
        self._tree_ref = BinaryNodeRef(
            address=self._storage.get_root_address())

    def get(self, key):
        """
        gets the value associated with the given `key`. Raises an error if 'key' does not exist in the tree. 
        
        Parameters
        ----------
        key : int, float, or str
            The key component in a key value pair
        """
        #your code here
        #if tree is not locked by another writer
        #refresh the references and get new tree if needed
        if not self._storage.locked:
            self._refresh_tree_ref()
        #get the top level node
        node = self._follow(self._tree_ref)
        #traverse until you find appropriate node
        while node is not None:
            # print(node.key, node.color)
            if key < node.key:
                node = self._follow(node.left_ref)
            elif key > node.key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def get_ref(self, key):
        """
        gets the reference for the node in the tree which has the key given by `key`.
        raises a KeyError if the given key is not in the tree
        Parameters
        ----------
        key : int, float, or str
            The key component in a key value pair
        """
        #if tree is not locked by another writer
        #refresh the references and get new tree if needed
        if not self._storage.locked:
            self._refresh_tree_ref()
        #get the top level node
        node = self._follow(self._tree_ref)

        # check if head node
        if node.key == key:
            return self._tree_ref

        #traverse until you find appropriate node
        while node is not None:

            # check if either children are the target node
            L_node = self._follow(node.left_ref)
            R_node = self._follow(node.right_ref)

            if L_node is not None and L_node.key == key:
                return node.left_ref
            elif R_node is not None and R_node.key == key:
                return node.right_ref
            # if not, keep traversing
            else:
                if key < node.key:
                    node = L_node
                elif key > node.key:
                    node = R_node

        # raise error if key is not in tree
        raise KeyError


    def get_parent(self, key):
        """
        gets the parent node of the node with key given by `key`
        returns a tuple of the parent and string 'L' when the child
        node with key is the left child or string 'R' when the child
        node with key is the right child
        raises a KeyError if the key is not in the tree
        returns the reference to the tree if key is of the head node
        Parameters
        ----------
        key : int, float, or str
            The key component in a key value pair
        """

        #if tree is not locked by another writer
        #refresh the references and get new tree if needed
        if not self._storage.locked:
            self._refresh_tree_ref()
        #get the top level node
        node = self._follow(self._tree_ref)

        # check if head node
        if node.key == key:
            return self._tree_ref

        #traverse until you find appropriate child node
        while node is not None:

            # check if either children are the target node
            L_node = self._follow(node.left_ref)
            R_node = self._follow(node.right_ref)

            if L_node is not None and L_node.key == key:
                return node, 'L'
            elif R_node is not None and R_node.key == key:
                return node, 'R'
            # if not, keep traversing
            else:
                if key < node.key:
                    node = L_node
                elif key > node.key:
                    node = R_node
                    
        # raise error if key is not in tree
        raise KeyError

    def set(self, key, value):
        """
        set a new value for a given key in the tree. will create a new tree
        Parameters
        ----------
        key : int, float, or str
            The key component in a key value pair
        value : int, float, or str
            The value component in a key value pair
        Notes
        -----
        - `key` and `value` must both be specified. The method will not work as
        intended unless both key and value are specified.
        """
        #try to lock the tree. If we succeed make sure
        #we dont lose updates from any other process
        if self._storage.lock():
            self._refresh_tree_ref()
        #get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        
        #insert and get new node ref
        self._tree_ref = self._insert(node, key, value_ref)
        # print('----------------')
        # print('inserted ', key)
        # print('- - - - - - - - ')
        
        # get reference for new node added
        new_node_ref = self.get_ref(key)
        
        # update the tree (which will balance tree)
        # call update on the new node added and the head of the tree
        self.update(new_node_ref)
        #self.update(new_node_ref, self._tree_ref)

##        print('--------------------------')
##        print('head after update', self._follow(self._tree_ref).key)
##        print('--------------------------')
##        print('\n')

        # then blacken the head after everything is updated
        self._follow(self._tree_ref).blacken()



    def recolored(self, node_ref):
        """
        makes the node present at `node_ref` red and its children black
        Parameters
        ----------
        node_ref: BinaryNodeRef
            A reference to the node to be colored red, its children will be colored black
        """
        curr_node = self._follow(node_ref)
        L_node = self._follow(curr_node.left_ref)
        R_node = self._follow(curr_node.right_ref)
        
        if L_node is not None:
            L_node.blacken()
        if curr_node is not None:
            curr_node.redden()
        if R_node is not None:
            R_node.blacken()



    def rotate_left(self, node_ref):
        """
        a left rotation occurs at `node_ref`
        no color changes here
        Parameters
        ----------
        node_ref: BinaryNodeRef
            A reference to the node where a left rotation must be carried out     
        """
        # print('rotating left')

        curr_node = self._follow(node_ref)
        R_node = self._follow(curr_node.right_ref)

        # update parent of node_ref to point to the new rotated node
        # update reference to head if it is being rotated
        if node_ref == self._tree_ref:
            # print('changed head to R')
            self._tree_ref = curr_node.right_ref
        # for all non-head nodes
        else:
            # print('changed child to R')
            # find parent
            # update their child ref
            P_node, side = self.get_parent(curr_node.key)
            if side == 'L':
                P_node.left_ref = curr_node.right_ref
            elif side == 'R':
                P_node.right_ref = curr_node.right_ref

        # set right child of current node to left child of R_node
        curr_node.right_ref = R_node.left_ref

        # set left child ref of R_node to current node_ref
        R_node.left_ref = node_ref


    def rotate_right(self, node_ref):
        """
        a right rotation occurs at `node_ref`
        no color change happens
        Parameters
        ----------
        node_ref: BinaryNodeRef
            A reference to the node where a right rotation must be carried out
        """
        # print('rotating right')
        curr_node = self._follow(node_ref)
        L_node = self._follow(curr_node.left_ref)

        # update parent of node_ref to point to the new rotated node
        # update reference to head if it is being rotated
        if node_ref == self._tree_ref:
            # print('changed head to L')
            self._tree_ref = curr_node.left_ref
        # for all non-head nodes
        else:
            # print('changed child to L')
            # find parent
            # update their child ref
            P_node, side = self.get_parent(curr_node.key)
            if side == 'L':
                P_node.left_ref = curr_node.left_ref
            elif side == 'R':
                P_node.right_ref = curr_node.left_ref

        # set left child of curr_node to right child of L_node
        curr_node.left_ref = L_node.right_ref

        # set right child of L_node to nod_ref
        L_node.right_ref = node_ref

    # reassign pointers
    def balance(self, node_ref):
        """
        balance the tree at the node given at `node_ref`
        color changes of nodes are dealt with here
        Parameters
        ----------
        node_ref: BinaryNodeRef
            A reference to the node where the tree must be balanced
        """

        curr_node = self._follow(node_ref)

        # stop if no further node
        if curr_node is None:
            return

        # print('balance on',curr_node.key)

        L_node = self._follow(curr_node.left_ref)
        R_node = self._follow(curr_node.right_ref)


        # if current node is red
        if curr_node.is_red():
            # print('it is red')
            return

        # print('it is black')
        # continues if it is black
        # if left node is red
        if L_node is not None and L_node.is_red():
            LofL = self._follow(L_node.left_ref)
            RofL = self._follow(L_node.right_ref)

            # if its left child is red
            if LofL is not None and LofL.is_red():
                # when the uncle is also red
                if R_node is not None and R_node.is_red():
                    self.recolored(node_ref)
                    return
                # uncle is not red
                else:
                    self.rotate_right(node_ref)
                    curr_node.redden()
                    L_node.blacken()
                    return

            # if its right child is red
            elif RofL is not None and RofL.is_red():
                # check the uncle
                if R_node is not None and R_node.is_red():
                    self.recolored(node_ref)
                    return
                else:
                    self.rotate_left(curr_node.left_ref)
                    self.rotate_right(node_ref)
                    curr_node.redden()
                    RofL.blacken()
                    return
                    

        # if right child is red
        if R_node is not None and R_node.is_red():
            LofR = self._follow(R_node.left_ref)
            RofR = self._follow(R_node.right_ref)

            # if its right child is also red
            if RofR is not None and RofR.is_red():
                # check uncle
                if L_node is not None and L_node.is_red():
                    self.recolored(node_ref)
                    return
                else:
                    self.rotate_left(node_ref)
                    curr_node.redden()
                    R_node.blacken()
                    return

            # if its left child is also red
            elif LofR is not None and LofR.is_red():
                # check uncle
                if L_node is not None and L_node.is_red():
                    self.recolored(node_ref)
                    return
                else:
                    self.rotate_right(curr_node.right_ref)
                    self.rotate_left(node_ref)
                    curr_node.redden()
                    LofR.blacken()
                    return



    def update(self, node_ref):
        """
        balances starting from the newly inserted node at `node_ref`,
        then balances each level above until the whole tree is balanced
        no direct color changes occur here, they occur when calls are made to balance
        Parameters
        ----------
        node_ref: BinaryNodeRef
            A reference to the node from where the balancing of the tree must begin
        """

        # start at inserted node and work way up parents
        key = self._follow(node_ref).key
        curr_ref = node_ref

        # go through every level of tree starting from the bottom
        while self._tree_ref != curr_ref:

            curr_node = self._follow(curr_ref)

            # first save reference to the level above
            P_node, __ = self.get_parent(curr_node.key)

            if self._follow(self._tree_ref).key != P_node.key:
                GP_node, side = self.get_parent(P_node.key)

                if side == 'L':
                    P_ref = GP_node.left_ref
                elif side == 'R':
                    P_ref = GP_node.right_ref
            else:
                P_ref = self._tree_ref

            # balance branch that key is in
            if key < curr_node.key:
                self.balance(curr_node.left_ref)
            else:
                self.balance(curr_node.right_ref)

            # then balance current tree
            if key < P_node.key:
                self.balance(P_node.left_ref)
            else:
                self.balance(P_node.right_ref)

            # move up level
            curr_ref = P_ref


        # when it is at the head, do one final balance round
        # balance branch that key is in
        curr_node = self._follow(curr_ref)

        if key < curr_node.key:
            self.balance(curr_node.left_ref)
        else:
            self.balance(curr_node.right_ref)

        # then balance current tree
        self.balance(self._tree_ref)

    
    
    def _insert(self, node, key, value_ref):
        """
        inserts a new node creating a new path from root
        returns the head of the new tree created
        Parameters
        ----------
        node : BinaryNode
            The node to be inserted 
        key : int, float, or str
            The key component in a key value pair
        value_ref : BinaryNodeRef
            A reference to the value associated with the node
            
        """
        # recursively inserts node after node to build entire tree
        # create a tree if there was none so far
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

        # return the reference to the head node of the new tree
        return BinaryNodeRef(referent=new_node)



    def delete(self, key):
        """
        deletes the node with key given by `key`, creating a new tree and path
        Parameters
        ----------
        key : int, float, or str
            The key component in a key value pair
        """
        if self._storage.lock():
            self._refresh_tree_ref()
        node = self._follow(self._tree_ref)
        self._tree_ref = self._delete(node, key)
        
    def _delete(self, node, key):
        """
        the underlying delete implementation.
        removes the node given by `node` when `key` matches.
        traverses the tree until it reaches the matching key.
        Parameters
        ----------
        node : BinaryNode
            The node to be deleted 
        key : int, float, or str
            The key component in a key value pair
        """
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
        """
        gets a node from the reference given by `ref`
        Parameters
        ----------
        ref : BinaryNodeRef
            A reference to the desired node 
        """
        #calls BinaryNodeRef.get
        return ref.get(self._storage)
    
    def _find_max(self, node):
        """
        returns the right most node, the maximum, of 'node''s children 
        Parameters
        ----------
        node: BinaryNode
             The node whose branch we want to find the maximum of  
        """
        while True:
            next_node = self._follow(node.right_ref)
            if next_node is None:
                return node
            node = next_node
        


class Storage(object):
    """
    Stoarge class manages the access to storage, controlling the reads and writes 
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
    """
    SUPERBLOCK_SIZE = 4096
    INTEGER_FORMAT = "!Q"
    INTEGER_LENGTH = 8

    def __init__(self, f):
        """
        Constructor for Storage class. Initializes with storage in file `f`,
        initial storage being unlocked, and calls _ensure_superblock method
        to ensure the first write starts on sector boundary.
        Parameters
        ----------
        f : String
            The name of the database file used for storage 
        """
        self._f = f
        self.locked = False
        #we ensure that we start in a sector boundary
        self._ensure_superblock()

    def _ensure_superblock(self):
        """"guarantees that the next write will start on a sector boundary"""
        self.lock()
        self._seek_end()
        end_address = self._f.tell()
        if end_address < self.SUPERBLOCK_SIZE:
            self._f.write(b'\x00' * (self.SUPERBLOCK_SIZE - end_address))
        self.unlock()

    def lock(self):
        """if not locked, then lock the file for writing"""
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False

    def unlock(self):
        """if file is locked, then unlock it"""
        if self.locked:
            self._f.flush()
            portalocker.unlock(self._f)
            self.locked = False

    def _seek_end(self):
        """finds the end of the storage file"""
        self._f.seek(0, os.SEEK_END)

    def _seek_superblock(self):
        """"goes to beginning of the file which is on sector boundary"""
        self._f.seek(0)

    def _bytes_to_integer(self, integer_bytes):
        """
        unpacks the string `integer_bytes` to format given by `INTEGER_FORMAT`
        returns the corresponding integer value
        Parameters
        ----------
        integer_bytes : String 
            the value to be converted to the corresponding integer value
        
        """
        return struct.unpack(self.INTEGER_FORMAT, integer_bytes)[0]

    def _integer_to_bytes(self, integer):
        """
        returns a string with value given by `integer` packed according to format given by `INTEGER_FORMAT`
        Parameters
        ----------
        integer : Int
            the integer value to be converted to string 
        
        """
        return struct.pack(self.INTEGER_FORMAT, integer)

    def _read_integer(self):
        """reads next `INTEGER_LENGTH` positions in file and returns its integer value"""
        return self._bytes_to_integer(self._f.read(self.INTEGER_LENGTH))

    def _write_integer(self, integer):
        """
        writes to storage file the value of `integer` in bytes
        Parameters
        ----------
        integer : Int
            the integer to be written to the stoage file in bytes
        
        """
        self.lock()
        self._f.write(self._integer_to_bytes(integer))

    def write(self, data):
        """
        writes data to disk, and returns the adress at which it was written
        Parameters
        ----------
        data 
            The information to be written to the disk
    
        """
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
        """
        returns the data at the location given by `address`
        Parameters
        ----------
        address : Int
            The index in the file from where the data needs to be read 
        """
        self._f.seek(address)
        length = self._read_integer()
        data = self._f.read(length)
        return data

    def commit_root_address(self, root_address):
        """
        writes the integer given by `root_address` into storage
        Parameters
        ----------
        root_address : Int
            the integer to be written into storage
        
        """
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
        """checks whether the storage file is closed or not. returns 'True' if closed, else 'False'"""
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
        returns the final stored value associated with 'key'
        calls BinaryTree get() to traverse the tree's branches
        if possible, returns an int or a float, but returns 
        a string otherwise.
        Raises an error if 'key' does not exist in the tree. 
        Parameters
        ----------
        key : int, float, or str
            The key component in a key value pair
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
        assigns a new value, denoted by 'value', to 'key'
        calls BinaryTree set() to set the new value of the given key
        Parameters
        ----------
        key : int, float, or str
            The key component in a key value pair
        value : int, float, or str
            The value component in a key value pair
        Notes
        -----
        `key` and `value` must both be specified. The method will not work as intended unless both key and value are specified.
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
        deletes node whose key is given by 'key' and its value
        calls the BinaryTree delete method to delete the node
        Parameters
        ----------
        key : int, float, or str
            The key component in a key value pair
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

"""
if __name__ == "__main__":
    db = connect('scratch.dbdb')
    
    # example tree
    # db.set(7,'x')
    # db.set(3,'x')
    # db.set(18,'x')
    # db.set(10,'x')
    # db.set(22,'x')
    # db.set(8,'x')
    # db.set(11,'x')
    # db.set(26,'x')
    # db.set(12,'x')
    # db.get(11)
    # db.set(3,'x')
    # db.set(7,'x')
    # db.set(18,'x')
    # db.set(22,'x')
    # db.set(20,'x')
    
    # db.set(23,'x')
    db.set(0,'x')
    db.set(1,'x')
    db.set(2,'x')
    db.set(3,'x')
    db.set(4,'x')
    db.set(5,'x')
    db.get(5)
    print('\n')
    #db.get(18)
    
    db.commit()
    db.close()
    # reopen
    db = connect('scratch.dbdb')
    db.get(5)
    db.close()
    
    os.remove('scratch.dbdb')
"""

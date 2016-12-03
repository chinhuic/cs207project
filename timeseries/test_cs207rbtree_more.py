import unittest
from cs207rbtree import *

class TestCS207BST(unittest.TestCase):
    # input types
    def test_string_key_and_string_value(self):
        db = connect("/tmp/test.dbdb")
        db.set('a','apple')
        db.commit()
        db.close()
        db = connect("/tmp/test.dbdb")

      
        self.assertEqual(db.get('a'),'apple')
        

        db.close()
        os.remove("/tmp/test.dbdb")

    def test_int_key_and_int_value(self):
        db = connect("/tmp/test.dbdb")
        db.set(5,42)
        db.commit()
        db.close()
        db = connect("/tmp/test.dbdb")

    
        self.assertEqual(db.get(5),42)

        db.close()
        os.remove("/tmp/test.dbdb")

    def test_float_key_and_float_value(self):
        db = connect("/tmp/test.dbdb")
        db.set(5.7,42.10)
        db.commit()
        db.close()
        db = connect("/tmp/test.dbdb")

     
        self.assertEqual(db.get(5.7),42.10)

        db.close()
        os.remove("/tmp/test.dbdb")

    def test_string_key_and_int_value(self):
        db = connect("/tmp/test.dbdb")
        db.set('a',42)
        db.commit()
        db.close()
        db = connect("/tmp/test.dbdb")

           
        self.assertEqual(db.get('a'),42)

        db.close()
        os.remove("/tmp/test.dbdb")

    def test_int_key_and_string_value(self):
        db = connect("/tmp/test.dbdb")
        db.set(5,'apple')
        db.commit()
        db.close()
        db = connect("/tmp/test.dbdb")

        self.assertEqual(db.get(5),'apple')

        db.close()
        os.remove("/tmp/test.dbdb")

    def test_tuple_key(self):
        db = connect("/tmp/test.dbdb")


        with self.assertRaises(TypeError):
            db.set((1,2),5)
        db.close()
        os.remove("/tmp/test.dbdb")

    # return types

    def test_numerical_string_key(self):
        db = connect("/tmp/test.dbdb")
        db.set('20',42)
        db.commit()
        db.close()
        db = connect("/tmp/test.dbdb")
    
   
        self.assertEqual(db.get('20'),42)

        db.close()
        os.remove("/tmp/test.dbdb")

    def test_numerical_string_value(self):
        db = connect("/tmp/test.dbdb")
        db.set(5,'42')
        db.commit()
        db.close()
        db = connect("/tmp/test.dbdb")

     
        self.assertTrue(type(db.get(5))==int)
        self.assertEqual(str(db.get(5)),'42')

        db.close()
        os.remove("/tmp/test.dbdb")

    def test_tuple_value(self):
        db = connect("/tmp/test.dbdb")
        
        
        with self.assertRaises(TypeError):
            db.set(5,(1,2))
        db.close()
        os.remove("/tmp/test.dbdb")

    # values before and after commiting
    def test_lost_values_by_no_commit(self):
        db = connect("/tmp/test.dbdb")
        db.set('a','apple')
        db.close()
        db = connect("/tmp/test.dbdb")

        
        with self.assertRaises(KeyError):
            db.get('a')
        db.close()
        os.remove("/tmp/test.dbdb")
        
        
    def test_get_without_inserting(self):
        db = connect("/tmp/test.dbdb")
        # db.set('a','apple')
        db.close()
        db = connect("/tmp/test.dbdb")


        with self.assertRaises(KeyError):
            db.get('a')
        db.close()
        os.remove("/tmp/test.dbdb")


    def test_get_parent(self):
        db = connect("/tmp/test.dbdb")
        db.set(0,'a')
        db.set(5.7,42.10)
        db.set(5,'apple')
        db.set(4,82)
        db.set('a',42)
        db.commit()
        db.close()
        db = connect("/tmp/test.dbdb")

        
        # using get_parent to check if the nodes have the correct parents
        parent, side = db._tree.get_parent(0)
        self.assertEqual(parent.key,5)
        self.assertEqual(side,'L')
        parent, side = db._tree.get_parent('a')
        self.assertEqual(parent.key,5.7)
        self.assertEqual(side,'R')
        db.close()
        os.remove("/tmp/test.dbdb")

    def test_get_parent_of_root(self):
        db = connect("/tmp/test.dbdb")
        db.set(0,'a')
        db.set(1,'b')
        db.set(2,'c')
        db.set(3,'d')
        db.set(4,'e')
        db.set(5,'f')
        db.commit()
        db.close()
        
        db = connect("/tmp/test.dbdb")
        parent = db._tree.get_parent(1)
        db.close()
        os.remove("/tmp/test.dbdb")

        
    def test_one_balancing(self):
        # one rotation at a time
        # creates the tree
        # without balancing, 2 should have been the parent of 3
        # after balancing, 1 is now the parent of 3

     
        db = connect("/tmp/test.dbdb")
        db.set(0,'a')
        db.set(1,'b')
        db.set(2,'c')
        db.set(3,'d')
        db.set(4,'e')
        db.set(5,'f')
        db.commit()
        db.close()
        db = connect("/tmp/test.dbdb")

        # using get_parent to check if tree has been balanced correctly
        # checking that 3 is now the right child of 1
        parent, side = db._tree.get_parent(3)
        self.assertEqual(parent.key,1)
        self.assertEqual(side,'R')

        db.close()
        os.remove("/tmp/test.dbdb")

    def test_two_balancing(self):
        # one rotation directly followed by another rotation
        # creates the tree
        # without balancing, 7 should have been the parent of 18, and 18 should have been the parent of 10
        # after balancing, 10 is now the parent of 7 and 18
        db = connect("/tmp/test.dbdb")
        db.set(7,'x')
        db.set(3,1)
        db.set(18,'a')
        db.set(10,'z')
        db.set(22,'hello')
        db.set(8,'x')
        db.set(11,'m')
        db.set(26,'p')
        db.set(12,23)
        db.commit()
        db.close()

        db = connect("/tmp/test.dbdb")
     
        # using get_parent to check if tree has been balanced correctly
        parent, side = db._tree.get_parent(7)
        # checking that 7 is now the left child of 10
        self.assertEqual(parent.key,10)
        self.assertEqual(side,'L')
        #self.assertEqual(str(side),'L')

        # using get_parent to check if tree has been balanced correctly
        parent, side = db._tree.get_parent(18)
        # checking that 18 is now the right child of 10
        self.assertEqual(parent.key,10)
        self.assertEqual(side,'R')
        #self.assertEqual(str(side),'R')

        db.close()
        os.remove("/tmp/test.dbdb")               


    def test_balance_after_update(self):
                
        db = connect("/tmp/test.dbdb")
        db.set(7,'x')
        db.set(3,'x')
        db.set(18,'x')
        db.set(10,'x')
        db.set(22,'x')
        db.set(8,'x')
        db.set(11,'x')
        db.set(26,'x')
        db.set(12,'x')
        db.commit()
        db.close()

        db = connect("/tmp/test.dbdb")
      
        db.set(27,'j')
                
        # after balancing, parent of 22 should change from 18 to 26
        # using get_parent to check if tree has been balanced correctly
        parent, side = db._tree.get_parent(22)
        # checking that 22 is now the left child of 26
        self.assertEqual(parent.key,26)
        self.assertEqual(side,'L')
        #self.assertEqual(str(side),'L')

        # after balancing, 26 should be the right child of 18
        # using get_parent to check if tree has been balanced correctly
        parent, side = db._tree.get_parent(26)
        # checking that 26 is now the right child of 18
        self.assertEqual(parent.key,18)
        self.assertEqual(side,'R')
        #self.assertEqual(str(side),'R')
    
        db.close()
        os.remove("/tmp/test.dbdb")


    def test_delete(self):
        db = connect("/tmp/test.dbdb")
        db.set(0,'a')
        db.set(1,'b')
        db.set(2,'c')
        db.set(3,'d')
        db.set(4,'e')
        db.set(5,'f')
        db.commit()
        db.close()
        db = connect("/tmp/test.dbdb")

        db.delete(4)
                
        # using get_parent to check if the nodes have the correct parents
        parent, side = db._tree.get_parent(5)
        self.assertEqual(parent.key,3)
        self.assertEqual(side,'R')
        db.close()
        os.remove("/tmp/test.dbdb")

    def test_delete_and_rebalance(self):
        db = connect("/tmp/test.dbdb")
        db.set(0,'a')
        db.set(1,'b')
        db.set(2,'c')
        db.set(3,'d')
        db.set(4,'e')
        db.set(5,'f')
        db.commit()
        db.close()
        db = connect("/tmp/test.dbdb")

        db.delete(2)
                
        # using get_parent to check if the nodes have the correct parents
        parent, side = db._tree.get_parent(5)
        self.assertEqual(parent.key,4)
        self.assertEqual(side,'R')
               
        parent, side = db._tree.get_parent(0)
        self.assertEqual(parent.key,1)
        self.assertEqual(side,'L')
    
        db.close()
        os.remove("/tmp/test.dbdb")

        """
        def test_recolored(self):
                        
                 # working on this
                 
        db = connect("/tmp/test.dbdb")
        db.set(0,'a')
        db.set(5.7,42.10)
        db.set(5,'apple')
        db.set(4,82)
        db.set('a',42)
        db.commit()
        db.close()
        db = connect("/tmp/test.dbdb")

        # using get_parent to check if tree has been balanced correctly
        # checking that 3 is now the right child of 1
        parent, side = db._tree.get_parent(0)
        self.assertEqual(parent.key,5)
        self.assertEqual(side,'L')
        parent, side = db._tree.get_parent('a')
        self.assertEqual(parent.key,5.7)
        self.assertEqual(side,'R')
        db.close()
        os.remove("/tmp/test.dbdb")


    def test_color(self):
        # checking whether the color of the nodes is correct or not
        # for instance, 10 (the root) should be black, and 12 should be red
                
        db = connect("/tmp/test.dbdb")
        db.set(0,'a')
        db.set(1,'b')
        db.set(2,'c')
        db.set(3,'d')
        db.set(4,'e')
        db.set(5,'f')
        db.commit()
        db.close()
        db = connect("/tmp/test.dbdb")

        col = db._tree.color()
        # col = db._tree.get(0).is_black()
        self.assertEqual(col, 1)

        db.close()
        os.remove("/tmp/test.dbdb")
        
    """

        

if __name__ == '__main__':
    unittest.main()

import unittest
from cs207bst import *

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



if __name__ == '__main__':
    unittest.main()
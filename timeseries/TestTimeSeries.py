from TimeSeries import TimeSeries
from pytest import raises
import numpy as np
import unittest


# testing the TimeSeries class
class TestTimeSeries(unittest.TestCase):

	# __init__
	
	# types of sequences
	def test_arg_type_range(self):
		self.assertEqual(TimeSeries(range(0,3)).value, [0,1,2])

	def test_arg_type_string(self):
		self.assertEqual(TimeSeries('time').value, ['t','i','m','e'])

	def test_arg_type_tuple(self):
		self.assertEqual(TimeSeries((1,42,3,10)).value, [1,42,3,10])

	def test_arg_type_list_of_tuples(self):
		self.assertEqual(TimeSeries([(1,2),(3,4),(5,6)]).value, [(1,2),(3,4),(5,6)])

	# number of arguments
	def test_omitted_arg(self):
		with self.assertRaises(TypeError):
			x = TimeSeries()

	def test_multiple_args(self):
		with self.assertRaises(TypeError):
			x = TimeSeries(1,2,3)

	# series length
	def test_no_data_value(self):
		self.assertEqual(TimeSeries([]).value, [])

	def test_one_data_value(self):
		self.assertEqual(TimeSeries([1]).value, [1])

	def test_multiple_data_values(self):
		self.assertEqual(TimeSeries([1,2,3]).value, [1,2,3])


	# __len__

	def test_length_zero(self):
		self.assertEqual(len(TimeSeries([])), 0)

	def test_length_nonzero(self):
		self.assertEqual(len(TimeSeries([8,12,42])), 3)


	
	# __getitem__

	def test_getitem_index_in_series(self):
		x = TimeSeries([2,4,6,8,10,12])
		self.assertEqual(x[3], 8)

	def test_getitem_large_index_outside_boundary(self):
		x = TimeSeries([2,4,6,8,10,12])
		with self.assertRaises(IndexError):
			x[10]

	def test_getitem_negative_index(self):
		x = TimeSeries([2,4,6,8,10,12])
		self.assertEqual(x[-1], 12)


	#### __setitem__
	def test_setitem(self):
		x = TimeSeries([2,4,6,8,10,12])
		x[2] = 7
		self.assertEqual(x.value, [2,4,7,8,10,12])

	#### __repr__ and __str__ ?




if __name__ == '__main__':
    unittest.main()





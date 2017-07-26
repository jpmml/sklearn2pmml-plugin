from com.mycompany import Aggregator, PowerFunction
from unittest import TestCase

import numpy

class AggregatorTest(TestCase): 

	def test_min(self):
		X = numpy.asarray([1, 0.5, 2, 3.0, 0, 1.0])
		min = Aggregator(function = "min")
		X = X.reshape((1, 6))
		self.assertEqual(0, min.transform(X))
		X = X.reshape((3, 2))
		self.assertEqual([0.5, 2, 0], min.transform(X).tolist())
		X = X.reshape((2, 3))
		self.assertEqual([0.5, 0], min.transform(X).tolist())
		X = X.reshape((6, 1))
		self.assertEqual([1, 0.5, 2, 3.0, 0, 1.0], min.transform(X).tolist())

class PowerTransformerTest(TestCase):

	def test_power(self):
		X = numpy.asarray([-2, -1, 0, 1, 2])
		pow = PowerFunction(power = 1)
		self.assertEquals(X.tolist(), pow.transform(X).tolist())
		pow = PowerFunction(power = 2)
		self.assertEquals([4, 1, 0, 1, 4], pow.transform(X).tolist())
		pow = PowerFunction(power = 3)
		self.assertEquals([-8, -1, 0, 1, 8], pow.transform(X).tolist())

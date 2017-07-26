from sklearn.base import TransformerMixin

import numpy

class Aggregator(TransformerMixin):

	def __init__(self, function):
		functions = ["min", "max", "mean"]
		if function not in functions:
			raise ValueError("Function {0} not in {1}".format(function, functions))
		self.function = function

	def fit(self, X, y = None):
		return self

	def transform(self, X, y = None):
		if self.function == "min":
			return numpy.amin(X, axis = 1) 
		elif self.function == "max":
			return numpy.amax(X, axis = 1)
		elif self.function == "mean":
			return numpy.mean(X, axis = 1)
		return X

class PowerFunction(TransformerMixin):

	def __init__(self, power):
		if not isinstance(power, int):
			raise ValueError("Power {0} is not an integer".format(power))
		self.power = power

	def fit(self, X, y = None):
		return self

	def transform(self, X, y = None):
		return numpy.power(X, self.power)

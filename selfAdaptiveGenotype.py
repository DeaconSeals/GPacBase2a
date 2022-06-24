from binaryGenotype import binaryGenotype
import random

class selfAdaptiveGenotype(binaryGenotype):
	def __init__(self):
		super().__init__()
		self.parameter = None

	def randomInitialization(self, min_parameter, max_parameter, **kwargs):
		super().randomInitialization(**kwargs)
		if min_parameter > max_parameter:
			min_parameter, max_parameter = max_parameter, min_parameter
		# TODO: assign self.parameter a value uniform randomly between
		# min_parameter and max_parameter
		pass

	def recombine(self, mate, **kwargs):
		child = selfAdaptiveGenotype()
		child.gene = super().recombine(mate, **kwargs).gene
		# TODO: assign child.parameter a value from self.parameter or
		# mate.parameter
		pass

		return child

	def mutate(self, **kwargs):
		copy = selfAdaptiveGenotype()
		copy.gene = super().mutate(**kwargs).gene
		copy.parameter = self.parameter
		# TODO: assign copy.parameter a modified value
		pass

		return copy

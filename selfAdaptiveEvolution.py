from baseEvolution import baseEvolutionPopulation
import random

class selfAdaptiveEvolutionPopulation(baseEvolutionPopulation):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.mutation_rate = None

	def generate_children(self):
		children = list()

		# TODO: Select parents
		pass

		# TODO: Recombine parents to generate children
		pass

		# TODO: Mutate children based on child.mutation_rate
		pass

		return children
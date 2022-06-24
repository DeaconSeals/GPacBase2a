class binaryGenotype():
	def __init__(self):
		self.fitness = None
		self.gene = None

	def randomInitialization(self, length):
		# TODO: Add random initialization of fixed-length binary gene
		pass

	def recombine(self, mate, method, **kwargs):
		child = binaryGenotype()
		
		# TODO: Recombine genes of self with mate and assign to child's gene member variable
		assert method.casefold() in {'uniform', '1-point crossover', 'multi-dimensional'}
		if method.casefold() == 'uniform':
			# perform uniform recombination
			pass
		elif method.casefold() == '1-point crossover':
			# perform 1-point crossover
			pass
		elif method.casefold() == 'multi-dimensional':
			# this is a red deliverable (i.e., bonus for anyone)
			
			height, width = kwargs['height'], kwargs['width']
			# transform the linear gene of both parents to a 2-dimensional representation.
			# Recombine 2D parent genes into 2D child gene using the method of your choice.
			# Convert child gene back down to 1-dimension.
			pass

		return child

	def mutate(self, **kwargs):
		copy = binaryGenotype()
		copy.gene = self.gene.copy()
		
		# TODO: mutate gene of copy
		pass

		return copy

	@classmethod
	def initialization(cls, mu, *args, **kwargs):
		population = [cls() for _ in range(mu)]
		for i in range(len(population)):
			population[i].randomInitialization(*args, **kwargs)
		return population
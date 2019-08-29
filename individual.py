import numpy.random as rd

class Individual(object):
	
	def __init__(self):
		self.phenotypicValues = None
		self.currentDeme = None
		self.resourcesAmount = None
		self.fertilityValue = None
		self.offspringNumber = None

	def mutate(self, mutRate, mutStep):
		self.mutant = bool(rd.binomial(1,mutRate))
		
		if self.mutant:
			self.mutationDeviation = rd.normal(0,mutStep)
		else:
			self.mutationDeviation = 0
		return 0.5
		
	def migrate(self):
		pass
	
	def reproduce(self):
		pass
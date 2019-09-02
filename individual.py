import numpy.random as rd
from operator import add

class Individual(object):
	
	def __init__(self):
		self.phenotypicValues = None
		self.currentDeme = None
		self.resourcesAmount = None
		self.fertilityValue = None
		self.offspringNumber = None

	def mutate(self, mutRate, mutStep):
		self.mutant = bool(rd.binomial(1,mutRate))
		self.deviate(mutStep, len(self.phenotypicValues))
		
		tmpPhenotypicValues = list(map(add, self.phenotypicValues, self.mutationDeviation))
		self.phenotypicValues = list(map(lambda x: min(max(x,float(0)),float(1)), tmpPhenotypicValues))
	
	def deviate(self, mutStep, n):
		if self.mutant:
			self.mutationDeviation = rd.normal(0,mutStep,n).tolist()
		else:
			self.mutationDeviation = [0] * n
		
	def migrate(self):
		self.destinationDeme = rd.randint(100)
	
	def reproduce(self):
		pass
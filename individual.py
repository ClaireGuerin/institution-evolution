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
		self.mutant = bool(rd.binomial(1, mutRate))
		self.deviate(mutStep, len(self.phenotypicValues))
		self.applyMutation(self.mutationDeviation)
	
	def deviate(self, ms, n):
		if self.mutant:
			dev = rd.normal(0,ms,n).tolist()
		else:
			dev = [0] * n
		self.mutationDeviation = dev
		
	def applyMutation(self, dev):
		phen = self.phenotypicValues
		unboundedphen = list(map(add, phen, dev))
		boundedphen = list(map(lambda x: min(max(x,float(0)),float(1)), unboundedphen))
		self.unboundedPhenotypicValues = unboundedphen
		setattr(self, "phenotypicValues", boundedphen)
		
	def migrate(self, nDemes, migRate):
		self.migrant = bool(rd.binomial(1, migRate))
		
		if self.migrant:
			self.destinationDeme = int(rd.choice(self.neighbours))
		else:
			self.destinationDeme = self.currentDeme
			
		setattr(self, "currentDeme", self.destinationDeme)
	
	def reproduce(self):
		self.fertilityValue = float(0)
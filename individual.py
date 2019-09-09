import numpy.random as rd
from operator import add
import fitness

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
	
	def reproduce(self, fun_name="pgg", **kwargs):
		self.fertility(fun_name, **kwargs)
		self.procreate()
		
		self.offspring = []
		for offspring in range(self.offspringNumber):
			newOffspringInstance = Individual()
			setattr(newOffspringInstance, "currentDeme", self.currentDeme)
			setattr(newOffspringInstance, "phenotypicValues", self.phenotypicValues)
			setattr(newOffspringInstance, "resourcesAmount", self.resourcesAmount)
			setattr(newOffspringInstance, "neighbours", self.neighbours)
			self.offspring.append(newOffspringInstance)
		
	def fertility(self, fun_name="pgg", **kwargs):
		self.fertilityValue = float(fitness.functions[fun_name](self.resourcesAmount, **kwargs))
		
	def procreate(self):
		self.offspringNumber = rd.poisson(self.fertilityValue)
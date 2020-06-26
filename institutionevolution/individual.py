import numpy.random as rd
from operator import add
import institutionevolution.fitness as fitness
import institutionevolution.production as production

class Individual(object):
	
	def __init__(self):
		self.phenotypicValues = None
		self.currentDeme = None
		self.resourcesAmount = None
		self.fertilityValue = None
		self.offspringNumber = None
		self.cheater = None
		self.punished = None
		self.punishmentFee = None
		self.leader = None 
		self.consensusTime = None
		self.productionTime = None

	def mutate(self, mutRate, mutStep, bounded = True):
		self.mutant = bool(rd.binomial(1, mutRate))
		self.deviate(mutStep, len(self.phenotypicValues))
		self.applyMutation(self.mutationDeviation, bounded)
	
	def deviate(self, ms, n):
		if self.mutant:
			dev = rd.normal(0,ms,n).tolist()
		else:
			dev = [0] * n
		self.mutationDeviation = dev
		
	def applyMutation(self, dev, bounded):
		phen = self.phenotypicValues
		unboundedphen = list(map(add, phen, dev))
		if bounded == False:
			setattr(self, "phenotypicValues", unboundedphen)
		else:
			boundedphen = list(map(lambda x: min(max(x,0.0),1.0), unboundedphen))
			self.unboundedPhenotypicValues = unboundedphen
			setattr(self, "phenotypicValues", boundedphen)
		
	def migrate(self, nDemes, migRate):
		self.migrant = bool(rd.binomial(1, migRate))
		
		if self.migrant:
			self.destinationDeme = int(rd.choice(self.neighbours))
		else:
			self.destinationDeme = self.currentDeme
			
		setattr(self, "currentDeme", self.destinationDeme)

	def ascend(self, leadProp):
		self.leader = bool(rd.binomial(1,leadProp))
	
	def reproduce(self, fun_name="pgg", **kwargs):
		self.produceResources(fun_name, **kwargs)
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
		assert type(kwargs["n"]) is int, "group size of deme {0} is {1}".format(self.currentDeme, kwargs["n"])
		assert type(kwargs["x"][0]) is float, "phenotype of individual in deme {0} is {1}".format(self.currentDeme, kwargs["x"])
		assert type(kwargs["xmean"][0]) is float, "mean phenotype in deme {0} is {1}".format(self.currentDeme, kwargs["xmean"])

		self.fertilityValue = float(fitness.functions[fun_name](self.resourcesAmount, **kwargs))
		
	def procreate(self):
		self.offspringNumber = rd.poisson(max(0,self.fertilityValue))

	def produceResources(self, fun_name="pgg", **kwargs):
		tmpRes = float(production.functions[fun_name](self.resourcesAmount,**{**{'productivity': self.productionTime},**kwargs}))
		self.resourcesAmount = tmpRes
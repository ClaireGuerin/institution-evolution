import pytest
from individual import Individual as Ind
from deme import Deme as Dem
from main import Population as Pop
import scipy.stats as scistats
from operator import add
import random
from statistics import mean
import gc
import fitness
import numpy.random as rd
from collections import Counter
import math as m


class TestReproductionFunction(object):
	
	def test_individual_has_resources_not_none(self, instantiateSingleIndividualPopulation):
		self.ind = instantiateSingleIndividualPopulation
		assert self.ind.resourcesAmount != None, "Your individual has no resources, cannot reproduce!"
		
	def test_individual_gets_fertility_at_reproduction(self, instantiateSingleIndividualPopulation, pggParameters):
		kwargs = pggParameters
		
		self.ind = instantiateSingleIndividualPopulation
		assert self.ind.fertilityValue == None, "Fertility assessed before reproduction. Beware: there must be a trailing background number somewhere."
		
		self.ind.reproduce(**kwargs)
		fertility = self.ind.fertilityValue
		assert fertility != None, "The individual reproduces and yet does not have a fertility value!"
		assert type(fertility) is float, "{0} is not a valid type of fertility. Should be float".format(type(fertility))
		
	def test_fertility_depends_on_resources_amount_in_reproduction_function(self, instantiateSingleDemePopulation, pggParameters):
		self.fakepop = instantiateSingleDemePopulation(2)
		kwargs = pggParameters
		
		for ind in range(len(self.fakepop.individuals)):
			indiv = self.fakepop.individuals[ind]
			setattr(indiv, "resourcesAmount", 1 + 9 * ind) 
			indiv.reproduce(**kwargs)
			
		assert self.fakepop.individuals[0].fertilityValue < self.fakepop.individuals[1].fertilityValue
		
	def test_fertility_depends_on_resources_amount_in_fertility_function(self, instantiateSingleDemePopulation, pggParameters):
		self.fakepop = instantiateSingleDemePopulation(2)
		kwargs = pggParameters
		
		for ind in range(len(self.fakepop.individuals)):
			indiv = self.fakepop.individuals[ind]
			setattr(indiv, "resourcesAmount", 1 + 9 * ind) 
			indiv.fertility(**kwargs)
			
		assert self.fakepop.individuals[0].fertilityValue < self.fakepop.individuals[1].fertilityValue, "Fertility does not change with individual resources!"
		
	def test_fertility_returns_positive_float(self, instantiateSingleDemePopulation, pggParameters):
		self.fakepop = instantiateSingleDemePopulation(10)
		kwargs = pggParameters
		
		for ind in range(len(self.fakepop.individuals)):
			indiv = self.fakepop.individuals[ind]
			setattr(indiv, "resourcesAmount", 1 + 9 * ind) 
			indiv.fertility(**kwargs)
			assert type(indiv.fertilityValue) is float
			assert indiv.fertilityValue >= 0
		
	def test_pgg_fitness_function(self, pggParameters):
		kwargs = pggParameters
		
		for x in range(10):
			assert fitness.functions["pgg"](res=x, **kwargs) == kwargs["fb"] * (x - kwargs["c"] * kwargs["x"] ** 2 + kwargs["b"] * kwargs["xmean"]) / (1 + kwargs["gamma"] * kwargs["n"]), "Wrong pgg function"
			
	def test_fertility_function_uses_fitness_function(self, instantiateSingleDemePopulation, pggParameters):
		self.fakepop = instantiateSingleDemePopulation(10)
		
		kwargs = pggParameters
		
		for ind in range(len(self.fakepop.individuals)):
			indiv = self.fakepop.individuals[ind]
			setattr(indiv, "resourcesAmount", 2 * ind) 
			indiv.fertility("pgg", **kwargs)
			assert indiv.fertilityValue == fitness.functions["pgg"](res=indiv.resourcesAmount, **kwargs), "The program does not call the requested fertility function!"
			
	def test_reproduction_gives_offspring_number(self, instantiateSingleIndividualPopulation, pggParameters):
		self.indiv = instantiateSingleIndividualPopulation
		kwargs = pggParameters
		
		self.indiv.reproduce(**kwargs)
		assert self.indiv.offspringNumber != None, "No offspring number generated"
		assert type(self.indiv.offspringNumber) is int, "Offspring number of wrong format: {0} instead of integer".format(type(self.indiv.offspringNumber))
		assert self.indiv.offspringNumber >= 0, "Offspring number cannot be negative"
			
	def test_reproduction_follows_a_poisson_distribution(self, instantiateSingleDemePopulation, pggParameters):
		#http://www2.stat-athens.aueb.gr/~exek/papers/Xekalaki-Statistician2000(355-382)ft.pdf
		random.seed(30)
		
		self.nIndividuals = 1000
		self.fakepop = instantiateSingleDemePopulation(self.nIndividuals)
		self.explambda = 4
		kwargs = pggParameters
		
		offspringPerInd = []
		for ind in self.fakepop.individuals:
			setattr(ind, "fertilityValue", self.explambda)
			ind.procreate()
			offspringPerInd.append(ind.offspringNumber)
		
		d = Counter(offspringPerInd)
		a, b = list(d.keys()), list(d.values())
		maxCount = max(a)
		observedCount = []
		expectedCount = []
		
		for k in range(maxCount):
			if k in a:
				observedCount.append(d[k])
			else:
				observedCount.append(0)
			
			expProbability = m.pow(m.e, (-self.explambda)) * (m.pow(self.explambda, k)) / m.factorial(k)
			expectedCount.append(self.nIndividuals * expProbability)
						
		chisq, pval = scistats.chisquare(observedCount, expectedCount)
		assert len(expectedCount) == len(observedCount), "len obs = {0}, len exp = {1}".format(len(observedCount), len(expectedCount))
		#assert sum(expectedCount) == sum(observedCount), "n obs = {0}, n exp = {1}".format(sum(observedCount), sum(expectedCount))
		assert pval > 0.05, "Test for goodness of fit failed: obs = {0}, exp = {1}".format(observedCount, expectedCount)	
		
	def test_individual_instances_are_created_based_on_offspring_number(self, instantiateSingleDemePopulation, pggParameters):
		self.fakepop = instantiateSingleDemePopulation(10)
		kwargs = pggParameters
		
		for ind in range(len(self.fakepop.individuals)):
			indiv = self.fakepop.individuals[ind]
			indiv.resourcesAmount = ind
			indiv.reproduce(**kwargs)
			assert len(indiv.offspring) == indiv.offspringNumber, "{0} offspring generated while there should be {1}".format(len(self.fakepop.offspring), offspringCounter)
	
	def test_individual_instances_have_same_deme_and_phenotypes_as_parent(self, instantiateSingleDemePopulation, pggParameters):
		self.fakepop = instantiateSingleDemePopulation(10)
		kwargs = pggParameters
		
		for ind in range(len(self.fakepop.individuals)):
			indiv = self.fakepop.individuals[ind]
			indiv.resourcesAmount = ind
			indiv.reproduce(**kwargs)
			
			for offspring in indiv.offspring:
				assert offspring.currentDeme == indiv.currentDeme, "Offspring is not in parent's deme: {0} instead of {1}".format(offspring.currentDeme, indiv.currentDeme)
				assert offspring.phenotypicValues == indiv.phenotypicValues, "Offspring does not inherit parent's phenotype: {0} instead of {1}".format(offspring.phenotypicValues, indiv.phenotypicValues)
		
	def test_offspring_are_added_to_the_population(self, makePopulationReproduce):
		self.fakepop, self.parents = makePopulationReproduce
		
		assert hasattr(self.fakepop, "offspring"), "No individual instances created in the population"
		
	def test_parents_are_replaced_by_offspring_in_population(self, makePopulationReproduce):
		self.fakepop, self.parents = makePopulationReproduce
		
		assert self.fakepop.individuals != self.parents, "Population not updated"
		assert self.fakepop.individuals == self.fakepop.offspring, "Population not updated correctly"
		
	def test_deme_demography_is_updated(self, makePopulationReproduce):
		self.fakepop, self.parents = makePopulationReproduce
		
		assert self.fakepop.demography == len(self.fakepop.individuals), "Population demography not updated"
		
	


			
			
		
	
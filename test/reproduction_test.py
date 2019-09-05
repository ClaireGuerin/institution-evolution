import pytest
from individual import Individual as Ind
from deme import Deme as Dem
from main import Population as Pop
import scipy.stats as scistats
from operator import add
import random
from statistics import mean
import gc
from fitness_function import fitness as fit

class TestReproductionFunction(object):
	
	def test_individual_has_resources_not_none(self, instantiateSingleIndividualPopulation):
		self.ind = instantiateSingleIndividualPopulation
		assert self.ind.resourcesAmount != None, "Your individual has no resources, cannot reproduce!"
		
	def test_individual_gets_fertility_at_reproduction(self, instantiateSingleIndividualPopulation):
		self.ind = instantiateSingleIndividualPopulation
		assert self.ind.fertilityValue == None, "Fertility assessed before reproduction. Beware: there must be a trailing background number somewhere."
		self.ind.reproduce()
		fertility = self.ind.fertilityValue
		assert fertility != None, "The individual reproduces and yet does not have a fertility value!"
		assert type(fertility) is float, "{0} is not a valid type of fertility. Should be float".format(type(fertility))
		
	def test_fertility_depends_on_resources_amount_in_reproduction_function(self, instantiateSingleDemePopulation):
		self.fakepop = instantiateSingleDemePopulation(2)
		
		for ind in range(len(self.fakepop.individuals)):
			indiv = self.fakepop.individuals[ind]
			setattr(indiv, "resourcesAmount", 1 + 9 * ind) 
			indiv.reproduce()
			
		assert self.fakepop.individuals[0].fertilityValue < self.fakepop.individuals[1].fertilityValue
		
	def test_fertility_depends_on_resources_amount_in_fertility_function(self, instantiateSingleDemePopulation):
		self.fakepop = instantiateSingleDemePopulation(2)
		
		for ind in range(len(self.fakepop.individuals)):
			indiv = self.fakepop.individuals[ind]
			setattr(indiv, "resourcesAmount", 1 + 9 * ind) 
			indiv.fertility()
			
		assert self.fakepop.individuals[0].fertilityValue < self.fakepop.individuals[1].fertilityValue
		
	def test_fertility_calculated_with_fitness_function(self, instantiateSingleDemePopulation):
		self.fakepop = instantiateSingleDemePopulation(10)
		
		expectedFunction = "pgg"
		
		for ind in range(len(self.fakepop.individuals)):
			indiv = self.fakepop.individuals[ind]
			setattr(indiv, "resourcesAmount", 1 + 9 * ind)
			indiv.fertility()
			assert indiv.fertilityValue == fit("pgg"), "Expected fertility of {0}, got {1}".format(fit("pgg"), indiv.fertilityValue)
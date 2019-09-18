import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop
import scipy.stats as scistats
from operator import add
import random
from statistics import mean
import gc

class TestPopulation(object):
	
	def test_population_contains_demes(self):
		self.pop = Pop()
		self.pop.createAndPopulateDemes()
		assert hasattr(self.pop, "demes"), "This population has no deme yet!"
		
		for deme in self.pop.demes:
			assert type(deme) is Dem
			
		gc.collect()
			
	def test_identify_deme_neighbours(self):
		self.fakepop = Pop()
		self.nd = self.fakepop.numberOfDemes
		
		for deme in range(self.nd):
			newDemeInstance = Dem()
			newDemeInstance.id = deme
			assert deme in range(self.nd)
			newDemeInstance.neighbours = self.fakepop.identifyNeighbours(self.nd, deme)
			assert deme not in newDemeInstance.neighbours, "Deme {0} counts itself as a neighbour".format(deme)
			assert all(x in range(self.nd) for x in newDemeInstance.neighbours), "Neighbour(s) of deme {0} are missing: takes into account {1} out of its {2} neighbours".format(deme, newDemeInstance.neighbours, self.nd - 1)
		
		gc.collect()
			
	def test_demes_are_populated(self):
		self.pop = Pop()
		self.pop.createAndPopulateDemes()
		for deme in self.pop.demes:
			assert deme.demography is not None, "Deme {0} is not populated".format(deme)
			
		gc.collect()
				
	def test_individual_attributes_are_non_empty(self, objectAttributesAreNotNone):
		self.pop = Pop()
		self.pop.createAndPopulateDemes()
		for ind in self.pop.individuals:
			testObj, attrObj = objectAttributesAreNotNone(ind, ["phenotypicValues", "currentDeme"])
			assert testObj, "Individual {0} has attribute(s) {1} set to None".format(ind, attrObj)
			
		gc.collect()
		
	def test_population_has_the_right_size(self):
		self.howManyDemes = 10
		self.howManyIndividualsPerDeme = 10
		self.pop = Pop()
		self.pop.createAndPopulateDemes(nDemes=self.howManyDemes, dSize=self.howManyIndividualsPerDeme)
		
		assert len(self.pop.individuals) == self.howManyIndividualsPerDeme * self.howManyDemes, "You created a population of {0} individuals instead of {1}!".format(len(self.pop.individuals), self.howManyIndividualsPerDeme * self.howManyDemes)
		
	def test_population_has_fitness_method_or_pgg_parameters(self):
		self.fakepop = Pop()
		
		assert hasattr(self.fakepop, "fitnessParameters"), "Provide fitness parameters"
		
		if not hasattr(self.fakepop, "fitnessMethod"):
			 for key in ["fb", "b", "c", "gamma"]:
					assert key in self.fakepop.fitnessParameters, "PGG parameter {0} not provided".format(key)

	def test_simulation_stops_if_population_extinct(self):
		self.fakepop = Pop()
		self.fakepop.numberOfDemes = 10
		self.fakepop.numberOfGenerations = 10

		self.fakepop.fitnessParameters["fb"] = 0.0001 # to make the population die out

		self.fakepop.createAndPopulateDemes()
		assert self.fakepop.demography == self.fakepop.numberOfDemes * self.fakepop.initialDemeSize
		
		self.fakepop.lifecycle(**self.fakepop.fitnessParameters)
		assert self.fakepop.demography == 0
		assert self.fakepop.individuals == []

		self.fakepop.lifecycle(**self.fakepop.fitnessParameters)
		assert self.fakepop.demography == 0
		assert self.fakepop.individuals == []

		for deme in self.fakepop.demes:
			#assert deme.demography == 0
			#assert deme.totalPhenotypes == []
			assert deme.meanPhenotypes == [None]

		self.fakepop.lifecycle(**self.fakepop.fitnessParameters)
		assert self.fakepop.demography == 0
		assert self.fakepop.individuals == []

	def test_update_function(self):
		self.fakepop = Pop()
		self.fakepop.numberOfDemes = 2

		self.fakepop.fitnessParameters["fb"] = 0.0001 # to make the population die out
		self.fakepop.createAndPopulateDemes()
		self.fakepop.populationMutationMigration()

		demogdeme0 = self.fakepop.demes[0].demography
		phendeme0 = self.fakepop.demes[0].totalPhenotypes[0]
		demogdeme1 = self.fakepop.demes[1].demography
		phendeme1 = self.fakepop.demes[1].totalPhenotypes[0]

		self.fakepop.update()

		assert self.fakepop.demes[0].meanPhenotypes[0] == self.fakepop.specialdivision(phendeme0, demogdeme0)
		assert self.fakepop.demes[1].meanPhenotypes[0] == self.fakepop.specialdivision(phendeme1, demogdeme1)
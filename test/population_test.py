import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop
import institutionevolution.myarithmetics as ar
import scipy.stats as scistats
from operator import add
import random
from statistics import mean
import gc

class TestPopulation(object):
	
	def test_population_contains_demes(self):
		self.pop = Pop(inst='test')
		self.pop.createAndPopulateDemes()
		assert hasattr(self.pop, "demes"), "This population has no deme yet!"
		
		for deme in self.pop.demes:
			assert type(deme) is Dem
			
		gc.collect()
			
	def test_identify_deme_neighbours(self):
		self.fakepop = Pop(inst='test')
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
		self.pop = Pop(inst='test')
		self.pop.createAndPopulateDemes()
		for deme in self.pop.demes:
			assert deme.demography is not None, "Deme {0} is not populated".format(deme)
			
		gc.collect()
				
	def test_individual_attributes_are_non_empty(self, objectAttributesAreNotNone):
		self.pop = Pop(inst='test')
		self.pop.createAndPopulateDemes()
		for ind in self.pop.individuals:
			testObj, attrObj = objectAttributesAreNotNone(ind, ["phenotypicValues", "currentDeme"])
			assert testObj, "Individual {0} has attribute(s) {1} set to None".format(ind, attrObj)
			
		gc.collect()
		
	def test_population_has_the_right_size(self):
		self.howManyDemes = 10
		self.howManyIndividualsPerDeme = 10
		self.pop = Pop(inst='test')
		self.pop.createAndPopulateDemes(nDemes=self.howManyDemes, dSize=self.howManyIndividualsPerDeme)
		
		assert len(self.pop.individuals) == self.howManyIndividualsPerDeme * self.howManyDemes, "You created a population of {0} individuals instead of {1}!".format(len(self.pop.individuals), self.howManyIndividualsPerDeme * self.howManyDemes)
		
	def test_population_has_fitness_method_or_pgg_parameters(self):
		self.fakepop = Pop(inst='test')
		
		assert hasattr(self.fakepop, "fitnessParameters"), "Provide fitness parameters"
		
		if not hasattr(self.fakepop, "fitnessMethod"):
			 for key in ["fb", "b", "c", "gamma"]:
					assert key in self.fakepop.fitnessParameters, "PGG parameter {0} not provided".format(key)

	def test_simulation_stops_if_population_extinct(self):
		self.fakepop = Pop(inst='test')
		self.fakepop.numberOfDemes = 10
		self.fakepop.numberOfGenerations = 10

		self.fakepop.fitnessParameters["fb"] = 0.0001 # to make the population die out

		self.fakepop.createAndPopulateDemes()
		assert self.fakepop.demography == self.fakepop.numberOfDemes * self.fakepop.initialDemeSize

	def test_population_mutation_updates_individual_phenotypes(self):
		self.fakepop = Pop(inst='test')
		self.fakepop.numberOfDemes = 2
		self.fakepop.initialDemeSize = 50
		self.fakepop.migrationRate = 0
		self.fakepop.mutationRate = 1
		# the two following lines are very important so that the test does not fail at the boundaries, 
		# e.g. if phen = 0 and dev < 0, mutated phenotype will still be 0
		self.fakepop.initialPhenotypes = [0.5] 
		self.fakepop.numberOfPhenotypes = 1

		self.fakepop.createAndPopulateDemes(nDemes=self.fakepop.numberOfDemes, dSize=self.fakepop.initialDemeSize)

		origPhenDeme0 = []
		origPhenDeme1 = []

		for ind in self.fakepop.individuals:
			if ind.currentDeme == 0:
				origPhenDeme0.append(ind.phenotypicValues[0])
			elif ind.currentDeme == 1:
				origPhenDeme1.append(ind.phenotypicValues[0])

		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()

		phenDeme0 = []
		devDeme0 = []
		phenDeme1 = []
		devDeme1 = []

		for ind in self.fakepop.individuals:
			if ind.currentDeme == 0:
				phenDeme0.append(ind.phenotypicValues[0])
				devDeme0.append(ind.mutationDeviation[0])
			elif ind.currentDeme == 1:
				phenDeme1.append(ind.phenotypicValues[0])
				devDeme1.append(ind.mutationDeviation[0])

		assert len(origPhenDeme0) == len(phenDeme0), "Number of individuals in deme 0 have changed from {0} to {1} after mutation".format(len(origPhenDeme0), len(phenDeme0))
		assert len(origPhenDeme1) == len(phenDeme1), "Number of individuals in deme 1 have changed from {0} to {1} after mutation".format(len(origPhenDeme1), len(phenDeme1))

		for i in range(self.fakepop.initialDemeSize):
			assert origPhenDeme0[i] != phenDeme0[i], "Individual {0} in deme 0 mutated from {1} to {2} when deviation was supposed to be {3}".format(i, origPhenDeme0[i], phenDeme0[i], devDeme0[i])
			assert origPhenDeme1[i] != phenDeme1[i], "Individual {0} in deme 1 mutated from {1} to {2} when deviation was supposed to be {3}".format(i, origPhenDeme1[i], phenDeme1[i], devDeme1[i])
		
	def test_demes_update_function(self):
		self.fakepop = Pop(inst='test')
		self.fakepop.numberOfDemes = 2

		self.fakepop.createAndPopulateDemes()
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()

		demogdeme0 = self.fakepop.demes[0].demography
		phendeme0 = self.fakepop.demes[0].totalPhenotypes[0]
		demogdeme1 = self.fakepop.demes[1].demography
		phendeme1 = self.fakepop.demes[1].totalPhenotypes[0]

		self.fakepop.updateDemeInfoPreProduction()
		self.fakepop.populationProduction()
		self.fakepop.updateDemeInfoPostProduction()

		assert self.fakepop.demes[0].meanPhenotypes[0] == ar.specialdivision(phendeme0, demogdeme0)
		assert self.fakepop.demes[1].meanPhenotypes[0] == ar.specialdivision(phendeme1, demogdeme1)
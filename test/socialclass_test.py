import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop
import institutionevolution.fitness as fitness
import institutionevolution.progress as progress
import random as rd
import scipy.stats as scistats
import gc

class TestSocialClassesFeature(object):

	def test_individual_can_become_leader(self):
		self.ind = Ind()
		assert hasattr(self.ind, "leader")

	def test_demes_have_a_number_of_elected_leaders(self):
		self.deme = Dem()
		assert "numberOfLeaders" in self.deme.progressValues
		assert "proportionOfLeaders" in self.deme.progressValues 

	def test_social_class_function_in_fitness_and_progress(self):
		assert 'socialclass' in fitness.functions, "create social class fitness function"
		assert 'socialclass' in progress.functions, "create social class progress function"

	def test_elections_take_place_in_demes(self):
		self.pop = Pop('socialclass')
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 2
		self.pop.migrationRate = 0

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updatePopulation()

		for deme in self.pop.demes:
			assert deme.progressValues["proportionOfLeaders"] is not None
			assert deme.progressValues["proportionOfLeaders"] == deme.meanPhenotypes[3]

	def test_individuals_get_assigned_a_role_during_elections(self, pseudorandom, instantiateSingleDemePopulation):
		#proportionOfLeaders = rd.random()
		pseudorandom(0)
		self.nIndividuals = 1000
		self.pop = instantiateSingleDemePopulation(self.nIndividuals)
		proportionOfLeaders = 0.896

		leaderCount = 0
		for ind in self.pop.individuals:
			assert hasattr(ind, "ascend"), "individual needs to be able to ascend social ladder"
			ind.ascend(leadProp=proportionOfLeaders)
			if ind.leader:
				leaderCount += 1

		stat1, pval1 = scistats.ttest_1samp([1] * leaderCount + [0] * (self.nIndividuals - leaderCount), proportionOfLeaders)
		assert pval1 > 0.05, "T-test mean failed. Observed: {0}, Expected: {1}".format(leaderCount/self.nIndividuals, proportionOfLeaders)
		self.test = scistats.binom_test(leaderCount, self.nIndividuals, proportionOfLeaders, alternative = "two-sided")
		assert self.test > 0.05, "Success rate = {0} when proportion of leaders = {1}".format(leaderCount/self.nIndividuals, proportionOfLeaders)
		
		gc.collect()

	def test_deme_gets_number_of_leaders(self, pseudorandom):
		pseudorandom(10)
		self.pop = Pop('socialclass')
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 1000
		self.pop.initialPhenotypes = [0.1,0.2,0.3,0.6]
		self.pop.migrationRate = 0
		self.pop.mutationRate = 0

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updatePopulation()
		self.pop.populationReproduction()

		plead = self.pop.initialPhenotypes[3]

		for deme in self.pop.demes:
			nlead = deme.progressValues["numberOfLeaders"]
			assert nlead is not None
			assert type(nlead) is int
			assert nlead >= 0
			assert pytest.approx(deme.progressValues["proportionOfLeaders"]) == plead
			stat1, pval1 = scistats.ttest_1samp([1] * nlead + [0] * (deme.demography - nlead), plead)
			#assert pval1 > 0.05, "T-test mean failed. Observed: {0}, Expected: {1}".format(nlead/deme.demography, plead)
			self.test = scistats.binom_test(nlead, deme.demography, plead, alternative = "two-sided")
			assert self.test > 0.05, "Success rate = {0} when proportion of leaders = {1}".format(nlead/deme.demography, plead)
		
		gc.collect()

	def test_deme_number_of_leaders_is_number_of_individuals_with_that_role(self, pseudorandom):
		pseudorandom(0)
		self.pop = Pop('socialclass')
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 10
		self.pop.initialPhenotypes = [0.1,0.2,0.3,0.6]
		self.pop.migrationRate = 0
		self.pop.mutationRate = 0

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updatePopulation()
		self.pop.populationReproduction()

		leaderCountPerDeme = [0] * self.pop.numberOfDemes
		for ind in self.pop.parents:
			leaderCountPerDeme[ind.currentDeme] += ind.leader

		for deme in range(self.pop.numberOfDemes):
			nl = self.pop.demes[deme].progressValues["numberOfLeaders"]
			assert nl != 10, "all individuals in deme have been elected leaders when proportion should be about: "+self.pop.initialPhenotypes[3]
			assert leaderCountPerDeme[deme] == nl, "deme counts {0} leaders when there are {1}".format(nl,leaderCountPerDeme[deme])

	def test_social_class_determines_fitness(self):
		assert False, "write this test!"
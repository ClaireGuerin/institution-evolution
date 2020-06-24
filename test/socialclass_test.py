import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop
import institutionevolution.fitness as fitness
import institutionevolution.progress as progress
import random as rd

class TestSocialClassesFeature(object):

	def test_individual_belongs_to_a_social_class(self):
		self.ind = Ind()
		assert hasattr(self.ind, "socialStatus")

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
		pseudorandom(0)
		self.nIndividuals = 1000
		self.pop = instantiateSingleDemePopulation(self.nIndividuals)
		proportionOfLeaders = rd.random()

		leaderCount = 0
		for ind in self.pop.individuals:
			assert hasattr(ind, "ascend"), "individual needs to be able to ascend social ladder"
			ind.ascend(leadProp=proportionOfLeaders, rds=96)
			if ind.leader:
				leaderCount += 1

		stat1, pval1 = scistats.ttest_1samp([1] * leaderCount + [0] * (self.nIndividuals - leaderCount), proportionOfLeaders)
		assert pval1 > 0.05, "T-test mean failed. Observed: {0}, Expected: {1}".format(leaderCount/self.nIndividuals, proportionOfLeaders)
		self.test = scistats.binom_test(leaderCount, self.nIndividuals, proportionOfLeaders, alternative = "two-sided")
		assert self.test > 0.05, "Success rate = {0} when proportion of leaders = {1}".format(leaderCount/self.nIndividuals, proportionOfLeaders)
		 

	def test_deme_gets_number_of_leaders(self):
		self.pop = Pop('socialclass')
		self.pop.numberOfDemes = 1000
		self.pop.initialDemeSize = 3
		self.pop.initialPhenotypes = [0.1,0.2,0.3,0.6]
		self.pop.migrationRate = 0
		self.pop.mutationRate = 0

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updatePopulation()

		for deme in self.pop.demes:
			nlead = deme.progressValues["numberOfLeaders"]
			assert nlead is not None
			assert type(nlead) is float
			assert nlead >= 0
			stat1, pval1 = scistats.ttest_1samp([1] * nlead + [0] * (deme.demography - nlead), self.pop.initialPhenotypes[3])
			assert pval1 > 0.05, "T-test mean failed. Observed: {0}, Expected: {1}".format(nlead/deme.demography, self.pop.initialPhenotypes[3])
			self.test = scistats.binom_test(nlead, deme.demography, self.pop.initialPhenotypes[3], alternative = "two-sided")
			assert self.test > 0.05, "Success rate = {0} when proportion of leaders = {1}".format(nlead/deme.demography, self.pop.initialPhenotypes[3])
		
		gc.collect()

		assert False, "write a test of distribution of numberOfLeaders"

	def test_deme__number_of_leaders_is_number_of_individuals_with_that_role(self):
		assert False, "write this test"
		


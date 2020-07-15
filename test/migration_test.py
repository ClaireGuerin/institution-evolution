import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop
import scipy.stats as scistats
from operator import add
import random
from statistics import mean
import gc
from collections import Counter

class TestMigrationFunction(object):
	
	def test_individual_has_destination_deme_after_migration(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes(10)
		
		for ind in self.fakepop.individuals:
			ind.migrate(nDemes=self.fakepop.numberOfDemes, migRate=self.fakepop.migrationRate)
			assert hasattr(ind, "destinationDeme"), "Your individual is going nowhere: no destination deme!"
			
		gc.collect()
		
	def test_migration_returns_a_destination_deme_of_correct_format(self, instantiateSingleIndividualsDemes):
		"""The migration function should return the new deme, which is an integer among all demes"""
		self.fakepop = instantiateSingleIndividualsDemes(10)
		
		for ind in self.fakepop.individuals:
			ind.migrate(nDemes=self.fakepop.numberOfDemes, migRate=self.fakepop.migrationRate)
			
			assert type(ind.destinationDeme) is int, "{0} is {1} instead of integer".format(ind.destinationDeme, type(ind.destinationDeme))
			assert ind.destinationDeme in range(self.fakepop.numberOfDemes), "The deme of destination {0} does not exist".format(ind.destinationDeme)
			
		gc.collect()
		
	def test_migrants_are_defined_properly(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes(10)
		
		for ind in self.fakepop.individuals:
			ind.migrate(nDemes=self.fakepop.numberOfDemes, migRate=self.fakepop.migrationRate)
			
			assert hasattr(ind, "migrant"), "Your individual does not know whether to migrate or not"
			assert type(ind.migrant) is bool, "Migrant must be a boolean"	
			
		gc.collect()

	def test_migrants_are_drawn_equally_depending_on_seed(self, pseudorandom):
		self.individualsPerDeme = 1000
		self.fakepop = Pop(inst='test/test')
		self.fakepop.initialDemeSize = self.individualsPerDeme
		self.fakepop.numberOfDemes = 3
		self.fakepop.createAndPopulateDemes()

		self.migrants = []

		for ind in self.fakepop.individuals:
			pseudorandom(56)
			ind.migrate(nDemes=self.fakepop.numberOfDemes, migRate=self.fakepop.migrationRate)
			self.migrants.append(ind.migrant)

		assert all(self.migrants) or not any(self.migrants), "Migration values differ for same seed resetting: {0}".format(set(self.migrants))

		gc.collect()

	def test_migrants_are_drawn_from_binomial(self, pseudorandom):
		self.individualsPerDeme = 1000
		self.fakepop = Pop(inst='test/test')
		self.fakepop.initialDemeSize = self.individualsPerDeme
		self.fakepop.numberOfDemes = 3
		self.fakepop.createAndPopulateDemes()
		
		i = 0
		for deme in range(self.fakepop.numberOfDemes):
			migrantsCount = 0
			for ind in range(self.individualsPerDeme):
				indiv = self.fakepop.individuals[ind]
				originalDeme = indiv.currentDeme
				pseudorandom(0)
				indiv.migrate(nDemes=self.fakepop.numberOfDemes, migRate=self.fakepop.migrationRate)
				if indiv.migrant:
					migrantsCount += 1
				i += 1
			
			stat1, pval1 = scistats.ttest_1samp([1] * migrantsCount + [0] * (self.individualsPerDeme - migrantsCount), self.fakepop.migrationRate)
			test = scistats.binom_test(x=migrantsCount, n=self.individualsPerDeme, p=self.fakepop.migrationRate, alternative="two-sided")
			
			assert any([pval1 > 0.05,migrantsCount/self.individualsPerDeme==self.fakepop.migrationRate]), "t-test mean failed. Observed: {0}, Expected: {1}".format(migrantsCount/self.individualsPerDeme, self.fakepop.migrationRate)
			assert test > 0.05, "Success rate = {0} when mutation rate = {1}".format(migrantsCount/self.individualsPerDeme, self.fakepop.migrationRate)
		
		gc.collect()
	
	def test_migrants_destinations_equally_likely_as_in_uniform_distribution(self, pseudorandom, instantiateSingleIndividualsDemes):
		pseudorandom(69)
		self.fakepop = Pop(inst='test/test')
		self.ds = 100
		self.nd = 10
		self.fakepop.createAndPopulateDemes(nDemes=self.nd, dSize=self.ds)
		
		destinations = []
		
		for ind in range(self.fakepop.demography):
			indiv = self.fakepop.individuals[ind]
			indiv.migrate(nDemes=self.fakepop.numberOfDemes, migRate=1)
			destinations.append(indiv.destinationDeme)

		observedCountUnsorted = Counter(destinations)
		observedCount = []
		for key, val in sorted(observedCountUnsorted.items()):
			observedCount.append(val)

		expectedCount = [self.ds for i in range(self.nd)]

		chisq, pval = scistats.chisquare(observedCount, expectedCount)
		assert len(expectedCount) == len(observedCount), "len obs = {0}, len exp = {1}".format(len(observedCount), len(expectedCount))
		assert pval > 0.05, "Test for goodness of fit failed: obs = {0}, exp = {1}".format(observedCount, expectedCount)
				
		gc.collect()
			
	def test_only_migrants_change_deme(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes(10)
		
		self.migrantIndivTrue = self.fakepop.individuals[0]
		self.migrantIndivFalse = self.fakepop.individuals[1]
		
		self.origDemeTrue = self.migrantIndivTrue.currentDeme
		self.migrantIndivTrue.migrate(self.fakepop.numberOfDemes, migRate=1)
		assert self.migrantIndivTrue.migrant, "Uh-oh, looks like the individual did not migrate when it should have..."
		assert self.origDemeTrue != self.migrantIndivTrue.destinationDeme, "Individual destination deme is the same as current even though it should migrate!"
		
		self.origDemeFalse = self.migrantIndivFalse.currentDeme
		self.migrantIndivFalse.migrate(self.fakepop.numberOfDemes, migRate=0)
		assert not self.migrantIndivFalse.migrant, "Uh-oh, looks like the individual did migrate when it shouldn't have..."
		assert self.origDemeFalse == self.migrantIndivFalse.destinationDeme, "Individual destination deme is different from current even though it does not migrate!"
		
		gc.collect()
		
	def test_current_individuals_deme_updated_with_new(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes(10)
		
		for ind in self.fakepop.individuals:
			originalDeme = ind.currentDeme
			ind.migrate(nDemes=self.fakepop.numberOfDemes, migRate=0.5)
			assert ind.currentDeme == ind.destinationDeme, "Ooops, looks like your individual got it wrong: it went from deme {0} to {1} instead of {2}".format(originalDeme, ind.currentDeme, ind.destinationDeme)
			
		gc.collect()
	
	def test_demes_collect_all_their_individuals_after_migration(self):
		self.demesize = 10
		self.fakepop = Pop(inst='test/test')
		self.nd = self.fakepop.numberOfDemes
		self.fakepop.createAndPopulateDemes(self.nd, self.demesize)
		
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()
		self.fakepop.updateDemeInfoPreProduction()
		
		self.newDemography = []		
		for ind in self.fakepop.individuals:
			self.newDemography.append(ind.destinationDeme)
		
		self.demographyKnownToDeme = []
		for deme in range(self.nd):
			focalDeme = self.fakepop.demes[deme]
			assert self.newDemography.count(deme) == focalDeme.demography, "Deme {0} think their demography has changed from {1} to {2} instead of {3} after migration".format(deme, self.demesize, focalDeme.demography, self.newDemography.count(deme))
		
		gc.collect()
		
	def test_migration_is_ran_at_the_population_level(self):
		self.fakepop = Pop(inst='test/test')
		self.nd = self.fakepop.numberOfDemes
		self.fakepop.createAndPopulateDemes(self.nd,10)
		
		assert hasattr(self.fakepop, "populationMutationMigration"), "Migration cannot be ran at the population level"
		assert callable(self.fakepop.populationMutationMigration)
		
		gc.collect()

	def test_migration_at_population_level_updates_phenotypes(self):
		self.fakepop = Pop(inst='test/test')
		self.fakepop.numberOfDemes = 2
		self.fakepop.initialDemeSize = 10
		self.fakepop.initialPhenotypes = [0.5]
		self.fakepop.numberOfPhenotypes = 1
		self.fakepop.mutationRate = 0
		self.fakepop.migrationRate = 1

		self.fakepop.createAndPopulateDemes()

		for ind in self.fakepop.individuals:
			if ind.currentDeme == 0:
				ind.phenotypicValues = [0.2]
			else:
				ind.phenotypicValues = [0.8]

		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()

		assert self.fakepop.demes[0].totalPhenotypes[0] == pytest.approx(0.8 * self.fakepop.initialDemeSize)
		assert self.fakepop.demes[1].totalPhenotypes[0] == pytest.approx(0.2 * self.fakepop.initialDemeSize)
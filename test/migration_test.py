import pytest
from individual import Individual as Ind
from deme import Deme as Dem
from main import Population as Pop
import scipy.stats as scistats
from operator import add
import random
from statistics import mean
import gc

class TestMigrationFunction(object):
	
	def test_individual_has_destination_deme_after_migration(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes()
		
		for ind in self.fakepop.individuals:
			ind.migrate(nDemes=self.fakepop.numberOfDemes, migRate=self.fakepop.migrationRate)
			assert hasattr(ind, "destinationDeme"), "Your individual is going nowhere: no destination deme!"
			
		gc.collect()
		
	def test_migration_returns_a_destination_deme_of_correct_format(self, instantiateSingleIndividualsDemes):
		"""The migration function should return the new deme, which is an integer among all demes"""
		self.fakepop = instantiateSingleIndividualsDemes()
		
		for ind in self.fakepop.individuals:
			ind.migrate(nDemes=self.fakepop.numberOfDemes, migRate=self.fakepop.migrationRate)
			
			assert type(ind.destinationDeme) is int, "{0} is {1} instead of integer".format(ind.destinationDeme, type(ind.destinationDeme))
			assert ind.destinationDeme in range(self.fakepop.numberOfDemes), "The deme of destination {0} does not exist".format(ind.destinationDeme)
			
		gc.collect()
		
	def test_migrants_are_defined_properly(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes()
		
		for ind in self.fakepop.individuals:
			ind.migrate(nDemes=self.fakepop.numberOfDemes, migRate=self.fakepop.migrationRate)
			
			assert hasattr(ind, "migrant"), "Your individual does not know whether to migrate or not"
			assert type(ind.migrant) is bool, "Migrant must be a boolean"	
			
		gc.collect()
		
	def test_migrants_are_drawn_from_binomial(self, instantiateSingleDemePopulation):
		random.seed(30)
		self.individualsPerDeme = 1000
		self.fakepop = Pop()
		self.nd = self.fakepop.numberOfDemes
		self.fakepop.createAndPopulateDemes(self.nd, self.individualsPerDeme)
		
		self.meanpvals = []
		self.distripvals = []
		self.allcounts = []
		self.countMigrantsInEachDeme = [0] * self.nd
		
		for ind in self.fakepop.individuals:
			originalDeme = ind.currentDeme
			ind.migrate(nDemes=self.nd, migRate=self.fakepop.migrationRate)
			if ind.migrant:
				self.countMigrantsInEachDeme[originalDeme] += 1
					
		for deme in range(self.nd):
			migrantCount = self.countMigrantsInEachDeme[deme]
			
			stat1, pval1 = scistats.ttest_1samp([1] * migrantCount + [0] * (self.individualsPerDeme - migrantCount), self.fakepop.migrationRate)
			self.meanpvals.append(pval1)
			
			test = scistats.binom_test(x=migrantCount, n=self.individualsPerDeme, p=self.fakepop.migrationRate, alternative="two-sided")
			self.distripvals.append(test)
			
			self.allcounts.append(migrantCount)
			
		assert sum([x > 0.05 for x in self.meanpvals]) >= len(self.meanpvals)-1, "T-test mean failed. Observed: {0}, Expected: {1}".format(mean(self.allcounts)/self.individualsPerDeme, self.fakepop.migrationRate)
		assert sum([x > 0.05 for x in self.distripvals]) >= len(self.distripvals)-1, "Success rate = {0} when mutation rate = {1}".format(mean(self.allcounts)/self.individualsPerDeme, self.fakepop.migrationRate)
		
		gc.collect()
	
	def test_migrants_destinations_equally_likely_as_in_uniform_distribution(self, instantiateSingleIndividualsDemes):
		self.fakepop = Pop()
		self.numberOfDemes = 10
		self.initialDemeSize = 100
		self.fakepop.createAndPopulateDemes()
		
		destinations = []
		
		for ind in self.fakepop.individuals:
			ind.migrate(self.fakepop.numberOfDemes, migRate=1)
			destinations.append(ind.destinationDeme)
			
		test, pval = scistats.kstest(destinations, scistats.randint.cdf, args=(0, self.numberOfDemes - 1))
		assert pval > 0.05, "Migrants destinations are not equally likely (distribution non uniform)"
		
		
	def test_only_migrants_change_deme(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes()
		
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
		self.fakepop = instantiateSingleIndividualsDemes()
		
		for ind in self.fakepop.individuals:
			originalDeme = ind.currentDeme
			ind.migrate(nDemes=self.fakepop.numberOfDemes, migRate=0.5)
			assert ind.currentDeme == ind.destinationDeme, "Ooops, looks like your individual got it wrong: it went from deme {0} to {1} instead of {2}".format(originalDeme, ind.currentDeme, ind.destinationDeme)
			
		gc.collect()
	
	def test_demes_collect_all_their_individuals_after_migration(self):
		self.demesize = 10
		self.fakepop = Pop()
		self.nd = self.fakepop.numberOfDemes
		self.fakepop.createAndPopulateDemes(self.nd, self.demesize)
		
		self.fakepop.migrationUpdate()
		
		self.newDemography = []		
		for ind in self.fakepop.individuals:
			self.newDemography.append(ind.destinationDeme)
		
		self.demographyKnownToDeme = []
		for deme in range(self.nd):
			focalDeme = self.fakepop.demes[deme]
			assert self.newDemography.count(deme) == focalDeme.demography, "Deme {0} think their demography has changed from {1} to {2} instead of {3} after migration".format(deme, self.demesize, focalDeme.demography, self.newDemography.count(deme))
		
		gc.collect()
		
	def test_migration_is_ran_at_the_population_level(self):
		self.fakepop = Pop()
		self.nd = self.fakepop.numberOfDemes
		self.fakepop.createAndPopulateDemes(self.nd,10)
		
		assert hasattr(self.fakepop, "migrationUpdate"), "Migration cannot be ran at the population level"
		assert callable(self.fakepop.migrationUpdate)
		
		gc.collect()
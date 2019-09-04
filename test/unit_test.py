import pytest
from individual import Individual as Ind
from deme import Deme as Dem
from main import Population as Pop
import scipy.stats as scistats
from operator import add
import random
from statistics import mean
import gc

class TestIndividual(object):
		
	def test_individual_attributes_exist(self, objectAttributesExist):
		self.indiv = Ind()
		self.attributes = ["phenotypicValues", "currentDeme", "resourcesAmount", "fertilityValue", "offspringNumber"]
		testAttr, whichAttr = objectAttributesExist(self.indiv, self.attributes)
		assert testAttr, "Individual is missing attribute(s) {0}".format(whichAttr)
		
		gc.collect()
		
	def test_mig_rep_mut_methods_exist_and_are_callable(self):
		self.methods = ['mutate', 'migrate', 'reproduce']
		
		for method in self.methods:
			assert hasattr(Ind(), method), "{0} method does not exist".format(method)
			assert callable(getattr(Ind, method)), "{0} method is not callable".format(method)
			
		gc.collect()
			
class TestMutationFunction(object):
			
	def test_mutation_function_takes_and_returns_phenotype(self, instantiateSingleIndividualPopulation):
		self.indiv = instantiateSingleIndividualPopulation
		assert type(self.indiv.phenotypicValues) is list, "You must give a list of phenotypic values"
		
		self.indiv.mutate(mutRate=0.5, mutStep=0.5)
		for x in self.indiv.phenotypicValues:
			assert type(x) is float, "Phenotypic values ({0}) must be of type float, and not {1}".format(x, type(x))
			assert 0 <= x <= 1, "Phenotypic values must be in range [0,1]"
			
		gc.collect()
			
	def test_mutants_are_defined(self, instantiateSingleIndividualPopulation):
		self.indiv = instantiateSingleIndividualPopulation
		
		self.indiv.mutate(mutRate=0.5, mutStep=0.5)
		assert hasattr(self.indiv, "mutant"), "We don't know if our individual is a mutant because it doesn't have this attribute"
		assert type(self.indiv.mutant) is bool
		
		gc.collect()
		
	def test_mutants_are_drawn_from_binomial(self, instantiateSingleDemePopulation):
		random.seed(30)
		self.nIndividuals = 1000
		self.fakepop = instantiateSingleDemePopulation(self.nIndividuals)
		
		self.mutantCount = 0
		for ind in self.fakepop.individuals:
			ind.mutate(mutRate=self.fakepop.mutationRate, mutStep=0.05)
			if ind.mutant:
				self.mutantCount += 1
		
		stat1, pval1 = scistats.ttest_1samp([1] * self.mutantCount + [0] * (self.nIndividuals - self.mutantCount), self.fakepop.mutationRate)
		assert pval1 > 0.05, "T-test mean failed. Observed: {0}, Expected: {1}".format(self.mutantCount/self.nIndividuals, self.fakepop.mutationRate)
		self.test = scistats.binom_test(self.mutantCount, self.nIndividuals, self.fakepop.mutationRate, alternative = "two-sided")
		assert self.test > 0.05, "Success rate = {0} when mutation rate = {1}".format(self.mutantCount/self.nIndividuals, self.fakepop.mutationRate)
		
		gc.collect()
		
	def test_deviation_function_returns_list_of_phenotype_size(self, instantiateSingleIndividualPopulation):
		self.indiv = instantiateSingleIndividualPopulation
		self.phen = self.indiv.phenotypicValues
		
		for mutationBool in [True, False]:
			self.indiv.mutant = mutationBool
			self.indiv.deviate(0.05, len(self.phen))
			assert type(self.indiv.mutationDeviation) is list
			assert len(self.indiv.mutationDeviation) == len(self.phen)
			
		gc.collect()
		
	def test_mutants_get_deviation_from_phenotype(self, instantiateSingleIndividualPopulation):
		self.indiv = instantiateSingleIndividualPopulation
		self.indiv.mutate(mutRate=1,mutStep=0.05)
		assert hasattr(self.indiv, "mutationDeviation"), "Individual is a mutant: it needs to be set a deviation from phenotype"
		
		for x in self.indiv.mutationDeviation:
			assert -1 < x < 1
			
		gc.collect()
			
	def test_only_mutants_change_phenotype(self, instantiateSingleDemePopulation):
		self.fakepop = instantiateSingleDemePopulation(2)
		self.mutantIndivTrue = self.fakepop.individuals[0]
		self.mutantIndivFalse = self.fakepop.individuals[1]
		
		self.mutantIndivTrue.mutate(mutRate=1, mutStep=0.05)
		assert self.mutantIndivTrue.mutant, "Uh-oh, looks like the individual did not mutate when it should have..."
		assert all([x != 0 for x in self.mutantIndivTrue.mutationDeviation]), "Your mutant (bool={0}) phenotype does not deviate!".format(self.mutantIndivTrue.mutant)
		
		self.mutantIndivFalse.mutate(mutRate=0, mutStep=0.05)
		assert not self.mutantIndivFalse.mutant
		assert all([x == 0 for x in self.mutantIndivFalse.mutationDeviation]), "Phenotype deviates even though individual not a mutant!"
		
		gc.collect()
		
	def test_mutation_deviation_follows_normal_distribution(self, instantiateSingleDemePopulation):
		random.seed(30)
		self.nIndividuals = 1000
		self.fakepop = instantiateSingleDemePopulation(self.nIndividuals)
		
		self.distri = []
		for ind in self.fakepop.individuals:
			ind.mutate(mutRate=1,mutStep=0.05) 
			self.distri.append(ind.mutationDeviation[0])
			
		stat1, pval1 = scistats.ttest_1samp(self.distri, float(0))
		assert pval1 > 0.05, "T-test mean failed. Observed: {0}, Expected: {1}".format(mean(self.distri),0)
		stat2, pval2 = scistats.kstest(self.distri, 'norm', args=(0,0.05), N=self.nIndividuals)
		assert pval2 > 0.05, "Test for goodness of fit failed"
		stat3, pval3 = scistats.shapiro(self.distri), "Test of normality failed"
		
		gc.collect()
 
	def test_mutation_adds_deviation_to_phenotype(self, instantiateSingleDemePopulation):
		self.fakepop = instantiateSingleDemePopulation(2)
		
		# WHEN THERE IS MUTATION
		self.trueMutant = self.fakepop.individuals[0]
		self.oldPhenTrueMutant = self.trueMutant.phenotypicValues
		
		self.trueMutant.mutant = True
		self.trueMutant.deviate(ms=0.05,n=len(self.oldPhenTrueMutant))
		assert all(x != 0 for x in self.trueMutant.mutationDeviation), "Deviation = {0}".format(self.trueMutant.mutationDeviation)
		
		self.trueMutant.applyMutation(self.trueMutant.mutationDeviation)
		assert all(x != y for x, y in zip(self.trueMutant.phenotypicValues, self.oldPhenTrueMutant)), "New:{0}, Old:{1}".format(self.falseMutant.phenotypicValues, self.oldPhenFalseMutant)
		
		# Reset to test the whole thing together:
		self.trueMutant.phenotypicValues = self.oldPhenTrueMutant
		self.trueMutant.mutant = None
		self.trueMutant.mutationDeviation = None
		
		self.trueMutant.mutate(mutRate=1, mutStep=0.05)
		assert type(self.oldPhenTrueMutant) is list and type(self.trueMutant.mutationDeviation) is list, "Check that both {0} and {1} are lists".format(self.oldPhenTrueMutant, self.trueMutant.mutationDeviation)
		assert all([x + y == z for x, y, z in zip(self.oldPhenTrueMutant, self.trueMutant.mutationDeviation, self.trueMutant.phenotypicValues)]), "Deviation not added to mutant phenotype!"
		
		# WHEN THERE IS NO MUTATION
		self.falseMutant = self.fakepop.individuals[1]
		self.oldPhenFalseMutant = self.falseMutant.phenotypicValues
		
		self.falseMutant.mutant = False
		self.falseMutant.deviate(ms=0.05, n=len(self.oldPhenFalseMutant))
		assert self.falseMutant.mutationDeviation == [0] * len(self.oldPhenFalseMutant), "Deviation = {0}".format(self.falseMutant.mutationDeviation)
		
		self.falseMutant.applyMutation(self.falseMutant.mutationDeviation)
		assert self.falseMutant.phenotypicValues == self.oldPhenFalseMutant, "New:{0}, Old:{1}".format(self.falseMutant.phenotypicValues, self.oldPhenFalseMutant)
		
		# Reset to test the whole thing together:
		self.falseMutant.phenotypicValues = self.oldPhenFalseMutant
		self.falseMutant.mutant = None
		self.falseMutant.mutationDeviation = None
		
		self.falseMutant.mutate(mutRate=0, mutStep=0.05)
		assert self.oldPhenFalseMutant == self.falseMutant.phenotypicValues, "Your individual shows mutant characteristic = {0}. Yet its phenotype deviates by {1}".format(self.falseMutant.mutant, [x-y for x, y in zip(self.falseMutant.phenotypicValues, self.oldPhenFalseMutant)])
		assert all([x == y for x, y in zip(self.oldPhenFalseMutant, self.falseMutant.phenotypicValues)]), "Before: {0}, Deviation: {1}, After: {2}".format(self.oldPhenFalseMutant, self.falseMutant.mutationDeviation, self.falseMutant.phenotypicValues)
		
		gc.collect()
		
	def test_mutation_does_not_affect_phenotype_size(self, instantiateSingleIndividualPopulation):
		self.indiv = instantiateSingleIndividualPopulation
		self.phen = self.indiv.phenotypicValues
		
		self.indiv.mutate(mutRate=1, mutStep=0.05)
		assert len(self.phen) == len(self.indiv.phenotypicValues)
		
		gc.collect()
		
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
		
	def test_only_migrants_change_deme(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes()
		
		self.migrantIndivTrue = self.fakepop.individuals[0]
		self.migrantIndivFalse = self.fakepop.individuals[0]
		
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
		
		self.fakepop.populationMigration()
		
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
		
		assert hasattr(self.fakepop, "populationMigration"), "Migration cannot be ran at the population level"
		assert callable(self.fakepop.populationMigration)
		
		gc.collect()
		
		
class TestDeme(object):
	
	def test_deme_attributes(self, objectAttributesExist):
		self.deme = Dem()
		self.attributes = ["id", "demography", "publicGood", "neighbours"]
		testAttr, whichAttr = objectAttributesExist(self.deme, self.attributes)
		assert testAttr, "Deme is missing attribute(s) {0}".format(whichAttr)
		
		gc.collect()
		
	def test_deme_object_knows_itself(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes()
		
		for deme in range(self.fakepop.numberOfDemes):
			focalDeme = self.fakepop.demes[deme]
			assert type(focalDeme.id) is int
			assert focalDeme.id == deme, "Deme number {0} has wrong id ={1}".format(deme, focalDeme.id)
			
		gc.collect()
	
	def test_deme_object_knows_other_demes(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes()
		
		for deme in range(self.fakepop.numberOfDemes):
			focalDeme = self.fakepop.demes[deme]
			otherDemes = list(range(self.fakepop.numberOfDemes))
			del otherDemes[focalDeme.id]
			assert type(focalDeme.neighbours) is list
			assert focalDeme.neighbours == otherDemes, "Neighbours of deme {0} are {1}, and not {2}!".format(deme, otherDemes, focalDeme.neighbours)
			
		gc.collect()

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
		

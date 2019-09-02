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
		
	def test_mig_rep_mut_methods_exist_and_are_callable(self):
		self.methods = ['mutate', 'migrate', 'reproduce']
		
		for method in self.methods:
			assert hasattr(Ind(), method), "{0} method does not exist".format(method)
			assert callable(getattr(Ind, method)), "{0} method is not callable".format(method)
			
class TestMutationFunction(object):
			
	def test_mutation_function_takes_and_returns_phenotype(self, instantiateSingleIndividualPopulation):
		self.indiv = instantiateSingleIndividualPopulation
		assert type(self.indiv.phenotypicValues) is list, "You must give a list of phenotypic values"
		
		self.indiv.mutate(mutRate=0.5, mutStep=0.5)
		for x in self.indiv.phenotypicValues:
			assert type(x) is float, "Phenotypic values ({0}) must be of type float, and not {1}".format(x, type(x))
			assert 0 <= x <= 1, "Phenotypic values must be in range [0,1]"
			
	def test_mutants_are_defined(self, instantiateSingleIndividualPopulation):
		self.indiv = instantiateSingleIndividualPopulation
		
		self.indiv.mutate(mutRate=0.5, mutStep=0.5)
		assert hasattr(self.indiv, "mutant"), "We don't know if our individual is a mutant because it doesn't have this attribute"
		assert type(self.indiv.mutant) is bool
		
	def test_mutants_are_drawn_from_binomial(self, instantiateSingleDemePopulation):
		random.seed(30)
		self.nIndividuals = 1000
		self.fakepop = instantiateSingleDemePopulation(self.nIndividuals)
		
		self.mutantCount = 0
		for ind in self.fakepop.allPopulationDemes[0].individuals:
			ind.mutate(mutRate=self.fakepop.mutationRate, mutStep=0.05)
			if ind.mutant:
				self.mutantCount += 1
		
		stat1, pval1 = scistats.ttest_1samp([1] * self.mutantCount + [0] * (self.nIndividuals - self.mutantCount), self.fakepop.mutationRate)
		assert pval1 > 0.05, "T-test mean failed. Observed: {0}, Expected: {1}".format(self.mutantCount/self.nIndividuals, self.fakepop.mutationRate)
		self.test = scistats.binom_test(self.mutantCount, self.nIndividuals, self.fakepop.mutationRate, alternative = "two-sided")
		assert self.test > 0.05, "Success rate = {0} when mutation rate = {1}".format(self.mutantCount/self.nIndividuals,self.fakepop.mutationRate)
		
		gc.collect()
		
	def test_deviation_function_returns_list_of_phenotype_size(self, instantiateSingleIndividualPopulation):
		self.indiv = instantiateSingleIndividualPopulation
		self.phen = self.indiv.phenotypicValues
		
		for mutationBool in [True, False]:
			self.indiv.mutant = mutationBool
			self.indiv.deviate(0.05, len(self.phen))
			assert type(self.indiv.mutationDeviation) is list
			assert len(self.indiv.mutationDeviation) == len(self.phen)
		
	def test_mutants_get_deviation_from_phenotype(self, instantiateSingleIndividualPopulation):
		self.indiv = instantiateSingleIndividualPopulation
		self.indiv.mutate(mutRate=1,mutStep=0.05)
		assert hasattr(self.indiv, "mutationDeviation"), "Individual is a mutant: it needs to be set a deviation from phenotype"
		
		for x in self.indiv.mutationDeviation:
			assert -1 < x < 1
			
	def test_only_mutants_change_phenotype(self, instantiateSingleDemePopulation):
		self.fakepop = instantiateSingleDemePopulation(2)
		self.mutantIndivTrue = self.fakepop.allPopulationDemes[0].individuals[0]
		self.mutantIndivFalse = self.fakepop.allPopulationDemes[0].individuals[1]
		
		self.mutantIndivTrue.mutate(mutRate=1, mutStep=0.05)
		assert self.mutantIndivTrue.mutant, "Uh-oh, looks like the individual did not mutate when it should have..."
		assert all([x != 0 for x in self.mutantIndivTrue.mutationDeviation]), "Your mutant (bool={0}) phenotype does not deviate!".format(self.mutantIndivTrue.mutant)
		
		self.mutantIndivFalse.mutate(mutRate=0, mutStep=0.05)
		assert not self.mutantIndivFalse.mutant
		assert all([x == 0 for x in self.mutantIndivFalse.mutationDeviation]), "Phenotype deviates even though individual not a mutant!"
		
	def test_mutation_deviation_follows_normal_distribution(self, instantiateSingleDemePopulation):
		random.seed(30)
		self.nIndividuals = 1000
		self.fakepop = instantiateSingleDemePopulation(self.nIndividuals)
		
		self.distri = []
		for ind in self.fakepop.allPopulationDemes[0].individuals:
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
		
		self.trueMutant = self.fakepop.allPopulationDemes[0].individuals[0]
#		self.falseMutant = self.fakepop.allPopulationDemes[0].individuals[1]
		
		self.oldPhenTrueMutant = self.trueMutant.phenotypicValues
#		self.oldPhenFalseMutant = self.falseMutant.phenotypicValues
		
		self.trueMutant.mutate(mutRate=1, mutStep=0.05)
		assert type(self.oldPhenTrueMutant) is list and type(self.trueMutant.mutationDeviation) is list, "Check that both {0} and {1} are lists".format(self.oldPhenTrueMutant, self.trueMutant.mutationDeviation)
		assert list(map(add, self.oldPhenTrueMutant, self.trueMutant.mutationDeviation)) == self.trueMutant.phenotypicValues, "Deviation not added to phenotype mutant!"
		
#		self.falseMutant.mutate(mutRate=0, mutStep=0.05)
#		assert list(map(add, self.oldPhenFalseMutant, [0] * len(self.oldPhenFalseMutant))) == self.falseMutant.phenotypicValues, "Deviation added to non-mutant phenotype!"
		
	def test_mutation_does_not_affect_phenotype_size(self, instantiateSingleIndividualPopulation):
		self.indiv = instantiateSingleIndividualPopulation
		self.phen = self.indiv.phenotypicValues
		
		self.indiv.mutate(mutRate=1, mutStep=0.05)
		assert len(self.phen) == len(self.indiv.phenotypicValues)
		
class TestMigrationFunction(object):
	
	def test_idividual_has_destination_deme_after_migration(self, instantiateSingleDemePopulation):
		self.fakepop = instantiateSingleDemePopulation(1)
		self.indiv = self.fakepop.allPopulationDemes[0].individuals[0]
		self.indiv.migrate(nDemes=self.fakepop.numberOfDemes, migRate=self.fakepop.migrationRate)
		
		assert hasattr(self.indiv, "destinationDeme"), "Your individual is going nowhere: no destination deme!"
		
	def test_migration_returns_a_destination_deme_of_correct_format(self, instantiateSingleDemePopulation):
		"""The migration function should return the new deme, which is an integer among all demes"""
		self.fakepop = instantiateSingleDemePopulation(1)
		self.indiv = self.fakepop.allPopulationDemes[0].individuals[0]
		self.indiv.migrate(nDemes=self.fakepop.numberOfDemes, migRate=self.fakepop.migrationRate)
		
		assert type(self.indiv.destinationDeme) is int, "{0} is {1} instead of integer".format(self.indiv.destinationDeme, type(self.indiv.destinationDeme))
		assert self.indiv.destinationDeme in range(self.fakepop.numberOfDemes)
		
	def test_migrants_are_defined_properly(self, instantiateSingleDemePopulation):
		self.fakepop = instantiateSingleDemePopulation(1)
		self.indiv = self.fakepop.allPopulationDemes[0].individuals[0]
		self.indiv.migrate(nDemes=self.fakepop.numberOfDemes, migRate=self.fakepop.migrationRate)
		
		assert hasattr(self.indiv, "migrant"), "Your individual does not know whether to migrate or not"
		assert type(self.indiv.migrant) is bool, "Migrant must be a boolean"		
		
	def test_migrants_are_drawn_from_binomial(self, instantiateSingleDemePopulation):
		random.seed(30)
		self.nIndividuals = 1000
		self.fakepop = instantiateSingleDemePopulation(self.nIndividuals)
		
		self.migrantCount = 0
		for ind in self.fakepop.allPopulationDemes[0].individuals:
			ind.migrate(nDemes=self.fakepop.numberOfDemes, migRate=self.fakepop.migrationRate)
			if ind.migrant:
				self.migrantCount += 1
		
		stat1, pval1 = scistats.ttest_1samp([1] * self.migrantCount + [0] * (self.nIndividuals - self.migrantCount), self.fakepop.migrationRate)
		assert pval1 > 0.05, "T-test mean failed. Observed: {0}, Expected: {1}".format(self.migrantCount/self.nIndividuals, self.fakepop.migrationRate)
		self.test = scistats.binom_test(self.migrantCount, self.nIndividuals, self.fakepop.migrationRate, alternative = "two-sided")
		assert self.test > 0.05, "Success rate = {0} when mutation rate = {1}".format(self.migrantCount/self.nIndividuals,self.fakepop.migrationRate)
		
	def test_only_migrants_change_deme(self, instantiateSingleDemePopulation):
		self.fakepop = instantiateSingleDemePopulation(2)
		self.migrantIndivTrue = self.fakepop.allPopulationDemes[0].individuals[0]
		self.migrantIndivFalse = self.fakepop.allPopulationDemes[0].individuals[1]
		
		self.migrantIndivTrue.migrate(2, migRate=1)
		assert self.migrantIndivTrue.migrant, "Uh-oh, looks like the individual did not migrate when it should have..."
		assert self.migrantIndivTrue.currentDeme != self.migrantIndivTrue.destinationDeme, "Individual destination deme is the same as current even though it should migrate!"
		
		self.migrantIndivFalse.migrate(2, migRate=0)
		assert not self.migrantIndivFalse.migrant, "Uh-oh, looks like the individual did migrate when it shouldn't have..."
		assert self.migrantIndivTrue.currentDeme == self.migrantIndivTrue.destinationDeme, "Individual destination deme is different from current even though it does not migrate!"
		
		
class TestDeme(object):
	
	def test_deme_attributes(self, objectAttributesExist):
		self.deme = Dem()
		self.attributes = ["id", "demography", "publicGood", "neighbours"]
		testAttr, whichAttr = objectAttributesExist(self.deme, self.attributes)
		assert testAttr, "Deme is missing attribute(s) {0}".format(whichAttr)
		
	def test_deme_object_knows_itself(self, instantiateSingleDemePopulation):
		self.fakepop = Pop()
		self.fakepop.createAndPopulateDemes(self.fakepop.numberOfDemes,1)
		
		for deme in range(self.fakepop.numberOfDemes):
			focalDeme = self.fakepop.allPopulationDemes[deme]
			assert type(focalDeme.id) is int
			assert focalDeme.id == deme, "Deme number {0} has wrong id ={1}".format(deme, focalDeme.id)
	
	def test_deme_object_knows_other_demes(self):
		self.fakepop = Pop()
		self.nd = self.fakepop.numberOfDemes
		self.alldemeslist = list(range(self.nd))
		self.fakepop.createAndPopulateDemes(self.nd,1)
		
		for deme in range(self.nd):
			focalDeme = self.fakepop.allPopulationDemes[deme]
			otherDemes = self.alldemeslist
			del otherDemes[focalDeme.id]
			assert type(focalDeme.neighbours) is list
			assert focalDeme.neighbours == otherDemes, "Know who your neighbours are!"

class TestPopulation(object):
	
	def assertObjectAttributesAreNotNone(self, obj, attrs):
		for attr in attrs:
			assert getattr(obj, attr) is not None, "object {0} has attribute {1} set to None".format(obj, attr)
	
	def test_population_contains_demes(self):
		self.pop = Pop()
		self.pop.createAndPopulateDemes()
		assert hasattr(self.pop, "allPopulationDemes"), "This population has no deme yet!"
		
		for deme in self.pop.allPopulationDemes:
			assert type(deme) is Dem
			
	def test_demes_are_populated(self):
		self.pop = Pop()
		self.pop.createAndPopulateDemes()
		for deme in self.pop.allPopulationDemes:
			assert hasattr(deme, "individuals"), "{0} is not populated. Create a list of individuals!".format(deme)
			for ind in deme.individuals:
				assert type(ind) is Ind
				
	def test_individual_attributes_are_non_empty(self):
		self.pop = Pop()
		self.pop.createAndPopulateDemes()
		for deme in self.pop.allPopulationDemes:
			for ind in deme.individuals:
				self.assertObjectAttributesAreNotNone(ind, ["phenotypicValues", "currentDeme"])

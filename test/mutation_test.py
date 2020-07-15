import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop
import scipy.stats as scistats
from operator import add
from statistics import mean
import gc

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

	def test_mutants_depend_on_seed(self, pseudorandom, instantiateSingleDemePopulation):
		self.nIndividuals = 1000
		self.fakepop = instantiateSingleDemePopulation(self.nIndividuals)

		mutants = []

		for ind in self.fakepop.individuals:
			pseudorandom(0)
			ind.mutate(mutRate=self.fakepop.mutationRate, mutStep=self.fakepop.mutationStep)
			mutants.append(ind.mutant)

		assert all(mutants) or not any(mutants), "Mutant does not depend on seed: {0}".format(set(mutants))
		
	def test_mutants_are_drawn_from_binomial(self, pseudorandom, instantiateSingleDemePopulation):
		pseudorandom(0)
		self.nIndividuals = 1000
		self.fakepop = instantiateSingleDemePopulation(self.nIndividuals)
		self.mutationRate = 0.2
		
		self.mutantCount = 0
		for ind in self.fakepop.individuals:
			ind.mutate(mutRate=self.mutationRate, mutStep=0.05)
			if ind.mutant:
				self.mutantCount += 1
		
		stat1, pval1 = scistats.ttest_1samp([1] * self.mutantCount + [0] * (self.nIndividuals - self.mutantCount), self.mutationRate)
		assert pval1 > 0.05, "T-test mean failed. Observed: {0}, Expected: {1}".format(self.mutantCount/self.nIndividuals, self.mutationRate)
		self.test = scistats.binom_test(self.mutantCount, self.nIndividuals, self.mutationRate, alternative = "two-sided")
		assert self.test > 0.05, "Success rate = {0} when mutation rate = {1}".format(self.mutantCount/self.nIndividuals, self.mutationRate)
		
		gc.collect()

	def test_deviation_depends_on_seed(self, pseudorandom, instantiateSingleDemePopulation):
		self.nIndividuals = 1000
		self.fakepop = instantiateSingleDemePopulation(self.nIndividuals)

		mutationDeviations = []

		for ind in self.fakepop.individuals:
			pseudorandom(0)
			ind.mutate(mutRate=1, mutStep=self.fakepop.mutationStep)
			mutationDeviations.append(ind.mutationDeviation)

		assert all([x == mutationDeviations[0] for x in mutationDeviations]), "Mutation deviation does not depend on seed: {0}".format(set(mutationDeviations))
		
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
		
	def test_mutation_deviation_follows_normal_distribution(self, pseudorandom, instantiateSingleDemePopulation):
		pseudorandom(0)
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
		stat3, pval3 = scistats.shapiro(self.distri)
		assert pval3 > 0.05, "Test of normality failed"

		gc.collect()
 
	def test_mutation_adds_deviation_to_phenotype(self, instantiateSingleDemePopulation):
		self.fakepop = instantiateSingleDemePopulation(2)
		
		# WHEN THERE IS MUTATION
		self.trueMutant = self.fakepop.individuals[0]
		self.oldPhenTrueMutant = self.trueMutant.phenotypicValues
		
		self.trueMutant.mutant = True
		self.trueMutant.deviate(ms=0.05,n=len(self.oldPhenTrueMutant))
		assert all(x != 0 for x in self.trueMutant.mutationDeviation), "Deviation = {0}".format(self.trueMutant.mutationDeviation)
		
		self.trueMutant.applyMutation(self.trueMutant.mutationDeviation, bounded = True)
		assert all(x != y for x, y in zip(self.trueMutant.phenotypicValues, self.oldPhenTrueMutant)), "New:{0}, Old:{1}".format(self.falseMutant.phenotypicValues, self.oldPhenFalseMutant)
		
		# Reset to test the whole thing together:
		self.trueMutant.phenotypicValues = self.oldPhenTrueMutant
		self.trueMutant.mutant = None
		self.trueMutant.mutationDeviation = None
		
		self.trueMutant.mutate(mutRate=1, mutStep=0.05)
		assert type(self.oldPhenTrueMutant) is list and type(self.trueMutant.mutationDeviation) is list, "Check that both {0} and {1} are lists".format(self.oldPhenTrueMutant, self.trueMutant.mutationDeviation)
		
		for i in range(len(self.oldPhenTrueMutant)):
			assert min(1, max(0, self.oldPhenTrueMutant[i] + self.trueMutant.mutationDeviation[i])) == pytest.approx(self.trueMutant.phenotypicValues[i]), "Deviation not added to mutant phenotype no {0}: returns {1} instead of {2}!".format(i, self.trueMutant.phenotypicValues[i], self.oldPhenTrueMutant[i] + self.trueMutant.mutationDeviation[i])
		
		# WHEN THERE IS NO MUTATION
		self.falseMutant = self.fakepop.individuals[1]
		self.oldPhenFalseMutant = self.falseMutant.phenotypicValues
		
		self.falseMutant.mutant = False
		self.falseMutant.deviate(ms=0.05, n=len(self.oldPhenFalseMutant))
		assert self.falseMutant.mutationDeviation == [0] * len(self.oldPhenFalseMutant), "Deviation = {0}".format(self.falseMutant.mutationDeviation)
		
		self.falseMutant.applyMutation(self.falseMutant.mutationDeviation, bounded = True)
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

	def test_individual_mutation_can_be_unbounded(self, instantiateSingleDemePopulation):
		self.pop = instantiateSingleDemePopulation(100)
		self.pop.initialPhenotypes = [1,1,1,1]
		self.pop.createAndPopulateDemes()

		collectPhenotypes = []

		for ind in self.pop.individuals:
			ind.mutate(1,0.5,bounded = False)
			for phen in ind.phenotypicValues:
				collectPhenotypes.append(phen)

		assert any([i > 1 for i in collectPhenotypes]), "no phenotype went over 1, even when unbounded."

	def test_population_mutation_can_be_unbounded(self, instantiateSingleIndividualsDemes):
		self.pop = Pop(inst='test/test', mutationBoundaries = False)
		self.pop.numberOfDemes = 10
		self.pop.initialDemeSize = 10
		self.pop.mutationRate = 1
		self.pop.mutationStep = 0.5
		self.pop.migrationRate = 0
		self.pop.initialPhenotypes

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()

		collectPhenotypes = []

		for ind in self.pop.individuals:
			for phen in ind.phenotypicValues:
				collectPhenotypes.append(phen)

		assert any([i > 1 for i in collectPhenotypes]), "no phenotype went over 1, even when unbounded."


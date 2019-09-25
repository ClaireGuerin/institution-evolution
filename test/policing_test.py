import pytest
import institutionevolution.fitness as fitness
from institutionevolution.population import Population as Pop

class TestPolicingFunction(object):

	def test_policing_function_returns_value_correct_format(self, getFitnessParameters):
		pars = getFitnessParameters('policing')
		reproductiveValue = fitness.functions['policing'](1, **pars)

		assert reproductiveValue is not None, "Fitness function with policing returns None"
		assert type(reproductiveValue) is float, "Fitness function with policing returns a {0} instead of a float".format(type(reproductiveValue))
		assert reproductiveValue >= 0, "Fitness function with policing returns a negative value"

	def test_policing_depends_on_public_good(self, getFitnessParameters):
		fitfun = 'policing'
		self.fakepop = Pop(fitfun)
		self.fakepop.fitnessParameters = getFitnessParameters(fitfun)
		self.fakepop.numberOfDemes = 2
		self.fakepop.initialDemeSize = 10
		self.fakepop.individualResources = 4
		self.fakepop.initialPhenotypes = [0.2,0.3]
		self.fakepop.numberOfPhenotypes = len(self.fakepop.initialPhenotypes)
		self.fakepop.migrationRate = 0
		self.fakepop.mutationRate = 0

		self.fakepop.createAndPopulateDemes()
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()

		for ind in range(self.fakepop.demography):
			indiv = self.fakepop.individuals[ind]
			indiv.fertility(self.fakepop.fit_fun, **self.fakepop.fitnessParameters)
			assert self.fakepop.demes[indiv.currentDeme].publicGood % indiv.fertilityValue == 0
import pytest
import institutionevolution.fitness as fitness

class TestPolicingFunction(object):

	def test_policing_function_returns_value_correct_format(self, getFitnessParameters):
		pars = getFitnessParameters('policing')
		reproductiveValue = fitness.functions['policing'](1, **pars)

		assert reproductiveValue is not None, "Fitness function with policing returns None"
		assert type(reproductiveValue) is float, "Fitness function with policing returns a {0} instead of a float".format(type(reproductiveValue))
		assert reproductiveValue >= 0, "Fitness function with policing returns a negative value"

	def test_policing_depends_on_public_good(self, instantiateSingleDemePopulation,getFitnessParameters):
		self.fakepop = instantiateSingleDemePopulation(10)
		self.fakepop.fitnessParameters = getFitnessParameters('policing')
		self.fakepop.fit_fun = 'policing'
		pg = self.fakepop.demes[0].publicGood

		self.fakepop.createAndPopulateDemes()

		for ind in range(self.fakepop.demography):
			indiv = self.fakepop.individuals[ind]
			indiv.fertility(self.fakepop.fit_fun, **self.fakepop.fitnessParameters)
			assert pg % indiv.fertilityValue == 0
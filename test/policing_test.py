import pytest
import institutionevolution.fitness as fitness
from institutionevolution.population import Population as Pop
from institutionevolution.deme import Deme as Dem
import gc

class TestPolicingFunction(object):

	def test_policing_function_returns_value_correct_format(self, getFitnessParameters):
		pars = getFitnessParameters('policing')
		reproductiveValue = fitness.functions['policing'](1, **pars)

		assert reproductiveValue is not None, "Fitness function with policing returns None"
		assert type(reproductiveValue) is float, "Fitness function with policing returns a {0} instead of a float".format(type(reproductiveValue))
		assert reproductiveValue >= 0, "Fitness function with policing returns a negative value"

		gc.collect()

	def test_fertility_depends_on_public_good(self, getFitnessParameters):
		fitfun = 'policing'
		self.fakepop = Pop(fitfun)
		self.fakepop.fitnessParameters = getFitnessParameters(fitfun)
		self.fakepop.numberOfDemes = 2
		self.fakepop.initialDemeSize = 1
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
			if indiv.currentDeme == 0:
				self.fakepop.fitnessParameters.update({"pg": 1})
				indiv.fertility(self.fakepop.fit_fun, **self.fakepop.fitnessParameters)
				fertility0 = indiv.fertilityValue
			elif indiv.currentDeme == 1:
				self.fakepop.fitnessParameters.update({"pg": 3})
				indiv.fertility(self.fakepop.fit_fun, **self.fakepop.fitnessParameters)
				fertility1 = indiv.fertilityValue

		assert fertility0 < fertility1

		gc.collect()

	def test_individual_fertility_calculation(self, getFitnessParameters):
		fitfun = 'policing'
		kwargs = getFitnessParameters(fitfun)
		self.fakepop = Pop(fitfun)
		self.fakepop.fitnessParameters = kwargs
		self.fakepop.numberOfDemes = 2
		self.fakepop.initialDemeSize = 10
		self.fakepop.individualResources = 2
		self.fakepop.initialPhenotypes = kwargs["x"]
		self.fakepop.numberOfPhenotypes = len(self.fakepop.initialPhenotypes)
		self.fakepop.migrationRate = 0
		self.fakepop.mutationRate = 0

		self.fakepop.createAndPopulateDemes()
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()

		for ind in self.fakepop.individuals:
			# x = ind.phenotypicValues[0]
			# y = ind.phenotypicValues[1]
			# p = self.fakepop.demes[ind.currentDeme].publicGood
			# n = self.fakepop.demes[ind.currentDeme].demography

			# kwargs.update({"x":ind.phenotypicValues, "pg":p, "n":n})

			x = kwargs["x"][0]
			y = kwargs["x"][1]
			p = kwargs["pg"]
			n = kwargs["n"]
			ind.fertility(fitfun, **kwargs)
			payoff = (1 - x) * ind.resourcesAmount + kwargs["b"] * (1 - y) * (p / n) - kwargs["c"] * y * ((1 - x) ** 2) * (p / n)
			assert ind.fertilityValue == (kwargs["fb"] * payoff) / (kwargs["gamma"] * n), "Fitness function does not return what is expected"
			assert ind.fertilityValue == 22.385, "python disagrees with mathematica. Payoff {0}(p) vs {1}(m). Parameters: {2}".format(payoff, 1.11925, kwargs)

		gc.collect()

	def test_population_fertility_calculation(self):
		fitfun = 'policing'
		self.fakepop = Pop()
		self.fakepop.fit_fun = fitfun
		self.fakepop.fitnessParameters = {"b":0.5,
		"c":0.05,
		"fb":2,
		"gamma":0.01}
		self.fakepop.numberOfDemes = 2
		self.fakepop.initialDemeSize = 10
		self.fakepop.individualResources = 2
		self.fakepop.initialPhenotypes = [0.2, 0.5]
		self.fakepop.numberOfPhenotypes = len(self.fakepop.initialPhenotypes)
		self.fakepop.migrationRate = 0
		self.fakepop.mutationRate = 0

		self.fakepop.createAndPopulateDemes()
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()

		x = self.fakepop.initialPhenotypes[0]
		y = self.fakepop.initialPhenotypes[1]
		r = self.fakepop.individualResources
		b = self.fakepop.fitnessParameters["b"]
		c = self.fakepop.fitnessParameters["c"]
		fb = self.fakepop.fitnessParameters["fb"]
		gamma = self.fakepop.fitnessParameters["gamma"]
		n = self.fakepop.initialDemeSize
		p = x * r * n

		payoff = (1 - x) * r + b * (1 - y) * (p / n) - c * y * (p / n) * ((1 - x) ** 2)
		expectedFertility = (fb * payoff) / (gamma * n)

		for indiv in self.fakepop.individuals:
			# REPRODUCTION
			infoToAdd = {}
			infoToAdd["n"] = self.fakepop.demes[indiv.currentDeme].demography
			infoToAdd["xmean"] = self.fakepop.demes[indiv.currentDeme].meanPhenotypes
			infoToAdd["pg"] = self.fakepop.demes[indiv.currentDeme].publicGood
			infoToAdd["x"] = indiv.phenotypicValues

			test = fitness.functions['policing'](r, **{**self.fakepop.fitnessParameters, **infoToAdd})
			assert test == expectedFertility, "pars fed to function = res: {1}, {0}".format({**self.fakepop.fitnessParameters, **infoToAdd}, indiv.resourcesAmount)
			#assert False, test

			indiv.fertility(self.fakepop.fit_fun, **{**self.fakepop.fitnessParameters, **infoToAdd})
			assert indiv.fertilityValue == expectedFertility, "pars fed to function {2} = res: {1}, {0}".format({**self.fakepop.fitnessParameters, **infoToAdd}, indiv.resourcesAmount, self.fakepop.fit_fun)

			indiv.reproduce(self.fakepop.fit_fun, **{**self.fakepop.fitnessParameters, **infoToAdd})
			assert indiv.fertilityValue == expectedFertility, "pars fed to function {2} = res: {1}, {0}".format({**self.fakepop.fitnessParameters, **infoToAdd}, indiv.resourcesAmount, self.fakepop.fit_fun)

		gc.collect()

	def test_policing_function_in_population_reproduction(self):
		self.fakepop = Pop()
		self.fakepop.fit_fun = 'policing'
		self.fakepop.numberOfDemes = 3
		self.fakepop.initialDemeSize = 3
		self.fakepop.createAndPopulateDemes()
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()

		try:
			self.fakepop.populationReproduction(**self.fakepop.fitnessParameters)
		except Exception as e:
			assert False, "something went wrong, raised {0}: {1}".format(e.__class__.__name__, str(e))

	def test_deme_has_policing_consensus(self):
		self.fakeDeme = Dem()

		assert hasattr(self.fakeDeme, "policingConsensus")
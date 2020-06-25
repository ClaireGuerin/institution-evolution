import pytest
import institutionevolution.fitness as fitness
from institutionevolution.population import Population as Pop
from institutionevolution.individual import Individual as Ind
import gc
import glob, os
from files import OUTPUT_FOLDER

class TestPolicingDemographyFunction(object):

	def test_function_returns_value_correct_format(self, getFitnessParameters):
		pars = getFitnessParameters('policingdemog')
		reproductiveValue = fitness.functions['policingdemog'](1, **pars)

		assert reproductiveValue is not None, "Fitness function with policing and demography regulation returns None"
		assert type(reproductiveValue) is float, "Fitness function with policing and demography regulation returns a {0} instead of a float".format(type(reproductiveValue))
		#assert reproductiveValue >= 0, "Fitness function with policing and demography regulation returns a negative value"

	def test_individual_gets_correct_value(self, getFitnessParameters, instantiateSingleIndividualPopulation):
		pars = getFitnessParameters('policingdemog')
		ind = instantiateSingleIndividualPopulation

		ind.fertility('policingdemog',**pars)
		reproductiveValue = fitness.functions['policingdemog'](1, **pars)

		assert reproductiveValue == ind.fertilityValue, "Individual is not assigned the correct fertility value"

	def test_offspring_cannot_go_negative(self, getFitnessParameters, instantiateSingleIndividualPopulation):
		pars = getFitnessParameters('policingdemog')
		ind = instantiateSingleIndividualPopulation

		ind.fertility('policingdemog',**pars)
		try:
			ind.procreate()
		except ValueError as e:
			assert False, "Poisson ditribution cannot draw offspring number from negative lambda value" + str(e)

	def test_all_pars_provided_in_test(self, getFitnessParameters):
		pars = getFitnessParameters('policingdemog')
		list_of_parameters = ["x", "xmean", "n", "phi", "th", "rb", "kb", "p", "alpha", "gamma", "beta0", "beta1", "epsilon", "eta", "zeta0", "zeta1"]
		presence = [i in pars for i in list_of_parameters]

		assert all(presence), "fitness parameters missing:{0}".format([i for i in list_of_parameters if i not in pars])


	def test_function_calculation_right(self, getFitnessParameters):
		pars = getFitnessParameters('policingdemog')
		reproductiveValue = fitness.functions['policingdemog'](1, **pars)

		x = pars["x"][0]
		assert x >= 0, "{0}".format(x)
		assert type(x) is float
		xmean = pars["xmean"][0]
		assert xmean >= 0
		assert type(xmean) is float
		n = pars["n"]
		assert n >= 0
		assert type(n) is int

		b = pars["alpha"] * (((1 - pars["p"]) * n * xmean) ** pars["gamma"]) / (pars["beta1"] + pars["beta0"] * (((1 - pars["p"]) * n * xmean) ** pars["gamma"]))
		d = pars["epsilon"] * ((pars["p"] * n * xmean) ** pars["eta"]) / (pars["zeta1"] + pars["zeta0"] * ((pars["p"] * n * xmean) ** pars["eta"]))
		r = pars["rb"]/n + b / n - pars["kb"] * x - (1 - x) * d / ((1 - xmean) * n)

		assert reproductiveValue == pars["phi"] * r / (1 + r * pars["th"])

	# def test_simulation_does_not_run_if_pars_missing(self):
	# 	fakepop = Pop("policingdemog")
	# 	fakepop.fitnessParameters = {}

	# 	fakepop.createAndPopulateDemes(3,3)
	# 	try:
	# 		fakepop.populationReproduction(**fakepop.fitnessParameters)
	# 	except KeyError as e:
	# 		assert str(e) == 'Missing fitness parameters for policing demography'
	# 	else:
	# 		assert False, "do not let simulations be called when pars are missing"

	def test_function_runs_at_population_level(self):
		fakepop = Pop(fit_fun='policingdemog', inst='test')
		fakepop.numberOfDemes = 3
		fakepop.initialDemeSize = 4

		fakepop.createAndPopulateDemes()
		fakepop.clearDemeInfo()
		fakepop.populationMutationMigration()
		fakepop.updateDemeInfo()
		
		try:
			fakepop.populationReproduction(**fakepop.fitnessParameters)
		except:
			assert False, "not running"

	def test_simulation_cycle(self):
		fakepop = Pop(fit_fun='policingdemog', inst='test')
		fakepop.numberOfDemes = 3
		fakepop.initialDemeSize = 10
		fakepop.numberOfGenerations = 10

		self.out = 'output_test'

		try:
			fakepop.runSimulation(outputfile=self.out)
			for f in glob.glob('{0}/test/{1}'.format(OUTPUT_FOLDER, self.out)):
				os.remove(f)
		except ValueError as e:
			assert False, str(e)


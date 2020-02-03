import pytest
import institutionevolution.fitness as fitness
from institutionevolution.population import Population as Pop
import gc

class TestPolicingDemographyFunction(object):

	def test_function_returns_value_correct_format(self, getFitnessParameters):
		pars = getFitnessParameters('policingdemog')
		reproductiveValue = fitness.functions['policingdemog'](1, **pars)

		assert reproductiveValue is not None, "Fitness function with policing and demography regulation returns None"
		assert type(reproductiveValue) is float, "Fitness function with policing and demography regulation returns a {0} instead of a float".format(type(reproductiveValue))
		assert reproductiveValue >= 0, "Fitness function with policing and demography regulation returns a negative value"

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
		r = pars["rb"] + b / n - pars["kb"] * x - (1 - x) * d / ((1 - xmean) * n)

		assert reproductiveValue == pars["phi"] * r / (1 + r * pars["th"])
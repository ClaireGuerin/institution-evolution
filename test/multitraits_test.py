import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop
import institutionevolution.fitness as fitness
from files import PARAMETER_FOLDER, INITIAL_PHENOTYPES_FILE, OUTPUT_FOLDER
import os
from math import exp, sqrt

class TestMultipleTraits(object):

	def test_phenotype_can_be_multiple(self):
		self.ntraits = 2
		with open('{0}/{1}'.format(PARAMETER_FOLDER, INITIAL_PHENOTYPES_FILE), "w") as f:
			for i in range(self.ntraits):
				f.write('{0}\n'.format(i/self.ntraits))

		self.fakepop = Pop()
		self.fakepop.numberOfDemes = 3
		self.fakepop.initialDemeSize = 2
		self.fakepop.numberOfGenerations = 5

		self.fakepop.createAndPopulateDemes()

		try:
			self.fakepop.runSimulation('tmptest')
		except Exception as e:
			assert False, "Simulation does not run with multiple traits because of {0}: {1}".format(e.__class__.__name__, str(e))
		else:
			os.remove(OUTPUT_FOLDER + '/tmptest_phenotypes.txt')
			os.remove(OUTPUT_FOLDER + '/tmptest_demography.txt')

	def test_all_phenotype_means_in_output(self):
		self.ntraits = 4
		with open('{0}/{1}'.format(PARAMETER_FOLDER, INITIAL_PHENOTYPES_FILE), "w") as f:
			for i in range(self.ntraits):
				f.write('{0}\n'.format(i/self.ntraits))

		self.fakepop = Pop()
		assert self.fakepop.numberOfPhenotypes == self.ntraits, "uh-oh, the test did not change the number of phenotypes"

		self.fakepop.numberOfDemes = 3
		self.fakepop.initialDemeSize = 2
		self.fakepop.numberOfGenerations = 5

		self.fakepop.createAndPopulateDemes()
		self.fakepop.runSimulation('tmptest')
		
		with open(OUTPUT_FOLDER + '/tmptest_phenotypes.txt') as fp:
			firstline = fp.readline()
			phenotypeMeans = firstline.split(',')

		assert len(phenotypeMeans) == self.ntraits, "Simulation returns mean of {0} phenotypes instead of {1}".format(len(phenotypeMeans), self.ntraits)

		#os.remove(OUTPUT_FOLDER + '/tmptest_phenotypes.txt')
		#os.remove(OUTPUT_FOLDER + '/tmptest_demography.txt')

	def test_stabilizing_selection_fitness_function_is_set(self):
		assert 'geom' in fitness.functions, "Did not find 'geom' method in fitness functions dictionary"
		kwargs = {"fb": 2, "x": [0.5], "gamma": 0.07, "n": 20}		
		assert fitness.functions['geom'](1, **kwargs) is not None, "Fisher's geometric function does not return a fertility value"
		assert type(fitness.functions['geom'](1, **kwargs)) is float, "Fisher's geometric function does not return a valid fertility value: {0}".format(type(fitness.functions['geom'](1)))

	def test_stabilizing_selection_fitness_function_gives_correct_fertility_value(self, instantiateSingleIndividualPopulation):
		self.indiv = instantiateSingleIndividualPopulation
		self.ntraits = 4
		self.indiv.phenotypicValues = [1.0] * self.ntraits
		kwargs = {"fb":2, "x":self.indiv.phenotypicValues, "xmean":[0.2] * self.ntraits, "gamma":0.07, "n":20}
		expected = kwargs["fb"] * exp(-sqrt(sum([x ** 2 for x in self.indiv.phenotypicValues]))) / (1 + kwargs["gamma"] * kwargs["n"])
		self.indiv.fertility(fun_name='geom', **kwargs)

		assert self.indiv.fertilityValue == expected, "Fisher's geometric function should return a fertility of {0}, not {1}".format(expected, self.indiv.fertilityValue)

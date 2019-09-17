import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop
from files import PARAMETER_FOLDER, INITIAL_PHENOTYPES_FILE, OUTPUT_FOLDER
import os

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
			self.fakepop.runSimulation('tmptest.txt')
		except:
			assert False, "Simulation does not run with multiple traits"

		os.remove('{0}/tmptest.txt'.format(OUTPUT_FOLDER))


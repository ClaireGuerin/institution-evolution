import pytest
import os
import sys
from institutionevolution.population import Population as Pop
from files import PARAMETER_FOLDER, INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, INITIAL_TECHNOLOGY_FILE, PARAMETER_FILE, OUTPUT_FOLDER, FITNESS_PARAMETERS_FILE

class TestAutomaticWorkflow(object):

	def test_single_sim_reads_and_writes_from_same_folder(self):
		self.pop = Pop(inst='test')
		self.pop.runSimulation()

		assert ["consensus", "demography", "phenotypes", "resources", "technology"] in os.listdir('test')

	def test_script_writes_par_files(self):
		launcher = open("launch_simulations.py").read()
		sys.argv = ["launch_simulations.py", "arg1", "arg2", "arg3"]
		exec(launcher)

		self.dirpath = os.getcwd()
		self.fileslist = os.listdir('{0}/{1}/{2}'.format(self.dirpath, PARAMETER_FOLDER, "workflow_test"))

		assert INITIALISATION_FILE in self.fileslist, "{0} not found".format(INITIALISATION_FILE)
		assert INITIAL_PHENOTYPES_FILE in self.fileslist, "{0} not found".format(INITIAL_PHENOTYPES_FILE)
		assert PARAMETER_FILE in self.fileslist, "{0} not found".format(PARAMETER_FILE)
		assert FITNESS_PARAMETERS_FILE in self.fileslist, "{0} not found".format(FITNESS_PARAMETERS_FILE)
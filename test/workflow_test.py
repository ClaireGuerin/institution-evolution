import pytest
from files import PARAMETER_FOLDER, INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, INITIAL_TECHNOLOGY_FILE, PARAMETER_FILE, OUTPUT_FOLDER, FITNESS_PARAMETERS_FILE

class TestAutomaticWorkflow(object):

	def test_script_writes_par_files(self):
		exec(open("script.py").read())

		self.dirpath = os.getcwd()
		self.fileslist = os.listdir('{0}/{1}'.format(self.dirpath, PARAMETER_FOLDER))

		assert INITIALISATION_FILE in self.fileslist, "{0} not found".format(INITIALISATION_FILE)
		assert INITIAL_PHENOTYPES_FILE in self.fileslist, "{0} not found".format(INITIAL_PHENOTYPES_FILE)
		assert PARAMETER_FILE in self.fileslist, "{0} not found".format(PARAMETER_FILE)
		assert FITNESS_PARAMETERS_FILE in self.fileslist, "{0} not found".format(FITNESS_PARAMETERS_FILE)
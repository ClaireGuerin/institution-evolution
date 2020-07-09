import pytest
import re
import os
import sys
import shutil
from io import StringIO
from ast import literal_eval
from launch_multiple_simulations import Launcher
import institutionevolution.filemanip as fman
from institutionevolution.population import Population as Pop
from files import INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, INITIAL_TECHNOLOGY_FILE, PARAMETER_FILE, FITNESS_PARAMETERS_FILE

class TestAutomaticWorkflow(object):

	def test_single_sim_reads_and_writes_from_same_folder(self):
		shutil.copytree('pars/test', 'simulations')
		self.pop = Pop(inst='simulations')
		self.pop.numberOfGenerations = 3
		self.pop.runSimulation()

		self.outputfiles = ["out_consensus.txt", "out_demography.txt", "out_phenotypes.txt", "out_resources.txt", "out_technology.txt"] 

		for file in self.outputfiles:
			assert file in os.listdir('simulations')

		shutil.rmtree('simulations')

	def test_script_reads_arguments_properly(self):
		self.l = Launcher("tralala", "blablabla")

		assert self.l.metafolder == "tralala"
		assert self.l.parfile == "blablabla"

	def test_script_creates_metafolder(self):
		self.l = Launcher("simulations", "blablabla")
		self.l.createMetaFolder()

		assert os.path.exists('simulations') == 1, "did not create metafolder"
		shutil.rmtree('simulations')

	def test_script_writes_par_files(self):
		self.l = Launcher("simulations", "blablabla")
		self.l.writeParameterFiles(fitval="")

		self.dirpath = os.getcwd()
		self.fileslist = os.listdir('simulations/pgg0.0first1.0secnd2.0third3.0')
		self.inputfiles = [INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, INITIAL_TECHNOLOGY_FILE, PARAMETER_FILE, FITNESS_PARAMETERS_FILE]

		try:
			for file in self.inputfiles:
				assert file in self.fileslist
				shutil.rmtree('simulations')
				os.remove('parameter_ranges.txt')
		except AssertionError:
			shutil.rmtree('simulations')
			os.remove('parameter_ranges.txt')
			assert False, "one or more parameter file(s) missing. Folder contents: {0}".format(self.fileslist)

	def test_script_handles_files_already_exists_issue(self):
		shutil.copytree('pars/test', 'simulations')
		self.l = Launcher('simulations', 'blablabla')
		self.l.writeParameterFiles('first,1.0\nsecnd,2.0\nthird,3.0')
		try:
			with open('simulations/func_first1.0secnd2.0third3.0/'+FITNESS_PARAMETERS_FILE, 'r') as f:
				assert len(f.readlines()) == 3, "file not replaced by correct parameter values"
				shutil.rmtree('simulations')
				os.remove('parameter_ranges.txt')
		except AssertionError:
			shutil.rmtree('simulations')
			os.remove('parameter_ranges.txt')
			assert False, "file not replaced by correct parameter values"

	def test_script_takes_parameter_ranges_file(self, createParameterRangesFile):
		createParameterRangesFile()
		self.l = Launcher()

		self.subfoldername = 'func_first1.0secnd2.0third3.0'

		assert os.path.exists('simulations/'+self.subfoldername), "did not create specific simulation file: {0}".format(os.listdir('simulations'))
		self.fileslist = os.listdir('simulations/'+self.subfoldername)
		self.inputfiles = [INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, INITIAL_TECHNOLOGY_FILE, PARAMETER_FILE, FITNESS_PARAMETERS_FILE]
		try:
			for file in self.inputfiles:
				assert file in self.fileslist
			pars = fman.extractColumnFromFile('simulations/'+self.subfoldername+'/'+FITNESS_PARAMETERS_FILE, 0, str)
			vals = fman.extractColumnFromFile('simulations/'+self.subfoldername+'/'+FITNESS_PARAMETERS_FILE, 1, float)
			assert pars == ['first','secnd','third'], "wrong parameter name"
			assert vals == [float(1),float(2),float(3)], "wrong parameter value"
			shutil.rmtree('simulations')
			os.remove('parameter_ranges.txt')
		except AssertionError:
			shutil.rmtree('simulations')
			os.remove('parameter_ranges.txt')
			assert False, "one or more parameter value(s) missing. File contents: {0},{1}".format(pars,vals) 

	def test_parameter_files_are_not_empty(self, createParameterRangesFile):
		createParameterRangesFile()
		self.l = Launcher()

		self.fileslist = os.listdir('simulations')
		try:
			for file in self.fileslist:
				assert os.path.getsize('simulations/'+file) != 0, "file is empty"
			shutil.rmtree('simulations')
			os.remove('parameter_ranges.txt')
		except AssertionError:
			shutil.rmtree('simulations')
			os.remove('parameter_ranges.txt')
			assert False, "file is empty"

	def test_script_can_take_parameter_ranges(self, createParameterRangesFile):
		createParameterRangesFile(multi=True)
		self.l = Launcher()

		files = folders = 0

		for _, dirnames, filenames in os.walk('simulations'):
		  # ^ this idiom means "we won't be using this value"
		    files += len(filenames)
		    folders += len(dirnames)

		shutil.rmtree('simulations')
		os.remove('parameter_ranges.txt')

		assert files == 5*4, "wrong total number of parameters files"
		assert folders == 4, "wrong number of subfolders"
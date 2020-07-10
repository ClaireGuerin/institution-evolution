import pytest
import re
import os
import sys
import shutil
from pathlib import Path
from io import StringIO
from ast import literal_eval
from launch_multiple_simulations import Launcher
import institutionevolution.filemanip as fman
from institutionevolution.population import Population as Pop
from files import INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, INITIAL_TECHNOLOGY_FILE, PARAMETER_FILE, FITNESS_PARAMETERS_FILE

class TestAutomaticWorkflow(object):

	def test_single_sim_reads_and_writes_from_same_folder(self):
		dirpath = Path('simulations')
		if dirpath.exists() and dirpath.is_dir():
			shutil.rmtree(dirpath)

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
		self.l.createFolder(self.l.metafolder)

		assert os.path.exists('simulations') == 1, "did not create metafolder"
		shutil.rmtree('simulations')

	def test_script_writes_par_files(self):
		self.l = Launcher("simulations", "blablabla")
		self.l.createFolder(self.l.metafolder)
		self.l.writeParameterFiles(fitfun="func", pname=["first","secnd","third"], pval=[1,2,3])

		self.dirpath = os.getcwd()
		self.fileslist = os.listdir('simulations/func_first1secnd2third3')
		self.inputfiles = [INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, INITIAL_TECHNOLOGY_FILE, PARAMETER_FILE, FITNESS_PARAMETERS_FILE]

		try:
			for file in self.inputfiles:
				assert file in self.fileslist
			shutil.rmtree('simulations')
		except AssertionError:
			shutil.rmtree('simulations')
			assert False, "one or more parameter file(s) missing. Folder contents: {0}".format(self.fileslist)

	def test_script_handles_files_already_exists_issue(self):
		shutil.copytree('pars/test', 'simulations')
		self.l = Launcher('simulations', 'blablabla')
		self.l.writeParameterFiles(fitfun="func", pname=["first","secnd","third"], pval=[1,2,3])
		try:
			with open('simulations/func_first1secnd2third3/'+FITNESS_PARAMETERS_FILE, 'r') as f:
				assert len(f.readlines()) == 3, "file not replaced by correct parameter values"
			shutil.rmtree('simulations')
		except AssertionError:
			shutil.rmtree('simulations')
			assert False, "file not replaced by correct parameter values"

	def test_script_reads_parameter_ranges_file(self, createParameterRangesFile):
		# SIMPLE, NO RANGES

		createParameterRangesFile()
		self.l = Launcher('simulations', 'parameter_ranges.txt')
		self.l.readParameterInfo()

		#assert False, "names:{0},start:{1},end:{2},step:{3},fit:{4}".format(self.l.parname,self.l.parstart,self.l.parend,self.l.parstep,self.l.fitnessFunction)

		assert self.l.parname == ["first", "secnd", "third"]
		self.l.parstart == [1,2,3]
		self.l.parend == [None] * 3
		self.l.parstep == [None] * 3
		assert self.l.fitnessFunction == 'pgg', self.l.lastLine

		# WITH RANGES
		createParameterRangesFile(multi=True)
		#self.l = Launcher('simulations', 'parameter_ranges.txt')
		self.l.readParameterInfo()

		assert self.l.parname == ["first", "secnd", "third"]
		self.l.parstart == [1.1,2.3,3.5]
		self.l.parend == [1.2,None,3.6]
		self.l.parstep == [0.1,None,0.1]
		assert self.l.fitnessFunction == 'pgg'

	def test_ranges_creation(self, createParameterRangesFile):
		createParameterRangesFile(multi=True)
		self.l = Launcher('simulations', 'parameter_ranges.txt')
		self.l.readParameterInfo()
		self.l.createRanges()

		assert len(self.l.ranges) == 3, "wrong number of ranges"
		assert self.l.ranges == [[1.1,1.2],[2.3],[3.5,3.6]], "wrong ranges"

	def test_combinations_creation(self):
		assert False, "write this test!"

	def test_script_reads_parameter_ranges_file_and_writes_files_correctly(self, createParameterRangesFile):
		createParameterRangesFile()
		self.l = Launcher('simulations', 'parameter_ranges.txt')
		self.l.writeParameterFilesInAllFolders()

		self.subfoldername = 'pgg_first1.0secnd2.0third3.0'

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
		self.l = Launcher('simulations', 'parameter_ranges.txt')
		self.l.writeParameterFilesInAllFolders()

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
		self.l = Launcher('simulations', 'parameter_ranges.txt')
		self.l.writeParameterFilesInAllFolders()

		files = folders = 0

		for _, dirnames, filenames in os.walk('simulations'):
		  # ^ this idiom means "we won't be using this value"
		    files += len(filenames)
		    folders += len(dirnames)

		shutil.rmtree('simulations')
		os.remove('parameter_ranges.txt')

		assert files == 5*4, "wrong total number of parameters files"
		assert folders == 4, "wrong number of subfolders"
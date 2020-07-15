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

		shutil.copytree('test/test', 'simulations')
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
		self.l.writeParameterFilesInFolder(fitfun="func", pname=["first","secnd","third"], pval=[1,2,3])

		self.dirpath = os.getcwd()
		self.fileslist = os.listdir('simulations/func_first1secnd2third3')
		self.inputfiles = [INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, INITIAL_TECHNOLOGY_FILE, PARAMETER_FILE, FITNESS_PARAMETERS_FILE]

		try:
			for file in self.inputfiles:
				assert file in self.fileslist
			shutil.rmtree('simulations')
		except AssertionError as e:
			shutil.rmtree('simulations')
			assert False, "one or more parameter file(s) missing. Folder contents: {0}".format(self.fileslist)

	def test_script_handles_files_already_exists_issue(self):
		shutil.copytree('test/test', 'simulations')
		self.l = Launcher('simulations', 'blablabla')
		self.l.writeParameterFilesInFolder(fitfun="func", pname=["first","secnd","third"], pval=[1,2,3])
		try:
			with open('simulations/func_first1secnd2third3/'+FITNESS_PARAMETERS_FILE, 'r') as f:
				assert len(f.readlines()) == 3, "file not replaced by correct parameter values"
			shutil.rmtree('simulations')
		except AssertionError as e:
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
		self.l.parstart == [1.1,2.3,3.4]
		self.l.parend == [1.3,None,3.6]
		self.l.parstep == [0.1,None,0.1]
		assert self.l.fitnessFunction == 'pgg'

		os.remove('parameter_ranges.txt')

	def test_ranges_creation(self, createParameterRangesFile):
		createParameterRangesFile(multi=True)
		self.l = Launcher('simulations', 'parameter_ranges.txt')
		self.l.readParameterInfo()
		assert self.l.parend == ['1.3',None,'3.6']
		assert self.l.parstep == ['0.1', None, '0.1']

		self.l.createRanges()

		assert self.l.parend == ['1.3',None,'3.6']
		assert self.l.parstep == ['0.1', None, '0.1']

		assert len(self.l.ranges) == 3, "wrong number of ranges"
		checkList = [[1.1,1.2],[2.3],[3.4,3.5]]
		for par in range(len(self.l.ranges)):
			assert pytest.approx(self.l.ranges[par]) == checkList[par], "wrong range for {0}: {1} when it should be {2}".format(self.l.parname[par],self.l.ranges[par],checkList[par])

		os.remove('parameter_ranges.txt')

	def test_combinations_creation(self, createParameterRangesFile):
		createParameterRangesFile(multi=True)
		self.l = Launcher('simulations', 'parameter_ranges.txt')
		self.l.readParameterInfo()
		self.l.createRanges()
		self.l.createCombinations()

		allCombs = [(1.1,2.3,3.4),(1.1,2.3,3.5),(1.2,2.3,3.4),(1.2,2.3,3.5)]
		for parcomb in allCombs:
			assert pytest.approx(parcomb) in self.l.combinations

		os.remove('parameter_ranges.txt')

	def test_single_par_combination_gets_a_full_folder(self):
		self.l = Launcher('simulations', 'parameter_ranges.txt')
		self.l.createFolder(self.l.metafolder)
		self.l.writeParameterFilesInFolder(fitfun='pgg', pname=('small','big'), pval=(0.3,0.5))

		self.subfoldername = 'pgg_small0.3big0.5'
		assert os.path.exists('simulations/'+self.subfoldername), "create subfolder"
		self.fileslist = os.listdir('simulations/'+self.subfoldername)
		self.inputfiles = [INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, INITIAL_TECHNOLOGY_FILE, PARAMETER_FILE, FITNESS_PARAMETERS_FILE]
		try:
			for file in self.inputfiles:
				assert file in self.fileslist
			pars = fman.extractColumnFromFile('simulations/'+self.subfoldername+'/'+FITNESS_PARAMETERS_FILE, 0, str)
			vals = fman.extractColumnFromFile('simulations/'+self.subfoldername+'/'+FITNESS_PARAMETERS_FILE, 1, float)
			assert pars == ['small','big'], "wrong parameter name"
			assert vals == [0.3,0.5], "wrong parameter value"
			shutil.rmtree('simulations')
		except AssertionError as e:
			shutil.rmtree('simulations')
			assert False, "one or more parameter value(s) missing. File contents: {0},{1}".format(pars,vals) 

	def test_script_reads_parameter_ranges_file_and_writes_files_correctly_in_different_folders(self, createParameterRangesFile):
		createParameterRangesFile(multi=True)
		self.l = Launcher('simulations', 'parameter_ranges.txt')
		self.l.writeParameterFilesInFolders()

		self.subfoldernames = ['pgg_first1.1secnd2.3third3.4','pgg_first1.1secnd2.3third3.5','pgg_first1.2secnd2.3third3.4','pgg_first1.2secnd2.3third3.5']
		self.parvalues = [[1.1,2.3,3.4],[1.1,2.3,3.5],[1.2,2.3,3.4],[1.2,2.3,3.5]]
		self.inputfiles = [INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, INITIAL_TECHNOLOGY_FILE, PARAMETER_FILE, FITNESS_PARAMETERS_FILE]

		for comb in range(len(self.parvalues)):
			folder = self.subfoldernames[comb]
			assert os.path.exists('simulations/'+folder), "did not create specific simulation file: {0}".format(os.listdir('simulations'))
			fileslist = os.listdir('simulations/'+folder)
			try:
				for file in self.inputfiles:
					assert file in fileslist
				pars = fman.extractColumnFromFile('simulations/'+folder+'/'+FITNESS_PARAMETERS_FILE, 0, str)
				vals = fman.extractColumnFromFile('simulations/'+folder+'/'+FITNESS_PARAMETERS_FILE, 1, float)
				assert pars == ['first','secnd','third'], "wrong parameter name"
				assert pytest.approx(vals) == self.parvalues[comb], "wrong parameter value"
			except AssertionError as e:
				shutil.rmtree('simulations')
				os.remove('parameter_ranges.txt')
				assert False, "one or more parameter value(s) missing. File contents: {0},{1}".format(pars,vals) 
		shutil.rmtree('simulations')
		os.remove('parameter_ranges.txt')

	def test_parameter_files_are_not_empty(self, createParameterRangesFile):
		createParameterRangesFile()
		self.l = Launcher('simulations', 'parameter_ranges.txt')
		self.l.writeParameterFilesInFolders()

		self.fileslist = os.listdir('simulations')
		try:
			for file in self.fileslist:
				assert os.path.getsize('simulations/'+file) != 0, "file is empty"
			shutil.rmtree('simulations')
			os.remove('parameter_ranges.txt')
		except AssertionError as e:
			shutil.rmtree('simulations')
			os.remove('parameter_ranges.txt')
			assert False, "file is empty"

	def test_script_can_take_parameter_ranges(self, createParameterRangesFile):
		createParameterRangesFile(multi=True)
		self.l = Launcher('simulations', 'parameter_ranges.txt')
		self.l.writeParameterFilesInFolders()

		files = folders = 0

		for _, dirnames, filenames in os.walk('simulations'):
		  # ^ this idiom means "we won't be using this value"
		    files += len(filenames)
		    folders += len(dirnames)

		shutil.rmtree('simulations')
		os.remove('parameter_ranges.txt')

		assert folders == 4, "wrong number of subfolders"
		assert files == 5*4, "wrong total number of parameters files"

	def test_script_can_launch_single_simulation(self):
		self.dir = 'simulations/pgg_test01'
		shutil.copytree('test/test', self.dir)
		self.l = Launcher('simulations', 'parameter_ranges.txt')
		sim = self.l.launchSimulation(path=self.dir)

		assert os.path.exists(self.dir)
		self.fileslist = os.listdir(self.dir)
		self.outputfiles = ['out_phenotypes.txt', 'out_demography.txt', 'out_technology.txt', 'out_resources.txt', 'out_consensus.txt']

		try:
			for file in self.outputfiles:
				assert file in self.fileslist, "file {0} missing from output".format(file)
			shutil.rmtree('simulations')
		except AssertionError as e:
			shutil.rmtree('simulations')
			assert False, "file {0} missing from output".format(file)

	def test_single_simulation_output_not_empty(self):
		self.dir = 'simulations/pgg_test02'
		shutil.copytree('test/test', self.dir)
		assert os.path.isdir(self.dir), "not a directory"
		self.l = Launcher('simulations', 'parameter_ranges.txt')
		sim = self.l.launchSimulation(path=self.dir)

		self.outputfiles = ['out_phenotypes.txt', 'out_demography.txt', 'out_technology.txt', 'out_resources.txt', 'out_consensus.txt']

		for file in self.outputfiles:
			with open(self.dir+'/'+file) as f:
				lines = f.readlines()
				assert len(lines) == 10, "printed {0} generations instead of 10".format(len(lines))
				try:
					floatlines = [float(x.split(',')[0]) for x in lines]
				except AssertionError as e:
					shutil.rmtree('simulations')
					assert False, "{0} are not numbers".format(lines)
		shutil.rmtree('simulations')

	def test_script_can_launch_all_simulations(self):
		self.dirs = ['pgg_test1','pgg_test2','pgg_test3']
		os.mkdir('simulations')
		for fold in self.dirs:
			shutil.copytree('test/test', 'simulations/'+fold)
			assert fold in os.listdir('simulations')
			assert os.path.isdir('simulations/'+fold), "not a directory"

		self.l = Launcher('simulations', 'parameter_ranges.txt')
		sim = self.l.launchSimulations(path='simulations')

		self.outputfiles = ['out_phenotypes.txt', 'out_demography.txt', 'out_technology.txt', 'out_resources.txt', 'out_consensus.txt']

		for fold in self.dirs:
			for file in self.outputfiles:
				try:
					assert file in os.listdir('simulations/'+fold), "file {0} missing from output in folder {1}".format(file,fold)
				except AssertionError as e:
					shutil.rmtree('simulations')
					assert False, "file {0} missing from output in folder {1}".format(file,fold)

		shutil.rmtree('simulations')

	def test_full_workflow(self):
		with open("parameter_ranges.txt", 'w') as f:
			f.writelines(['fun,pgg\n','fb,2\n','b,0.5,0.7,0.1\n','c,0.05,0.07,0.01\n','gamma,0.01\n'])
		self.l = Launcher('simulations', 'parameter_ranges.txt')
		sims = self.l.launch()

		self.dirs = os.listdir('simulations')
		self.infiles = [INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, INITIAL_TECHNOLOGY_FILE, PARAMETER_FILE, FITNESS_PARAMETERS_FILE]
		self.outfiles = ['out_phenotypes.txt', 'out_demography.txt', 'out_technology.txt', 'out_resources.txt', 'out_consensus.txt']
		self.allfiles = self.infiles + self.outfiles

		for fold in self.dirs:
			for file in self.allfiles:
				try:
					assert file in os.listdir('simulations/'+fold), "file {0} missing from folder {1}".format(file,fold)
				except AssertionError as e:
					shutil.rmtree('simulations')
					assert False, "file {0} missing from output in folder {1}".format(file,fold)
		shutil.rmtree('simulations')
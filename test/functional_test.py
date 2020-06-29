import pytest
import os
import glob
import institutionevolution.filemanip as fman
from institutionevolution.population import Population as Pop
from files import PARAMETER_FOLDER, INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, PARAMETER_FILE, OUTPUT_FOLDER, FITNESS_PARAMETERS_FILE

class TestSimpleRun(object):
	
	def test_initialisation_file_exists(self):
		# Claire wants to model the evolution of a structured population.
		# She provides the initial conditions for the run: number of demes, initial deme size, number of generations in a file called initialisation.txt
		self.dirpath = os.getcwd()
		self.fileslist = os.listdir('{0}/{1}/test'.format(self.dirpath, PARAMETER_FOLDER))
		assert INITIALISATION_FILE in self.fileslist, "Initialisation file not found in {0}".format(self.dirpath)
		
	def test_initialisation_parameters_listed(self):
		self.pathToFile = fman.getPathToFile(filename=INITIALISATION_FILE, dirname=PARAMETER_FOLDER+'/test')
		for par in ['numberOfDemes','initialDemeSize','numberOfGenerations']:
			fman.searchFile(self.pathToFile, par)
			
	def test_initialisation_values_provided(self):
		self.pathToFile = fman.getPathToFile(filename=INITIALISATION_FILE, dirname=PARAMETER_FOLDER+'/test')
		
		self.pars = fman.extractColumnFromFile(self.pathToFile, 1, int)
		for par in self.pars:
			assert type(par) is int, "Did you insert a non integer value for deme number, deme size or generation number?"
			assert par > 0, "Did you insert a negative value for deme number, deme size or generation number?"
				
	def test_parameter_file_exists(self):
		# Claire provides parameters needed by the program to run functions in a file called parameters.txt
		self.dirpath = os.getcwd()
		self.fileslist = os.listdir('{0}/{1}'.format(self.dirpath, PARAMETER_FOLDER+'/test'))
		assert PARAMETER_FILE in self.fileslist, "Parameter file not found in {0}".format(self.dirpath) 
		
	def test_initial_phenotypes_file_exists(self):
		self.dirpath = os.getcwd()
		self.fileslist = os.listdir('{0}/{1}'.format(self.dirpath, PARAMETER_FOLDER+'/test'))
		assert INITIAL_PHENOTYPES_FILE in self.fileslist, "Initial phenotypes file not found in {0}".format(self.dirpath) 
	
	def test_fitness_parameters_file_exists(self):
		self.dirpath = os.getcwd()
		self.fileslist = os.listdir('{0}/{1}'.format(self.dirpath, PARAMETER_FOLDER+'/test'))
		assert FITNESS_PARAMETERS_FILE in self.fileslist, "Fitness parameter file not found in {0}".format(self.dirpath) 
		
	def test_initial_phenotypes_format(self):
		self.pathToFile = fman.getPathToFile(filename=INITIAL_PHENOTYPES_FILE, dirname=PARAMETER_FOLDER+'/test')
		with open(self.pathToFile) as f:
			lines = [float(x) for x in f.readlines()]
			for line in lines: 
				assert type(line) is float 
				assert 0 <= line <= 1
				
	# Unfortunately, it would seem that she created a a well-mixed population, i.e. the population is not structured in demes / number of demes = 1. 
	# This program is not meant for well-mixed populations, and tells Claire so.
	def test_simulations_only_run_on_structured_populations(self):
		self.out = 'output_test.txt'
		self.population = Pop(inst='test')
		setattr(self.population, "numberOfDemes", 1)
		setattr(self.population, "numberOfGenerations", 4)
		try:
			self.population.runSimulation(self.out)
		except ValueError as e:
			assert str(e) == 'This program runs simulations on well-mixed populations only. "numberOfDemes" in initialisation.txt must be > 1', "Explain why the program fails!, not '{0}'".format(e)
		else:
			assert False, "You cannot let people run simulations on well-mixed populations (only {0} deme)!".format(self.population.numberOfDemes)
			os.remove('{0}/{1}'.format(OUTPUT_FOLDER, self.out))
			
	# She then changes the number of demes so that the population is structured into multiple demes.
	# Unfortunately, she asks the program to run a simulation with a 'gibberish' fitness function, which is not yet known by the program. The programs tells her to add the function in the fitness function dictionary
	
	def test_program_requires_valid_fitness_function(self):
		self.out = 'output_test.txt'
		self.population = Pop(fit_fun="gibberish", inst='test')
		setattr(self.population, "numberOfGenerations", 4)
		try:
			self.population.runSimulation(self.out)
		except KeyError as e:
			assert str(e).replace("'", "") == 'Fitness function "gibberish" unknown. Add it to the functions in fitness.py', "Explain why the program fails!, not '{0}'".format(e)
		else:
			assert False, "The program should return an error message when trying to run simulations with unknown fitness function".format(self.population.numberOfDemes)
			os.remove('{0}/{1}'.format(OUTPUT_FOLDER, self.out))
		
		# She runs the program:
	def test_population_is_initialised_with_right_values(self, objectAttributesExist, objectAttributesValues):
		# First, the population is initialised according to the initialisation settings
		self.pathToFile = fman.getPathToFile(filename=INITIALISATION_FILE, dirname=PARAMETER_FOLDER+'/test')
		self.attributeNames = fman.extractColumnFromFile(self.pathToFile, 0, str)
		self.attributeValues = fman.extractColumnFromFile(self.pathToFile, 1, int)
		self.population = Pop(inst='test')
		
		testAttr, whichAttr = objectAttributesExist(self.population, self.attributeNames)
		assert testAttr, "Population does not have attribute(s) {0}".format(whichAttr)
		testVal, attributes, expected, observed = objectAttributesValues(self.population, self.attributeNames, self.attributeValues)
		assert testVal, "Population has {1}={2} instead of {3}".format(attributes, expected, observed)
		
	def test_program_writes_output_for_x_generations(self, runSim):
		# Second, the population evolves over x generations following the iteration function
		# After the run, the results are saved in a folder called "res"
		self.out = 'output_test'
		self.outputFile = fman.getPathToFile(filename=self.out, dirname=OUTPUT_FOLDER+'/test')
		ngen = runSim(self.out,5)
		
		with open(self.outputFile + '_phenotypes.txt') as fp, open(self.outputFile + '_demography.txt') as fd:
			self.fplines = fp.readlines()
			self.fdlines = fd.readlines()
			
		#self.pathToFile = fman.getPathToFile(filename=INITIALISATION_FILE, dirname=PARAMETER_FOLDER)
		#self.attributeNames = fman.extractColumnFromFile(self.pathToFile, 0, str)
		#self.attributeValues = fman.extractColumnFromFile(self.pathToFile, 1, int) 
			
		assert len(self.fplines) == ngen, "wrong # of generations, {0}".format(self.fplines)
		assert len(self.fdlines) == ngen

		os.remove(self.outputFile + '_phenotypes.txt')
		os.remove(self.outputFile + '_demography.txt')

	def test_program_writes_non_empty_output(self, runSim):
		self.out = 'output_test'
		self.outputFile = fman.getPathToFile(filename=self.out, dirname=OUTPUT_FOLDER+'/test')
		runSim(self.out)

		with open(self.outputFile + '_phenotypes.txt') as fp, open(self.outputFile + '_demography.txt') as fd:
			self.resfp = [len(line.strip()) for line in fp.readlines()]
			self.resfd = [len(line.strip()) for line in fd.readlines()]
			
		assert sum(self.resfp) > 0
		assert sum(self.resfd) > 0

		os.remove(self.outputFile + '_phenotypes.txt')
		os.remove(self.outputFile + '_demography.txt')

	# She goes to the output folder and sees that two files have been written by the program, one with the mean phenotypes and the other with the mean deme size
	def test_program_writes_all_variable_files(self, runSim):
		self.out = 'output_test'
		self.outputFile = fman.getPathToFile(filename=self.out, dirname=OUTPUT_FOLDER+'/test')
		runSim(self.out)

		allOutput = glob.glob(self.outputFile + '*.txt')
		assert len(allOutput) == 4, f"did not find output files with pattern: {self.outputFile + '*.txt'} in {allOutput}"
		assert self.outputFile + '_phenotypes.txt' in allOutput, f"did not find phenotypes output file in {allOutput}"
		assert self.outputFile + '_demography.txt' in allOutput, f"did not find demography output file in {allOutput}"
		assert self.outputFile + '_technology.txt' in allOutput, f"did not find technology output file in {allOutput}"
		assert self.outputFile + '_resources.txt' in allOutput, f"did not find resources output file in {allOutput}"
		assert self.outputFile + '_consensustime.txt' in allOutput, f"did not find consensus time output file in {allOutput}"

		os.remove(self.outputFile + '_phenotypes.txt')
		os.remove(self.outputFile + '_demography.txt')
		os.remove(self.outputFile + '_technology.txt')
		os.remove(self.outputFile + '_resources.txt')
		os.remove(self.outputFile + '_consensustime.txt')

	def test_simulation_stops_with_information_message_when_population_extinct(self, runSim):
		self.out = 'output_test'
		self.outputFile = fman.getPathToFile(filename=self.out, dirname=OUTPUT_FOLDER+'/test')

		try:
			runSim(self.out,0)
		except TypeError as e:
			assert False, "The program should exit with information message when population goes extinct!"

		os.remove(self.outputFile + '_phenotypes.txt')
		os.remove(self.outputFile + '_demography.txt')
		os.remove(self.outputFile + '_pheno_var.txt')
		os.remove(self.outputFile + '_demo_var.txt')
		
		# Satisfied, she goes to sleep.
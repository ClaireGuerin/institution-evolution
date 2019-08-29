import pytest
import os
import filemanip as fman
from main import Population as Pop
from main import INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, PARAMETER_FILE, OUTPUT_FOLDER, OUTPUT_FILE

class TestSimpleRun(object):
	
	def assertObjectAttributesExist(self, obj, attrs):
		for attr in attrs:
			assert hasattr(obj, attr), "object {0} has no attribute {1}".format(obj, attr)	
			
	def assertObjectAttributeValues(self, obj, attrs, vals):
		for attr,val in zip(attrs, vals):
			assert getattr(obj, attr) == val, "{0} has {1}={2} instead of {3}".format(obj, attr, getattr(obj, attr), val)
	
	def test_initialisation_file_exists(self):
		# Claire wants to model the evolution of a structured population.
		# She provides the initial conditions for the run: number of demes, initial deme size, number of generations in a file called initialisation.txt
		self.dirpath = os.getcwd()
		self.fileslist = os.listdir(self.dirpath)
		assert INITIALISATION_FILE in self.fileslist, "Initialisation file not found in {0}".format(self.dirpath)
		
	def test_initialisation_parameters_listed(self):
		self.pathToFile = fman.getPathToFile(INITIALISATION_FILE)
		for par in ['numberOfDemes','initialDemeSize','numberOfGenerations']:
			fman.searchFile(self.pathToFile, par)
			
	def test_initialisation_values_provided(self):
		self.pathToFile = fman.getPathToFile(INITIALISATION_FILE)
		
		self.pars = fman.extractColumnFromFile(self.pathToFile, 1, int)
		for par in self.pars:
			assert type(par) is int, "Did you insert a non integer value for deme number, deme size or generation number?"
			assert par > 0, "Did you insert a negative value for deme number, deme size or generation number?"
				
	def test_parameter_file_exists(self):
		# Claire provides parameters needed by the program to run functions in a file called parameters.txt
		self.dirpath = os.getcwd()
		self.fileslist = os.listdir(self.dirpath)
		assert PARAMETER_FILE in self.fileslist, "Parameter file not found in {0}".format(self.dirpath) 
		
	def test_initial_phenotypes_file_exists(self):
		self.dirpath = os.getcwd()
		self.fileslist = os.listdir(self.dirpath)
		assert INITIAL_PHENOTYPES_FILE in self.fileslist, "Initial phenotypes file not found in {0}".format(self.dirpath) 
		
	def test_initial_phenotypes_format(self):
		self.pathToFile = fman.getPathToFile(INITIAL_PHENOTYPES_FILE)
		with open(self.pathToFile) as f:
			lines = [float(x) for x in f.readlines()]
			for line in lines: 
				assert type(line) is float 
				assert line >= 0 and line <= 1
		
		# She runs the program:
	def test_population_is_initialised_with_right_values(self):
		# First, the population is initialised according to the initialisation settings
		self.pathToFile = fman.getPathToFile(INITIALISATION_FILE)
		self.attributeNames = fman.extractColumnFromFile(self.pathToFile, 0, str)
		self.attributeValues = fman.extractColumnFromFile(self.pathToFile, 1, int)
		self.population = Pop()
		
		self.assertObjectAttributesExist(self.population, self.attributeNames)
		self.assertObjectAttributeValues(self.population, self.attributeNames, self.attributeValues)
		
	def test_program_writes_output_for_x_generations(self):
		# Second, the population evolves over x generations following the iteration function
		# After the run, the results are saved in a folder called "res"
		self.population = Pop()
		self.population.runSimulation()
		
		self.outputFile = fman.getPathToFile('{0}/{1}'.format(OUTPUT_FOLDER, OUTPUT_FILE))
		with open(self.outputFile) as f:
			self.lineNumber = len(f.readlines())
			
		self.pathToFile = fman.getPathToFile(INITIALISATION_FILE)
		self.attributeNames = fman.extractColumnFromFile(self.pathToFile, 0, str)
		self.attributeValues = fman.extractColumnFromFile(self.pathToFile, 1, int)
		self.nGen = self.attributeValues[self.attributeNames.index('numberOfGenerations')]
			
		assert self.lineNumber == self.nGen
		
	def test_program_write_non_empty_output(self):
		self.outputFile = fman.getPathToFile('{0}/{1}'.format(OUTPUT_FOLDER, OUTPUT_FILE))
		with open(self.outputFile) as f:
			self.res = [len(line.strip()) for line in f.readlines()]
			
		assert sum(self.res) > 0
		
		# Satisfied, she goes to sleep.
import pytest
import os
from main import Population as pop

INITIALISATION_FILE = 'initialisation.txt'
PARAMETER_FILE = 'parameters.txt'

class TestSimpleRun(object):
	
	def searchFile(self, fileToRead, string):
		with open(fileToRead) as f:
			if string in f.read():
				assert True
			else:
				assert False, "{0} not provided in {1}".format(string, fileToRead)
				
	def checkObjectAttribute(self, obj, attrs):
		for attr in attrs:
			assert hasattr(obj, attr), "object {0} has no attribute {1}".format(obj, attr)		
			
	def extractParameters(self, fileToRead, col):
		with open(self.pathToFile) as f:
			return [int(line.split(',')[col]) for line in f.readlines()]
	
	def test_initialisation_file_exists(self):
		# Claire wants to model the evolution of a structured population.
		# She provides the initial conditions for the run: number of demes, initial deme size, number of generations in a file called initialisation.txt
		self.dirpath = os.getcwd()
		self.fileslist = os.listdir(self.dirpath)
		assert INITIALISATION_FILE in self.fileslist, "Initialisation file not found in {0}".format(self.dirpath)
		
	def test_initialisation_parameters_listed(self):
		self.dirpath = os.getcwd()
		self.pathToFile = "{0}/{1}".format(self.dirpath, INITIALISATION_FILE)
		for par in ['numberOfDemes','initialDemeSize','numberOfGenerations']:
			self.searchFile(self.pathToFile, par)
			
	def test_initialisation_values_provided(self):
		self.dirpath = os.getcwd()
		self.pathToFile = "{0}/{1}".format(self.dirpath, INITIALISATION_FILE)
		
		self.pars = self.extractParameters(pathToFile, 1)
		for par in self.pars:
			assert type(par) is int
			assert par > 0	
				
	def test_parameter_file_exists(self):
		# Claire provides parameters needed by the program to run functions in a file called parameters.txt
		self.dirpath = os.getcwd()
		self.fileslist = os.listdir(self.dirpath)
		assert PARAMETER_FILE in self.fileslist, "Initialisation file not found in {0}".format(self.dirpath) 
		
		# She runs the program:
	def test_population_is_initialised_with_right_values(self):
		# First, the population is initialised according to the initialisation settings
		self.runpop = pop()
		self.checkObjectAttribute(self.runpop, ['numberOfDemes','initialDemeSize','numberOfGenerations'])
		
	def test_program_runs_x_generations(self):
		# Second, the population evolves over x generations following the iteration function
		
		# After the run, the results are saved in a folder called "res"
		# Satisfied, she goes to sleep.

		assert False, "Finish the functional test!"
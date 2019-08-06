import pytest
import os
import filemanip as fman
from main import Population as pop

INITIALISATION_FILE = 'initialisation.txt'
PARAMETER_FILE = 'parameters.txt'

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
		self.pathToFile = fman.getPathToFile(INITIALISATION_FILE)
		self.attributeNames = fman.extractColumnFromFile(self.pathToFile, 0, str)
		self.attributeValues = fman.extractColumnFromFile(self.pathToFile, 1, int)
		self.runpop = pop()
		
		self.assertObjectAttributesExist(self.runpop, self.attributeNames)
		self.assertObjectAttributeValues(self.runpop, self.attributeNames, self.attributeValues)
		
	def test_program_runs_x_generations(self):
		# Second, the population evolves over x generations following the iteration function
		
		# After the run, the results are saved in a folder called "res"
		# Satisfied, she goes to sleep.

		assert False, "Finish the functional test!"
import pytest
import os

class TestSimpleRun(object):
	
	def test_initialisation_file_exists(self):
		# Claire wants to model the evolution of a structured population.
		# She provides the initial conditions for the run: number of demes, initial deme size, number of generations in a file called initialisation.txt
		dirpath = os.getcwd()
		fileslist = os.listdir(dirpath)
		assert 'initialisation.txt' in fileslist, "Initialisation file not found in {0}".format(dirpath)

		# She provides parameters needed by the program to run functions in a file called parameters.txt
		# She runs the program
		# After the run, the results are saved in a folder called "res"
		# Satisfied, she goes to sleep.

		assert False, "Finish the functional test!"
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
		self.fileslist = os.listdir('test/test')
		assert INITIALISATION_FILE in self.fileslist, "Initialisation file not found in test/test"
		
	def test_initialisation_parameters_listed(self):
		self.pathToFile = fman.getPathToFile(filename=INITIALISATION_FILE, dirname='test/test')
		for par in ['numberOfDemes','initialDemeSize','numberOfGenerations']:
			fman.searchFile(self.pathToFile, par)
			
	def test_initialisation_values_provided(self):
		self.pathToFile = fman.getPathToFile(filename=INITIALISATION_FILE, dirname='test/test')
		
		self.pars = fman.extractColumnFromFile(self.pathToFile, 1, int)
		for par in self.pars:
			assert type(par) is int, "Did you insert a non integer value for deme number, deme size or generation number?"
			assert par > 0, "Did you insert a negative value for deme number, deme size or generation number?"
				
	def test_parameter_file_exists(self):
		# Claire provides parameters needed by the program to run functions in a file called parameters.txt
		self.dirpath = os.getcwd()
		self.fileslist = os.listdir('{0}/{1}'.format(self.dirpath, 'test/test'))
		assert PARAMETER_FILE in self.fileslist, "Parameter file not found in {0}".format(self.dirpath) 
		
	def test_initial_phenotypes_file_exists(self):
		self.dirpath = os.getcwd()
		self.fileslist = os.listdir('{0}/{1}'.format(self.dirpath, 'test/test'))
		assert INITIAL_PHENOTYPES_FILE in self.fileslist, "Initial phenotypes file not found in {0}".format(self.dirpath) 
	
	def test_fitness_parameters_file_exists(self):
		self.dirpath = os.getcwd()
		self.fileslist = os.listdir('{0}/{1}'.format(self.dirpath, 'test/test'))
		assert FITNESS_PARAMETERS_FILE in self.fileslist, "Fitness parameter file not found in {0}".format(self.dirpath) 
		
	def test_initial_phenotypes_format(self):
		self.pathToFile = fman.getPathToFile(filename=INITIAL_PHENOTYPES_FILE, dirname='test/test')
		with open(self.pathToFile) as f:
			lines = [float(x) for x in f.readlines()]
			for line in lines: 
				assert type(line) is float 
				assert 0 <= line <= 1
				
	# Unfortunately, it would seem that she created a a well-mixed population, i.e. the population is not structured in demes / number of demes = 1. 
	# This program is not meant for well-mixed populations, and tells Claire so.
	def test_simulations_only_run_on_structured_populations(self, clearOutputFiles):
		self.population = Pop(inst='test/test')
		setattr(self.population, "numberOfDemes", 1)
		setattr(self.population, "numberOfGenerations", 4)
		try:
			self.population.runSimulation()
		except ValueError as e:
			assert str(e) == 'This program runs simulations on well-mixed populations only. "numberOfDemes" in initialisation.txt must be > 1', "Explain why the program fails!, not '{0}'".format(e)
		else:
			assert False, "You cannot let people run simulations on well-mixed populations (only {0} deme)!".format(self.population.numberOfDemes)
			clearOutputFiles('test/test/')
			
	# She then changes the number of demes so that the population is structured into multiple demes.
	# Unfortunately, she asks the program to run a simulation with a 'gibberish' fitness function, which is not yet known by the program. The programs tells her to add the function in the fitness function dictionary
	
	def test_program_requires_valid_fitness_function(self, clearOutputFiles):
		self.population = Pop(fit_fun="gibberish", inst='test/test')
		setattr(self.population, "numberOfGenerations", 4)
		try:
			self.population.runSimulation()
		except KeyError as e:
			assert str(e).replace("'", "") == 'Fitness function "gibberish" unknown. Add it to the functions in fitness.py', "Explain why the program fails!, not '{0}'".format(e)
		else:
			assert False, "The program should return an error message when trying to run simulations with unknown fitness function".format(self.population.numberOfDemes)
			clearOutputFiles('test/test/')
		
		# She runs the program:
	def test_population_is_initialised_with_right_values(self, objectAttributesExist, objectAttributesValues):
		# First, the population is initialised according to the initialisation settings
		self.pathToFile = fman.getPathToFile(filename=INITIALISATION_FILE, dirname='test/test')
		self.attributeNames = fman.extractColumnFromFile(self.pathToFile, 0, str)
		self.attributeValues = fman.extractColumnFromFile(self.pathToFile, 1, int)
		self.population = Pop(inst='test/test')
		
		testAttr, whichAttr = objectAttributesExist(self.population, self.attributeNames)
		assert testAttr, "Population does not have attribute(s) {0}".format(whichAttr)
		testVal, attributes, expected, observed = objectAttributesValues(self.population, self.attributeNames, self.attributeValues)
		assert testVal, "Population has {1}={2} instead of {3}".format(attributes, expected, observed)
		
	def test_program_writes_output_for_x_generations(self, runSim, clearOutputFiles):
		# Second, the population evolves over x generations following the iteration function
		# After the run, the results are saved in a folder called "res"
		ngen = runSim(5)
		
		with open('test/test/out_phenotypes.txt') as fp, open('test/test/out_demography.txt') as fd:
			self.fplines = fp.readlines()
			self.fdlines = fd.readlines()
			
		#self.pathToFile = fman.getPathToFile(filename=INITIALISATION_FILE, dirname=PARAMETER_FOLDER)
		#self.attributeNames = fman.extractColumnFromFile(self.pathToFile, 0, str)
		#self.attributeValues = fman.extractColumnFromFile(self.pathToFile, 1, int) 
			
		assert len(self.fplines) == ngen, "wrong # of generations, {0}".format(self.fplines)
		assert len(self.fdlines) == ngen

		clearOutputFiles('test/test/')

	def test_program_writes_non_empty_output(self, runSim, clearOutputFiles):
		runSim()

		with open('test/test/out_phenotypes.txt') as fp, open('test/test/out_demography.txt') as fd:
			self.resfp = [len(line.strip()) for line in fp.readlines()]
			self.resfd = [len(line.strip()) for line in fd.readlines()]
			
		assert sum(self.resfp) > 0
		assert sum(self.resfd) > 0

		clearOutputFiles('test/test/')

	# She goes to the output folder and sees that two files have been written by the program, one with the mean phenotypes and the other with the mean deme size
	def test_program_writes_all_variable_files(self, runSim, clearOutputFiles):
		runSim()

		allOutput = glob.glob('test/test/out_*.txt')
		assert len(allOutput) == 5, f"did not find all output files with pattern: {'out_*.txt'} in {allOutput}"
		assert 'test/test/out_phenotypes.txt' in allOutput, f"did not find phenotypes output file in {allOutput}"
		assert 'test/test/out_demography.txt' in allOutput, f"did not find demography output file in {allOutput}"
		assert 'test/test/out_technology.txt' in allOutput, f"did not find technology output file in {allOutput}"
		assert 'test/test/out_resources.txt' in allOutput, f"did not find resources output file in {allOutput}"
		assert 'test/test/out_consensus.txt' in allOutput, f"did not find consensus time output file in {allOutput}"

		clearOutputFiles('test/test/')

	# she opens the phenotypes file, and check that the number of phenotypes is right and that the value seem correct.
	def test_phenotype_file_has_correct_output(self, runSim, clearOutputFiles): 
		runSim(mutRate=0)

		with open('test/test/initial_phenotypes.txt', 'r') as initphen:
			phens = [float(x) for x in initphen.readlines()]
			nphens = len(phens)

		with open('test/test/out_phenotypes.txt') as outphenfile:
			for line in outphenfile:
				getphens = [float(x) for x in line.split(',')][0:nphens]
				assert len(getphens) == nphens, "wrong number of phenotypes printed in line: {0}".format(line)
				assert getphens == phens, "this line is not identical to initial phenotypes even though mutaiton rate is null"

		clearOutputFiles('test/test/')

	#she then moves on to verify every single output file: first, demography...
	def test_demography_file_has_correct_output(self, pseudorandom, runSim, clearOutputFiles):
		pseudorandom(69) 
		self.pop = Pop(inst='test/test')
		self.pop.mutationRate = 0.1
		self.pop.numberOfDemes = 5
		self.pop.initialDemeSize = 8
		self.pop.fitnessParameters.clear()
		self.pop.fitnessParameters.update({"fb": 10, "b": 0.5, "c": 0.05, "gamma": 0.01})
		self.pop.createAndPopulateDemes()
		expDemog = []
		for gen in range(5):
			self.pop.lifecycle()
			assert self.pop.numberOfDemes == 5
			expDemog.append(self.pop.demography / self.pop.numberOfDemes)

		pseudorandom(69)
		runSim()
		obsDemog = fman.extractColumnFromFile('test/test/out_demography.txt', 0, float)

		assert obsDemog == expDemog, "unexpected value of group size has been printed"

		clearOutputFiles('test/test/')

	# next, technology...
	def test_technology_file_has_correct_output(self, pseudorandom, runSim, clearOutputFiles):
		parameters = {"gamma": 0.01, "p": 0.6, "q":0.9, "d":0.2, "productionTime": 1, "alphaResources": 0.6, "rb": 10, "atech": 2, "btech":0.2, "betaTech": 0.6}
		pseudorandom(85) 
		self.pop = Pop(fit_fun='technology', inst='test/test')
		self.pop.mutationRate = 0.1
		self.pop.numberOfDemes = 5
		self.pop.initialDemeSize = 8
		self.pop.fitnessParameters.clear()
		self.pop.fitnessParameters.update(parameters)
		self.pop.createAndPopulateDemes()
		expTechno = []
		for gen in range(5):
			self.pop.lifecycle()
			assert self.pop.numberOfDemes == 5
			collectDemeTech = []
			for deme in self.pop.demes:
				collectDemeTech.append(deme.technologyLevel)
			expTechno.append(sum(collectDemeTech)/len(collectDemeTech))

		pseudorandom(85)
		runSim(fun='technology', pars=parameters)
		obsTechno = fman.extractColumnFromFile('test/test/out_technology.txt', 0, float)

		assert obsTechno == expTechno, "unexpected value of technology level has been printed"

		clearOutputFiles('test/test/')

	# then, resources...
	def test_resources_file_has_correct_output(self, pseudorandom, runSim, clearOutputFiles):
		parameters = {"gamma": 0.01, "p": 0.6, "q":0.9, "d":0.2, "productionTime": 1, "alphaResources": 0.6, "rb": 10, "atech": 2, "btech":0.2, "betaTech": 0.6}
		pseudorandom(54) 
		self.pop = Pop(fit_fun='technology', inst='test/test')
		self.pop.mutationRate = 0.1
		self.pop.numberOfDemes = 5
		self.pop.initialDemeSize = 8
		self.pop.fitnessParameters.clear()
		self.pop.fitnessParameters.update(parameters)
		self.pop.createAndPopulateDemes()
		expTotRes = []
		for gen in range(5):
			self.pop.lifecycle()
			assert self.pop.numberOfDemes == 5
			collectDemeTotRes = []
			for deme in self.pop.demes:
				collectDemeTotRes.append(deme.totalResources)
			expTotRes.append(sum(collectDemeTotRes)/len(collectDemeTotRes))

		pseudorandom(54)
		runSim(fun='technology', pars=parameters)
		obsTotRes = fman.extractColumnFromFile('test/test/out_resources.txt', 0, float)

		assert obsTotRes == expTotRes, "unexpected value of total resources has been printed"

		clearOutputFiles('test/test/')

	# finally, consensus...
	def test_consensus_file_has_correct_output(self, pseudorandom, runSim, clearOutputFiles):
		parameters = {"gamma": 0.01, "aconsensus":3, "bconsensus":2, "epsilon":0.01, "aquality":4, "alphaquality":0.9, "alphaResources":0.8, "techcapital":50, "rb":10}
		pseudorandom(22) 
		self.pop = Pop(fit_fun='debate', inst='test/test')
		self.pop.mutationRate = 0.1
		self.pop.numberOfDemes = 5
		self.pop.initialDemeSize = 8
		self.pop.fitnessParameters.clear()
		self.pop.fitnessParameters.update(parameters)
		self.pop.createAndPopulateDemes()
		expCons = []
		for gen in range(5):
			self.pop.lifecycle()
			assert self.pop.numberOfDemes == 5
			collectDemeCons = []
			for deme in self.pop.demes:
				collectDemeCons.append(deme.politicsValues["consensusTime"])
			expCons.append(sum(collectDemeCons)/len(collectDemeCons))

		pseudorandom(22)
		runSim(fun='debate', pars=parameters)
		obsCons = fman.extractColumnFromFile('test/test/out_consensus.txt', 0, float)

		assert obsCons == expCons, "unexpected value of total resources has been printed"

		clearOutputFiles('test/test/')

	# she tries a new set of parameters for which the population size goes to zero. The prgoram exits with a warning
	def test_simulation_stops_with_information_message_when_population_extinct(self, runSim, clearOutputFiles):
		try:
			runSim(fb=0)
		except TypeError as e:
			assert False, "The program should exit with information message when population goes extinct!"

		clearOutputFiles('test/test/')
		
	# Satisfied, she goes to sleep.
import os
import logging
import institutionevolution.filemanip as fman
from institutionevolution.deme import Deme as Dem
from institutionevolution.individual import Individual as Ind
import institutionevolution.fitness as fitness
from statistics import variance
from files import PARAMETER_FOLDER, INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, PARAMETER_FILE, OUTPUT_FOLDER, FITNESS_PARAMETERS_FILE
import random

class Population(object):
	
	def __init__(self, fit_fun='pgg'):

		logging.basicConfig(level=logging.INFO,
							format='[%(asctime)s]::%(levelname)s  %(message)s',
							datefmt='%Y.%m.%d - %H:%M:%S')

		logging.info('Creating population')
		
		self.pathToInitFile = fman.getPathToFile(filename=INITIALISATION_FILE, dirname=PARAMETER_FOLDER)		
		self.attrs = fman.extractColumnFromFile(self.pathToInitFile, 0, str)
		self.vals = fman.extractColumnFromFile(self.pathToInitFile, 1, int)
		
		for attr,val in zip(self.attrs, self.vals):
			setattr(self, attr, val)
			
		self.pathToPhenFile = fman.getPathToFile(filename=INITIAL_PHENOTYPES_FILE, dirname=PARAMETER_FOLDER)
		with open(self.pathToPhenFile) as f:
			self.initialPhenotypes = [float(line) for line in f.readlines()]
			
		self.pathToParFile = fman.getPathToFile(filename=PARAMETER_FILE, dirname=PARAMETER_FOLDER)		
		self.parattrs = fman.extractColumnFromFile(self.pathToParFile, 0, str)
		self.parvals = fman.extractColumnFromFile(self.pathToParFile, 1, float)
		
		for parattr,parval in zip(self.parattrs, self.parvals):
			setattr(self, parattr, parval)
			
		self.pathToFitFile = fman.getPathToFile(filename=FITNESS_PARAMETERS_FILE, dirname=PARAMETER_FOLDER)		
		self.fitattrs = fman.extractColumnFromFile(self.pathToFitFile, 0, str)
		self.fitvals = fman.extractColumnFromFile(self.pathToFitFile, 1, float)
		
		self.fitnessParameters = {}
		for fitattr,fitval in zip(self.fitattrs, self.fitvals):
			self.fitnessParameters[fitattr] = fitval
			
		if hasattr(self, "individualResources") == False:
			setattr(self, "individualResources", 1)
			
		self.fit_fun = fit_fun

		self.numberOfPhenotypes = len(self.initialPhenotypes)
			
	def createAndPopulateDemes(self, nDemes = None, dSize = None):
		if nDemes == None:
			nDemes = self.numberOfDemes
		if dSize == None:
			dSize = self.initialDemeSize
		
		self.demography = nDemes * dSize
			
		self.demes = []
		self.individuals = []
		
		for deme in range(nDemes):
			newDemeInstance = Dem()
			newDemeInstance.id = deme
			
			newDemeInstance.neighbours = self.identifyNeighbours(nDemes, deme)
			newDemeInstance.demography = dSize
			newDemeInstance.meanPhenotypes = self.initialPhenotypes
			newDemeInstance.totalPhenotypes = [x * dSize for x in self.initialPhenotypes]
						
			for ind in range(dSize):
				indiv = Ind()
				setattr(indiv, "phenotypicValues", self.initialPhenotypes)
				setattr(indiv, "currentDeme", deme)
				setattr(indiv, "neighbours", newDemeInstance.neighbours)
				setattr(indiv, "resourcesAmount", self.individualResources)
				self.individuals.append(indiv)
			
			self.demes.append(newDemeInstance)

	def publicGood(self):
		for individual in self.individuals:
			self.demes[individual.currentDeme].publicGood += individual.phenotypicValues[0] * individual.resourcesAmount

			
	def identifyNeighbours(self, nd, demeID):
		tmp = list(range(nd))
		del tmp[demeID]
		return tmp
			
	def specialmean(self, lst):
		length, total = 0, 0
		for phenotype in lst:
			total += phenotype
			length += 1
		if length == 0:
			tmpmean = None
		else:
			tmpmean = total / length
		return tmpmean

	def specialdivision(self, x, y):
		if y == 0:
			tmp = None
		else:
			tmp = x / y
		return tmp

	# def specialvariance(self, lst, samplelength, samplemean):
	# 	if samplelength == 0:
	# 		tmpvar = None
	# 	else:
	# 		total = 0
	# 		for phenotype in lst:
	# 			total += (phenotype - samplemean) ** 2
	# 		tmpvar = total / samplelength


	def populationReproduction(self, seed=None, **kwargs):
		random.seed(seed)
		self.offspring = []
		testdemog = 0

		for ind in self.individuals:
			# REPRODUCTION
			kwargs["n"] = self.demes[ind.currentDeme].demography
			kwargs["xmean"] = self.demes[ind.currentDeme].meanPhenotypes
			kwargs["x"] = ind.phenotypicValues

			assert type(kwargs["n"]) is int, "group size of deme {0} is {1}".format(ind.currentDeme, kwargs["n"])
			assert kwargs["n"] > 0, "group size of deme {0} is {1}".format(ind.currentDeme, kwargs["n"])
			assert type(kwargs["x"][0]) is float, "phenotype of individual in deme {0} is {1}".format(ind.currentDeme, kwargs["x"])
			assert type(kwargs["xmean"][0]) is float, "mean phenotype in deme {0} of individual with phen {3} is {1}. N={2}, n={4}, totalx={5}. Special division returns {6}".format(ind.currentDeme, kwargs["xmean"], self.demography, ind.phenotypicValues, self.demes[ind.currentDeme].demography, self.demes[ind.currentDeme].totalPhenotypes, self.specialdivision(self.demes[ind.currentDeme].totalPhenotypes[0], self.demes[ind.currentDeme].demography))

			ind.reproduce(self.fit_fun, **kwargs)
			self.offspring += ind.offspring
			testdemog += ind.offspringNumber

		assert len(self.offspring) == testdemog
		self.individuals = self.offspring
		assert len(self.individuals) == testdemog
		self.demography = len(self.offspring)

	def clearDemePhenotypeAndSizeInfo(self):
		for deme in range(self.numberOfDemes):
			self.demes[deme].totalPhenotypes = [0] * self.numberOfPhenotypes
			self.demes[deme].demography = 0

	def populationMutationMigration(self):

		for ind in self.individuals:
			# MUTATION
			ind.mutate(self.mutationRate, self.mutationStep)
			
			# MIGRATION
			ind.migrate(nDemes=self.numberOfDemes, migRate=self.migrationRate)

			# UPDATE
			assert ind.currentDeme == ind.destinationDeme
			ind.neighbours = self.demes[ind.currentDeme].neighbours
			self.demes[ind.currentDeme].demography += 1
			for phen in range(self.numberOfPhenotypes):
				self.demes[ind.currentDeme].totalPhenotypes[phen] += ind.phenotypicValues[phen]

	def update(self):
		for deme in self.demes:
			meanphen = []
			for phen in range(self.numberOfPhenotypes):
				calculateMean = self.specialdivision(deme.totalPhenotypes[phen], deme.demography)
				meanphen.append(calculateMean) 

			setattr(deme, "meanPhenotypes", meanphen)

	def lifecycle(self, **kwargs):
		logging.info("migration and mutation")
		self.clearDemePhenotypeAndSizeInfo()
		self.populationMutationMigration()
		logging.info("updating...")
		self.update()
		logging.info("reproduction")
		self.populationReproduction(**kwargs)
		
	def runSimulation(self, outputfile):
		kwargs = self.fitnessParameters
		
		if self.numberOfDemes >= 2 and self.fit_fun in fitness.functions:
			self.createAndPopulateDemes()
		
			self.pathToOutputFolder = fman.getPathToFile(OUTPUT_FOLDER)
			if not os.path.exists(self.pathToOutputFolder):
				os.makedirs(self.pathToOutputFolder)
			
			with open('{0}/{1}'.format(self.pathToOutputFolder, outputfile), "w") as f:
				for gen in range(self.numberOfGenerations):
					logging.info(f'Running generation {gen}')
					self.lifecycle(**kwargs)

					phenmeans = []

					for phen in range(self.numberOfPhenotypes):
						tmpPhenotypes = [ind.phenotypicValues[phen] for ind in self.individuals]
						tmpMean = self.specialmean(tmpPhenotypes)
						# tmpVariance = self.specialvariance(tmpPhenotypes, len(tmpPhenotypes), tmpMean)
						phenmeans.append(str(tmpMean))

					sep = ','
					f.write('{0}\n'.format(sep.join(phenmeans)))
					
		elif self.numberOfDemes < 2 and self.fit_fun in fitness.functions:
			raise ValueError('This program runs simulations on well-mixed populations only. "numberOfDemes" in initialisation.txt must be > 1')
			
		elif self.numberOfDemes >= 2 and self.fit_fun not in fitness.functions:
			raise KeyError(str('Fitness function "{0}" unknown. Add it to the functions in fitness.py').format(self.fit_fun))
			
		else:
			raise ValueError('This program runs simulations on well-mixed populations only. "numberOfDemes" in initialisation.txt must be > 1')
			raise KeyError('Fitness function "{0}" unknown. Add it to the functions in fitness.py'.format(self.fit_fun))
			
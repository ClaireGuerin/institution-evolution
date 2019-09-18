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

		for ind in self.individuals:
			# REPRODUCTION
			kwargs["n"] = self.demes[ind.currentDeme].demography
			kwargs["xmean"] = self.demes[ind.currentDeme].meanPhenotypes
			kwargs["x"] = ind.phenotypicValues
			ind.reproduce(self.fit_fun, **kwargs)
			self.offspring += ind.offspring

		self.individuals = self.offspring
		self.demography = len(self.offspring)

	def clearDemePhenotypeAndSizeInfo(self):
		for deme in range(self.numberOfDemes):
			self.demes[deme].totalPhenotypes = [0] * self.numberOfPhenotypes
			self.demes[deme].demography = 0

	def populationMutationMigration(self):
		updateDemeSizes = [0] * self.numberOfDemes
		#updateDemePhenotypes = [[[]] * self.numberOfPhenotypes] * self.numberOfDemes

		for ind in self.individuals:
			# MUTATION
			ind.mutate(self.mutationRate, self.mutationStep)
			
			# MIGRATION
			ind.migrate(nDemes=self.numberOfDemes, migRate=self.migrationRate)

			# UPDATE
			ind.neighbours = self.demes[ind.currentDeme].neighbours
			self.demes[ind.currentDeme].demography += 1
			for phen in range(self.numberOfPhenotypes):
				self.demes[ind.currentDeme].totalPhenotypes[phen] += ind.phenotypicValues[phen]

	def update(self):
		for deme in range(self.numberOfDemes):
			for phen in range(self.numberOfPhenotypes):
				self.demes[deme].meanPhenotypes[phen] = self.specialdivision(self.demes[deme].totalPhenotypes[phen], self.demes[deme].demography)

	def lifecycle(self, **kwargs, seed):
		logging.info("migration and mutation")
		self.clearDemePhenotypeAndSizeInfo()
		self.populationMutationMigration()
		logging.info("updating...")
		self.update()
		logging.info("reproduction")
		self.populationReproduction(seed, **kwargs)
		
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

					for phen in range(self.numberOfPhenotypes):
						tmpPhenotypes = [ind.phenotypicValues[phen] for ind in self.individuals]
						tmpMean = self.specialmean(tmpPhenotypes)
						# tmpVariance = self.specialvariance(tmpPhenotypes, len(tmpPhenotypes), tmpMean)
						f.write('{0},'.format(tmpMean))
					f.write('\n'.rstrip(','))
					
		elif self.numberOfDemes < 2 and self.fit_fun in fitness.functions:
			raise ValueError('This program runs simulations on well-mixed populations only. "numberOfDemes" in initialisation.txt must be > 1')
			
		elif self.numberOfDemes >= 2 and self.fit_fun not in fitness.functions:
			raise KeyError(str('Fitness function "{0}" unknown. Add it to the functions in fitness.py').format(self.fit_fun))
			
		else:
			raise ValueError('This program runs simulations on well-mixed populations only. "numberOfDemes" in initialisation.txt must be > 1')
			raise KeyError('Fitness function "{0}" unknown. Add it to the functions in fitness.py'.format(self.fit_fun))
			
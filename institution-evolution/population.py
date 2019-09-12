import os
import logging
import filemanip as fman
from deme import Deme as Dem
from individual import Individual as Ind
import fitness
from statistics import variance
from files import INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, PARAMETER_FILE, OUTPUT_FOLDER, OUTPUT_FILE, FITNESS_PARAMETERS_FILE

class Population:
	
	def __init__(self, fit_fun='pgg'):

		logging.basicConfig(level=logging.INFO,
							format='[%(asctime)s]::%(levelname)s  %(message)s',
							datefmt='%Y.%m.%d - %H:%M:%S')

		logging.info('Creating population')
		
		self.pathToInitFile = fman.getPathToFile(INITIALISATION_FILE)		
		self.attrs = fman.extractColumnFromFile(self.pathToInitFile, 0, str)
		self.vals = fman.extractColumnFromFile(self.pathToInitFile, 1, int)
		
		for attr,val in zip(self.attrs, self.vals):
			setattr(self, attr, val)
			
		self.pathToPhenFile = fman.getPathToFile(INITIAL_PHENOTYPES_FILE)
		with open(self.pathToPhenFile) as f:
			self.initialPhenotypes = [float(line) for line in f.readlines()]
			
		self.pathToParFile = fman.getPathToFile(PARAMETER_FILE)		
		self.parattrs = fman.extractColumnFromFile(self.pathToParFile, 0, str)
		self.parvals = fman.extractColumnFromFile(self.pathToParFile, 1, float)
		
		for parattr,parval in zip(self.parattrs, self.parvals):
			setattr(self, parattr, parval)
			
		self.pathToFitFile = fman.getPathToFile(FITNESS_PARAMETERS_FILE)		
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

	# def specialvariance(self, lst, samplelength, samplemean):
	# 	if samplelength == 0:
	# 		tmpvar = None
	# 	else:
	# 		total = 0
	# 		for phenotype in lst:
	# 			total += (phenotype - samplemean) ** 2
	# 		tmpvar = total / samplelength


	def populationReproduction(self, **kwargs):
		offspring = []

		for ind in self.individuals:
			# REPRODUCTION
			kwargs["n"] = self.demes[ind.currentDeme].demography
			kwargs["xmean"] = self.demes[ind.currentDeme].meanPhenotypes
			kwargs["x"] = ind.phenotypicValues
			ind.reproduce(self.fit_fun, **kwargs)
			offspring += ind.offspring

		return offspring

	def populationMigrationMutation(self):
		updateDemeSizes = [0] * self.numberOfDemes
		updateDemePhenotypes = [[[]] * self.numberOfPhenotypes] * self.numberOfDemes

		for ind in self.individuals:
			# MIGRATION
			ind.migrate(nDemes=self.numberOfDemes, migRate=self.migrationRate)
			ind.neighbours = self.demes[ind.currentDeme].neighbours
			updateDemeSizes[ind.currentDeme] += 1

			# MUTATION
			ind.mutate(self.mutationRate, self.mutationStep)
			for phen in range(self.numberOfPhenotypes):
				updateDemePhenotypes[ind.currentDeme][phen].append(ind.phenotypicValues[phen])

		return (updateDemeSizes, updateDemePhenotypes)

	def update(self, upSizes, upPhenotypes):
		for deme in range(self.numberOfDemes):
			self.demes[deme].demography = upSizes[deme]
			# self.demes[deme].meanPhenotypes = [self.specialmean(upPhenotypes[deme][phen]) for phen in range(self.numberOfPhenotypes)]
			for phen in range(self.numberOfPhenotypes):
				self.demes[deme].meanPhenotypes[phen] = self.specialmean(upPhenotypes[deme][phen])

	def lifecycle(self, **kwargs):
		logging.info("migration and mutation")
		dsizes, dpheno = self.populationMigrationMutation()
		logging.info("updating...")
		self.update(upSizes=dsizes, upPhenotypes=dpheno)
		logging.info("reproduction")
		self.individuals = self.populationReproduction(**kwargs)
		self.demography = len(self.individuals)
		
	def runSimulation(self, outputfile):
		kwargs = self.fitnessParameters
		
		if self.numberOfDemes >= 2 and self.fit_fun in fitness.functions:
			self.createAndPopulateDemes()
		
			self.pathToOutputFolder = fman.getPathToFile(OUTPUT_FOLDER)
			if not os.path.exists(self.pathToOutputFolder):
				os.makedirs(self.pathToOutputFolder)
			
			with open('{}/{}'.format(self.pathToOutputFolder, outputfile), "w") as f:
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
			
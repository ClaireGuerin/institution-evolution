import os
import logging
import institutionevolution.filemanip as fman
from institutionevolution.deme import Deme as Dem
from institutionevolution.individual import Individual as Ind
import institutionevolution.fitness as fitness
import institutionevolution.progress as progress
from statistics import variance
from files import PARAMETER_FOLDER, INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, INITIAL_TECHNOLOGY_FILE, PARAMETER_FILE, OUTPUT_FOLDER, FITNESS_PARAMETERS_FILE
import random

class Population(object):
	
	def __init__(self, fit_fun='pgg', inst=None, mutationBoundaries=True):

		logging.basicConfig(level=logging.INFO,
							format='[%(asctime)s]::%(levelname)s  %(message)s',
							datefmt='%Y.%m.%d - %H:%M:%S')

		logging.info('Creating population')

		if inst is None:
			self.pathToInputFiles = PARAMETER_FOLDER
			self.pathToOutputFiles = OUTPUT_FOLDER
		else:
			self.pathToInputFiles = '{0}/{1}'.format(PARAMETER_FOLDER,inst)
			self.pathToOutputFiles = '{0}/{1}'.format(OUTPUT_FOLDER,inst)
		
		self.pathToInitFile = fman.getPathToFile(filename=INITIALISATION_FILE, dirname=self.pathToInputFiles)		
		self.attrs = fman.extractColumnFromFile(self.pathToInitFile, 0, str)
		self.vals = fman.extractColumnFromFile(self.pathToInitFile, 1, int)
		
		for attr,val in zip(self.attrs, self.vals):
			setattr(self, attr, val)
			
		self.pathToPhenFile = fman.getPathToFile(filename=INITIAL_PHENOTYPES_FILE, dirname=self.pathToInputFiles)
		with open(self.pathToPhenFile) as f:
			self.initialPhenotypes = [float(line) for line in f.readlines()]

		self.pathToTechFile = fman.getPathToFile(filename=INITIAL_TECHNOLOGY_FILE, dirname=self.pathToInputFiles)
		self.initialTechnologyLevel = fman.extractColumnFromFile(self.pathToTechFile, 0, float)[0]
			
		self.pathToParFile = fman.getPathToFile(filename=PARAMETER_FILE, dirname=self.pathToInputFiles)		
		self.parattrs = fman.extractColumnFromFile(self.pathToParFile, 0, str)
		self.parvals = fman.extractColumnFromFile(self.pathToParFile, 1, float)
		
		for parattr,parval in zip(self.parattrs, self.parvals):
			setattr(self, parattr, parval)
			
		self.pathToFitFile = fman.getPathToFile(filename=FITNESS_PARAMETERS_FILE, dirname=self.pathToInputFiles)		
		self.fitattrs = fman.extractColumnFromFile(self.pathToFitFile, 0, str)
		self.fitvals = fman.extractColumnFromFile(self.pathToFitFile, 1, float)
		
		self.fitnessParameters = {}
		for fitattr,fitval in zip(self.fitattrs, self.fitvals):
			self.fitnessParameters[fitattr] = fitval
			
		if hasattr(self, "individualBaseResources") == False:
			setattr(self, "individualBaseResources", 1)
			
		self.fit_fun = fit_fun
		self.mutationBoundaries = mutationBoundaries

		self.numberOfPhenotypes = len(self.initialPhenotypes)
			
	def createAndPopulateDemes(self, nDemes = None, dSize = None):
		if nDemes == None:
			nDemes = self.numberOfDemes
		if dSize == None:
			dSize = self.initialDemeSize
		
		self.populationStructure = [dSize] * nDemes
		self.demography = dSize * nDemes
			
		self.demes = []
		self.individuals = []
		
		for deme in range(nDemes):
			newDemeInstance = Dem()
			newDemeInstance.id = deme
			
			newDemeInstance.neighbours = self.identifyNeighbours(nDemes, deme)
			newDemeInstance.demography = dSize
			newDemeInstance.meanPhenotypes = self.initialPhenotypes
			newDemeInstance.totalPhenotypes = [x * dSize for x in self.initialPhenotypes]
			newDemeInstance.progressValues['technologyLevel'] = self.initialTechnologyLevel
						
			for ind in range(dSize):
				indiv = Ind()
				setattr(indiv, "phenotypicValues", self.initialPhenotypes)
				setattr(indiv, "currentDeme", deme)
				setattr(indiv, "neighbours", newDemeInstance.neighbours)
				setattr(indiv, "resourcesAmount", self.individualBaseResources)
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

	def specialvariance(self, lst, samplelength, samplemean):
		if samplelength == 0:
			tmpvar = 0
		else:
			total = 0
			for phenotype in lst:
				total += (phenotype - samplemean) ** 2
			tmpvar = total / samplelength
		return tmpvar

	def populationReproduction(self, seed=None, **kwargs):
		random.seed(seed)
		self.offspring = []
		self.populationStructure = [0] * self.numberOfDemes
		testdemog = 0

		for ind in self.individuals:
			# REPRODUCTION
			infoToAdd = {}
			infoToAdd["n"] = self.demes[ind.currentDeme].demography
			infoToAdd["xmean"] = self.demes[ind.currentDeme].meanPhenotypes
			infoToAdd["pg"] = self.demes[ind.currentDeme].publicGood
			infoToAdd["x"] = ind.phenotypicValues

			assert type(infoToAdd["n"]) is int, "group size of deme {0} is {1}".format(ind.currentDeme, infoToAdd["n"])
			assert infoToAdd["n"] > 0, "group size of deme {0} is {1}".format(ind.currentDeme, infoToAdd["n"])
			assert type(infoToAdd["x"][0]) is float, "phenotype of individual in deme {0} is {1}".format(ind.currentDeme, infoToAdd["x"])
			assert type(infoToAdd["xmean"][0]) is float, "mean phenotype in deme {0} of individual with phen {3} is {1}. N={2}, n={4}, totalx={5}. Special division returns {6}".format(ind.currentDeme, infoToAdd["xmean"], self.demography, ind.phenotypicValues, self.demes[ind.currentDeme].demography, self.demes[ind.currentDeme].totalPhenotypes, self.specialdivision(self.demes[ind.currentDeme].totalPhenotypes[0], self.demes[ind.currentDeme].demography))

			ind.reproduce(self.fit_fun, **{**kwargs, **infoToAdd})
			self.offspring += ind.offspring
			testdemog += ind.offspringNumber
			self.populationStructure[ind.currentDeme] += ind.offspringNumber


		assert len(self.offspring) == testdemog
		self.individuals = self.offspring
		assert len(self.individuals) == testdemog
		self.demography = len(self.offspring)

	def clearDemeInfo(self):
		for deme in range(self.numberOfDemes):
			if self.fit_fun == 'technology':
				tmpTech = self.initialTechnologyLevel if self.demes[deme].publicGood == None else (1 + self.fitnessParameters['atech'] * self.demes[deme].publicGood) * self.demes[deme].progressValues['technologyLevel'] / (1 + self.fitnessParameters['btech'] * self.demes[deme].progressValues['technologyLevel'])
			else:
				tmpTech = None
			self.demes[deme].totalPhenotypes = [0] * self.numberOfPhenotypes
			self.demes[deme].demography = 0
			self.demes[deme].publicGood = 0
			# progress
			self.demes[deme].progressValues.update({"technologyLevel": tmpTech,
			"numberOfLeaders": 0, 
			"civilianPublicTime": 0, 
			"leaderPublicTime": 0, 
			"labourForce": 0, 
			"policingConsensus": 0,
			"returnedGoods": 0,
			"effectivePublicGood": 0})

	def populationMutationMigration(self):

		for ind in self.individuals:
			# MUTATION
			ind.mutate(self.mutationRate, self.mutationStep, bounded=self.mutationBoundaries)
			
			# MIGRATION
			ind.migrate(nDemes=self.numberOfDemes, migRate=self.migrationRate)

			# UPDATE
			assert ind.currentDeme == ind.destinationDeme
			ind.neighbours = self.demes[ind.currentDeme].neighbours
			## demography
			self.demes[ind.currentDeme].demography += 1
			## public good
			self.demes[ind.currentDeme].publicGood += ind.phenotypicValues[0] * ind.resourcesAmount
			## total phenotypes
			for phen in range(self.numberOfPhenotypes):
				self.demes[ind.currentDeme].totalPhenotypes[phen] += ind.phenotypicValues[phen]

	def update(self):
		for deme in self.demes:
			meanphen = []
			for phen in range(self.numberOfPhenotypes):
				calculateMean = self.specialdivision(deme.totalPhenotypes[phen], deme.demography)
				meanphen.append(calculateMean) 

			setattr(deme, "meanPhenotypes", meanphen)

			try:
				tmpmean = deme.meanPhenotypes[1]
				if tmpmean is not None:
					setattr(deme, "policingConsensus", tmpmean)
				else:
					setattr(deme, "policingConsensus", 0.0)
			except IndexError as e:
				setattr(deme, "policingConsensus", 0.0)
			## effective public good
			setattr(deme, "effectivePublicGood", float((1.0 - deme.policingConsensus) * deme.publicGood))
			
			## progress
			progressPars = {'n': deme.demography, 'phen': deme.meanPhenotypes}
			deme.progressValues.update(progress.functions[self.fit_fun](**{**self.fitnessParameters,**progressPars}))

	def lifecycle(self, **kwargs):
		logging.info("migration and mutation")
		self.clearDemeInfo()
		self.populationMutationMigration()
		logging.info("updating...")
		self.update()
		logging.info("reproduction")
		self.populationReproduction(**kwargs)
		
	def runSimulation(self, outputfile):
		
		if self.numberOfDemes >= 2 and self.fit_fun in fitness.functions:
			self.createAndPopulateDemes()
		
			self.pathToOutputFolder = fman.getPathToFile(self.pathToOutputFiles)
			if not os.path.exists(self.pathToOutputFolder):
				os.makedirs(self.pathToOutputFolder)

			phenotypesfile = '{0}/{1}_phenotypes.txt'.format(self.pathToOutputFolder, outputfile)
			phenvariancefile = '{0}/{1}_pheno_var.txt'.format(self.pathToOutputFolder, outputfile)
			demographyfile = '{0}/{1}_demography.txt'.format(self.pathToOutputFolder, outputfile)
			demovariancefile = '{0}/{1}_demo_var.txt'.format(self.pathToOutputFolder, outputfile)
			
			with open(phenotypesfile, "w", buffering=1) as fp, \
			open(demographyfile, "w", buffering=1) as fd, \
			open(demovariancefile, "w", buffering=1) as vd, \
			open(phenvariancefile, "w", buffering=1) as vp:
				for gen in range(self.numberOfGenerations):
					logging.info('Running generation {0}'.format(gen))
					
					self.lifecycle(**self.fitnessParameters)

					if self.demography == 0:
						#raise ValueError("The population went extinct after {0} generations".format(gen))
						logging.info('Population went extinct after {0} generations'.format(gen))
						phenmeans = [None] * self.numberOfPhenotypes
						break
					else:
						phenmeans = []
						phenvars = []

						for phen in range(self.numberOfPhenotypes):
							tmpPhenotypes = [ind.phenotypicValues[phen] for ind in self.individuals]
							tmpMean = self.specialmean(tmpPhenotypes)
							tmpVar = self.specialvariance(tmpPhenotypes, len(tmpPhenotypes), tmpMean)

							phenmeans.append(str(round(tmpMean, 3)))
							assert type(tmpVar) is float, "phenotype variance = {0}, phenotypes = {1}".format(tmpVar, tmpPhenotypes)
							phenvars.append(str(round(tmpVar, 3)))


						sep = ','
						fp.write('{0}\n'.format(sep.join(phenmeans)))
						vp.write('{0}\n'.format(sep.join(phenvars)))
						fd.write('{0}\n'.format(self.demography / self.numberOfDemes))
						vd.write('{0}\n'.format(self.specialvariance(self.populationStructure, len(self.populationStructure), self.demography / self.numberOfDemes)))
				
		elif self.numberOfDemes < 2 and self.fit_fun in fitness.functions:
			raise ValueError('This program runs simulations on well-mixed populations only. "numberOfDemes" in initialisation.txt must be > 1')
			
		elif self.numberOfDemes >= 2 and self.fit_fun not in fitness.functions:
			raise KeyError(str('Fitness function "{0}" unknown. Add it to the functions in fitness.py').format(self.fit_fun))
			
		else:
			raise ValueError('This program runs simulations on well-mixed populations only. "numberOfDemes" in initialisation.txt must be > 1')
			raise KeyError('Fitness function "{0}" unknown. Add it to the functions in fitness.py'.format(self.fit_fun))
			
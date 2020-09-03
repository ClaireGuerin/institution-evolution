import os
import logging
import institutionevolution.filemanip as fman
from institutionevolution.deme import Deme as Dem
from institutionevolution.individual import Individual as Ind
import institutionevolution.fitness as fitness
import institutionevolution.progress as progress
import institutionevolution.politics as politics
import institutionevolution.myarithmetics as ar
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
			self.pathToInputFiles = os.path.abspath(PARAMETER_FOLDER)
			self.pathToOutputFiles = os.path.abspath(OUTPUT_FOLDER)
		else:
			self.pathToInputFiles = os.path.abspath(inst)
			self.pathToOutputFiles = os.path.abspath(inst)
		
		self.pathToInitFile = os.path.join(self.pathToInputFiles, INITIALISATION_FILE)		
		self.attrs = fman.extractColumnFromFile(self.pathToInitFile, 0, str)
		self.vals = fman.extractColumnFromFile(self.pathToInitFile, 1, int)
		
		for attr,val in zip(self.attrs, self.vals):
			setattr(self, attr, val)
			
		self.pathToPhenFile = os.path.join(self.pathToInputFiles, INITIAL_PHENOTYPES_FILE)
		with open(self.pathToPhenFile) as f:
			self.initialPhenotypes = [float(line) for line in f.readlines()]

		self.pathToTechFile = os.path.join(self.pathToInputFiles, INITIAL_TECHNOLOGY_FILE)
		self.initialTechnologyLevel = fman.extractColumnFromFile(self.pathToTechFile, 0, float)[0]
			
		self.pathToParFile = os.path.join(self.pathToInputFiles, PARAMETER_FILE)		
		self.parattrs = fman.extractColumnFromFile(self.pathToParFile, 0, str)
		self.parvals = fman.extractColumnFromFile(self.pathToParFile, 1, float)
		
		for parattr,parval in zip(self.parattrs, self.parvals):
			setattr(self, parattr, parval)
			
		self.pathToFitFile = os.path.join(self.pathToInputFiles, FITNESS_PARAMETERS_FILE)		
		self.fitattrs = fman.extractColumnFromFile(self.pathToFitFile, 0, str)
		self.fitvals = fman.extractColumnFromFile(self.pathToFitFile, 1, float)
		
		self.fitnessParameters = {}
		for fitattr,fitval in zip(self.fitattrs, self.fitvals):
			self.fitnessParameters[fitattr] = fitval
			
		if hasattr(self, "individualBaseResources") == False:
			setattr(self, "individualBaseResources", 1)
			
		self.fit_fun = fit_fun
		self.mutationBoundaries = mutationBoundaries

	def createAndPopulateDemes(self, nDemes = None, dSize = None):
		if nDemes == None:
			nDemes = self.numberOfDemes
		if dSize == None:
			dSize = self.initialDemeSize
		
		self.populationStructure = [dSize] * nDemes
		self.demography = dSize * nDemes
			
		self.demes = []
		self.individuals = []

		self.numberOfPhenotypes = len(self.initialPhenotypes)
		
		for deme in range(nDemes):
			newDemeInstance = Dem()
			newDemeInstance.id = deme
			
			newDemeInstance.neighbours = self.identifyNeighbours(nDemes, deme)
			newDemeInstance.demography = dSize
			newDemeInstance.meanPhenotypes = self.initialPhenotypes
			newDemeInstance.varPhenotypes = 0
			newDemeInstance.totalPhenotypes = [x * dSize for x in self.initialPhenotypes]
			newDemeInstance.totalPhenotypeSquares = [(x ** 2) * dSize for x in self.initialPhenotypes]
			newDemeInstance.technologyLevel = self.initialTechnologyLevel
						
			for ind in range(dSize):
				indiv = Ind()
				setattr(indiv, "phenotypicValues", self.initialPhenotypes)
				setattr(indiv, "currentDeme", deme)
				setattr(indiv, "neighbours", newDemeInstance.neighbours)
				setattr(indiv, "resourcesAmount", self.individualBaseResources)
				self.individuals.append(indiv)
			
			self.demes.append(newDemeInstance)

	def identifyNeighbours(self, nd, demeID):
		tmp = list(range(nd))
		del tmp[demeID]
		return tmp

	def clearDemeInfo(self):
		self.parents = None
		self.advances = []
		for deme in range(self.numberOfDemes):
			# INCREMENT TECHNOLOGY LEVEL IN DEME
			if self.fit_fun == 'technology':
				tech = self.demes[deme].technologyLevel
				try:
					tmpTech = tech * (self.fitnessParameters['atech'] + ((1 - self.fitnessParameters['p']) * self.demes[deme].publicGood) ** (1 - self.fitnessParameters['betaTech'])) / (1 + self.fitnessParameters['btech'] * tech)
				except TypeError as e:
					tmpTech = tech
			else:
				tmpTech = -99
			self.demes[deme].technologyLevel = tmpTech
			self.advances.append(tmpTech)

			# RESET ALL OTHER DEME INFORMATION
			self.demes[deme].totalPhenotypes = [0] * self.numberOfPhenotypes
			self.demes[deme].demography = 0
			self.demes[deme].publicGood = 0
			self.demes[deme].totalResources = 0
			self.demes[deme].numberOfLeaders = 0
			# politics
			self.demes[deme].politicsValues = {"civilianPublicTime": 0, 
			"leaderPublicTime": 0, 
			"labourForce": 0,
			"consensus": 0,
			"consensusTime": 0}
			# progress
			self.demes[deme].progressValues.update({"returnedGoods": 0,
			"effectivePublicGood": None,
			"institutionQuality": 0,
			"fine": 0,
			"fineBudget": 0,
			"investmentReward": 0})

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
			# total phenotypes
			for phen in range(self.numberOfPhenotypes):
				self.demes[ind.currentDeme].totalPhenotypes[phen] += ind.phenotypicValues[phen]
				self.demes[ind.currentDeme].totalPhenotypeSquares[phen] += ind.phenotypicValues[phen] * ind.phenotypicValues[phen]

	def updateDemeInfoPreProduction(self):
		self.debatetime = []
		for deme in self.demes:
			meanphen = []
			varphen = []
			for phen in range(self.numberOfPhenotypes):
				calculateMean = ar.specialdivision(deme.totalPhenotypes[phen], deme.demography)
				meanphen.append(calculateMean) 

				calculateVar = ar.specialvariance(deme.totalPhenotypes[phen],deme.totalPhenotypeSquares[phen],deme.demography)
				varphen.append(calculateVar)

			setattr(deme, "meanPhenotypes", meanphen)
			setattr(deme, "varPhenotypes", varphen)

		for ind in self.individuals:
			# ELECTIONS
			try:
				proportion = self.demes[ind.currentDeme].meanPhenotypes[3]
			except IndexError as e:
				proportion = 0
			ind.ascend(leadProp=proportion)
			## increment number of leaders within deme
			self.demes[ind.currentDeme].numberOfLeaders += ind.leader

		for deme in self.demes:
			if deme.demography > 0:
				politicsPars = {'n': deme.demography, 'phen': deme.meanPhenotypes, 'varphen': deme.varPhenotypes}
				deme.politicsValues.update(politics.functions[self.fit_fun](**{**self.fitnessParameters,**politicsPars}))
			self.debatetime.append(deme.politicsValues["consensusTime"])

	def populationProduction(self):
		# INDIVIDUAL PRODUCTION AND CONTRIBUTION TO PUBLIC GOOD:
		for ind in self.individuals:
			infoToAdd = {'n': self.demes[ind.currentDeme].demography, 'tech': self.demes[ind.currentDeme].technologyLevel}
			ind.produceResources(self.fit_fun, **{**infoToAdd, **self.fitnessParameters, **self.demes[ind.currentDeme].politicsValues})
			self.demes[ind.currentDeme].totalResources += ind.resourcesAmount
			self.demes[ind.currentDeme].publicGood += ind.phenotypicValues[0] * ind.resourcesAmount

	def updateDemeInfoPostProduction(self):
		self.resources = []
		for deme in self.demes:
			self.resources.append(deme.totalResources)
			## progress
			if deme.demography > 0:
				progressPars = {'n': deme.demography, 'phen': deme.meanPhenotypes, 'pg': deme.publicGood, 'totRes': deme.totalResources}
				deme.progressValues.update(progress.functions[self.fit_fun](**{**self.fitnessParameters,**progressPars,**deme.politicsValues}))

	def populationReproduction(self, seed=None):
		if seed is not None: random.seed(seed)
		self.offspring = []
		self.populationStructure = [0] * self.numberOfDemes
		testdemog = 0

		for ind in self.individuals:
			# REPRODUCTION
			## add deme information necessary to calculate individual fitness
			infoToAdd = {}
			infoToAdd["tech"] = self.demes[ind.currentDeme].technologyLevel
			infoToAdd["n"] = self.demes[ind.currentDeme].demography
			infoToAdd["xmean"] = self.demes[ind.currentDeme].meanPhenotypes
			infoToAdd["pg"] = self.demes[ind.currentDeme].publicGood

			assert type(infoToAdd["n"]) is int, "group size of deme {0} is {1}".format(ind.currentDeme, infoToAdd["n"])
			assert infoToAdd["n"] > 0, "group size of deme {0} is {1}".format(ind.currentDeme, infoToAdd["n"])
			#assert type(infoToAdd["x"][0]) is float, "phenotype of individual in deme {0} is {1}".format(ind.currentDeme, infoToAdd["x"])
			assert type(infoToAdd["xmean"][0]) is float, "mean phenotype in deme {0} of individual with phen {3} is {1}. N={2}, n={4}, totalx={5}. Special division returns {6}".format(ind.currentDeme, infoToAdd["xmean"], self.demography, ind.phenotypicValues, self.demes[ind.currentDeme].demography, self.demes[ind.currentDeme].totalPhenotypes, self.specialdivision(self.demes[ind.currentDeme].totalPhenotypes[0], self.demes[ind.currentDeme].demography))

			ind.reproduce(self.fit_fun, **{**self.fitnessParameters, **infoToAdd, **self.demes[ind.currentDeme].progressValues})
			self.offspring += ind.offspring
			testdemog += ind.offspringNumber
			self.populationStructure[ind.currentDeme] += ind.offspringNumber

		self.parents = self.individuals
		assert len(self.offspring) == testdemog
		self.individuals = self.offspring
		assert len(self.individuals) == testdemog
		self.demography = len(self.offspring)

	def lifecycle(self):
		logging.info("migration and mutation")
		self.clearDemeInfo()
		self.populationMutationMigration()
		logging.info("updating...")
		self.updateDemeInfoPreProduction()
		self.populationProduction()
		self.updateDemeInfoPostProduction()
		logging.info("reproduction")
		self.populationReproduction()
		
	def runSimulation(self):
		
		if self.numberOfDemes >= 2 and self.fit_fun in fitness.functions:
			self.createAndPopulateDemes()
		
			self.pathToOutputFolder = self.pathToOutputFiles
			if not os.path.exists(self.pathToOutputFolder):
				os.makedirs(self.pathToOutputFolder, exist_ok=True)

			phenotypesfile = self.pathToOutputFolder + '/out_phenotypes.txt'
			demographyfile = self.pathToOutputFolder + '/out_demography.txt'
			technologyfile = self.pathToOutputFolder + '/out_technology.txt'
			resourcesfile = self.pathToOutputFolder + '/out_resources.txt'
			consensusfile = self.pathToOutputFolder + '/out_consensus.txt'
			
			with open(phenotypesfile, "w", buffering=1) as fp, \
			open(demographyfile, "w", buffering=1) as fd, \
			open(technologyfile, "w", buffering=1) as ft, \
			open(resourcesfile, "w", buffering=1) as fr, \
			open(consensusfile, "w", buffering=1) as fc:
				for gen in range(self.numberOfGenerations):
					logging.info('Running generation {0}'.format(gen))
					
					self.lifecycle()

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
							tmpMean = ar.specialmean(tmpPhenotypes)
							tmpVar = ar.specialvariance(sum(tmpPhenotypes), sum(x ** 2 for x in tmpPhenotypes), len(tmpPhenotypes))

							phenmeans.append(str(round(tmpMean, 3)))
							assert type(tmpVar) is float, "phenotype variance = {0}, phenotypes = {1}".format(tmpVar, tmpPhenotypes)
							phenvars.append(str(round(tmpVar, 3)))


						sep = ','
						fp.write('{0},{1}\n'.format(sep.join(phenmeans),sep.join(phenvars)))
						(demmean,demvar) = ar.extractMeanAndVariance(lst=self.populationStructure, n=self.numberOfDemes)
						assert all([x is not None for x in self.advances]), "some or all deme tech entries are none at generation {1}: {0}".format(self.advances,gen)
						(techmean,techvar) = ar.extractMeanAndVariance(lst=self.advances, n=self.numberOfDemes)
						(resmean,resvar) = ar.extractMeanAndVariance(lst=self.resources, n=self.numberOfDemes)
						assert all([x is not None for x in self.debatetime]), "some or all deme debate time entries are none at generation {1}: {0}".format(self.debatetime,gen)
						(consmean,consvar) = ar.extractMeanAndVariance(lst=self.debatetime, n=self.numberOfDemes)
						fd.write('{0},{1}\n'.format(demmean, demvar))
						ft.write('{0},{1}\n'.format(techmean, techvar))
						fr.write('{0},{1}\n'.format(resmean,resvar))
						fc.write('{0},{1}\n'.format(consmean,consvar))

		elif self.numberOfDemes < 2 and self.fit_fun in fitness.functions:
			raise ValueError('This program runs simulations on well-mixed populations only. "numberOfDemes" in initialisation.txt must be > 1')
			
		elif self.numberOfDemes >= 2 and self.fit_fun not in fitness.functions:
			raise KeyError(str('Fitness function "{0}" unknown. Add it to the functions in fitness.py').format(self.fit_fun))
			
		else:
			raise ValueError('This program runs simulations on well-mixed populations only. "numberOfDemes" in initialisation.txt must be > 1')
			raise KeyError('Fitness function "{0}" unknown. Add it to the functions in fitness.py'.format(self.fit_fun))

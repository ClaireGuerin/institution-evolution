import os
import filemanip as fman
from deme import Deme as Dem
from individual import Individual as Ind
from statistics import mean

INITIALISATION_FILE = 'initialisation.txt'
PARAMETER_FILE = 'parameters.txt'
INITIAL_PHENOTYPES_FILE = 'initial_phenotypes.txt'
FITNESS_PARAMETERS_FILE = 'fitness_parameters.txt'
OUTPUT_FOLDER = 'res'
OUTPUT_FILE = 'output.txt'

class Population:
	
	def __init__(self, fit_fun='pgg'):
		
		self.pathToInitFile = fman.getPathToFile(INITIALISATION_FILE)		
		self.attrs = fman.extractColumnFromFile(self.pathToInitFile,0, str)
		self.vals = fman.extractColumnFromFile(self.pathToInitFile,1, int)
		
		for attr,val in zip(self.attrs, self.vals):
			setattr(self, attr, val)
			
		self.pathToPhenFile = fman.getPathToFile(INITIAL_PHENOTYPES_FILE)
		with open(self.pathToPhenFile) as f:
			self.initialPhenotypes = [float(line) for line in f.readlines()]
			
		self.pathToParFile = fman.getPathToFile(PARAMETER_FILE)		
		self.parattrs = fman.extractColumnFromFile(self.pathToParFile,0, str)
		self.parvals = fman.extractColumnFromFile(self.pathToParFile,1, float)
		
		for parattr,parval in zip(self.parattrs, self.parvals):
			setattr(self, parattr, parval)
			
		self.pathToFitFile = fman.getPathToFile(FITNESS_PARAMETERS_FILE)		
		self.fitattrs = fman.extractColumnFromFile(self.pathToFitFile,0, str)
		self.fitvals = fman.extractColumnFromFile(self.pathToFitFile,1, float)
		
		self.fitnessParameters = {}
		for fitattr,fitval in zip(self.fitattrs, self.fitvals):
			self.fitnessParameters[fitattr] = fitval
			
		if hasattr(self, "individualResources") == False:
			setattr(self, "individualResources", 1)
			
		self.fit_fun = fit_fun
			
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
					
	def migrationUpdate(self):
		updateDemeSizes = [0] * self.numberOfDemes
		for ind in self.individuals:
			ind.migrate(nDemes=self.numberOfDemes, migRate=self.migrationRate)
			ind.neighbours = self.demes[ind.currentDeme].neighbours
			updateDemeSizes[ind.currentDeme] += 1
			
		for deme in range(self.numberOfDemes):
			focalDeme = self.demes[deme]
			focalDeme.demography = updateDemeSizes[deme]
	
	def mutationUpdate(self):
		nPhen = len(self.initialPhenotypes)
		updateDemePhenotypes = [[[]] * nPhen] * self.numberOfDemes
		
		for ind in self.individuals:
			ind.mutate(self.mutationRate, self.mutationStep)
			for phen in range(nPhen):
				updateDemePhenotypes[ind.currentDeme][phen].append(ind.phenotypicValues[phen])
		
		for deme in range(self.numberOfDemes):
			focalDeme = self.demes[deme]
			focalDeme.meanPhenotypes = [self.meanWithSingleValue(updateDemePhenotypes[deme][phen]) for phen in range(nPhen)]
			
	def meanWithSingleValue(self, lst):
		if len(lst) > 1:
			tmpmean = mean(lst)
		elif len(lst) == 1:
			tmpmean = lst[0]
		return tmpmean
		
	def reproductionUpdate(self):
		self.offspring = []
			
		for ind in self.individuals:
			self.offspring += ind.offspring
			
		self.individuals = self.offspring
		self.demography = len(self.individuals)
		
			
	def runSimulation(self):
		kwargs = self.fitnessParameters
		
		if self.numberOfDemes >= 2:
			self.createAndPopulateDemes()
		
			self.pathToOutputFolder = fman.getPathToFile(OUTPUT_FOLDER)
			if not os.path.exists(self.pathToOutputFolder):
				os.makedirs(self.pathToOutputFolder)
			
			with open('{}/{}'.format(self.pathToOutputFolder, OUTPUT_FILE), "w") as f:
				for gen in range(self.numberOfGenerations):
					phenotypes = []
					self.migrationUpdate()
					self.mutationUpdate()
					for ind in self.individuals:
												
						kwargs["n"] = self.demes[ind.currentDeme].demography
						kwargs["xmean"] = self.demes[ind.currentDeme].meanPhenotypes[0]
						kwargs["x"] = ind.phenotypicValues[0]
						
						ind.reproduce(self.fit_fun, **kwargs)
					
					self.reproductionUpdate()
					phenotypes = [ind.phenotypicValues[0] for ind in self.individuals]
					f.write('{0}\n'.format(mean(phenotypes)))
		else:
			raise ValueError('This program runs simulations on well-mixed populations only. "numberOfDemes" in initialisation.txt must be > 1')
			
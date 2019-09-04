import os
import filemanip as fman
from deme import Deme as Dem
from individual import Individual as Ind
from statistics import mean

INITIALISATION_FILE = 'initialisation.txt'
PARAMETER_FILE = 'parameters.txt'
INITIAL_PHENOTYPES_FILE = 'initial_phenotypes.txt'
OUTPUT_FOLDER = 'res'
OUTPUT_FILE = 'output.txt'

class Population:
	
	def __init__(self):
		
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
			
		if hasattr(self, "individualResources") == False:
			setattr(self, "individualResources", 1)
			
	def createAndPopulateDemes(self, nDemes = None, dSize = None):
		if nDemes == None:
			nDemes = self.numberOfDemes
		if dSize == None:
			dSize = self.initialDemeSize
			
		self.demes = []
		self.individuals = []
		
		for deme in range(nDemes):
			newDemeInstance = Dem()
			newDemeInstance.id = deme
			
			newDemeInstance.neighbours = self.identifyNeighbours(nDemes, deme)
			newDemeInstance.demography = dSize
						
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
					
	def populationMigration(self):
		updateDemeSizes = [0] * self.numberOfDemes
		for ind in self.individuals:
			ind.migrate(nDemes=self.numberOfDemes, migRate=self.migrationRate)
			updateDemeSizes[ind.currentDeme] += 1
			
		for deme in range(self.numberOfDemes):
			focalDeme = self.demes[deme]
			focalDeme.demography = updateDemeSizes[deme]
	
	def runSimulation(self):
		if self.numberOfDemes >= 2:
			self.createAndPopulateDemes()
		
			self.pathToOutputFolder = fman.getPathToFile(OUTPUT_FOLDER)
			if not os.path.exists(self.pathToOutputFolder):
				os.makedirs(self.pathToOutputFolder)
			
			with open('{}/{}'.format(self.pathToOutputFolder, OUTPUT_FILE), "w") as f:
				for gen in range(self.numberOfGenerations):
					phenotypes = []
					self.populationMigration()
					for ind in self.individuals:
						ind.mutate(self.mutationRate, self.mutationStep)
						ind.reproduce()
						
						phenotypes.append(ind.phenotypicValues[0])
					f.write('{0}\n'.format(mean(phenotypes)))
		else:
			raise ValueError('This program runs simulations on well-mixed populations only. "numberOfDemes" in initialisation.txt must be > 1')
			
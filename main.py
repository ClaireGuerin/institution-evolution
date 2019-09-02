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
			
	def createAndPopulateDemes(self, nDemes = None, dSize = None):
		if nDemes == None:
			nDemes = self.numberOfDemes
		if dSize == None:
			dSize = self.initialDemeSize
			
		allDemes = list(range(nDemes))
				
		self.allPopulationDemes = []
		for deme in range(nDemes):
			newDemeInstance = Dem()
			newDemeInstance.id = deme
			
			newDemeInstance.neighbours = self.identifyNeighbours(allDemes, deme)
			
			newDemeInstance.individuals = [Ind()] * dSize
			
			for ind in newDemeInstance.individuals:
				setattr(ind, "phenotypicValues", self.initialPhenotypes)
				setattr(ind, "currentDeme", deme)
			
			self.allPopulationDemes.append(newDemeInstance)
			
	def identifyNeighbours(self, demeNumber, demeID):
		tmp = demeNumber
		del tmp[demeID]
		return tmp
			
			
					
	def runSimulation(self):
		self.createAndPopulateDemes()
		
		self.pathToOutputFolder = fman.getPathToFile(OUTPUT_FOLDER)
		if not os.path.exists(self.pathToOutputFolder):
			os.makedirs(self.pathToOutputFolder)
			
		with open('{}/{}'.format(self.pathToOutputFolder, OUTPUT_FILE), "w") as f:
			for gen in range(self.numberOfGenerations):
				meanPhenDeme = []
				for deme in self.allPopulationDemes:
					phenDeme = []
					for ind in deme.individuals:
						ind.mutate(self.mutationRate, self.mutationStep)
						ind.migrate()
						ind.reproduce()
						
						phenDeme.append(ind.phenotypicValues[0])
					meanPhenDeme.append(mean(phenDeme))
				f.write('{0}\n'.format(mean(meanPhenDeme)))
			
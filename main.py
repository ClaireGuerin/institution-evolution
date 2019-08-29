import os
import filemanip as fman
from deme import Deme as Dem
from individual import Individual as Ind

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
			
	def createAndPopulateDemes(self):
		self.allPopulationDemes = []
		for deme in range(self.numberOfDemes):
			newDemeInstance = Dem()
			newDemeInstance.individuals = [Ind()] * self.initialDemeSize
			
			for ind in newDemeInstance.individuals:
				setattr(ind, "phenotypicValues", self.initialPhenotypes)
				setattr(ind, "currentDeme", deme)
			
			self.allPopulationDemes.append(newDemeInstance)
					
	def runSimulation(self):
		self.pathToOutputFolder = fman.getPathToFile(OUTPUT_FOLDER)
		if not os.path.exists(self.pathToOutputFolder):
			os.makedirs(self.pathToOutputFolder)
			
		with open('{}/{}'.format(self.pathToOutputFolder, OUTPUT_FILE), "w") as f:
			for gen in range(self.numberOfGenerations):
				f.write('\n')
			
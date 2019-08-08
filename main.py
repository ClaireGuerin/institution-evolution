import os
import filemanip as fman

INITIALISATION_FILE = 'initialisation.txt'
OUTPUT_FOLDER = 'res'
OUTPUT_FILE = 'output.txt'

class Population:
	
	def __init__(self):
		
		self.pathToInitFile = fman.getPathToFile(INITIALISATION_FILE)
		
		self.attrs = fman.extractColumnFromFile(self.pathToInitFile,0, str)
		self.vals = fman.extractColumnFromFile(self.pathToInitFile,1, int)
		
		for attr,val in zip(self.attrs, self.vals):
			setattr(self, attr, val)
			
	def runSimulation(self):
		self.pathToOutputFolder = fman.getPathToFile(OUTPUT_FOLDER)
		if not os.path.exists(self.pathToOutputFolder):
			os.makedirs(self.pathToOutputFolder)
			
		with open('{}/{}'.format(self.pathToOutputFolder, OUTPUT_FILE), "w") as f:
			for gen in range(self.numberOfGenerations):
				f.write('\n')
			
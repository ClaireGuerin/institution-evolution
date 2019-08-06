import os
import filemanip as fman

INITIALISATION_FILE = 'initialisation.txt'

class Population:
	
	def __init__(self):
		
		self.pathToInitFile = fman.getPathToFile(INITIALISATION_FILE)
		
		self.attrs = fman.extractColumnFromFile(self.pathToInitFile,0, str)
		self.vals = fman.extractColumnFromFile(self.pathToInitFile,1, int)
		
		for attr,val in zip(self.attrs, self.vals):
			setattr(self, attr, val)
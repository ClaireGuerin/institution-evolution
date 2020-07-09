import os
import sys
from pathlib import Path
from numpy import arange
import institutionevolution.filemanip as fman
from files import INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, INITIAL_TECHNOLOGY_FILE, PARAMETER_FILE, FITNESS_PARAMETERS_FILE

class Launcher(object):

	def __init__(self, metafolder, parfile):
		ndemes = 10
		demesize = 20
		ngen = 20
		baseres = 1
		phen = [0.0] * 4
		tech = 1
		mutrate = 0.01
		mutstep = 0.02
		migrate = 0.5

		self.strINITFILE = "numberOfDemes,{0}\ninitialDemeSize,{1}\nnumberOfGenerations,{2}\nindividualBaseResources,{3}".format(ndemes,demesize,ngen,baseres)
		self.strPHENFILE = "\n".join(map(str,phen))
		self.strTECHFILE = str(tech)
		self.strPARAFILE = "mutationRate,{0}\nmutationStep,{1}\nmigrationRate,{2}".format(mutrate,mutstep,migrate)

		self.metafolder = metafolder
		self.parfile = parfile

	def createFolder(self,folder):
		# CREATE FOLDER
		try:
			os.mkdir(folder)
			print("Created folder {0} for simulation storage".format(folder))
		except FileExistsError:
			print("Folder {0} already exists".format(folder))

	def readParameterInfo(self):
		# READ PARAMETER RANGE FILE
		parname = []
		parstart = []
		parend = []
		parstep = []

		with open(self.parfile, 'r') as parranges:
			for line in parranges:
				listLine = line.split(',')
				parname.append(listLine[0])
				parstart.append(listLine[1])
				try:
					parend.append(listLine[2])
					try:
						parstep.append(listLine[3])
					except IndexError:
						raise TypeError("provide a step for range of parameter "+listLine[0])
				except IndexError:
					parend.append(None)
					parstep.append(None)

		self.parname = parname
		self.parstart = parstart
		self.parend = parend
		self.parstep = parstep

	def createRanges(self):
		# CREATE RANGES
		self.fitnessFunction = parstart[0]
		ranges = []
		for par in range(len(parname)-1):
			tmpstart = float(parstart[par+1])
			tmpend = float(parend[par+1])
			tmpstep = float(parstep[par+1])
			tmpRange = arange(tmpstart,tmpend,tmpstep)

	def createCombinations(self):
		# CREATE COMBINATIONS	
		pass

	def writeParameterFiles(self, fitfun, pname, pval):
		# CREATE SUBFOLDER 
		subfolder = Path(self.metafolder, fitfun+"_"+"".join([i+str(j) for i,j in zip(pname, pval)]))
		self.createFolder(subfolder)
		
		# WRITE PARAMETER FILE FOR SPECIFIC COMBINATION

		with open(Path(subfolder, FITNESS_PARAMETERS_FILE), "w", buffering=1) as f, \
		open(Path(subfolder, INITIALISATION_FILE), "w", buffering=1) as a, \
		open(Path(subfolder, INITIAL_PHENOTYPES_FILE), "w", buffering=1) as b, \
		open(Path(subfolder, INITIAL_TECHNOLOGY_FILE), "w", buffering=1) as c, \
		open(Path(subfolder, PARAMETER_FILE), "w", buffering=1) as d:
			## Fitness parameters
			for par in range(len(pname)):
				f.write("{0},{1}\n".format(pname[par],pval[par]))
			## Initialisation
			a.write(self.strINITFILE)
			## Initial phenotypes
			b.write(self.strPHENFILE)
			## Initial technology
			c.write(self.strTECHFILE)
			## Parameters
			d.write(self.strPARAFILE)

	def writeParameterFilesInAllFolders(self):
		# CREATE METAFOLDER
		self.createFolder(self.metafolder)

import os
import sys
from pathlib import Path
from numpy import linspace
import itertools as it
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

		with open(self.parfile, mode='r', newline='\n') as parranges:
			for line in parranges:
				removeTrailingNewline = line.replace('\n', '')
				listLine = removeTrailingNewline.split(',')
				#listLine = line.split(',')
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

		self.parname = parname[1:]
		self.parstart = parstart[1:]
		self.parend = parend[1:]
		self.parstep = parstep[1:]

		self.lastLine = listLine

		self.fitnessFunction = parstart[0]

	def _customArange(self, start, end, step):
		return linspace(start, end, num=round((end-start)/step), endpoint=False)

	def createRanges(self):
		# CREATE RANGES
		ranges = []
		for par in range(len(self.parname)):
			tmpstart = float(self.parstart[par])
			if self.parend[par] == None:
				tmpRange = [tmpstart]
			else:
				tmpend = float(self.parend[par])
				tmpstep = float(self.parstep[par])
				tmpRange = self._customArange(tmpstart,tmpend,tmpstep).tolist()
				
			ranges.append(tmpRange)

		self.ranges = ranges

	def _flattenTuple(self, object): 
		
		gather = []
		for item in object:
			if isinstance(item, tuple):
				gather.extend(self._flattenTuple(item))
			else:
				gather.append(item)
		return tuple(gather)

	def createCombinations(self):
		# CREATE COMBINATIONS
		lst = self.ranges[0]
		for par in range(len(self.ranges)-1):
			tmplst = list(it.product(lst,self.ranges[par+1]))
			lst = tmplst

		flatlst = []
		for comb in lst:
			flatcomb = self._flattenTuple(comb)
			flatlst.append(flatcomb)

		self.combinations = flatlst

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

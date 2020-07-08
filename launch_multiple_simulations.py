import os
import sys
from numpy import arange
import institutionevolution.filemanip as fman
from files import INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, INITIAL_TECHNOLOGY_FILE, PARAMETER_FILE, FITNESS_PARAMETERS_FILE

ndemes = 10
demesize = 20
ngen = 20
baseres = 1
phen = [0.0] * 4
tech = 1
mutrate = 0.01
mutstep = 0.02
migrate = 0.5

strINITFILE = "numberOfDemes,{0}\ninitialDemeSize,{1}\nnumberOfGenerations,{2}\nindividualBaseResources,{3}".format(ndemes,demesize,ngen,baseres)
strPHENFILE = "\n".join(map(str,phen))
strTECHFILE = str(tech)
strPARAFILE = "mutationRate,{0}\nmutationStep,{1}\nmigrationRate,{2}".format(mutrate,mutstep,migrate)

args = sys.argv
print(args)

metafolder = args[1]
parfile = args[2]

print(parfile)
print(type(parfile))

# CREATE METAFOLDER
try:
	os.mkdir(metafolder)
	print("Created metafolder to store all simulations")
except FileExistsError:
	print("Metafolder already exists")

# READ PARAMETER RANGE FILE
parname = []
parstart = []
parend = []
parstep = []

with open(parfile, 'r') as parranges:
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

# CREATE RANGES
fitnessFunction = parstart[0]
ranges = []
for par in range(len(parname-1)):
	tmpstart = float(parstart[par+1])
	tmpend = float(parend[par+1])
	tmpstep = float(parstep[par+1])
	tmpRange = arange(tmpstart,tmpend,tmpstep)

# CREATE COMBINATIONS



parname = fman.extractColumnFromFile(parfile,0,str)
parvalue = fman.extractColumnFromFile(parfile,1,float)
try:
	subfolder = metafolder+'/'+"".join([i+str(j) for i,j in zip(parname, parvalue)])
	os.mkdir(subfolder)
	print("Created subfolder to store one simulation")
except FileExistsError:
	print("Subfolder already exists")

#parameterFileNames = [INITIALISATION_FILE, INITIAL_PHENOTYPES_FILE, INITIAL_TECHNOLOGY_FILE, PARAMETER_FILE, FITNESS_PARAMETERS_FILE]
fitnessFunction = parname[0]

with open(subfolder+'/'+FITNESS_PARAMETERS_FILE, "w") as f:
	for par in range(1,len(parname)):
		f.write("{0},{1}\n".format(parname[par],parvalue[par]))

with open(subfolder+'/'+INITIALISATION_FILE, "w") as a:
	a.write(strINITFILE)

with open(subfolder+'/'+INITIAL_PHENOTYPES_FILE, "w") as b:
	b.write(strPHENFILE)

with open(subfolder+'/'+INITIAL_TECHNOLOGY_FILE, "w") as c:
	c.write(strTECHFILE)

with open(subfolder+'/'+PARAMETER_FILE, "w") as d:
	d.write(strPARAFILE)
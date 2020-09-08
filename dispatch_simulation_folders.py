#import os
import pathlib
import sys
from ast import literal_eval
from launch_multiple_simulations import Launcher

# REMINDER: list of all combinations created by Launcher is a list of **TUPLES**

globalname = str(sys.argv[1])
firstComb = int(sys.argv[2])
lastComb = int(sys.argv[3])

fitparfile = 'pars/fitness_' + globalname + '.txt'
genparfile = 'pars/general_parameters.txt'

try:
	## get the combination filename (if provided, the program assumes the user wants to create / overwrite list)
	combfilename = str(sys.argv[4])

	## Calculate all combinations 
	launch = Launcher(metafolder='../' + globalname + str(firstComb) + '-' + str(lastComb), parfile=fitparfile, launchfile=genparfile)
	launch.readParameterInfo()
	launch.createRanges()
	launch.createCombinations()

	## Save it somewhere
	count = 0
	with open(combfilename, 'w') as f:
		for listitem in launch.combinations:
			f.write('{0}\n'.format(listitem))
			count += 1
			print('writing parameter combination #{0} in file {1}'.format(count, combfilename))

except IndexError as e:
	## (the user did not provide any arguments, the program assumes that the list already exists somewhere)
	combfilename = 'combinationslist.txt' 
	try:
		## Check that file does indeed exist
		assert pathlib.Path(combfilename).exists()

	## Except file does not exist:
	except AssertionError as e:
		### catch error and inform user that file not found
		print("could not find the combination file combinationslist.txt")

finally:
	## Regardless of whether the file had to be created or not, it now exists
	## Read file lines x to y
	desiredRange = range(firstComb, lastComb)
	combinationCollector = []
	with open(combfilename, 'r') as f:
		## For each line, create folder in metafolder (named globalname + 'x-y')
		lineIterator = 0
		for line in f:
			line = f.readline()
			linestr = line.strip('\n')
			lineIterator += 1
			if lineIterator in desiredRange:
				combinationCollector.append(literal_eval(linestr))
			else:
				continue

	## create / overwrite launcher
	launch = Launcher(metafolder='../' + globalname + str(firstComb) + '-' + str(lastComb), parfile=fitparfile, launchfile=genparfile)
	launch.readParameterInfo()
	launch.combinations = combinationCollector
	launch.createFolder(launch.metafolder)
	for comb in launch.combinations:
		launch.writeParameterFilesInFolder(fitfun=launch.fitnessFunction, pname=launch.parname, pval=comb)

print('End of task')
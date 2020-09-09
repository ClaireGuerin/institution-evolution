#import os
import pathlib
import argparse
#import sys
from ast import literal_eval
from launch_multiple_simulations import Launcher

# REMINDER: list of all combinations created by Launcher is a list of **TUPLES**

# Options for the program (action argument):
## 1: just create the list
## 2: just create the folder from the extant list
## 3: both create the list and the folder

parser = argparse.ArgumentParser(description='Create a list of parameter combinations and / or a folder from a sublist.')
# Postional arguments: necessary for all options
parser.add_argument('target', type=str, help='a string containing the target name of the fitness parameter list and the end folder name')
parser.add_argument('action', type=str, help='a string to indicate which action is required of the program: \
	"l" creates a list; \
	"f" creates a folder; \
	"fl" or "lf" create both.')
# Optional arguments: necessary only for options 2 and 3
parser.add_argument('-b', '--boundaries', type=int, nargs=2, default=["",""], \
	help='integers indicating where to start and end the subset of combinations in the list.')

# parse the arguments above
args = parser.parse_args()

fitparfile = 'pars/fitness_' + args.target + '.txt'
genparfile = 'pars/general_parameters.txt'
combinfile = 'combinationslist.txt'
folder = '../{0}{1}-{2}'.format(args.target, args.boundaries[0], args.boundaries[1])

### ACTION ###
if "f" and "l" not in args.action:
	raise NameError(args.action + " is not a valid action argument. Use l, f or both")
else:
	if "l" in args.action:
		### CREATE LIST ###
		# Calculate all combinations 
		launch = Launcher(metafolder=folder, parfile=fitparfile, launchfile=genparfile)
		launch.readParameterInfo()
		launch.createRanges()
		launch.createCombinations()

		## Save them in combinations list file
		count = 0
		with open(combinfile, 'w') as f:
			for listitem in launch.combinations:
				f.write('{0}\n'.format(listitem))
				count += 1
				print('writing parameter combination #{0} in file {1}'.format(count, combinfile))
	if "f" in args.action:
		### CREATE FOLDER ###
		## Regardless of whether the list had to be created or not, it now exists
		## let's ensure that start and end info has been provided
		start = args.boundaries[0]
		end = args.boundaries[1]
		assert start and end is int, "provide a start and end value for the subset of combinations"
		assert start < end, "starting value must be less than end value"
		## Read file lines from start to end of specified range
		desiredRange = range(start, end)
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
		if "l" not in args.action:
			## create launcher if not already done
			launch = Launcher(metafolder=folder, parfile=fitparfile, launchfile=genparfile)
			launch.readParameterInfo()
			launch.combinations = combinationCollector
		launch.createFolder(launch.metafolder)
		for comb in launch.combinations:
			launch.writeParameterFilesInFolder(fitfun=launch.fitnessFunction, pname=launch.parname, pval=comb)
### THE END ###
print('End of task')
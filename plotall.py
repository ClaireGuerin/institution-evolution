import matplotlib.pyplot as plt
from statistics import mean, variance
from math import sqrt
import glob
import csv
import os
import sys
import logging

dirpath = os.getcwd()
time = range(0,10000)

VARIABLES = ('phenotypes','demography')
variableID = int(sys.argv[1])

meanVariable = []
varianceVariable = []
npoints = 9

for i in range(npoints):
	parvalue = (i + 1) / 10
	#fileslist = glob.glob('{0}/res/out-d{1}_{2}.txt'.format(dirpath,parvalue,VARIABLES[variableID]))
	fileslist = glob.glob('/home/claire/Desktop/res/pars3-bign0/out-d{0}_{1}.txt'.format(parvalue,VARIABLES[variableID]))
	
	# FIGURE OF VARIABLE CHANGE OVER TIME FOR 1 SIMULATION RUN
	fig = plt.figure(figsize=(20,10))
	ax1 = fig.add_subplot(111)

	vmean = []
	vvar = []
	print('graph {0}'.format(i))
	
	for simfile in fileslist:
		variable = []

		with open(simfile,'r') as sf:
			res = csv.reader(sf, delimiter=',')
			for row in res:
				variable.append(float(row[0]))
				
		ldiff = len(time) - len(variable)
		if ldiff > 0:
			variable.extend([0]*ldiff)
		
		plt.plot(time,variable, label=simfile)
		vmean.append(mean(variable[9000:-1]))
		vvar.append(variance(variable[9000:-1]))

	plt.xlabel('Generations')
	plt.ylabel(VARIABLES[variableID])
	plt.ylim(0,max(1,max(variable)))
	#plt.ylim(0,1)
	plt.title('Simulation, dispersal={0}'.format(parvalue))
	plt.legend()
	plt.savefig('{0}/res/plot-{2}-d{1}.png'.format(dirpath,parvalue,VARIABLES[variableID]), dpi=300, bbox_inches='tight')
	#plt.show()

	meanVariable.append(mean(vmean))
	varianceVariable.append(mean(vvar))
	print('mean: {0}'.format(mean(vmean)))

plt.close('all') # close all figures before plotting the general figure
	
#GENERAL FIGURE
figG = plt.figure(figsize=(10,10))
axG = figG.add_subplot(111)

x = []
y = []

with open('{0}/analyticalpredictions.txt'.format(dirpath),'r') as csvfile:
	plots = csv.reader(csvfile, delimiter=',')
	for row in plots:
		x.append(float(row[0])) # dispersal rate
		y.append(float(row[1+variableID])) # row 1=phenotype, row2=demography

xerror = [0]*len(varianceVariable)
yerror = [sqrt(i) for i in varianceVariable]

plt.plot(x[0:npoints],y[0:npoints], label='Predictions')
plt.plot(x[0:npoints],meanVariable, label='Simulations')
axG.errorbar(x[0:npoints],meanVariable, xerr=xerror, yerr=yerror, fmt='none')

plt.xlabel('Dispersal')
plt.xlim(0,1)
plt.ylabel(VARIABLES[variableID])
plt.ylim(0,max(1,max(meanVariable)*1.5,max(y)*1.5))
plt.title('Compare results')
plt.legend()
plt.savefig('{0}/res/plot-comparison-{1}.png'.format(dirpath,VARIABLES[variableID]), dpi=300, bbox_inches='tight')
plt.close('all')

print('plots for {0} ready.'.format(VARIABLES[variableID]))
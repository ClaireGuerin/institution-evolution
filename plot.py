import matplotlib.pyplot as plt
from statistics import mean, variance
from math import sqrt
import glob
import csv
import os

dirpath = os.getcwd()
#time = range(0,10000)
targetdir = '/home/claire/Desktop/res/pars3-bign0/'

meancoop = []
varcoop = []

for i in range(9):
	parvalue = (i + 1) / 10
	#fileslist = glob.glob('{0}/res/test/out-d{1}*'.format(dirpath,dispersal))
	fileslist = glob.glob(targetdir+'out-d{0}_demography.txt'.format(parvalue))
	#fileslist = glob.glob('/home/claire/Desktop/pol-demog/rawdat/out-p{0}-[0123456789].txt_d*'.format(parvalue))
	fig = plt.figure(figsize=(20,10))
	ax1 = fig.add_subplot(111)

	dispcoopmean = []
	dispcoopvar = []
	for simfile in fileslist:
		coop = []

		with open(simfile,'r') as sf:
			res = csv.reader(sf, delimiter=',')
			for row in res:
				coop.append(float(row[0]))
		time = range(0,len(coop))
		plt.plot(time,coop, label=simfile)
		filelength = len(coop)
		dispcoopmean.append(mean(coop[filelength-1000:filelength]))
		dispcoopvar.append(variance(coop[filelength-1000:filelength]))

		plt.xlabel('Generations')
		plt.ylabel('Value')
		plt.ylim(0,max(coop))
		plt.title('Simulation, dispersal={0}'.format(parvalue))
		plt.legend()
		plt.savefig('{0}-plot.png'.format(simfile), dpi=300, bbox_inches='tight')
	#plt.show()

	meancoop.append(mean(dispcoopmean))
	varcoop.append(mean(dispcoopvar))

print(meancoop)
print(varcoop)
import matplotlib.pyplot as plt
from statistics import mean, variance
from math import sqrt
import glob
import csv
import os

dirpath = os.getcwd()
time = range(0,10000)

meancoop = []
varcoop = []

for i in range(8):
	parvalue = (i + 1) / 10
#	fileslist = glob.glob('{0}/res/test/out-d{1}*'.format(dirpath,dispersal))
	fileslist = glob.glob('/home/claire/Desktop/pol-demog/rawdat/out-p{0}-[0123456789].txt_d*'.format(parvalue))
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

		plt.plot(time,coop, label=simfile)
		dispcoopmean.append(mean(coop[9000:-1]))
		dispcoopvar.append(variance(coop[9000:-1]))

	plt.xlabel('Generations')
	plt.ylabel('Demography')
	plt.ylim(0,max(coop))
	plt.title('Simulation, policing={0}'.format(parvalue))
	plt.legend()
	plt.savefig('/home/claire/Desktop/pol-demog/figures/plot-demography-p{0}.png'.format(parvalue), dpi=300, bbox_inches='tight')
	#plt.show()

	meancoop.append(mean(dispcoopmean))
	varcoop.append(mean(dispcoopvar))

print(meancoop)
print(varcoop)
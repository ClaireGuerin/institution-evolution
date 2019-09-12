import matplotlib.pyplot as plt
from statistics import mean, variance
from math import sqrt
import glob
import csv
import os

dirpath = os.getcwd()
time = range(0,5000)

meancoop = []
varcoop = []

for i in range(9):
	dispersal = (i + 1) / 10
	fileslist = glob.glob('{0}/res/out-d{1}*'.format(dirpath,dispersal))

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
		dispcoopmean.append(mean(coop[4500:4999]))
		dispcoopvar.append(variance(coop[4500:4999]))

	plt.xlabel('Generations')
	plt.ylabel('Cooperation')
	plt.ylim(0,1)
	plt.title('Simulation, dispersal={0}'.format(dispersal))
	plt.legend()
	plt.savefig('plot-d{0}.png'.format(dispersal), dpi=300, bbox_inches='tight')
	plt.show()

	meancoop.append(mean(dispcoopmean))
	varcoop.append(mean(dispcoopvar))

print(meancoop)
print(varcoop)
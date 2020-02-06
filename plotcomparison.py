import matplotlib.pyplot as plt
from statistics import mean, variance
from math import sqrt
import glob
import csv
import os

dirpath = os.getcwd()

fig2 = plt.figure(figsize=(10,10))
ax2 = fig2.add_subplot(111)

meancoop = [10.395527527527527, 10.336311311311311, 10.144686686686686, 10.376505505505506, 10.250788788788789, 10.339353353353353, 10.07926926926927, 10.26939039039039]
varcoop = [0.11481501050148345, 0.11625390189788988, 0.11968362721438873, 0.11651472368159743, 0.11487569752116847, 0.12079208904295077, 0.11402325842876945, 0.1154559733480976]

x = [(i+1)/10 for i in range(8)]
y = []
#z = []

# with open('/home/claire/institution-evolution/analyticalpredictions.txt','r') as csvfile:
#     plots = csv.reader(csvfile, delimiter=',')
#     for row in plots:
#         x.append(float(row[0])) # dispersal rate
#         y.append(float(row[1])) # cooperation
#         #z.append(float(row[2])) # deme size

xerror = [0]*len(varcoop)
yerror = [sqrt(x) for x in varcoop]

# plt.plot(x,y, label='Predictions')
plt.plot(x,meancoop, label='Simulations')
ax2.errorbar(x,meancoop, xerr=xerror, yerr=yerror, fmt='none')

plt.xlabel('Policing')
plt.xlim(0,1)
plt.ylabel('Demography')
plt.ylim(0,max(meancoop)*1.5)
plt.title('Compare results')
plt.legend()
plt.savefig('/home/claire/Desktop/pol-demog/figures/plot-comparison-demography.png', dpi=300, bbox_inches='tight')
plt.show()
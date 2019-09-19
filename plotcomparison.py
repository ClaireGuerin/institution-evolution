import matplotlib.pyplot as plt
from statistics import mean, variance
from math import sqrt
import glob
import csv
import os

dirpath = os.getcwd()

fig2 = plt.figure(figsize=(10,10))
ax2 = fig2.add_subplot(111)

meancoop = [0.5399798487342802, 0.49572097014039923, 0.4419390736126729, 0.45018719325405476, 0.3937387996223269, 0.43575198971908524, 0.42398154934368976, 0.38670825661381936, 0.3864682191449452]
varcoop = [0.00012708400097636422, 0.00018145909873083866, 0.0001300657737211161, 0.00022490496728090755, 0.0003419391250907176, 0.00015451045782816932, 0.0003494917635666848, 0.00021927794258262272, 0.00018392572703428787]

x = []
y = []
#z = []

with open('/home/claire/institution-evolution/analyticalpredictions.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(float(row[0])) # dispersal rate
        y.append(float(row[1])) # cooperation
        #z.append(float(row[2])) # deme size

xerror = [0]*len(varcoop)
yerror = [sqrt(x) for x in varcoop]

plt.plot(x,y, label='Predictions')
plt.plot(x,meancoop, label='Simulations')
ax2.errorbar(x,meancoop, xerr=xerror, yerr=yerror, fmt='none')

plt.xlabel('Dispersal')
plt.xlim(0,1)
plt.ylabel('Cooperation')
plt.ylim(0,1)
plt.title('Compare results')
plt.legend()
plt.savefig('{0}/res/figures/test/plot-comparison.png'.format(dirpath), dpi=300, bbox_inches='tight')
plt.show()
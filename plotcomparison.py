import matplotlib.pyplot as plt
from statistics import mean, variance
from math import sqrt
import glob
import csv
import os

dirpath = os.getcwd()

fig2 = plt.figure(figsize=(10,10))
ax2 = fig2.add_subplot(111)

meancoop = [0.19770736839982203, 0.19008390893631474, 0.19101502944075835, 0.19851824926401818, 0.1280023626402745, 0.2096386070795548, 0.18480829415825584, 0.1975642269494036, 0.16437057832202367]
varcoop = [0.0003407031410195947, 0.00020384613001037328, 0.000213076381286691, 0.00014923760626115834, 0.00022503047557951937, 0.00012668602394252075, 0.0002037995810953795, 0.00015763935566705757, 0.00023879530514835838]

x = []
y = []
z = []

with open('/home/claire/institution-evolution/analyticalpredictions.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(float(row[0])) # dispersal rate
        y.append(float(row[1])) # cooperation
        z.append(float(row[2])) # deme size

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
plt.savefig('plot-comparison.png', dpi=300, bbox_inches='tight')
plt.show()
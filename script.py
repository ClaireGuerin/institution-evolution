from institutionevolution.population import Population as Pop
from time import perf_counter

# for i in range(9):
# 	dispersal = (i + 1) / 10

# 	for i in range(10):
# 		trial = main.Population()
# 		trial.migrationRate = dispersal
# 		trial.createAndPopulateDemes()

# 		tic = perf_counter()
# 		trial.runSimulation(outputfile="out-d{0}-{1}.txt".format(trial.migrationRate,i))
# 		toc = perf_counter()

# 		print("Ran {0} generations with {1} demes in {2} seconds".format(trial.numberOfGenerations, trial.numberOfDemes, toc - tic))

singlerun = Pop('geom')
singlerun.createAndPopulateDemes
tic = perf_counter()
singlerun.runSimulation(outputfile="out_multipletraits.txt")
toc = perf_counter()

print("Ran {0} generations with {1} demes in {2} seconds".format(singlerun.numberOfGenerations, singlerun.numberOfDemes, toc - tic))
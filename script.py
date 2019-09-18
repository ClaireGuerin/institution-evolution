from institutionevolution.population import Population as Pop
from time import perf_counter

## THIS CODE IS TO TEST DIFFERENT DISPERSAL (MIGRATION) RATES IN RANGE [0,1]
for i in range(9):
	dispersal = (i + 1) / 10

	for i in range(10):
		trial = Pop()
		trial.migrationRate = dispersal
		trial.createAndPopulateDemes()

		tic = perf_counter()
		trial.runSimulation(outputfile="test/out-d{0}-{1}.txt".format(trial.migrationRate,i))
		toc = perf_counter()

		print("Ran {0} generations with {1} demes in {2} seconds".format(trial.numberOfGenerations, trial.numberOfDemes, toc - tic))

#singlerun = Pop()
#singlerun.createAndPopulateDemes()
#tic = perf_counter()
#singlerun.runSimulation(outputfile="outputtest.txt")
#toc = perf_counter()

#print("Ran {0} generations with {1} demes in {2} seconds".format(singlerun.numberOfGenerations, singlerun.numberOfDemes, toc - tic))
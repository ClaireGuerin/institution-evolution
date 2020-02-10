from institutionevolution.population import Population as Pop
from time import perf_counter

# THIS CODE IS TO TEST DIFFERENT PARAMETER VALUES
big_tic = perf_counter()

for parval in range(9):
	policing = (parval + 1) / 10

	# for replicate in range(10):
	# 	trial = Pop()
	# 	trial.fitnessParameters.update({"p": policing})

	# 	tic = perf_counter()
	# 	trial.runSimulation(outputfile="test/out-p{0}-{1}.txt".format(policing,replicate))
	# 	toc = perf_counter()

	# 	print("Ran {0} generations with {1} demes in {2} seconds".format(trial.numberOfGenerations, trial.numberOfDemes, toc - tic))

	population = Pop()
	population.fitnessParameters.update({"p": policing})

	tic = perf_counter()
	population.runSimulation(outputfile="out-p{0}-{1}.txt".format(policing,replicate))
	toc = perf_counter()

big_toc = perf_counter()
print("Ran 9 simulations in {0} seconds".format(big_toc - big_tic))

# # THIS CODE IS TO RUN A SINGLE SIMULATION

# singlerun = Pop("policingdemog")
# tic = perf_counter()
# singlerun.runSimulation(outputfile="outputtestdemog.txt")
# toc = perf_counter()

# print("Ran {0} generations with {1} demes in {2} seconds".format(singlerun.numberOfGenerations, singlerun.numberOfDemes, toc - tic))
from institutionevolution.population import Population as Pop
from time import perf_counter

# THIS CODE IS TO TEST DIFFERENT PARAMETER VALUES
# big_tic = perf_counter()

# for parval in range(9):
# 	policing = (parval + 1) / 10

# 	# for replicate in range(10):
# 	# 	trial = Pop()
# 	# 	trial.fitnessParameters.update({"p": policing})

# 	# 	tic = perf_counter()
# 	# 	trial.runSimulation(outputfile="test/out-p{0}-{1}.txt".format(policing,replicate))
# 	# 	toc = perf_counter()

# 	# 	print("Ran {0} generations with {1} demes in {2} seconds".format(trial.numberOfGenerations, trial.numberOfDemes, toc - tic))

# THIS CODE IS TO RUN A SINGLE SIMULATION

singlerun = Pop("policingdemog2")
tic = perf_counter()
singlerun.runSimulation(outputfile="outputtestdemog.txt")
toc = perf_counter()

print("Ran {0} generations with {1} demes in {2} seconds".format(singlerun.numberOfGenerations, singlerun.numberOfDemes, toc - tic))

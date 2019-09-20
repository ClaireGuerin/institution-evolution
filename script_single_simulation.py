from institutionevolution.population import Population as Pop
from time import perf_counter

# THIS CODE IS TO RUN A SINGLE SIMULATION

singlerun = Pop()
tic = perf_counter()
singlerun.runSimulation(outputfile="outputtest.txt")
toc = perf_counter()

print("Ran {0} generations with {1} demes in {2} seconds".format(singlerun.numberOfGenerations, singlerun.numberOfDemes, toc - tic))
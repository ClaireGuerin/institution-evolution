import main
from time import perf_counter

trial = main.Population()
trial.createAndPopulateDemes()

tic = perf_counter()
trial.runSimulation()
toc = perf_counter()

print("Ran {0} generations with {1} demes in {2} seconds".format(trial.numberOfGenerations, trial.numberOfDemes, toc - tic))
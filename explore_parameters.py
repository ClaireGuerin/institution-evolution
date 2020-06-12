from institutionevolution.population import Population as Pop
from itertools import product as prod
import multiprocessing as mp
import sys

# DEFINE FUNCTION TO RUN SINGLE SIMULATION BASED ON PARS COMBINATION

inst_FOLDER = str(sys.argv[1])

def single_simulation_run(parameter_combination):
	population = Pop('policingdemog2', inst_FOLDER)
	population.fitnessParameters.update({"rb": parameter_combination[0], 
		"c1": parameter_combination[1], 
		"bb": parameter_combination[2], 
		"pp": parameter_combination[3], 
		"p": parameter_combination[4]})
	population.runSimulation(outputfile="out-pars{0}".format(parameter_combination))



rb = range(10,50,10)
c1 = [x * 0.1 for x in range(2,100,20)]
bb = range(10,100,20)
pp = [x * 0.1 for x in range(5,100,20)]
p = [x * 0.1 for x in range(1,9,2)]

all_parameter_combinations = prod(*[rb,c1,bb,pp,p])

pool = mp.Pool(mp.cpu_count())
res = pool.map(single_simulation_run, all_parameter_combinations)
pool.close()

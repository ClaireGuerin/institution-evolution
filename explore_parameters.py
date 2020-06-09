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
		"p"}: parameter_combination[4])
	population.runSimulation(outputfile="out-d{0}".format(migrationRate))



rb = range(10,50,10)
c1 = range(0.2,10,2)
bb = range(10,100,20)
pp = range(0.5,10,2)
p = range(0.1,0.9,0.2)

all_parameter_combinations = prod(*[rb,c1,bb,pp,p])

pool = mp.Pool(mp.cpu_count())
res = pool.map(single_simulation_run, all_parameter_combinations)
pool.close()

from institutionevolution.population import Population as Pop
import multiprocessing as mp

def single_simulation_run(migrationRateIndex):
	migrationRate = (migrationRateIndex + 1) / 10
	population = Pop('policingdemog2')
	population.migrationRate = migrationRate
	population.runSimulation(outputfile="out-d{0}.txt".format(migrationRate))

pool = mp.Pool(mp.cpu_count())
res = pool.map(single_simulation_run, [i for i in range(9)])
pool.close()
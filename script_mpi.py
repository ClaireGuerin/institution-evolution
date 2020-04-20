from institutionevolution.population import Population as Pop
import multiprocessing as mp

inst_FOLDER = ''

def single_simulation_run(migrationRateIndex):
	migrationRate = (migrationRateIndex + 1) / 10
	population = Pop('policingdemog2',inst_FOLDER)
	population.migrationRate = migrationRate
	population.runSimulation(outputfile="out-d{0}".format(migrationRate))

pool = mp.Pool(mp.cpu_count())
res = pool.map(single_simulation_run, [i for i in range(9)])
pool.close()
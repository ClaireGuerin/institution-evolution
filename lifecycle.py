from main import Population as pop
import random as rd

class runOneCycle(object):
	
	def __init__(self):
		self.population = pop()
	
	def migration(self, individual):
		migrate = np.random.choice([0,1],1,True,[1-dispersalRate,dispersalRate]) #true stands for replacementself.population.migrationProbability
		### USE RANDOM here instead!!!
		if random.randint(0,100) < 36:
    do_stuff()
		
		if migrate:
			pass
			
	
	def reproduction(self):
		pass
	
	def mutation(self):
		pass
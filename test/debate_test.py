import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop

class TestDebateFeature(object):

	def test_individuals_invest_time_into_debate(self):
		self.ind = Ind()
		assert hasattr(self.ind, "consensusTime"), "the individual does not have time for debate"

	def test_deme_has_consensus(self):
		self.deme = Dem()
		assert "consensus" in self.deme.progressValues, "the deme cannot reach consensus"
		assert "consensusTime" in self.deme.progressValues, "reaching consensus does not take any time"

	def test_debate_fitness_function_exists(self, getFitnessParameters):
		self.ind = Ind()
		self.ind.neighbours = [0]
		pars = getFitnessParameters('debate')

		try:
			self.ind.reproduce('debate', **pars)
		except ValueError as e:
			assert False, "include a debate function"

	def test_consensus_is_aggregate_of_opinions(self):
		self.pop = Pop(inst='test')
		self.pop.fit_fun = 'debate'
		self.pop.initialPhenotypes = [0.1,0.2,0.3,0.4]
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 2
		self.pop.mutationRate = 0
		self.pop.migrationRate = 0

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updateDemeInfo()

		for deme in self.pop.demes:
			assert deme.progressValues["consensus"] == 0.3, "wrong consensus value"

	def test_consensus_takes_time_to_reach(self):
		self.pop = Pop(inst='test')
		self.pop.fit_fun = 'debate'
		self.pop.initialPhenotypes = [0.1,0.2,0.3,0.4]
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 2
		self.pop.mutationRate = 0
		self.pop.migrationRate = 0

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updateDemeInfo()

		for deme in self.pop.demes:
			assert deme.progressValues["consensusTime"] is not None, "consensus reaching time has not been calculated"
			assert deme.progressValues["consensusTime"] > 0, "consensus reaching should take a bare minimum of time"
			disagreement = self.pop.fitnessParameters["aconsensus"] * deme.demography * deme.varPhenotypes[2]
			assert deme.progressValues["consensusTime"] == self.pop.fitnessParameters["epsilon"] + disagreement / (self.pop.fitnessParameters["bconsensus"] + disagreement)

	def test_consensus_time_affects_individual_time_for_production(self):
		self.pop = Pop(inst='test')
		self.pop.fit_fun = 'debate'
		self.pop.initialPhenotypes = [0.1,0.2,0.3,0.4]
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 2
		self.pop.mutationRate = 0

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updateDemeInfo()
		self.pop.populationReproduction()

		for ind in self.pop.parents:
			assert ind.consensusTime is not None, "no consensus time given"
			assert ind.consensusTime == self.pop.demes[ind.currentDeme].progressValues["consensusTime"], "wrong individual consensus time"
			assert ind.productionTime == 1 - ind.consensusTime, "wrong individual production time"

	def test_consensus_value_defines_policing_amount(self):
		self.pop = Pop(inst='test')
		self.pop.fit_fun = 'debate'
		self.pop.initialPhenotypes = [0.1,0.2,0.3,0.4]
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 2
		self.pop.mutationRate = 0
		self.pop.migrationRate = 0

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updateDemeInfo()

		allres = [0] * self.pop.numberOfDemes
		for ind in self.pop.individuals:
			allres[ind.currentDeme] += ind.resourcesAmount

		for deme in self.pop.demes:
			assert deme.progressValues["institutionQuality"] is not None
			assert deme.progressValues["institutionQuality"] == (deme.progressValues['consensus'] * deme.publicGood * self.pop.fitnessParameters['aquality'] / allres[deme.id]) ** self.pop.fitnessParameters['alphaquality']
			assert deme.progressValues["fineBudget"] is not None
			assert deme.progressValues["fineBudget"] == deme.progressValues['consensus'] * deme.publicGood * (1 - self.pop.fitnessParameters['aquality'])

	def test_individual_consensus_time_always_less_than_one(self):
		self.pop = Pop(inst='test')
		self.pop.fit_fun = 'debate'
		self.pop.initialPhenotypes = [0.1,0.2,0.3,0.4]
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 2
		self.pop.mutationRate = 0
		self.pop.migrationRate = 0

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updateDemeInfo()

		for deme in self.pop.demes:
			assert deme.progressValues['consensusTime'] < 1, "epsilon is {2} so asymptote should be: {1}. variance in opinions: {0}".format(deme.varPhenotypes[2], self.pop.fitnessParameters['epsilon']+1, self.pop.fitnessParameters['epsilon'])
import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop

class TestDebateFeature(object):

	def test_individuals_invest_time_into_debate(self):
		self.ind = Ind()
		assert hasattr(self.ind, "debateTime"), "the individual does not have time for debate"

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
		self.pop = Pop()
		self.pop.fit_fun = 'debate'
		self.pop.initialPhenotypes = [0.1,0.2,0.3,0.4]
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 2
		self.pop.mutationRate = 0
		self.pop.migrationRate = 0

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.update()

		for deme in self.pop.demes:
			assert deme.progressValues["consensus"] == 0.3, "wrong consensus value"

	def test_consensus_takes_time_to_reach(self):
		self.pop = Pop()
		self.pop.fit_fun = 'debate'
		self.pop.initialPhenotypes = [0.1,0.2,0.3,0.4]
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 2
		self.pop.mutationRate = 0

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.update()

		for deme in self.pop.demes:
			assert deme.progressValues["consensusTime"] is not None, "consensus reaching time has not been calculated"
			assert deme.progressValues["consensusTime"] > 0, "consensus reaching should take a bare minimum of time"
			disagreement = self.pop.fitnessParameters["aconsensus"] * deme.demography * deme.varPhenotypes[2]
			assert deme.progressValues["consensusTime"] == self.pop.fitnessParameters["epsilon"] + disagreement / (1 + disagreement)

	def test_consensus_time_affects_individual_time_for_production(self):
		assert False, "write this test!"

	def test_consensus_value_defines_policing_amount(self):
		assert False, "write this test!"
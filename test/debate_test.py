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
		assert "consensus" in self.deme.politicsValues, "the deme cannot reach consensus"
		assert "consensusTime" in self.deme.politicsValues, "reaching consensus does not take any time"

	def test_debate_fitness_function_exists(self, getFitnessParameters):
		self.ind = Ind()
		self.ind.neighbours = [0]
		self.ind.resourcesAmount = 10
		pars = getFitnessParameters('debate')

		try:
			self.ind.reproduce('debate', **{**{'productivity': 0.6},**pars})
		except ValueError as e:
			assert False, "include a debate function"

	def test_consensus_is_aggregate_of_opinions(self):
		self.pop = Pop(inst='test/test')
		self.pop.fit_fun = 'debate'
		self.pop.initialPhenotypes = [0.1,0.2,0.3,0.4]
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 2
		self.pop.mutationRate = 0
		self.pop.migrationRate = 0

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updateDemeInfoPreProduction()

		for deme in self.pop.demes:
			assert deme.politicsValues["consensus"] == 0.3, "wrong consensus value"

	def test_consensus_takes_time_to_reach(self):
		self.pop = Pop(inst='test/test')
		self.pop.fit_fun = 'debate'
		self.pop.initialPhenotypes = [0.1,0.2,0.3,0.4]
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 2
		self.pop.mutationRate = 0
		self.pop.migrationRate = 0

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updateDemeInfoPreProduction()

		for deme in self.pop.demes:
			assert deme.politicsValues["consensusTime"] is not None, "consensus reaching time has not been calculated"
			assert deme.politicsValues["consensusTime"] > 0, "consensus reaching should take a bare minimum of time"
			disagreement = self.pop.fitnessParameters["aconsensus"] * deme.demography * deme.varPhenotypes[2]
			assert deme.politicsValues["consensusTime"] == self.pop.fitnessParameters["epsilon"] + disagreement / (self.pop.fitnessParameters["bconsensus"] + disagreement)

	def test_consensus_time_affects_individual_time_for_production(self):
		self.pop = Pop(inst='test/test')
		self.pop.fit_fun = 'debate'
		self.pop.initialPhenotypes = [0.1,0.2,0.3,0.4]
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 2
		self.pop.mutationRate = 0
		self.pop.migrationRate = 0

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updateDemeInfoPreProduction()

		for deme in self.pop.demes:
			assert "productionTime" in deme.politicsValues, deme.politicsValues
			assert deme.politicsValues["productionTime"] == 1 - deme.politicsValues["consensusTime"] , "wrong individual production time"

	def test_consensus_value_defines_policing_amount(self):
		self.pop = Pop(inst='test/test')
		self.pop.fit_fun = 'debate'
		self.pop.initialPhenotypes = [0.1,0.2,0.3,0.4]
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 2
		self.pop.mutationRate = 0
		self.pop.migrationRate = 0

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updateDemeInfoPreProduction()
		self.pop.populationProduction()
		self.pop.updateDemeInfoPostProduction()

		allres = [0] * self.pop.numberOfDemes
		for ind in self.pop.individuals:
			allres[ind.currentDeme] += ind.resourcesAmount

		for deme in self.pop.demes:
			assert deme.progressValues["institutionQuality"] is not None
			assert deme.progressValues["institutionQuality"] == (deme.politicsValues['consensus'] * deme.publicGood * self.pop.fitnessParameters['aquality'] / allres[deme.id]) ** self.pop.fitnessParameters['alphaquality']
			assert deme.progressValues["fineBudget"] is not None
			assert deme.progressValues["fineBudget"] == deme.politicsValues['consensus'] * deme.publicGood * (1 - self.pop.fitnessParameters['aquality'])

	def test_individual_consensus_time_always_less_than_one(self):
		self.pop = Pop(inst='test/test')
		self.pop.fit_fun = 'debate'
		self.pop.initialPhenotypes = [0.1,0.2,0.3,0.4]
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 2
		self.pop.mutationRate = 0
		self.pop.migrationRate = 0

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updateDemeInfoPreProduction()

		for deme in self.pop.demes:
			assert deme.politicsValues['consensusTime'] < 1, "epsilon is {2} so asymptote should be: {1}. variance in opinions: {0}".format(deme.varPhenotypes[2], self.pop.fitnessParameters['epsilon']+1, self.pop.fitnessParameters['epsilon'])

	def test_production_depends_on_debate_time(self, getFitnessParameters):
		fitfun = 'debate'
		pars = getFitnessParameters(fitfun)
		self.firstInd = Ind()
		self.firstInd.produceResources(fitfun, **{**{'productionTime':0.8},**pars})

		self.secndInd = Ind()
		self.secndInd.produceResources(fitfun, **{**{'productionTime':0.2},**pars})

		assert self.firstInd.resourcesAmount > self.secndInd.resourcesAmount, "Individual with {0}% production time should get more resources than individual with {1}%".format(self.firstInd.productionTime*100, self.secndInd.productionTime*100)

	def test_fitness_depends_on_debate_time(self, getFitnessParameters):
		fitfun = 'debate'
		pars = getFitnessParameters(fitfun)
		self.firstInd = Ind()
		self.firstInd.neighbours = [1,2]
		self.firstInd.produceResources(fitfun, **{**{'productionTime':0.8},**pars})
		self.firstInd.reproduce(fitfun, **pars)

		self.secndInd = Ind()
		self.secndInd.neighbours = [1,2]
		self.secndInd.produceResources(fitfun, **{**{'productionTime':0.2},**pars})
		self.secndInd.reproduce(fitfun, **pars)

		assert self.firstInd.fertilityValue > self.secndInd.fertilityValue, "Individual with {0}% production time should have higher fitness than individual with {1}%".format(self.firstInd.productionTime*100, self.secndInd.productionTime*100)
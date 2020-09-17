import pytest
from random import random as rdreal
import institutionevolution.fitness as fitness
import institutionevolution.progress as progress
import institutionevolution.politics as politics
from institutionevolution.individual import Individual as Ind
from institutionevolution.population import Population as Pop
from institutionevolution.deme import Deme as Dem
import institutionevolution.myarithmetics as ar

class TestFullModel(object):

	def test_full_model_fitness_function_exists(self):
		funcdict = fitness.functions
		assert 'full' in funcdict, "missing fitness function for full model"

	def test_individual_can_reproduce_correctly(self, getFitnessParameters):
		fitpars = getFitnessParameters("full")
		indiv = Ind()
		indiv.neighbours = [1,2,3]

		try:
			indiv.reproduce("full", **fitpars)
			assert indiv.fertilityValue is not None
			assert type(indiv.fertilityValue) is float
			assert indiv.fertilityValue > 0
			assert indiv.offspringNumber is not None
			assert type(indiv.offspringNumber) is int
			assert indiv.offspringNumber >= 0
		except Exception as e:
			assert False, str(e)

	def test_full_model_progress_function_exists(self):
		progressdict = progress.functions
		assert 'full' in progressdict, "missing progress function for full model"

	def test_full_model_politics_function_exists(self):
		politicsdict = politics.functions
		assert 'full' in politicsdict, "missing politics function for full model"

	def test_all_phenotypes_are_provided(self, getFitnessParameters):
		self.fakepop = Pop(fit_fun="full", inst="test/test")
		assert len(self.fakepop.initialPhenotypes) == 4

		pars = getFitnessParameters('full')
		assert len(pars['x']) == 4
		assert len(pars['xmean']) == 4

	def test_elections_take_place_in_demes(self, runElections):
		# set leader proportion to 1
		# set mutation rate to 0
		# execute population step up to pre-tech update
		# check that all individuals are leaders
		# do the same for leader proportion of 0.5 and 1

		allleaders = runElections(1)
		for indiv in allleaders:
			assert indiv.leader, "all individuals should be leaders!"

		noleaders = runElections(0)
		for indiv in noleaders:
			assert not indiv.leader, "no individual should be a leader!"

		expectedProportion = rdreal()
		halfleaders = runElections(prop=expectedProportion, d=100, s=100)
		nLeaders = 0
		nIndivs = len(halfleaders)
		for indiv in halfleaders:
			nLeaders += indiv.leader

		assert pytest.approx(nLeaders, abs=100) == expectedProportion * nIndivs, \
		"there should be {0} perc. leaders, instead there is {1}".format(expectedProportion, nLeaders/nIndivs)

	def test_mean_deme_phenotype_determines_leader_number(self):
		#NB: opinion on leadership is a phenotype, stored in 4th position (i.e. index 3 in python) 
		self.fakepop = Pop(fit_fun="full", inst="test/test")
		self.fakepop.numberOfDemes = 10
		self.fakepop.initialDemeSize = 1000
		self.fakepop.mutationRate = 1
		self.fakepop.mutationStep = 0.15
		self.fakepop.initialPhenotypes = [0.5] * 4

		self.fakepop.createAndPopulateDemes()

		for i in range(10):
			# have a good shuffling of things and allow mutations to introduce great variety
			self.fakepop.clearDemeInfo()
			self.fakepop.populationMutationMigration()
		
		self.fakepop.updateDemeInfoPreProduction()

		collectCommoners = []
		leadersCount = [0] * self.fakepop.numberOfDemes
		commonersCount = [0] * self.fakepop.numberOfDemes
		individualsCount = [0] * self.fakepop.numberOfDemes
		for ind in self.fakepop.individuals:
			collectCommoners.append(not ind.leader)
			leadersCount[ind.currentDeme] += ind.leader
			commonersCount[ind.currentDeme] += not ind.leader
			individualsCount[ind.currentDeme] += 1

		assert any(collectCommoners), "there is no commoner at all"
		assert any([x - y for (x,y) in zip(individualsCount,commonersCount)]), "as many commoners as indivs in each deme!"
		assert any([x - y for (x,y) in zip(individualsCount,leadersCount)]), "as many leaders as indivs in each deme!"

		for deme in range(self.fakepop.numberOfDemes):
			demeMean = self.fakepop.demes[deme].meanPhenotypes[3]
			assert leadersCount[deme] == pytest.approx(individualsCount[deme] * demeMean, abs=100), \
			"mean opinion is {0}, when rendered proportion of leaders is {1}".format(demeMean, \
				leadersCount[deme] / individualsCount[deme])

	def test_consensus_is_mean_opinion_when_no_leaders(self):
		#NB: opinion on policing vs R&D is a phenotype, stored in 3rd position (i.e. index 2 in python)
		self.fakepop = Pop(fit_fun="full", inst="test/test")
		self.fakepop.initialPhenotypes = [0.2] * 4
		self.fakepop.initialDemeSize = 100
		self.fakepop.numberOfDemes = 10

		self.fakepop.createAndPopulateDemes()
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()
		self.fakepop.updateDemeInfoPreProduction()

		collectVotes = [0] * self.fakepop.numberOfDemes

		for indiv in self.fakepop.individuals:
			collectVotes[indiv.currentDeme] += indiv.phenotypicValues[2]

		for deme in self.fakepop.demes:
			expectedMean = collectVotes[deme.id] / deme.demography
			assert expectedMean == pytest.approx(deme.politicsValues['consensus'], abs=1.0e-10), "wrong proportion of policing!"

	def test_i_am_sane_and_can_sum_squares(self):
		# simple vector, sort of equivalent to a single phenotype
		self.somevector = [1,2,3,4,5,6,7,8,9]
		self.somevectorsquared = [1,4,9,16,25,36,49,64,81]

		assert self.somevectorsquared == [x * x for x in self.somevector], "what is this list comprehension doing??"

		self.somesquaressummed = 285

		assert self.somesquaressummed == sum(self.somevectorsquared), "what is this sum function doing??"

		self.mySumSquare = 0
		self.mySumMultip = 0
		for i in self.somevector:
			self.mySumSquare += i **2
			self.mySumMultip += i * i

		assert self.mySumMultip == self.mySumSquare, "why are they not the same??"
		assert self.mySumMultip == self.somesquaressummed, "why are they not the same??"
		assert self.mySumSquare == self.somesquaressummed, "why are they not the same??"

		# list of lists, equivalent to three individuals, two phenotypes
		self.phen = [[1,2],[3,4],[5,6]]
		self.phenSquared = [[1,4],[9,16],[25,36]]

		sumofsq = [0,0]
		for phenpair in self.phen:
			for phen in range(2):
				sumofsq[phen] += phenpair[phen] * phenpair[phen]

		assert sumofsq == [35,56], "why????"


	def test_deme_phen_sum_of_square_correct(self):
		self.fakepop = Pop(fit_fun="full", inst="test/test")
		self.fakepop.initialPhenotypes = [0.5] * 4
		self.fakepop.initialDemeSize = 10
		self.fakepop.numberOfDemes = 3
		self.fakepop.mutationRate = 0
		self.fakepop.migrationRate = 0.5

		self.fakepop.createAndPopulateDemes()
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()

		# could the error come from the fakepop registered phenotype number?
		assert self.fakepop.numberOfPhenotypes == 4, "you need to update the number of phenotypes in your tests"

		# collect individual phenotypes BY DEME:
		deme1Phenotypes = []
		deme2Phenotypes = []
		deme3Phenotypes = []
		deme1Squares = []
		deme2Squares = []
		deme3Squares = []

		for indiv in self.fakepop.individuals:
			if indiv.currentDeme == 0:
				deme1Phenotypes.append(indiv.phenotypicValues)
				deme1Squares.append([x * x for x in indiv.phenotypicValues])
			elif indiv.currentDeme == 1:
				deme2Phenotypes.append(indiv.phenotypicValues)
				deme2Squares.append([x * x for x in indiv.phenotypicValues])
			else:
				deme3Phenotypes.append(indiv.phenotypicValues)
				deme3Squares.append([x * x for x in indiv.phenotypicValues])

		assert len(deme1Phenotypes) == self.fakepop.demes[0].demography
		assert len(deme2Phenotypes) == self.fakepop.demes[1].demography
		assert len(deme3Phenotypes) == self.fakepop.demes[2].demography

		alldemePhens = [deme1Phenotypes, deme2Phenotypes, deme3Phenotypes]
		alldemeSqrs = [deme1Squares, deme2Squares, deme3Squares]

		for deme in range(3):
			phen = alldemePhens[deme]
			sqrs = alldemeSqrs[deme]
			addSquares = [0] * 4
			for ind in range(len(phen)):
				for pheno in range(4):
					assert phen[ind][pheno] ** 2 == sqrs[ind][pheno]
					addSquares[pheno] += sqrs[ind][pheno]
			assert addSquares == [0.25 * len(phen)] * 4, len(phen)

		# repeat method from population code
		totalPhenSq = [[0] * 4 for i in range(self.fakepop.numberOfDemes)]
		demeSizes = [0] * self.fakepop.numberOfDemes

		for ind in self.fakepop.individuals:
			demeSizes[ind.currentDeme] += 1
			for phen in range(4):
				totalPhenSq[ind.currentDeme][phen] += (ind.phenotypicValues[phen] * ind.phenotypicValues[phen])

		# check that squares are 0.25 * deme size
		for deme in self.fakepop.demes:
			assert totalPhenSq[deme.id] == deme.totalPhenotypeSquares, "same method, different results. expected:{0}".format([0.25 * deme.demography] * 4)
			assert totalPhenSq[deme.id] == [0.25 * deme.demography] * 4, "the method is wrong"
			assert all([x / deme.demography == 0.25 for x in totalPhenSq[deme.id]]), "phen={0}, n={1}".format(totalPhenSq, deme.demography)
			assert deme.totalPhenotypeSquares == [0.25 * deme.demography] * 4, "there is a problem in the square sum, n={0}".format(deme.demography)
			assert demeSizes[deme.id] == deme.demography, "wrong deme size"

			# THE TESTS BELOW ONLY PASS IF MIGRATION RATE = 0
			if self.fakepop.migrationRate == 0:
				assert totalPhenSq[deme.id] == [2.5] * 4, "the method is wrong"
				assert deme.totalPhenotypeSquares == [2.5] * 4, "there is a problem in the square sum, n={0}".format(deme.demography)

	def test_global_consensus_time_is_correct_regardless_of_leaders(self):
		self.fakepop = Pop(fit_fun="full", inst="test/test")
		self.fakepop.initialPhenotypes = [0.2] * 4
		self.fakepop.initialDemeSize = 100
		self.fakepop.numberOfDemes = 10

		self.fakepop.createAndPopulateDemes()
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()
		self.fakepop.updateDemeInfoPreProduction()

		# consensus time (when everyone is a commoner) is 
		# aConsensus * n * var(z) / (bConsensus + aConsensus * n * var(z)) + epsilon
		acons = self.fakepop.fitnessParameters["aconsensus"]
		bcons = self.fakepop.fitnessParameters["bconsensus"]
		epsil = self.fakepop.fitnessParameters["epsilon"]

		for deme in self.fakepop.demes:
			opinions = [ind.phenotypicValues[2] for ind in self.fakepop.individuals if ind.currentDeme == deme.id]
			assert sum([x * x for x in opinions]) == deme.totalPhenotypeSquares[2], "wrong phenotype squares"

			var = ar.specialvariance(sum(opinions), sum([x * x for x in opinions]), len(opinions))
			assert var == deme.varPhenotypes[2], "wrong variance calculation"
			
			opinionBreadth = deme.demography * var
			expectedTime = epsil + (acons * opinionBreadth) / (bcons + acons * opinionBreadth)
			assert deme.politicsValues["consensusTime"] == pytest.approx(expectedTime), "wrong time to reach consensus"

	def test_leader_cooperation_influences_individual_production_time(self):
		self.fakepop = Pop(fit_fun="full", inst="test/test")
		self.fakepop.initialPhenotypes = [0.2] * 4
		self.fakepop.initialDemeSize = 100
		self.fakepop.numberOfDemes = 10
		self.fakepop.mutationRate = 0.5
		self.fakepop.mutationStep = 0.2

		self.fakepop.createAndPopulateDemes()
		self.fakepop.clearDemeInfo()
		# good shuffling and mutating:
		for i in range(10):
			self.fakepop.populationMutationMigration()
		self.fakepop.updateDemeInfoPreProduction()

		for deme in self.fakepop.demes:
			assert deme.technologyLevel > 0
			assert (deme.demography - deme.totalConsensusContributions) > 0

		self.fakepop.populationProduction()
		# Rig = (1 - Tig) * SUM(1 - Tjg) ** (- alphaResources) * tech ** alphaResources

		aRes = self.fakepop.fitnessParameters["alphaResources"]
		
		for ind in self.fakepop.individuals:
			n = self.fakepop.demes[ind.currentDeme].demography
			assert self.fakepop.demes[ind.currentDeme].totalConsensusContributions is not None, self.fakepop.demes[ind.currentDeme].totalConsensusContributions
			assert self.fakepop.demes[ind.currentDeme].meanLeaderContribution is not None
			cons = self.fakepop.demes[ind.currentDeme].politicsValues['consensusTime']
			t = self.fakepop.demes[ind.currentDeme].totalConsensusContributions * cons
			tech = self.fakepop.demes[ind.currentDeme].technologyLevel
			# WHAT THE PRODUCTION FUNCTION DOES:
			contrib = ind.phenotypicValues[1] if ind.leader else (1 - self.fakepop.demes[ind.currentDeme].meanLeaderContribution)
			resourcesProduced = (1 - contrib * cons) * (n - t) ** (-aRes) * (tech ** aRes)
	
			if ind.leader:
				# LEADERS PRODUCTION TIME DECREASES WITH OWN TIME COOPERATION
				status = 'Leader'
				ctime = ind.phenotypicValues[1] * cons
			else:
				# COMMONERS PRODUCTION TIME DECREASES WITH AVERAGE LEADER TIME COOPERATION
				status = 'Commoner'
				ctime = (1 - self.fakepop.demes[ind.currentDeme].meanLeaderContribution) * cons
			assert (1 - ctime) == (1 - contrib * cons)
			expectedResources = (1 - ctime) * ((n - t) ** (-aRes)) * (tech ** aRes)
			assert resourcesProduced == expectedResources, "same method, different result"
			assert ind.resourcesAmount == expectedResources, "wrong production time. {0} produced {1} instead of {2}".format(status, ind.resourcesAmount, expectedResources)

	def test_leader_cooperation_increases_producer_production_but_decreases_own(self):
		self.fakepop = Pop(fit_fun="full", inst="test/test")
		self.fakepop.initialPhenotypes = [0.2] * 4
		self.fakepop.initialDemeSize = 100
		self.fakepop.numberOfDemes = 10
		self.fakepop.mutationRate = 0.5
		self.fakepop.mutationStep = 0.2

		self.fakepop.createAndPopulateDemes()
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()
		self.fakepop.updateDemeInfoPreProduction()

		for ind in self.fakepop.individuals:
			ind.phenotypicValues[1] = 0

		# LOW LEADER CONTRIBUTION
		for deme in self.fakepop.demes:
			deme.meanLeaderContribution = 0
			deme.totalConsensusContributions = deme.demography - deme.numberOfLeaders

		self.fakepop.populationProduction()

		lowCommoners = []
		lowLeaders = []
		for ind in self.fakepop.individuals:
			if ind.leader:
				lowLeaders.append(ind.resourcesAmount)
			else:
				lowCommoners.append(ind.resourcesAmount)

		# HIGH LEADER CONTRIBUTION
		for deme in self.fakepop.demes:
			deme.meanLeaderContribution = 1
			deme.totalConsensusContributions = deme.numberOfLeaders

		self.fakepop.populationProduction()

		highCommoners = []
		highLeaders = []
		for ind in self.fakepop.individuals:
			if ind.leader:
				highLeaders.append(ind.resourcesAmount)
			else:
				highCommoners.append(ind.resourcesAmount)

		assert ar.specialmean(lowCommoners) < ar.specialmean(highCommoners), "commoners should produce less when low leader contribution"
		assert ar.specialmean(lowLeaders) > ar.specialmean(highLeaders), "leaders should produce more when they contribute less"

	def test_producer_time_cooperation_does_not_influence_production_time(self):
		self.fakepop = Pop(fit_fun="full", inst="test/test")
		self.fakepop.initialPhenotypes = [0.2] * 4
		self.fakepop.initialDemeSize = 100
		self.fakepop.numberOfDemes = 10
		self.fakepop.mutationRate = 0
		self.fakepop.mutationStep = 0

		self.fakepop.createAndPopulateDemes()
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()
		self.fakepop.updateDemeInfoPreProduction()

		# LOW COMMONER COOPERATION
		for ind in self.fakepop.individuals:
			if ind.leader:
				ind.phenotypicValues[1] = 0.5
			else:
				ind.phenotypicValues[1] = 0

		for deme in self.fakepop.demes:
			deme.meanLeaderContribution = 0.5
			deme.totalConsensusContributions = deme.demography * 0.5

		self.fakepop.populationProduction()

		low = []
		for ind in self.fakepop.individuals:
			low.append(ind.resourcesAmount)
		
		# HIGH COMMONER COOPERATION
		for ind in self.fakepop.individuals:
			if ind.leader:
				ind.phenotypicValues[1] = 0.5
			else:
				ind.phenotypicValues[1] = 1

		for deme in self.fakepop.demes:
			deme.meanLeaderContribution = 0.5
			deme.totalConsensusContributions = deme.demography * 0.5

		self.fakepop.populationProduction()

		high = []
		for ind in self.fakepop.individuals:
			high.append(ind.resourcesAmount)

		assert low == high

	def test_consensus_result_depends_on_leadership(self):
		self.fakepop = Pop(fit_fun="full", inst="test/test")
		self.fakepop.initialPhenotypes = [0.2] * 4
		self.fakepop.initialDemeSize = 100
		self.fakepop.numberOfDemes = 10
		self.fakepop.mutationRate = 0
		self.fakepop.mutationStep = 0

		self.fakepop.createAndPopulateDemes()
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()
		self.fakepop.updateDemeInfoPreProduction()

		sumVotes = [0] * self.fakepop.numberOfDemes
		sumWeights = [0] * self.fakepop.numberOfDemes
		for ind in self.fakepop.individuals:
			weight = ind.phenotypicValues[1] if ind.leader else (1 - self.fakepop.demes[ind.currentDeme].meanLeaderContribution)
			sumVotes[ind.currentDeme] += ind.phenotypicValues[2] * weight
			sumWeights[ind.currentDeme] += weight

		for deme in self.fakepop.demes:
			expectedConsensusValue = sumVotes[deme.id] / sumWeights[deme.id]
			assert deme.politicsValues['consensus'] == pytest.approx(expectedConsensusValue, abs=1.0e-10)

		## TO DO IN POP:
		## sum([v * w for v, w in values, weights] / sum(weights))

	def test_consensus_time_depends_on_leadership(self):
		assert False, "write this test!"

	def test_individuals_produce_resources_depending_on_status(self):
		assert False, "write this test!"

	def test_individuals_produce_resources_depending_on_consensus_time(self):
		assert False, "write this test!"

	def test_only_producers_have_economic_cooperation_level(self):
		assert False, "write this test!"

	def test_public_good_game_takes_place_and_pg_is_gathered(self):
		assert False, "write this test!"

	def test_producers_cooperation_influences_public_good(self):
		assert False, "write this test!"

	def test_leaders_cooperation_does_not_influence_public_good(self):
		assert False, "write this test!"

	def test_policing_takes_place_in_demes(self):
		assert False, "write this test!"

	def test_policing_corresponds_to_consensus(self):
		assert False, "write this test!"

	def test_producers_who_cheat_are_punished(self):
		assert False, "write this test!"

	def test_leaders_who_cheat_are_punished(self):
		assert False, "write this test!"

	def test_technology_level_increases_at_next_gen(self):
		assert False, "write this test!"

	def test_taxes_are_applied(self):
		assert False, "write this test!"

	def test_final_individual_fertility_is_correct(self):
		assert False, "write this test!"
import pytest
from random import random as rdreal
import institutionevolution.fitness as fitness
import institutionevolution.progress as progress
import institutionevolution.politics as politics
from institutionevolution.individual import Individual as Ind
from institutionevolution.population import Population as Pop

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

		assert pytest.approx(nLeaders, abs=60) == expectedProportion * nIndivs, \
		"there should be {0} perc. leaders, instead there is {1}".format(expectedProportion, nLeaders/nIndivs)

	def test_mean_deme_phenotype_determines_leader_number(self):
		#NB: opinion on leadership is a phenotype, stored in 4th position (i.e. index 3 in python) 
		self.fakepop = Pop(fit_fun="full", inst="test/test")
		self.fakepop.numberOfDemes = 100
		self.fakepop.initialDemeSize = 100
		self.fakepop.mutationRate = 1
		self.fakepop.mutationStep = 0.15
		self.fakepop.initialPhenotypes = [0.5] * 4

		self.fakepop.createAndPopulateDemes()

		for i in range(10):
			# have a good shuffling of things and allow mutations to introduce great variety
			self.fakepop.clearDemeInfo()
			self.fakepop.populationMutationMigration()
		
		self.fakepop.updateDemeInfoPreProduction()

		collectStatus = []
		leadersCount = individualsCount = [0] * self.fakepop.numberOfDemes
		for ind in self.fakepop.individuals:
			collectStatus.append(ind.leader)
			leadersCount[ind.currentDeme] += ind.leader
			individualsCount[ind.currentDeme] += 1

		assert any(collectStatus), "all individuals have been elected leaders"
		assert any(individualsCount - leadersCount), "as many leaders as indivs in each deme!"

		for deme in range(self.fakepop.numberOfDemes):
			demeMean = self.fakepop.demes[deme].meanPhenotypes[3]
			assert leadersCount[deme] == pytest.approx(individualsCount[deme] * demeMean), \
			"mean opinion is {0}, when rendered proportion of leaders is {1}".format(demeMean, \
				leadersCount[deme] / individualsCount[deme])

	def test_individuals_have_policing_opinions(self):
		assert False, "write this test!"

	def test_leaders_have_cooperation_level(self):
		assert False, "write this test!"

	def test_political_debate_takes_place(self):
		assert False, "write this test!"

	def test_leader_cooperation_influences_debate_time(self):
		assert False, "write this test!"

	def test_producer_cooperation_does_not_influence_debate_time(self):
		assert False, "write this test!"

	def test_consensus_result_depends_on_leadership(self):
		assert False, "write this test!"

	def test_consensus_time_depends_on_leadership(self):
		assert False, "write this test!"

	def test_individuals_produce_resources_depending_on_status(self):
		assert False, "write this test!"

	def test_individuals_produce_resources_depending_on_consensus_time(self):
		assert False, "write this test!"

	def test_producers_have_cooperation_level(self):
		assert False, "write this test!"

	def test_public_good_game_takes_place_and_pg_is_gathered(self):
		assert False, "write this test!"

	def test_producers_cooperation_influences_public_good(self):
		assert False, "write this test!"

	def test_leaders_cooperation_does_not_influence_public_good(self):
		assert False, "write this test!"

	def test_policing_takes_place_in_demes(self):
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
import pytest
import institutionevolution.fitness as fitness
from institutionevolution.individual import Individual as Ind

class TestFullModel(object):

	def test_full_model_fitness_function_exists(self):
		funcdict = fitness.functions
		assert 'fullmodel' in funcdict, "missing fitness function for full model"

	def test_individual_can_reproduce_correctly(self, getFitnessParameters):
		fitpars = getFitnessParameters("fullmodel")
		indiv = Ind()
		indiv.neighbours = [1,2,3]

		try:
			indiv.reproduce("fullmodel", **fitpars)
			assert indiv.fertilityValue is not None
			assert type(indiv.fertilityValue) is float
			assert indiv.fertilityValue > 0
			assert indiv.offspringNumber is not None
			assert type(indiv.offspringNumber) is int
			assert indiv.offspringNumber >= 0
		except Exception as e:
			assert False, str(e)

	def test_individuals_have_leadership_opinions(self):
		assert False, "write this test!"

	def test_elections_take_place_in_demes(self):
		assert False, "write this test!"

	def test_individual_gets_social_status_after_elections(self):
		assert False, "write this test!"

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
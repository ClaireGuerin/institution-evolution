import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop
import institutionevolution.fitness as fitness
import institutionevolution.progress as progress

class TestSocialClassesFeature(object):

	def test_individual_belongs_to_a_social_class(self):
		self.ind = Ind()
		assert hasattr(self.ind, "socialStatus")

	def test_demes_have_a_number_of_elected_leaders(self):
		self.deme = Dem()
		assert "numberOfLeaders" in self.deme.progressValues
		assert "proportionOfLeaders" in self.deme.progressValues 

	def test_social_class_function_in_fitness_and_progress(self):
		assert 'socialclass' in fitness.functions, "create social class fitness function"
		assert 'socialclass' in progress.functions, "create social class progress function"

	def test_elections_take_place_in_demes(self):
		self.pop = Pop('socialclass')
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 2

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updatePopulation()

		for deme in self.pop.demes:
			assert deme.progressValues["proportionOfLeaders"] is not None
			assert deme.progressValues["proportionOfLeaders"] == deme.meanPhenotypes[3]

	def test_individuals_get_assigned_a_role_after_elections(self):
		assert False, "write this test"

	def test_deme_counts_actual_number_of_leaders_after_elections(self):
		assert False, "write this test"


import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop

class TestSocialClassesFeature(object):

	def test_individual_belongs_to_a_social_class(self):
		self.ind = Ind()
		assert hasattr(self.ind, "socialStatus")

	def test_demes_have_a_number_of_elected_leaders(self):
		self.deme = Dem()
		assert "numberOfLeaders" in self.deme.progressValues
		assert "proportionOfLeaders" in self.deme.progressValues  

	def test_elections_take_place_in_demes(self):
		self.pop = Pop('socialclass')
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 2

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.update()

		for deme in self.pop.demes:
			assert deme.proportionOfLeaders is not None
			assert deme.proportionOfLeaders == deme.meanPhenotypes[3]

	def test_individuals_get_assigned_a_role_after_elections(self):
		assert False, "write this test"

	def test_deme_counts_actual_number_of_leaders_after_elections(self):
		assert False, "write this test"


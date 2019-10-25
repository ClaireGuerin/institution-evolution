import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop

class TestTechnology(object):

	def test_technology_can_be_calculated(self, instantiateSingleDemePopulation):
		self.fakepop = instantiateSingleDemePopulation(10)
		
		try:
			self.fakepop.demes[0].technologyGrowth()
		except AttributeError as e:
			assert False, "Claire stupid you, there is no function to calculate the technology in a deme!"

	def test_deme_technology_is_right_format(self):
		self.fakeDeme = Dem()
		self.fakeDeme.publicGood = 20
		self.fakeDeme.meanPhenotypes = [0.5] * 4

		assert self.fakeDeme.technologyLevel is None

		self.fakeDeme.technologyGrowth()

		assert self.fakeDeme.technologyLevel is not None
		assert type(self.fakeDeme.technologyLevel) is float
		assert self.fakeDeme.technologyLevel >= 0

	def test_deme_technology_calculation_is_right(self):
		self.fakeDeme = Dem()
		self.fakeDeme.publicGood = 20
		self.fakeDeme.meanPhenotypes = [0.5] * 4

		assert self.fakeDeme.technologyLevel is None 

		self.fakeDeme.technologyGrowth()

		#assert self.fakeDeme.technologyLevel == (1 - ) * self.fakeDeme.publicGood *

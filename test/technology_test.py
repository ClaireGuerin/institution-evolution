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

	def test_deme_technology_not_none(self):
		pass
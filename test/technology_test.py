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

	def test_deme_has_effective_public_good_after_policing(self):
		self.fakeDeme = Dem()

		try:
			tmp = getattr(self.fakeDeme, "effectivePublicGood")
		except AttributeError as e:
			assert False, "where is the effective public good?"

	def test_effective_public_good_of_right_format(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes(2)
		
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()


		for dem in self.fakepop.demes:
			assert dem.effectivePublicGood is not None, "No value in the effective public good"
			assert dem.effectivePublicGood > 0, "Effective public good shouldn't be negative"
			assert type(dem.effectivePublicGood) is float, "Effective public good should be float, not {0}".format(type(dem.effectivePublicGood))


	def test_deme_technology_calculation_is_right(self):
		self.fakeDeme = Dem()
		self.fakeDeme.publicGood = 20
		self.fakeDeme.meanPhenotypes = [0.5] * 4

		assert self.fakeDeme.technologyLevel is None 

		self.fakeDeme.technologyGrowth()

		#assert self.fakeDeme.technologyLevel == (1 - ) * self.fakeDeme.publicGood * 

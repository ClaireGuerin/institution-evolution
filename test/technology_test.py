import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop
import gc

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

	def test_deme_has_consensus_policing_level(self):
		self.fakeDeme = Dem()

		try:
			tmp = getattr(self.fakeDeme, "policingConsensus")
		except AttributeError as e:
			assert False, "where is the policing consensus?"

	def test_deme_policing_consensus_of_right_format(self, instantiateSingleIndividualsDemes):
		gc.collect()

		self.fakepop = instantiateSingleIndividualsDemes(2)
		
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()
		self.fakepop.update()

		for dem in self.fakepop.demes:
			assert dem.policingConsensus is not None, "No value in the policing consensus"
			assert dem.policingConsensus >= 0, "Policing consensus shouldn't be negative"
			assert type(dem.policingConsensus) is float, "Policing consensus should be float, not {0} ({1})".format(type(dem.policingConsensus),dem.policingConsensus)
			if dem.demography > 0:
				assert dem.policingConsensus == dem.meanPhenotypes[1], "Group size: {0}, phenotypes: {1}".format(dem.demography, [i.phenotypicValues for i in self.fakepop.individuals if i.currentDeme == dem.id])
			else:
				assert dem.policingConsensus == 0, "It would seem we have a format issue: deme mean phenotypes are {0}".format(dem.meanPhenotypes)

	def test_policing_generates_returned_goods_and_effective_public_good(self):
		self.fakeDeme = Dem()

		try:
			tmp1 = getattr(self.fakeDeme, "effectivePublicGood")
			tmp2 = getattr(self.fakeDeme, "returnedGoods")
		except AttributeError as e:
			assert False, str(e)

	def test_individuals_return_goods(self, getFitnessParameters):
		self.indiv = Ind()
		assert hasattr(self.indiv, "cheater"), "Individual instance does not have an attribute indicating whether it cheated or not"
		assert hasattr(self.indiv, "punishmentFee"), "No punishment fee assigned to individual instance"
		assert hasattr(self.indiv, "punished"), "Individual instance does not have an attribute indicating whether it is punished or not"

		self.pars = getFitnessParameters()
		self.indiv.reproduce("technology", self.pars)
		
		assert self.indiv.punishmentFee is not None
		assert type(self.indiv.punishmentFee) is float
		assert self.indiv.punishmentFee >= 0

	def test_returned_goods_get_calculated_and_in_right_format(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes(2)
		
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()
		self.fakepop.update()

		for dem in self.fakepop.demes:
			assert dem.returnedGoods is not None, "No value in the effective public good"
			assert dem.returnedGoods >= 0, "Effective public good shouldn't be negative"
			assert type(dem.returnedGoods) is float, "Effective public good should be float, not {0}".format(type(dem.effectivePublicGood))

			# resources = 0

			# for ind in self.fakepop.individuals:
			# 	if ind.currentDeme == dem:
			# 		ind.

			# assert dem.returnedGoods == 

	def test_individual_returns_resources(self, instantiateSingleIndividualsDemes):
		self.nDemes = 2
		self.fakepopNoPolicing = instantiateSingleIndividualsDemes(self.nDemes)
		self.fakepopPolicing = instantiateSingleIndividualsDemes(self.nDemes)

		self.fakepopNoPolicing.clearDemeInfo()
		self.fakepopPolicing.clearDemeInfo()

		for dem in self.fakepopNoPolicing.demes:
			dem.policingConsensus = 0

		for dem in self.fakepopPolicing.demes:
			dem.policingConsensus = 1

		self.fakepopNoPolicing.populationMutationMigration()
		self.fakepopPolicing.populationMutationMigration()

		for dem in self.fakepopNoPolicing.demes:
			assert dem.publicGood == dem.meanPhenotypes[0] * 1

		for dem in self.fakepopPolicing.demes:
			assert dem.policingConsensus > dem.meanPhenotypes[0] * 1

	def test_effective_public_good_of_right_format(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes(2)
		
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()
		self.fakepop.update()

		for dem in self.fakepop.demes:
			assert dem.effectivePublicGood is not None, "No value in the effective public good"
			assert dem.effectivePublicGood >= 0, "Effective public good shouldn't be negative"
			assert type(dem.effectivePublicGood) is float, "Effective public good should be float, not {0}".format(type(dem.effectivePublicGood))
			assert dem.effectivePublicGood == (1 - dem.policingConsensus) * dem.publicGood

	def test_deme_technology_calculation_is_right(self):
		self.fakeDeme = Dem()
		self.fakeDeme.publicGood = 20
		self.fakeDeme.meanPhenotypes = [0.5] * 4

		assert self.fakeDeme.technologyLevel is None 

		self.fakeDeme.technologyGrowth()

		#assert self.fakeDeme.technologyLevel == (1 - ) * self.fakeDeme.publicGood * 
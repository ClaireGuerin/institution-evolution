import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop
import scipy.stats as scistats
from operator import add
import random
from statistics import mean
import gc

class TestDeme(object):
	
	def test_deme_attributes(self, objectAttributesExist):
		self.deme = Dem()
		self.attributes = ["id", "demography", "publicGood", "neighbours", "meanPhenotypes", "totalPhenotypes", "technologyLevel", "effectivePublicGood", "returnedGoods"]
		testAttr, whichAttr = objectAttributesExist(self.deme, self.attributes)
		assert testAttr, "Deme is missing attribute(s) {0}".format(whichAttr)
		
		gc.collect()
		
	def test_deme_object_knows_itself(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes(10)
		
		for deme in range(self.fakepop.numberOfDemes):
			focalDeme = self.fakepop.demes[deme]
			assert type(focalDeme.id) is int
			assert focalDeme.id == deme, "Deme number {0} has wrong id ={1}".format(deme, focalDeme.id)
			
		gc.collect()
	
	def test_deme_object_knows_other_demes(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes(10)
		
		for deme in range(self.fakepop.numberOfDemes):
			focalDeme = self.fakepop.demes[deme]
			otherDemes = list(range(self.fakepop.numberOfDemes))
			del otherDemes[focalDeme.id]
			assert type(focalDeme.neighbours) is list
			assert focalDeme.neighbours == otherDemes, "Neighbours of deme {0} are {1}, and not {2}!".format(deme, otherDemes, focalDeme.neighbours)
			
		gc.collect()
		
	def test_deme_mean_phenotype_gets_calculated(self):
		self.fakepop = Pop()
		self.fakepop.createAndPopulateDemes(10, 2)
		
		for dem in self.fakepop.demes:
			assert dem.meanPhenotypes == self.fakepop.initialPhenotypes, "Deme mean phenotype not calculated"
			
	def test_deme_mean_phenotype_updated_after_mutation(self):
		self.fakepop = Pop()
		self.fakepop.numberOfDemes = 2
		self.fakepop.initialDemeSize = 50
		self.fakepop.migrationRate = 0# the two following lines are very important so that the test does not fail at the boundaries, 
		# e.g. if phen = 0 and dev < 0, mutated phenotype will still be 0
		self.fakepop.initialPhenotypes = [0.5] 
		self.fakepop.numberOfPhenotypes = 1

		self.fakepop.createAndPopulateDemes(nDemes=self.fakepop.numberOfDemes, dSize=self.fakepop.initialDemeSize)

		origPhenDeme0 = []
		origPhenDeme1 = []

		for ind in self.fakepop.individuals:
			if ind.currentDeme == 0:
				origPhenDeme0.append(ind.phenotypicValues[0])
			elif ind.currentDeme == 1:
				origPhenDeme1.append(ind.phenotypicValues[0])

		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()
		self.fakepop.update()

		phenDeme0 = []
		phenDeme1 = []
		i0 = 0
		i1 = 0

		for ind in self.fakepop.individuals:

			if ind.currentDeme == 0:
				phen = ind.phenotypicValues[0]
				phenDeme0.append(phen)
				assert origPhenDeme0[i0] + ind.mutationDeviation[0] == phen
				i0 += 1

			elif ind.currentDeme == 1:
				phen = ind.phenotypicValues[0]
				phenDeme1.append(phen)
				assert origPhenDeme1[i1] + ind.mutationDeviation[0] == phen
				i1 +=1
		
		assert self.fakepop.demes[0].meanPhenotypes[0] == pytest.approx(mean(phenDeme0)), "deme 0: mean returned by pop mut func not mean of all indivs in deme"
		assert self.fakepop.demes[1].meanPhenotypes[0] == pytest.approx(mean(phenDeme1)), "deme 1: mean returned by pop mut func not mean of all indivs in deme"

	def test_deme_public_good_calculated_from_cooperation(self):
		self.fakepop = Pop()
		self.fakepop.initialDemeSize = 2
		self.fakepop.numberOfDemes = 10
		self.fakepop.initialPhenotypes = [0.5]
		self.fakepop.numberOfPhenotypes = len(self.fakepop.initialPhenotypes)
		self.fakepop.individualResources = 2
		self.fakepop.mutationRate = 0
		self.fakepop.migrationRate = 0
		self.fakepop.createAndPopulateDemes(self.fakepop.numberOfDemes, self.fakepop.initialDemeSize)

		expectedPG = self.fakepop.initialDemeSize * self.fakepop.initialPhenotypes[0] * self.fakepop.individualResources
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()
		
		for dem in self.fakepop.demes:
			assert dem.publicGood is not None, "Deme public good not calculated"
			assert dem.publicGood == expectedPG, "Deme public good has wrong value"
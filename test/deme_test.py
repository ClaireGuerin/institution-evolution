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
		self.attributes = ["id", "demography", "publicGood", "neighbours", "meanPhenotypes"]
		testAttr, whichAttr = objectAttributesExist(self.deme, self.attributes)
		assert testAttr, "Deme is missing attribute(s) {0}".format(whichAttr)
		
		gc.collect()
		
	def test_deme_object_knows_itself(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes()
		
		for deme in range(self.fakepop.numberOfDemes):
			focalDeme = self.fakepop.demes[deme]
			assert type(focalDeme.id) is int
			assert focalDeme.id == deme, "Deme number {0} has wrong id ={1}".format(deme, focalDeme.id)
			
		gc.collect()
	
	def test_deme_object_knows_other_demes(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes()
		
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
		self.fakepop.migrationRate = 0
		self.fakepop.createAndPopulateDemes()
		dsizes, dpheno = self.fakepop.populationMutationMigration()
		self.fakepop.update(upSizes=dsizes, upPhenotypes=dpheno)

		phenDeme0 = []
		phenDeme1 = []

		for ind in self.fakepop.individuals:
			if ind.currentDeme == 0:
				phenDeme0.append(ind.phenotypicValues[0])
			elif ind.currentDeme == 1:
				phenDeme1.append(ind.phenotypicValues[0])
		
		assert self.fakepop.demes[0].meanPhenotypes[0] == pytest.approx(mean(dpheno[0][0])), "Mean deme 0 phenotype not updated after mutation"
		assert self.fakepop.demes[0].meanPhenotypes[0] == pytest.approx(mean(phenDeme0)), "Mean deme 0 phenotype not updated after mutation"
		assert self.fakepop.demes[1].meanPhenotypes[0] == pytest.approx(mean(phenDeme1)), "Mean deme 0 phenotype not updated after mutation"		
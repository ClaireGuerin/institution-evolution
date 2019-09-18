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
		self.attributes = ["id", "demography", "publicGood", "neighbours", "meanPhenotypes", "totalPhenotypes"]
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
			
	def test_deme_mean_phenotype_updated_after_mutation(self, instantiateSingleDemePopulation):
		self.fakepop = instantiateSingleDemePopulation(100)
		self.fakepop.migrationRate = 0
		self.fakepop.clearDemePhenotypeAndSizeInfo()
		self.fakepop.populationMutationMigration()
		self.fakepop.update()
		
		phen = [ind.phenotypicValues[0] for ind in self.fakepop.individuals]
		
		assert self.fakepop.demes[0].meanPhenotypes[0] == mean(phen), "Mean deme phenotype not updated after mutation"
		
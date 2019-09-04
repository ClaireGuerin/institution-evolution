import pytest
from individual import Individual as Ind
from deme import Deme as Dem
from main import Population as Pop
import scipy.stats as scistats
from operator import add
import random
from statistics import mean
import gc

class TestDeme(object):
	
	def test_deme_attributes(self, objectAttributesExist):
		self.deme = Dem()
		self.attributes = ["id", "demography", "publicGood", "neighbours"]
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
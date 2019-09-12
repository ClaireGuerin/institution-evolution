import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop
import scipy.stats as scistats
from operator import add
import random
from statistics import mean
import gc

class TestIndividual(object):
		
	def test_individual_attributes_exist(self, objectAttributesExist):
		self.indiv = Ind()
		self.attributes = ["phenotypicValues", "currentDeme", "resourcesAmount", "fertilityValue", "offspringNumber"]
		testAttr, whichAttr = objectAttributesExist(self.indiv, self.attributes)
		assert testAttr, "Individual is missing attribute(s) {0}".format(whichAttr)
		
		gc.collect()
		
	def test_mig_rep_mut_methods_exist_and_are_callable(self):
		self.methods = ['mutate', 'migrate', 'reproduce']
		
		for method in self.methods:
			assert hasattr(Ind(), method), "{0} method does not exist".format(method)
			assert callable(getattr(Ind, method)), "{0} method is not callable".format(method)
			
		gc.collect()
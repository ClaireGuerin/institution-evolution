import pytest
from individual import Individual as Ind
from deme import Deme as Dem
from main import Population as Pop

class TestIndividual(object):
	
	def assertObjectAttributesExist(self, obj, attrs):
		for attr in attrs:
			assert hasattr(obj, attr), "object {0} has no attribute {1}".format(obj, attr)
			
	def test_individual_attributes(self):
		self.indiv = Ind()
		self.assertObjectAttributesExist(self.indiv, ["phenotypicValues", "currentDeme", "resourcesAmount", "fertilityValue", "offspringNumber"])
		
class TestDeme(object):
	
	def assertObjectAttributesExist(self, obj, attrs):
		for attr in attrs:
			assert hasattr(obj, attr), "object {0} has no attribute {1}".format(obj, attr)
	
	def test_deme_attributes(self):
		self.deme = Dem()
		self.assertObjectAttributesExist(self.deme, ["demeNumber", "demeSize", "publicGood"])
		
class TestPopulation(object):
	
	def test_population_contains_demes(self):
		self.pop = Pop()
		self.pop.createDemes()
		assert hasattr(self.pop, "allPopulationDemes"), "This population has no deme yet!"
		
	
		
		
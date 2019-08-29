import pytest
from individual import Individual as Ind
from deme import Deme as Dem
from main import Population as Pop

class TestIndividual(object):
	
	def assertObjectAttributesExist(self, obj, attrs):
		for attr in attrs:
			assert hasattr(obj, attr), "object {0} has no attribute {1}".format(obj, attr)
			
	def test_individual_attributes_exist(self):
		self.indiv = Ind()
		self.assertObjectAttributesExist(self.indiv, ["phenotypicValues", "currentDeme", "resourcesAmount", "fertilityValue", "offspringNumber"])
		
	def test_mig_rep_mut_methods_exist_and_are_callable(self):
		self.methods = ['mutate', 'migrate', 'reproduce']
		
		for method in self.methods:
			assert hasattr(Ind(), method), "{0} method does not exist".format(method)
			assert callable(getattr(Ind, method)), "{0} method is not callable".format(method)
			
	def test_mutation_function_returns_phenotype(self):
		self.indiv = Ind()
		self.mut = self.indiv.mutate()
		assert type(self.mut) is float
		assert 0 <= self.mut <= 1
		
class TestDeme(object):
	
	def assertObjectAttributesExist(self, obj, attrs):
		for attr in attrs:
			assert hasattr(obj, attr), "object {0} has no attribute {1}".format(obj, attr)
	
	def test_deme_attributes(self):
		self.deme = Dem()
		self.assertObjectAttributesExist(self.deme, ["demeNumber", "demeSize", "publicGood"])
		
class TestPopulation(object):
	
	def assertObjectAttributesAreNotNone(self, obj, attrs):
		for attr in attrs:
			assert getattr(obj, attr) is not None, "object {0} has attribute {1} set to None".format(obj, attr)
	
	def test_population_contains_demes(self):
		self.pop = Pop()
		self.pop.createAndPopulateDemes()
		assert hasattr(self.pop, "allPopulationDemes"), "This population has no deme yet!"
		
		for deme in self.pop.allPopulationDemes:
			assert type(deme) is Dem
		
	def test_demes_are_populated(self):
		self.pop = Pop()
		self.pop.createAndPopulateDemes()
		for deme in self.pop.allPopulationDemes:
			assert hasattr(deme, "individuals"), "{0} is not populated. Create a list of individuals!".format(deme)
			for ind in deme.individuals:
				assert type(ind) is Ind
				
			
	def test_individual_attributes_are_non_empty(self):
		self.pop = Pop()
		self.pop.createAndPopulateDemes()
		for deme in self.pop.allPopulationDemes:
			for ind in deme.individuals:
				self.assertObjectAttributesAreNotNone(ind, ["phenotypicValues", "currentDeme"])
		
		
	
		
		
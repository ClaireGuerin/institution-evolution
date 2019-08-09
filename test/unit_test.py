import pytest
import lifecycle as lc

class TestLifeCycle(object):
	
	#def test_class_has_method(self):
	#	assert hasattr(myclass, 'mymethod') and callable(getattr(myclass, 'mymethod'))
		
	def test_mig_rep_mut_methods_exist_and_are_callable(self):
		self.methods = ['migration', 'reproduction', 'mutation']
		
		for method in self.methods:
			assert hasattr(lc.runOneCycle, method), "{0} method does not exist".format(method)
			assert callable(getattr(lc.runOneCycle, method)), "{0} method is not callable".format(method)
			
	def test_population_attribute_generated_at_initialisation(self):
		self.method = 'population'
		assert hasattr(lc.runOneCycle, self.method), "life cycle does has not been fed a with a {0} to run on".format(self.method)
		assert callable(getattr(lc.runOneCycle, self.method)), "{0} method is not callable in life cycle".format(self.method)
	
	def test_migration_returns_a_destination_deme(self):
		self.destinationDeme = lc.runOneCycle().migration()
		
		assert self.destinationDeme is not None, "{0} returns nothing".format(self.destinationDeme)
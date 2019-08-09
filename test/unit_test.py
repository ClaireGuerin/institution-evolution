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

import pytest
import lifecycle as lc

class TestLifeCycle(object):
	
	#def test_class_has_method(self):
	#	assert hasattr(myclass, 'mymethod') and callable(getattr(myclass, 'mymethod'))
		
	def test_life_cycle_function_creates_non_empty_output(self):
		test = lc.runOneCycle()
		
		assert test is not None


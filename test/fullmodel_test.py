import pytest
import institutionevolution.fitness as fitness

class TestFullModel(object):

	def test_full_model_fitness_function_exists(self):
		funcdict = fitness.functions
		assert 'fullmodel' in funcdict, "missing fitness function for full model"


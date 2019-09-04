import pytest
from individual import Individual as Ind
from deme import Deme as Dem
from main import Population as Pop
import scipy.stats as scistats
from operator import add
import random
from statistics import mean
import gc

class TestReproductionFunction(object):
	
	def test_individual_has_resources_not_none(self, instantiateSingleIndividualPopulation):
		self.ind = instantiateSingleIndividualPopulation
		assert self.ind.resourcesAmount != None, "Your individual has no resources, cannot reproduce!"
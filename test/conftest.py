import pytest
from main import Population as Pop
from individual import Individual as Ind

@pytest.fixture
def instantiateSingleIndividualPopulation():
		fakepop = Pop()
		fakepop.createAndPopulateDemes(1,1)
		return fakepop.allPopulationDemes[0].individuals[0]

@pytest.fixture
def instantiateSingleDemePopulation():
	def _foo(nIndivs):
		fakepop = Pop()
		fakepop.createAndPopulateDemes(1,nIndivs)
		return fakepop
	
	return _foo
			
	
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
	def _foo1(nIndivs):
		fakepop = Pop()
		fakepop.createAndPopulateDemes(1,nIndivs)
		return fakepop
	
	return _foo1

@pytest.fixture
def objectAttributesExist():
	def _foo2(obj, attrs):
		tests = []
		for attr in attrs:
			tests.append(hasattr(obj, attr))
		thereIsNoProblem = all(tests)
		if thereIsNoProblem:
			result = None
		else:
			problemIndices = [i for i, x in enumerate(tests) if x == False]
			problemAttr = [attrs[a] for a in problemIndices]
			result = problemAttr	
		
		return (thereIsNoProblem, result)
	
	return _foo2

	
import pytest
from main import Population as Pop
from individual import Individual as Ind

fitpardict = {"x": 0.5,
			  "xmean": 0.2, 
			  "fb": 2, 
			  "b": 0.5,
			  "c": 0.05, 
			  "gamma": 0.01,
			  "n": 10}

@pytest.fixture
def instantiateSingleIndividualPopulation():
		fakepop = Pop()
		fakepop.createAndPopulateDemes(1,1)
		return fakepop.individuals[0]

@pytest.fixture
def instantiateSingleDemePopulation():
	def _foo(nIndivs):
		fakepop = Pop()
		fakepop.numberOfDemes = 1
		fakepop.createAndPopulateDemes(fakepop.numberOfDemes,nIndivs)
		return fakepop
	
	return _foo

@pytest.fixture
def instantiateSingleIndividualsDemes():
	def _foo():
		fakepop = Pop()
		fakepop.createAndPopulateDemes(fakepop.numberOfDemes, 1)
		return fakepop
	
	return _foo
		

@pytest.fixture
def objectAttributesExist():
	def _foo(obj, attrs):
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
	
	return _foo

@pytest.fixture
def objectAttributesValues():
	def _foo(obj, attrs, vals):
		tests = []
		values = []
		for attr,val in zip(attrs, vals):
			tests.append(getattr(obj, attr) == val)
			values.append(getattr(obj, attr))
		thereIsNoProblem = all(tests)
		if thereIsNoProblem:
			attributes = None
			expected = None
			observed = None
		else:
			indices = [i for i, x in enumerate(tests) if x == False]
			attributes = [attrs[a] for a in problemIndices]
			expected = [vals[a] for a in problemIndices]
			observed = [values[a] for a in problemIndices]
		
		return (thereIsNoProblem, attributes, expected, observed)
	
	return _foo

@pytest.fixture
def objectAttributesAreNotNone():
	def _foo(obj, attrs):
		tests = []
		for attr in attrs:
			tests.append(getattr(obj, attr) is not None)
		thereIsNoProblem = all(tests)
		if thereIsNoProblem:
			attributes = None
		else:
			indices = [i for i, x in enumerate(tests) if x == False]
			attributes = [attrs[a] for a in problemIndices]
		
		return (thereIsNoProblem, attributes)
	
	return _foo

@pytest.fixture
def pggParameters():
	return fitpardict

@pytest.fixture
def makePopulationReproduce():
	fakepop = Pop(10)
	fakepop.numberOfDemes = 1
	fakepop.initialDemeSize = 10
	fakepop.fitnessParameters = fitpardict
	fakepop.fit_fun = 'pgg'
	fakepop.createAndPopulateDemes()
	parents = fakepop.individuals
	
	for ind in range(len(parents)):
		indiv = fakepop.individuals[ind]
		indiv.resourcesAmount = ind * 2
		indiv.reproduce(fakepop.fit_fun, **fakepop.fitnessParameters)
	
	fakepop.reproductionUpdate()
	
	return (fakepop, parents)
	
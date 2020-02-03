import pytest
from institutionevolution.population import Population as Pop
from institutionevolution.individual import Individual as Ind
import random as rd
import numpy.random as np

fitpardict = {'pgg': {"x": [0.5],
			  "xmean": [0.2], 
			  "fb": 2, 
			  "b": 0.5,
			  "c": 0.05, 
			  "gamma": 0.01,
			  "n": 10},
			  'policing': {"x": [0.5, 0.2],
			  "xmean": [0.2, 0.5],
			  "pg": 2,
			  "fb": 2, 
			  "b": 0.5,
			  "c": 0.05,
			  "gamma": 0.01,
			  "n": 10},
			  'policingdemog':{"x": [0.5],
			  "xmean": [0.2], 
			  "n": 10,
			  "phi": 1,
			  "th": 0.1,
			  "rb": 1, 
			  "kb": 1.2, 
			  "p": 0.2, 
			  "alpha": 2, 
			  "gamma": 0.01, 
			  "beta0": 0, 
			  "beta1": 1, 
			  "epsilon": 3, 
			  "eta": 0.001, 
			  "zeta0": 0, 
			  "zeta1": 1}}

@pytest.fixture
def pseudorandom():
	def _foo(n):
		rd.seed(n)
		np.seed(n)

	return _foo

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
	return fitpardict['pgg']

@pytest.fixture
def makePopulationReproduce():
	def _foo(fitfun='pgg'):
		fakepop = Pop()
		fakepop.numberOfDemes = 1
		fakepop.initialDemeSize = 10
		fakepop.fitnessParameters = fitpardict[fitfun]
		fakepop.fit_fun = fitfun
		fakepop.mutationRate = 0
		fakepop.migrationRate = 0
		fakepop.createAndPopulateDemes()
		for i in range(fakepop.demography):
			fakepop.individuals[i].resourcesAmount = i * 2
		parents = fakepop.individuals
		
		for ind in range(len(parents)):
			indiv = fakepop.individuals[ind]
			indiv.resourcesAmount = ind * 2
		
		fakepop.populationReproduction(**fakepop.fitnessParameters)
		return (fakepop, parents)
	return _foo

@pytest.fixture
def getFitnessParameters():
	def _foo(fitfun='pgg'):
		return fitpardict[fitfun]
	return _foo
	
@pytest.fixture
def runSim():
	def _foo(outputfile):
		population = Pop()
		population.numberOfDemes = 2
		population.initialDemeSize = 1
		population.numberOfGenerations = 5
		population.runSimulation(outputfile)
		return population.numberOfGenerations
	return _foo
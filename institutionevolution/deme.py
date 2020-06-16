class Deme(object):
	
	def __init__(self):
		self.id = None
		self.demography = None
		self.publicGood = None
		self.neighbours = []
		self.meanPhenotypes = None
		self.varPhenotypes = None
		self.totalPhenotypes = None
		self.totalPhenotypeSquares = None
		self.policingConsensus = None
		self.progressValues = {"technologyLevel": None,
		"numberOfLeaders": None, 
		"civilianPublicTime": None, 
		"leaderPublicTime": None, 
		"labourForce": None, 
		"policingConsensus": None,
		"returnedGoods": None,
		"effectivePublicGood": None,
		"consensus": None,
		"consensusTime": None}
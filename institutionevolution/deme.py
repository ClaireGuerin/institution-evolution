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
		self.numberOfLeaders = None,
		self.technologyLevel = None,
		self.politicsValues = {"civilianPublicTime": None, 
		"leaderPublicTime": None, 
		"labourForce": None,
		"consensus": None,
		"consensusTime": None,
		"productionTime": None}
		self.progressValues = {"returnedGoods": None,
		"effectivePublicGood": None,
		"institutionQuality": None,
		"fine": None,
		"fineBudget": None,
		"investmentReward": None}
class Deme(object):
	
	def __init__(self):
		self.id = None
		self.demography = None
		self.publicGood = None
		self.neighbours = []
		self.meanPhenotypes = None
		self.totalPhenotypes = None
		self.technologyLevel = None
		self.policingConsensus = None
		self.returnedGoods = None
		self.effectivePublicGood = None

	def technologyGrowth(self):
		self.technologyLevel = 1.0
		#usablePG = (1 - deme.policingCredit) * deme.publicGood + deme.returnedGood
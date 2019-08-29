class Individual(object):
	
	def __init__(self):
		self.phenotypicValues = None
		self.currentDeme = None
		self.resourcesAmount = None
		self.fertilityValue = None
		self.offspringNumber = None

	def mutate(self):
		return 0.5
		
	def migrate(self):
		pass
	
	def reproduce(self):
		pass
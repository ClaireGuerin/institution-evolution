import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop
import gc

class TestTechnology(object):

	def test_deme_technology_is_right_format(self):
		self.pop = Pop()
		self.pop.fit_fun = 'technology'
		self.pop.numberOfDemes = 2
		self.pop.initialDemeSize = 3
		#self.fakeDeme.publicGood = 20
		self.pop.initialPhenotypes = [0.5] * 4
		self.pop.createAndPopulateDemes()

		assert self.pop.demes[0].progressValues['technologyLevel'] is self.pop.initialTechnologyLevel

		self.pop.clearDemeInfo()

		assert self.pop.demes[0].progressValues['technologyLevel'] is not None
		assert type(self.pop.demes[0].progressValues['technologyLevel']) is float
		assert self.pop.demes[0].progressValues['technologyLevel'] >= 0

	def test_deme_has_consensus_policing_level(self):
		self.fakeDeme = Dem()

		try:
			tmp = getattr(self.fakeDeme, "progressValues")
			get = tmp['policingConsensus']
		except AttributeError as e:
			assert False, "where is the policing consensus?"

	# def test_deme_policing_consensus_of_right_format(self, instantiateSingleIndividualsDemes):
	# 	gc.collect()

	# 	self.fakepop = instantiateSingleIndividualsDemes(2)
		
	# 	self.fakepop.clearDemeInfo()
	# 	self.fakepop.populationMutationMigration()
	# 	self.fakepop.update()

	# 	for dem in self.fakepop.demes:
	# 		assert dem.policingConsensus is not None, "No value in the policing consensus"
	# 		assert dem.policingConsensus >= 0, "Policing consensus shouldn't be negative"
	# 		assert type(dem.policingConsensus) is float, "Policing consensus should be float, not {0} ({1})".format(type(dem.policingConsensus),dem.policingConsensus)
	# 		if dem.demography > 0:
	# 			assert dem.policingConsensus == dem.meanPhenotypes[1], "Group size: {0}, phenotypes: {1}".format(dem.demography, [i.phenotypicValues for i in self.fakepop.individuals if i.currentDeme == dem.id])
	# 		else:
	# 			assert dem.policingConsensus == 0, "It would seem we have a format issue: deme mean phenotypes are {0}".format(dem.meanPhenotypes)

	def test_technology_fitness_function_exists(self, getFitnessParameters):
		self.indiv = Ind()
		self.indiv.phenotypicValues = [0.5,0.2,0.3]
		self.indiv.resourcesAmount = 5
		self.indiv.neighbours = [0,2]

		try:
			self.pars = getFitnessParameters("technology")
			self.indiv.reproduce("technology", **self.pars)
		except KeyError as e:
			assert False, "{0}".format(e)

	# def test_individuals_return_goods(self, getFitnessParameters):
	# 	self.indiv = Ind()

	# 	self.pars = getFitnessParameters("technology")
	# 	self.indiv.reproduce("technology", **self.pars)

	# 	assert self.indiv.punishmentFee is not None
	# 	assert type(self.indiv.punishmentFee) is float
	# 	assert self.indiv.punishmentFee >= 0

	# def test_returned_goods_get_calculated_and_in_right_format(self, instantiateSingleIndividualsDemes):
	# 	self.fakepop = instantiateSingleIndividualsDemes(2)
		
	# 	self.fakepop.clearDemeInfo()
	# 	self.fakepop.populationMutationMigration()
	# 	self.fakepop.update()

	# 	for dem in self.fakepop.demes:
	# 		assert dem.returnedGoods is not None, "No value in the effective public good"
	# 		assert dem.returnedGoods >= 0, "Effective public good shouldn't be negative"
	# 		assert type(dem.returnedGoods) is float, "Effective public good should be float, not {0}".format(type(dem.effectivePublicGood))

	# 		# resources = 0

	# 		# for ind in self.fakepop.individuals:
	# 		# 	if ind.currentDeme == dem:
	# 		# 		ind.

	# 		# assert dem.returnedGoods == 

	def test_individual_returns_resources(self, getFitnessParameters):
		ndemes = 3
		initdemesize = 2
		pars = getFitnessParameters('technology')
		fitfun = 'technology'
		phen = [0.5] * 3

		## WHEN THERE IS NO POLICING, NO GOODS ARE RETURNED
		self.fakepopNoPolicing = Pop(fitfun)
		self.fakepopNoPolicing.fit_fun = fitfun
		self.fakepopNoPolicing.fitnessParameters = pars
		self.fakepopNoPolicing.nDemes = ndemes
		self.fakepopNoPolicing.initialDemeSize = initdemesize
		self.fakepopNoPolicing.initialPhenotypes = phen
		self.fakepopNoPolicing.migrationRate = 0
		self.fakepopNoPolicing.fitnessParameters.update({'p':0})

		self.fakepopNoPolicing.createAndPopulateDemes()
		self.fakepopNoPolicing.clearDemeInfo()
		self.fakepopNoPolicing.populationMutationMigration()
		self.fakepopNoPolicing.update()

		collectGoods = [0] * self.fakepopNoPolicing.numberOfDemes
		for ind in self.fakepopNoPolicing.individuals:
			collectGoods[ind.currentDeme] += ind.resourcesAmount * ind.phenotypicValues[0]
		for dem in range(self.fakepopNoPolicing.numberOfDemes):
			assert self.fakepopNoPolicing.fit_fun == 'technology'
			assert self.fakepopNoPolicing.fitnessParameters['p'] == 0
			assert self.fakepopNoPolicing.demes[dem].progressValues['effectivePublicGood'] == self.fakepopNoPolicing.demes[dem].publicGood
			assert self.fakepopNoPolicing.demes[dem].progressValues['effectivePublicGood'] == collectGoods[dem]

		## WHEN THERE IS POLICING, GOODS MUST BE RETURNED
		self.fakepopPolicing = Pop(fitfun)
		self.fakepopPolicing.fit_fun = fitfun
		self.fakepopPolicing.fitnessParameters = pars
		self.fakepopPolicing.nDemes = ndemes
		self.fakepopPolicing.initialDemeSize = initdemesize
		self.fakepopPolicing.initialPhenotypes = phen
		self.fakepopPolicing.migrationRate = 0
		self.fakepopPolicing.fitnessParameters.update({'p':0.8})

		self.fakepopPolicing.createAndPopulateDemes()
		self.fakepopPolicing.clearDemeInfo()
		self.fakepopPolicing.populationMutationMigration()
		self.fakepopPolicing.update()

		collectGoods = [0] * self.fakepopPolicing.numberOfDemes
		for ind in self.fakepopPolicing.individuals:
			collectGoods[ind.currentDeme] += ind.resourcesAmount * ind.phenotypicValues[0]
		for dem in range(self.fakepopPolicing.numberOfDemes):
			assert self.fakepopPolicing.demes[dem].progressValues['effectivePublicGood'] > collectGoods[dem] * (1-self.fakepopPolicing.fitnessParameters['p']), "goods are not returned after policing"

	def test_effective_public_good_of_right_format(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes(2)
		self.fakepop.fit_fun = 'technology'
		
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()
		self.fakepop.update()

		for dem in self.fakepop.demes:
			assert dem.progressValues['effectivePublicGood'] is not None, "No value in the effective public good"
			assert dem.progressValues['effectivePublicGood'] >= 0, "Effective public good shouldn't be negative"
			assert type(dem.progressValues['effectivePublicGood']) is float, "Effective public good should be float, not {0}".format(type(dem.effectivePublicGood))

	def test_technology_fitness_fct_returns_value(self, getFitnessParameters):
		self.ind = Ind()
		self.ind.resourcesAmount = 5
		pars = getFitnessParameters('technology')
		infoToAdd = {}
		infoToAdd['n'] = 10
		infoToAdd['xmean'] =[0.3]
		infoToAdd['x'] = [0.6]
		
		try:
			self.ind.fertility('technology',**{**pars,**infoToAdd})
		except TypeError as e:
			if str(e) == "float() argument must be a string or a number, not 'NoneType'":
				assert False, "technology fonction returns nothing!"
			else:
				assert False, str(e)

	def test_technology_fitness_fct_takes_args(self, getFitnessParameters):
		self.ind = Ind()
		pars = getFitnessParameters('technology')
		self.ind.resourcesAmount = 1
		
		try:
			self.ind.fertility('technology',**pars)
		except TypeError as e:
			assert False, "technology fitness function does not yet take arguments, fix this!"

	def test_initial_deme_technology_is_not_null(self):
		self.pop = Pop()
		self.pop.createAndPopulateDemes()

		assert type(self.pop.demes[0].progressValues['technologyLevel']) is float, "initial technology level info missing"
		assert self.pop.demes[0].progressValues['technologyLevel'] > 0, "technology level cannot be null or negative" 

	def test_deme_technology_level_gets_updated_with_individual_investments(self, getFitnessParameters):
		pars = getFitnessParameters('technology')
		self.pop = Pop()
		self.pop.numberOfDemes = 2
		self.pop.initialDemeSize = 10
		self.pop.fit_fun = 'technology'
		self.pop.initialPhenotypes = [0.5] * 4
		self.pop.createAndPopulateDemes()

		demeTech = self.pop.demes[0].progressValues['technologyLevel']

		self.pop.lifecycle(**pars)
		self.pop.clearDemeInfo()
		
		assert demeTech != self.pop.demes[0].progressValues['technologyLevel'], "the technology level has not changed!"

	def test_public_good_gets_updated(self):
		self.pop = Pop()
		self.pop.numberOfDemes = 2
		self.pop.initialDemeSize = 10
		self.pop.fit_fun = 'technology'
		self.pop.initialPhenotypes = [0.5] * 4
		self.pop.createAndPopulateDemes()

		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()

		assert type(self.pop.demes[0].publicGood) is float, "publicGood must be created due to individual investments during reproduction"
		assert self.pop.demes[0].publicGood >= 0, "public good cannot be negative"

	def test_technology_updates_with_correct_number(self):
		self.pop = Pop()
		self.pop.numberOfDemes = 2
		self.pop.initialDemeSize = 10
		self.pop.fit_fun = 'technology'
		self.pop.initialPhenotypes = [0.5] * 4
		self.pop.createAndPopulateDemes()

		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		publicGood = self.pop.demes[0].publicGood
		tech = self.pop.demes[0].progressValues['technologyLevel']

		tech_new = (1 + self.pop.fitnessParameters['atech'] * publicGood) * tech / (1 + self.pop.fitnessParameters['btech'] * tech)

		self.pop.update()
		self.pop.populationReproduction(**self.pop.fitnessParameters)
		self.pop.clearDemeInfo()
		assert self.pop.demes[0].progressValues['technologyLevel'] == tech_new, "wrong value for new technology level."

	def test_individual_can_produce_its_own_resources(self, instantiateSingleIndividualsDemes, getFitnessParameters):
		args = getFitnessParameters('technology')
		self.pop = instantiateSingleIndividualsDemes(2)
		self.pop.fit_fun = 'technology'
		self.pop.fitnessParameters.update(args)
		self.pop.initialPhenotypes = [0.5] * 4
		self.pop.individualResources = 0
		self.pop.fitnessParameters['p'] = 0

		self.pop.createAndPopulateDemes()
		self.pop.individuals[0].resourcesAmount = 0

		assert hasattr(self.pop.individuals[0], "produceResources"), "put your farmers to work!"
		self.resBEFORE = self.pop.individuals[0].resourcesAmount
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.update()
		self.ind = self.pop.individuals[0]
		self.deme = self.pop.demes[self.ind.currentDeme]
		self.ind.produceResources('technology', **{**self.pop.fitnessParameters,**self.deme.progressValues})
		assert self.ind.resourcesAmount > self.resBEFORE, "that one did not get the point of production: it didn't increase its amount of resources!"

	def test_individual_resources_increase_with_technology(self, getFitnessParameters):
		#up_dict = {'civilianPublicTime': 0, 'labourForce': 10}
		phen = [0.5] * 4
		res = 0

		# First Individual
		self.ind1 = Ind()
		self.pars = getFitnessParameters('technology')
		#self.pars.update({'civilianPublicTime': 0, 'labourForce': 10, 'technologyLevel': 2})
		res1 = 0.5*self.pars['productionTime'] * ((self.pars['n'] * self.pars['productionTime']) ** (-self.pars['alphaResources'])) * 2 ** self.pars['alphaResources']
		res2 = 0.5*self.pars['productionTime'] * ((self.pars['n'] * self.pars['productionTime']) ** (-self.pars['alphaResources'])) * 5 ** self.pars['alphaResources']
		assert res1 < res2
		
		self.pars.update({'tech': 2, 'p':0})
		self.ind1.phenotypicValues = phen
		self.ind1.resourcesAmount = res

		self.ind1.pars = self.pars
		self.ind1.produceResources('technology', **self.ind1.pars)
		assert self.ind1.resourcesAmount == res1

		# Second Individual
		self.ind2 = Ind()
		self.pars.update({'tech': 5})
		self.ind2.phenotypicValues = phen
		self.ind2.resourcesAmount = res

		self.ind2.pars = self.pars
		self.ind2.produceResources('technology', **self.ind2.pars)
		assert self.ind2.resourcesAmount == res2

		assert self.ind1.resourcesAmount < self.ind2.resourcesAmount, "ind1 knows 2 and gets {0}, ind2 knows 5 and gets {1}, when really those with more knowledge should get more resources, all else being equal".format(
			self.ind1.resourcesAmount,self.ind2.resourcesAmount)

	def test_group_labour_force_is_calculated_and_given_to_individual_instance(self):
		self.pop = Pop()
		self.pop.fit_fun = 'technology'
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 20
		self.pop.createAndPopulateDemes()
		self.deme = self.pop.demes[0]
		assert hasattr(self.deme, "progressValues"), "make dict"
		assert type(self.deme.progressValues) is dict
		progressKeys = ["numberOfLeaders", "civilianPublicTime", "leaderPublicTime", "labourForce"]
		for key in progressKeys:
			assert key in self.deme.progressValues

		self.pop.clearDemeInfo()
		for pheno in self.pop.demes[0].meanPhenotypes:
			assert pheno is not None, "none phenotypes before migration"
		self.pop.populationMutationMigration()
		for pheno in self.pop.demes[0].meanPhenotypes:
			assert pheno is not None, "none phenotypes before update"
		self.pop.update()

		self.demeAFTER = self.pop.demes[0]
		for key in progressKeys:
			assert self.demeAFTER.progressValues[key] is not None
		# deme labour force = total private time: (demography - nleaders)(1-T1) + nleaders(1-T2)
		# where T1 and T2 is effective time spent in debate by civilian and leader respectively

	def test_production_increase_function(self, getFitnessParameters):
		pars = getFitnessParameters('technology')
		self.pop = Pop()
		self.pop.fit_fun = 'technology'
		self.pop.numberOfDemes = 2
		self.pop.initialDemeSize = 5

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.update()

		for ind in self.pop.individuals:
			deme = self.pop.demes[ind.currentDeme]
			pars.update(deme.progressValues)
			assert deme.progressValues["labourForce"] is not None, "labour force is none!"
			assert deme.progressValues["labourForce"] != 0, "labour force is null!"
			assert deme.progressValues["technologyLevel"] is not None, "labour force is null!"
			resourcesProduced = pars['productionTime'] * ((pars['n'] * pars['productionTime']) ** (-pars['alphaResources'])) * pars['tech'] ** pars['alphaResources']
			payoff = (1 - ind.phenotypicValues[0]) * (resourcesProduced - pars['q'] * (pars['pg'] * pars['p'])/pars['n'])
			ind.produceResources(self.pop.fit_fun, **pars)
			assert ind.resourcesAmount == payoff, "ind produced {0} instead of {1}".format(ind.resourcesAmount, production)

	def test_fitness_function_returns_correct_value(self):
		self.pop = Pop()
		self.pop.fit_fun = 'technology'
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 5
		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.update()

		for ind in self.pop.individuals:
			#assert self.pop.demes[ind.currentDeme].progressValues['technologyLevel'] > 1, "technology level too low: {0}".format(self.pop.demes[ind.currentDeme].progressValues['technologyLevel'])
			#assert ind.resourcesAmount > 0, "not enough resources to reproduce: {0}".format(ind.resourcesAmount)
			infoToAdd = {}
			infoToAdd['n'] = self.pop.demes[ind.currentDeme].demography
			infoToAdd['xmean'] = self.pop.demes[ind.currentDeme].meanPhenotypes
			infoToAdd['tech'] = self.pop.demes[ind.currentDeme].progressValues['technologyLevel']
			infoToAdd['pg'] = self.pop.demes[ind.currentDeme].publicGood
			infoToAdd['x'] = ind.phenotypicValues
			ind.reproduce('technology', **{**self.pop.fitnessParameters, **infoToAdd})

			w = (self.pop.fitnessParameters['rb'] + ind.resourcesAmount) / (1 + self.pop.fitnessParameters['gamma'] * infoToAdd['n'])
			assert ind.fertilityValue == w, "wrong fitness calculation for individual, should return {0}".format(w)

	def test_individuals_reproduce_after_production(self, getFitnessParameters):
		pars = getFitnessParameters('technology')
		pars.update({'p':0})
		self.ind = Ind()
		self.ind.neighbours = [1,2]
		self.ind.phenotypicValues = [0.5] * 3
		self.ind.reproduce('technology',**pars)

		res = 0.5 * pars['productionTime'] * ((pars['n'] * pars['productionTime']) ** (-pars['alphaResources'])) * pars['tech'] ** pars['alphaResources']
		assert res > 0, "no resources produced"
		f = (pars["rb"] + res) / (1 + pars["gamma"] * pars["n"])
		assert self.ind.fertilityValue == f, "wrong fertility value"

		self.ind2 = Ind()
		self.ind2.neighbours = [1,2]
		self.ind2.phenotypicValues = [0.5] * 3
		self.ind2.reproduce('technology',**pars)
		res2 = pars['productionTime'] * ((pars['n'] * pars['productionTime']) ** (-pars['alphaResources'])) * pars['tech'] ** pars['alphaResources']
		payoff2 = (1 - self.ind.phenotypicValues[0]) * (res2 * (1 - pars['q'] * pars['d'] * pars['p']) - pars['q'] * (pars['pg'] * pars['p'])/pars['n'])
		assert pars['q'] * (pars['pg'] * pars['p'])/pars['n'] == 0
		assert (1 - pars['q'] * pars['d'] * pars['p']) == 1
		assert (1 - self.ind.phenotypicValues[0]) == 0.5
		assert payoff2 == 0.5 * res2
		assert res2 > 0, "no resources produced"
		f2 = (pars["rb"] + payoff2) / (1 + pars["gamma"] * pars["n"])
		assert f2 == f, "all being equal, the fertility values should be the same"
		assert self.ind2.fertilityValue == f, "wrong fertility value"

		pars.update({'p':0.7})
		self.ind3 = Ind()
		self.ind3.neighbours = [1,2]
		self.ind3.phenotypicValues = [0.5] * 3
		self.ind3.reproduce('technology',**pars)
		res3 = pars['productionTime'] * ((pars['n'] * pars['productionTime']) ** (-pars['alphaResources'])) * pars['tech'] ** pars['alphaResources']
		payoff3 = (1 - self.ind.phenotypicValues[0]) * (res3 * (1 - pars['q'] * pars['d'] * pars['p']) - pars['q'] * (pars['pg'] * pars['p'])/pars['n'])
		assert res3 > 0, "no resources produced"
		f3 = (pars["rb"] + payoff3) / (1 + pars["gamma"] * pars["n"])
		assert self.ind3.fertilityValue == f3, "wrong fertility value"
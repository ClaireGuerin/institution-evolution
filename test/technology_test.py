import pytest
from institutionevolution.individual import Individual as Ind
from institutionevolution.deme import Deme as Dem
from institutionevolution.population import Population as Pop
import gc

class TestTechnology(object):

	def test_deme_technology_is_right_format(self):
		self.pop = Pop(fit_fun='technology', inst='test/test')
		self.pop.numberOfDemes = 2
		self.pop.initialDemeSize = 3
		#self.fakeDeme.publicGood = 20
		self.pop.initialPhenotypes = [0.5] * 4
		self.pop.createAndPopulateDemes()

		assert self.pop.demes[0].technologyLevel is self.pop.initialTechnologyLevel

		self.pop.clearDemeInfo()

		assert self.pop.demes[0].technologyLevel is not None
		assert type(self.pop.demes[0].technologyLevel) is float
		assert self.pop.demes[0].technologyLevel >= 0

		gc.collect()

	def test_deme_has_consensus_policing_level(self):
		self.fakeDeme = Dem()

		try:
			tmp = getattr(self.fakeDeme, "politicsValues")
			get = tmp['consensus']
		except AttributeError as e:
			assert False, "where is the policing consensus?"

		gc.collect()

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
			self.indiv.reproduce("technology", **{**{'fine':0.4,'investmentReward':0.6},**self.pars})
		except KeyError as e:
			assert False, "{0}".format(e)

		gc.collect()

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

	# def test_individual_returns_resources(self, getFitnessParameters):
	# 	ndemes = 3
	# 	initdemesize = 2
	# 	pars = getFitnessParameters('technology')
	# 	fitfun = 'technology'
	# 	phen = [0.5] * 3

	# 	## WHEN THERE IS NO POLICING, NO GOODS ARE RETURNED
	# 	self.fakepopNoPolicing = Pop(fit_fun=fitfun, inst='test')
	# 	self.fakepopNoPolicing.fit_fun = fitfun
	# 	self.fakepopNoPolicing.fitnessParameters = pars
	# 	self.fakepopNoPolicing.nDemes = ndemes
	# 	self.fakepopNoPolicing.initialDemeSize = initdemesize
	# 	self.fakepopNoPolicing.initialPhenotypes = phen
	# 	self.fakepopNoPolicing.migrationRate = 0
	# 	self.fakepopNoPolicing.fitnessParameters.update({'p':0})

	# 	self.fakepopNoPolicing.createAndPopulateDemes()
	# 	self.fakepopNoPolicing.clearDemeInfo()
	# 	self.fakepopNoPolicing.populationMutationMigration()
	# 	self.fakepopNoPolicing.updateDemeInfo()

	# 	collectGoods = [0] * self.fakepopNoPolicing.numberOfDemes
	# 	for ind in self.fakepopNoPolicing.individuals:
	# 		collectGoods[ind.currentDeme] += ind.resourcesAmount * ind.phenotypicValues[0]
	# 	for dem in range(self.fakepopNoPolicing.numberOfDemes):
	# 		assert self.fakepopNoPolicing.fit_fun == 'technology'
	# 		assert self.fakepopNoPolicing.fitnessParameters['p'] == 0
	# 		assert self.fakepopNoPolicing.demes[dem].progressValues['effectivePublicGood'] == self.fakepopNoPolicing.demes[dem].publicGood
	# 		assert self.fakepopNoPolicing.demes[dem].progressValues['effectivePublicGood'] == collectGoods[dem]

	# 	## WHEN THERE IS POLICING, GOODS MUST BE RETURNED
	# 	self.fakepopPolicing = Pop(fit_fun=fitfun, inst='test')
	# 	self.fakepopPolicing.fitnessParameters = pars
	# 	self.fakepopPolicing.nDemes = ndemes
	# 	self.fakepopPolicing.initialDemeSize = initdemesize
	# 	self.fakepopPolicing.initialPhenotypes = phen
	# 	self.fakepopPolicing.migrationRate = 0
	# 	self.fakepopPolicing.fitnessParameters.update({'p':0.8})

	# 	self.fakepopPolicing.createAndPopulateDemes()
	# 	self.fakepopPolicing.clearDemeInfo()
	# 	self.fakepopPolicing.populationMutationMigration()
	# 	self.fakepopPolicing.updateDemeInfo()

	# 	collectGoods = [0] * self.fakepopPolicing.numberOfDemes
	# 	for ind in self.fakepopPolicing.individuals:
	# 		collectGoods[ind.currentDeme] += ind.resourcesAmount * ind.phenotypicValues[0]
	# 	for dem in range(self.fakepopPolicing.numberOfDemes):
	# 		assert self.fakepopPolicing.demes[dem].progressValues['effectivePublicGood'] > collectGoods[dem] * (1-self.fakepopPolicing.fitnessParameters['p']), "goods are not returned after policing"

	# def test_effective_public_good_of_right_format(self, instantiateSingleIndividualsDemes):
	# 	self.fakepop = instantiateSingleIndividualsDemes(2)
	# 	self.fakepop.fit_fun = 'technology'
		
	# 	self.fakepop.clearDemeInfo()
	# 	self.fakepop.populationMutationMigration()
	# 	self.fakepop.updateDemeInfo()

	# 	for dem in self.fakepop.demes:
	# 		assert dem.progressValues['effectivePublicGood'] is not None, "No value in the effective public good"
	# 		assert dem.progressValues['effectivePublicGood'] >= 0, "Effective public good shouldn't be negative"
	# 		assert type(dem.progressValues['effectivePublicGood']) is float, "Effective public good should be float, not {0}".format(type(dem.effectivePublicGood))

	def test_technology_fitness_fct_returns_value(self, getFitnessParameters):
		self.ind = Ind()
		self.ind.resourcesAmount = 5
		self.pars = getFitnessParameters('technology')
		infoToAdd = {}
		infoToAdd['n'] = 10
		infoToAdd['xmean'] =[0.3]
		infoToAdd['x'] = [0.6]
		infoToAdd['fine'] = 0.2
		infoToAdd['investmentReward'] = 0.4
		
		try:
			self.ind.fertility('technology',**{**self.pars,**infoToAdd})
		except TypeError as e:
			if str(e) == "float() argument must be a string or a number, not 'NoneType'":
				assert False, "technology fonction returns nothing!"
			else:
				assert False, str(e)

		gc.collect()

	def test_technology_fitness_fct_takes_args(self, getFitnessParameters):
		self.ind = Ind()
		self.pars = getFitnessParameters('technology')
		self.ind.resourcesAmount = 1
		
		try:
			self.ind.fertility('technology',**{**{'fine':0.2,'investmentReward':0.4},**self.pars})
		except TypeError as e:
			assert False, "technology fitness function does not yet take arguments, fix this!"

		gc.collect()

	def test_initial_deme_technology_is_not_null(self):
		self.pop = Pop(inst='test/test')
		self.pop.createAndPopulateDemes()

		assert type(self.pop.demes[0].technologyLevel) is float, "initial technology level info missing"
		assert self.pop.demes[0].technologyLevel > 0, "technology level cannot be null or negative" 

		gc.collect()

	def test_deme_technology_level_gets_updated_with_individual_investments(self, getFitnessParameters):
		self.pars = getFitnessParameters('technology')
		self.pop = Pop(fit_fun='technology', inst='test/test')
		self.pop.numberOfDemes = 2
		self.pop.initialDemeSize = 10
		self.pop.initialPhenotypes = [0.5] * 4
		self.pop.fitnessParameters = self.pars
		self.pop.createAndPopulateDemes()

		demeTech = self.pop.demes[0].technologyLevel

		self.pop.lifecycle()
		self.pop.clearDemeInfo()
		
		assert demeTech != self.pop.demes[0].technologyLevel, "the technology level has not changed!"

		gc.collect()

	def test_public_good_gets_updated(self):
		self.pop = Pop(fit_fun='technology', inst='test/test')
		self.pop.numberOfDemes = 2
		self.pop.initialDemeSize = 10
		self.pop.initialPhenotypes = [0.5] * 4
		self.pop.createAndPopulateDemes()

		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updateDemeInfoPreProduction()
		self.pop.populationProduction()
		self.pop.updateDemeInfoPostProduction()

		assert type(self.pop.demes[0].publicGood) is float, "publicGood must be created due to individual investments during reproduction"
		assert self.pop.demes[0].publicGood >= 0, "public good cannot be negative"

		gc.collect()

	def test_technology_updates_with_correct_number(self):
		self.pop = Pop(fit_fun='technology', inst='test/test')
		self.pop.numberOfDemes = 2
		self.pop.initialDemeSize = 10
		self.pop.fit_fun = 'technology'
		self.pop.initialPhenotypes = [0.5] * 4
		self.pop.createAndPopulateDemes()
		
		assert self.pop.demes[0].technologyLevel == self.pop.initialTechnologyLevel, "wrong technology level assigned to deme when created"
		self.pop.clearDemeInfo()
		assert self.pop.demes[0].technologyLevel == self.pop.initialTechnologyLevel, "wrong technology level after first clearing"
		self.pop.populationMutationMigration()
		self.pop.updateDemeInfoPreProduction()
		self.pop.populationProduction()
		self.pop.updateDemeInfoPostProduction()
		# calculate new technology level as it should be
		publicGood = self.pop.demes[0].publicGood
		tech = self.pop.demes[0].technologyLevel
		tech_new = tech * (self.pop.fitnessParameters['atech'] + ((1 - self.pop.fitnessParameters['p']) * publicGood) ** (1 - self.pop.fitnessParameters['betaTech'])) / (1 + self.pop.fitnessParameters['btech'] * tech)
		self.pop.populationReproduction()
		self.pop.clearDemeInfo()
		assert self.pop.demes[0].technologyLevel == tech_new, "wrong value for new technology level."

		gc.collect()

	def test_individual_can_produce_its_own_resources(self, instantiateSingleIndividualsDemes, getFitnessParameters):
		self.args = getFitnessParameters('technology')
		self.pop = instantiateSingleIndividualsDemes(2)
		self.pop.fit_fun = 'technology'
		self.pop.fitnessParameters.update(self.args)
		self.pop.initialPhenotypes = [0.5] * 4
		self.pop.individualResources = 0
		self.pop.fitnessParameters['p'] = 0

		self.pop.createAndPopulateDemes()
		self.pop.individuals[0].resourcesAmount = 0

		assert hasattr(self.pop.individuals[0], "produceResources"), "put your farmers to work!"
		self.resBEFORE = self.pop.individuals[0].resourcesAmount
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updateDemeInfoPreProduction()
		self.ind = self.pop.individuals[0]
		self.deme = self.pop.demes[self.ind.currentDeme]
		self.ind.produceResources('technology', **{**self.pop.fitnessParameters,**self.deme.progressValues})
		assert self.ind.resourcesAmount > self.resBEFORE, "that one did not get the point of production: it didn't increase its amount of resources!"

		gc.collect()

	def test_individual_resources_increase_with_technology(self, getFitnessParameters):
		#up_dict = {'civilianPublicTime': 0, 'labourForce': 10}
		phen = [0.5] * 4
		res = 0

		# First Individual
		self.ind1 = Ind()
		self.pars = getFitnessParameters('technology')
		#self.pars.update({'civilianPublicTime': 0, 'labourForce': 10, 'technologyLevel': 2})
		tech1 = 2.4
		tech2 = 5.9

		res1 = (self.pars['n'] ** (-self.pars['alphaResources'])) * (tech1 ** self.pars['alphaResources'])
		res2 = (self.pars['n'] ** (-self.pars['alphaResources'])) * (tech2 ** self.pars['alphaResources'])
		assert res1 < res2
		
		self.pars.update({'tech': tech1, 'p':0})
		self.ind1.phenotypicValues = phen
		self.ind1.resourcesAmount = res

		self.ind1.pars = self.pars
		self.ind1.produceResources('technology', **self.ind1.pars)
		assert self.ind1.resourcesAmount == res1

		# Second Individual
		self.ind2 = Ind()
		self.pars.update({'tech': tech2})
		self.ind2.phenotypicValues = phen
		self.ind2.resourcesAmount = res

		self.ind2.pars = self.pars
		self.ind2.produceResources('technology', **self.ind2.pars)
		assert self.ind2.resourcesAmount == res2

		assert self.ind1.resourcesAmount < self.ind2.resourcesAmount, "ind1 knows 2 and gets {0}, ind2 knows 5 and gets {1}, when really those with more knowledge should get more resources, all else being equal".format(
			self.ind1.resourcesAmount,self.ind2.resourcesAmount)

		gc.collect()

	def test_group_labour_force_is_calculated_and_given_to_individual_instance(self):
		self.pop = Pop(fit_fun='technology', inst='test/test')
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 20
		self.pop.createAndPopulateDemes()
		self.deme = self.pop.demes[0]
		assert hasattr(self.deme, "progressValues"), "make dict"
		assert type(self.deme.progressValues) is dict
		progressKeys = ["fine","investmentReward"]
		for key in progressKeys:
			assert key in self.deme.progressValues

		self.pop.clearDemeInfo()
		for pheno in self.pop.demes[0].meanPhenotypes:
			assert pheno is not None, "none phenotypes before migration"
		self.pop.populationMutationMigration()
		for pheno in self.pop.demes[0].meanPhenotypes:
			assert pheno is not None, "none phenotypes before update"
		self.pop.updateDemeInfoPreProduction()
		self.pop.populationProduction()
		self.pop.updateDemeInfoPostProduction()

		self.demeAFTER = self.pop.demes[0]
		for key in progressKeys:
			assert self.demeAFTER.progressValues[key] is not None
		# deme labour force = total private time: (demography - nleaders)(1-T1) + nleaders(1-T2)
		# where T1 and T2 is effective time spent in debate by civilian and leader respectively

		gc.collect()

	def test_production_increase_function(self):
		#pars = getFitnessParameters('technology')
		self.pop = Pop(fit_fun='technology', inst='test/test')
		self.pop.numberOfDemes = 2
		self.pop.initialDemeSize = 5

		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updateDemeInfoPreProduction()
		self.pars = self.pop.fitnessParameters

		for ind in self.pop.individuals:
			deme = self.pop.demes[ind.currentDeme]
			infoToAdd = {}
			infoToAdd["tech"] = deme.technologyLevel
			infoToAdd["n"] = deme.demography
			infoToAdd["xmean"] = deme.meanPhenotypes
			infoToAdd["pg"] = deme.publicGood
			infoToAdd["x"] = ind.phenotypicValues
			# assert deme.progressValues["labourForce"] is not None, "labour force is none!"
			# assert deme.progressValues["labourForce"] != 0, "labour force is null!"
			assert deme.technologyLevel is not None, "technology is none!"
			fine = deme.publicGood * self.pars['p'] / deme.demography
			benef = ((deme.publicGood * (1 - self.pars['p'])) ** self.pars["betaTech"]) / deme.demography
			resourcesProduced = deme.demography ** (-self.pars['alphaResources']) * infoToAdd['tech'] ** self.pars['alphaResources']
			
			ind.produceResources(self.pop.fit_fun, **{**self.pop.fitnessParameters,**infoToAdd})
			assert ind.resourcesAmount == resourcesProduced, "ind produced {0} instead of {1}".format(ind.resourcesAmount, payoff)

			gc.collect()

	def test_fitness_function_returns_correct_value(self):
		self.pop = Pop(fit_fun='technology', inst='test/test')
		self.pop.numberOfDemes = 3
		self.pop.initialDemeSize = 5
		self.pop.createAndPopulateDemes()
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.updateDemeInfoPreProduction()
		self.pop.populationProduction()
		self.pop.updateDemeInfoPostProduction()

		for ind in self.pop.individuals:
			#assert self.pop.demes[ind.currentDeme].progressValues['technologyLevel'] > 1, "technology level too low: {0}".format(self.pop.demes[ind.currentDeme].progressValues['technologyLevel'])
			#assert ind.resourcesAmount > 0, "not enough resources to reproduce: {0}".format(ind.resourcesAmount)
			infoToAdd = {}
			infoToAdd['n'] = self.pop.demes[ind.currentDeme].demography
			infoToAdd['xmean'] = self.pop.demes[ind.currentDeme].meanPhenotypes
			infoToAdd['tech'] = self.pop.demes[ind.currentDeme].technologyLevel
			infoToAdd['pg'] = self.pop.demes[ind.currentDeme].publicGood
			infoToAdd['x'] = ind.phenotypicValues
			ind.reproduce('technology', **{**self.pop.fitnessParameters, **infoToAdd, **self.pop.demes[ind.currentDeme].progressValues})

			fine = infoToAdd['pg'] * self.pop.fitnessParameters['p'] / infoToAdd['n']
			benef = ((infoToAdd['pg'] * (1 - self.pop.fitnessParameters['p'])) ** self.pop.fitnessParameters["betaTech"]) / infoToAdd['n']
			payoff = (1 - self.pop.fitnessParameters['q']) * (1 - infoToAdd['x'][0]) * ind.resourcesAmount + self.pop.fitnessParameters['q'] * ((1 - infoToAdd['x'][0]) * ind.resourcesAmount - fine) + benef
			w = (self.pop.fitnessParameters['rb'] + payoff) / (1 + self.pop.fitnessParameters['gamma'] * infoToAdd['n'])
			assert ind.fertilityValue == w, "wrong fitness calculation for individual, should return {0}".format(w)

		gc.collect()

	def test_individuals_reproduce_after_production(self, getFitnessParameters):
		self.params = getFitnessParameters('technology')
		self.params.update({'p':0,'tech':10.5})
		self.ind = Ind()
		self.ind.neighbours = [1,2]
		self.ind.phenotypicValues = [0.5] * 3

		res = (self.params['n'] ** (-self.params['alphaResources'])) * (self.params['tech'] ** self.params['alphaResources'])
		assert res > 0, "no resources produced"
		fine = self.params['pg'] * self.params['p'] / self.params['n']
		benef = ((self.params['pg'] * (1 - self.params['p'])) ** self.params["betaTech"]) / self.params['n']
		payoff = (1 - self.params['q']) * (1 - self.ind.phenotypicValues[0]) * res + self.params['q'] * ((1 - self.ind.phenotypicValues[0]) * res - fine) + benef
		f = (self.params["rb"] + payoff) / (1 + self.params["gamma"] * self.params["n"])

		self.ind.produceResources('technology',**self.params)
		self.ind.reproduce('technology',**{**{'fine':fine,'investmentReward':benef},**self.params})
		assert self.ind.fertilityValue == f, "wrong fertility value"

		self.ind2 = Ind()
		self.ind2.neighbours = [1,2]
		self.ind2.phenotypicValues = [0.5] * 3
		res2 = (self.params['n'] ** (-self.params['alphaResources'])) * (self.params['tech'] ** self.params['alphaResources'])
		fine2 = self.params['pg'] * self.params['p'] / self.params['n']
		benef2 = ((self.params['pg'] * (1 - self.params['p'])) ** self.params["betaTech"]) / self.params['n']
		payoff2 = (1 - self.params['q']) * (1 - self.ind2.phenotypicValues[0]) * res2 + self.params['q'] * ((1 - self.ind2.phenotypicValues[0]) * res2 - fine2) + benef2
		assert self.params['q'] * (self.params['pg'] * self.params['p'])/self.params['n'] == 0
		assert (1 - self.params['q'] * self.params['d'] * self.params['p']) == 1
		assert (1 - self.ind.phenotypicValues[0]) == 0.5
		assert res2 > 0, "no resources produced"
		f2 = (self.params["rb"] + payoff2) / (1 + self.params["gamma"] * self.params["n"])
		assert f2 == f, "all being equal, the fertility values should be the same"

		self.ind2.produceResources('technology',**self.params)
		self.ind2.reproduce('technology',**{**{'fine':fine2,'investmentReward':benef2},**self.params})
		assert self.ind2.fertilityValue == f, "wrong fertility value"

		self.params.update({'p':0.7})
		self.ind3 = Ind()
		self.ind3.neighbours = [1,2]
		self.ind3.phenotypicValues = [0.5] * 3
		res3 = (self.params['n'] ** (-self.params['alphaResources'])) * (self.params['tech'] ** self.params['alphaResources'])
		fine3 = self.params['pg'] * self.params['p'] / self.params['n']
		benef3 = ((self.params['pg'] * (1 - self.params['p'])) ** self.params["betaTech"]) / self.params['n']
		payoff3 = (1 - self.params['q']) * (1 - self.ind3.phenotypicValues[0]) * res3 + self.params['q'] * ((1 - self.ind3.phenotypicValues[0]) * res3 - fine3) + benef3
		assert res3 > 0, "no resources produced"
		f3 = (self.params["rb"] + payoff3) / (1 + self.params["gamma"] * self.params["n"])

		self.ind3.produceResources('technology',**self.params)
		self.ind3.reproduce('technology',**{**{'fine':fine3,'investmentReward':benef3},**self.params})
		assert self.ind3.fertilityValue == f3, "wrong fertility value"

		gc.collect()
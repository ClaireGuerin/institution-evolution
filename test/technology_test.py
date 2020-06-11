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

	def test_deme_policing_consensus_of_right_format(self, instantiateSingleIndividualsDemes):
		gc.collect()

		self.fakepop = instantiateSingleIndividualsDemes(2)
		
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()
		self.fakepop.update()

		for dem in self.fakepop.demes:
			assert dem.policingConsensus is not None, "No value in the policing consensus"
			assert dem.policingConsensus >= 0, "Policing consensus shouldn't be negative"
			assert type(dem.policingConsensus) is float, "Policing consensus should be float, not {0} ({1})".format(type(dem.policingConsensus),dem.policingConsensus)
			if dem.demography > 0:
				assert dem.policingConsensus == dem.meanPhenotypes[1], "Group size: {0}, phenotypes: {1}".format(dem.demography, [i.phenotypicValues for i in self.fakepop.individuals if i.currentDeme == dem.id])
			else:
				assert dem.policingConsensus == 0, "It would seem we have a format issue: deme mean phenotypes are {0}".format(dem.meanPhenotypes)

	def test_technology_fitness_function_exists(self, getFitnessParameters):
		self.indiv = Ind()
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

	def test_individual_returns_resources(self, instantiateSingleIndividualsDemes):
		self.nDemes = 2
		self.fakepopNoPolicing = instantiateSingleIndividualsDemes(self.nDemes)
		self.fakepopPolicing = instantiateSingleIndividualsDemes(self.nDemes)

		self.fakepopNoPolicing.clearDemeInfo()
		self.fakepopPolicing.clearDemeInfo()

		for dem in self.fakepopNoPolicing.demes:
			dem.policingConsensus = 0

		for dem in self.fakepopPolicing.demes:
			dem.policingConsensus = 1

		self.fakepopNoPolicing.populationMutationMigration()
		self.fakepopPolicing.populationMutationMigration()

		for dem in self.fakepopNoPolicing.demes:
			assert dem.publicGood == dem.meanPhenotypes[0] * 1

		for dem in self.fakepopPolicing.demes:
			assert dem.policingConsensus > dem.meanPhenotypes[0] * 1

	def test_effective_public_good_of_right_format(self, instantiateSingleIndividualsDemes):
		self.fakepop = instantiateSingleIndividualsDemes(2)
		
		self.fakepop.clearDemeInfo()
		self.fakepop.populationMutationMigration()
		self.fakepop.update()

		for dem in self.fakepop.demes:
			assert dem.effectivePublicGood is not None, "No value in the effective public good"
			assert dem.effectivePublicGood >= 0, "Effective public good shouldn't be negative"
			assert type(dem.effectivePublicGood) is float, "Effective public good should be float, not {0}".format(type(dem.effectivePublicGood))
			assert dem.effectivePublicGood == (1 - dem.policingConsensus) * dem.publicGood

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
		self.pop = instantiateSingleIndividualsDemes(2)
		self.pop.fit_fun = 'technology'
		self.pop.initialPhenotypes = [0.5] * 4
		self.pop.individualResources = 0

		self.pop.createAndPopulateDemes()
		self.pop.individuals[0].resourcesAmount = 0
		self.ind = self.pop.individuals[0]

		assert hasattr(self.ind, "produceResources"), "put your farmers to work!"
		self.resBEFORE = self.ind.resourcesAmount
		self.pop.clearDemeInfo()
		self.pop.populationMutationMigration()
		self.pop.update()
		self.ind = self.pop.individuals[0]
		self.deme = self.pop.demes[self.ind.currentDeme]
		args = getFitnessParameters(self.pop.fit_fun)
		args.update(self.deme.progressValues)
		self.ind.produceResources('technology', **args)
		assert self.ind.resourcesAmount > self.resBEFORE, "that one did not get the point of production: it didn't increase its amount of resources!"

	def test_individual_resources_increase_with_technology(self, getFitnessParameters):
		#up_dict = {'civilianPublicTime': 0, 'labourForce': 10}
		phen = [0.5] * 4
		res = 0

		# First Individual
		self.ind1 = Ind()
		self.pars = getFitnessParameters('technology')
		self.pars.update({'civilianPublicTime': 0, 'labourForce': 10, 'technologyLevel': 2})
		self.ind1.phenotypicValues = phen
		self.ind1.resourcesAmount = res

		self.ind1.produceResources('technology', **self.pars)
		save1 = self.ind1.resourcesAmount

		# Second Individual
		self.ind2 = Ind()
		self.pars.update({'technologyLevel': 5})
		self.ind2.phenotypicValues = phen
		self.ind2.resourcesAmount = res

		self.ind2.produceResources('technology', **self.pars)
		save2 = self.ind2.resourcesAmount

		#assert save1[0]['technologyLevel'] < save2[0]['technologyLevel'], "somehow the technology levels are the same here"
		assert save1 < save2, "ind1 knows 2 and gets {1}, ind2 knows 5 and gets {3}, when really those with more knowledge should get more resources, all else being equal".format(
			save1,save2)

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
			production = (1 - deme.progressValues["civilianPublicTime"]) * (deme.progressValues["labourForce"] ** (-pars['alphaResources'])) * deme.progressValues["technologyLevel"] ** pars['alphaResources']
			ind.produceResources(self.pop.fit_fun, **pars)
			assert ind.resourcesAmount == production, "ind produced {0} instead of {1}".format(ind.resourcesAmount, production)

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
			infoToAdd['x'] = ind.phenotypicValues
			ind.reproduce('technology', **{**self.pop.fitnessParameters, **infoToAdd})

			w = (self.pop.fitnessParameters['rb'] + ind.resourcesAmount) / (1 + self.pop.fitnessParameters['gamma'] * infoToAdd['n'])
			assert ind.fertilityValue == w, "wrong fitness calculation for individual, should return {0}".format(w)
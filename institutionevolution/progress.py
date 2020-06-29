def pgg(**kwargs):
	prog = {'proportionOfLeaders':0.0, 'consensusTime':0.0}
	return prog

def geom(**kwargs):
	prog = {'proportionOfLeaders':0.0, 'consensusTime':0.0}
	return prog

def policing(**kwargs):
	prog = {'proportionOfLeaders':0.0, 'consensusTime':0.0}
	return prog

def policingdemog(**kwargs):
	prog = {'proportionOfLeaders':0.0, 'consensusTime':0.0}
	return prog

def policingdemog2(**kwargs):
	prog = {'proportionOfLeaders':0.0, 'consensusTime':0.0}
	return prog

def technology(**kwargs):
	prog = {'proportionOfLeaders':0.0, 'consensusTime':0.0}
	phenos = [0 if p is None else p for p in kwargs['phen']]
	effectivePublicGood = kwargs['pg'] * (1 - kwargs['p']) + kwargs['q'] * kwargs['d'] * kwargs['p'] * (kwargs['totRes'] - kwargs['pg'])
	prog['numberOfLeaders'] = 0
	prog['effectivePublicGood'] = effectivePublicGood
	prog['civilianPublicTime'] = 0
	prog['leaderPublicTime'] = 1
	prog['labourForce'] = (kwargs['n'] - prog['numberOfLeaders']) * (1 - prog['civilianPublicTime']) + prog['numberOfLeaders'] * (1 - prog['leaderPublicTime'])
	return prog

def debate(**kwargs):
	prog = {'proportionOfLeaders':0.0}
	if kwargs['n'] > 0:
		prog['consensus'] = kwargs['phen'][2]
		tmpDisagreement = kwargs["aconsensus"] * kwargs['n'] * kwargs['varphen'][2]
		prog['consensusTime'] = kwargs['epsilon'] + tmpDisagreement / (kwargs['bconsensus'] + tmpDisagreement)
		prog['institutionQuality'] = (prog['consensus'] * kwargs['pg'] * kwargs['aquality'] / kwargs['totRes']) ** kwargs['alphaquality']
		prog['fineBudget'] = prog['consensus'] * kwargs['pg'] * (1 - kwargs['aquality'])
	return prog

def socialclass(**kwargs):
	prog = {'consensusTime':0.0}
	prog['proportionOfLeaders'] = kwargs['phen'][3]
	return prog

functions = {}
for key, value in list(locals().items()):
    if callable(value) and value.__module__ == __name__:
        functions[key] = value


	#prog['numberOfLeaders'] = None
	#prog['civilianPublicTime'] = None
	#prog['leaderPublicTime'] = None
	#prog['labourForce'] = None
	
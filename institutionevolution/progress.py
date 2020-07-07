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
	n = kwargs["n"]
	p = kwargs["p"]
	pg = kwargs['pg']
	assert type(pg) is float, "pg is {0} when it should be a float".format(type(pg))
	assert pg >= 0, "pg negative"

	fine = pg * p / n
	benef = ((pg * (1 - p)) ** kwargs["betaTech"]) / n
	assert fine >= 0, "fine is negative"
	assert benef >= 0, "benef is negative"

	prog = {'proportionOfLeaders':0.0, 'consensusTime':0.0,'fine':fine, 'investmentReward':benef}
	return prog

def debate(**kwargs):
	prog = {'proportionOfLeaders':0.0}
	if kwargs['n'] > 0:
		prog['institutionQuality'] = (kwargs['consensus'] * kwargs['pg'] * kwargs['aquality'] / kwargs['totRes']) ** kwargs['alphaquality']
		prog['fineBudget'] = kwargs['consensus'] * kwargs['pg'] * (1 - kwargs['aquality'])
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
	
def pgg(**kwargs):
	pol = {'consensusTime':0.0}
	return pol

def geom(**kwargs):
	pol = {'consensusTime':0.0}
	return pol

def policing(**kwargs):
	pol = {'consensusTime':0.0}
	return pol

def policingdemog(**kwargs):
	pol = {'consensusTime':0.0}
	return pol

def policingdemog2(**kwargs):
	pol = {'consensusTime':0.0}
	return pol

def technology(**kwargs):
	pol = {'consensusTime':0.0}
	return pol

def debate(**kwargs):
	pol = {}
	pol['consensus'] = kwargs['phen'][2]
	tmpDisagreement = kwargs["aconsensus"] * kwargs['n'] * kwargs['varphen'][2]
	pol['consensusTime'] = kwargs['epsilon'] + tmpDisagreement / (kwargs['bconsensus'] + tmpDisagreement)
	pol['productionTime'] = 1 - pol["consensusTime"]
	pol['labourForce'] = pol['consensusTime'] * kwargs['n']
	return pol

def socialclass(**kwargs):
	pol = {'consensusTime':0.0}
	return pol

def full(**kwargs):
	pol = {}
	pol['consensus'] = kwargs['phen'][2]
	return pol

functions = {}
for key, value in list(locals().items()):
    if callable(value) and value.__module__ == __name__:
        functions[key] = value
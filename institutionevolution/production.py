def pgg(res, **kwargs):
	return res

def geom(res, **kwargs):
	return res

def policing(res, **kwargs):
	return res

def policingdemog(res, **kwargs):
	return res

def policingdemog2(res, **kwargs):
	return res

def technology(res, **kwargs):
	consensusTime = 1 - kwargs['productionTime']
	resourcesProduced = (1 - consensusTime) * ((kwargs['n'] * (1 - consensusTime)) ** (-kwargs['alphaResources'])) * kwargs['tech'] ** kwargs['alphaResources']
	payoff = (1 - kwargs['x'][0]) * (resourcesProduced * (1 - kwargs['q'] * kwargs['d'] * kwargs['p']) - kwargs['q'] * (kwargs['pg'] * kwargs['p'])/kwargs['n'])
	return payoff
		
def debate(res, **kwargs):
	payoff = 1
	return payoff

def socialclass(res, **kwargs):
	return res

functions = {}
for key, value in list(locals().items()):
    if callable(value) and value.__module__ == __name__:
        functions[key] = value
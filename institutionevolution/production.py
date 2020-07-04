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
	x = kwargs['x'][0]
	q = kwargs['q']
	fine = kwargs['pg'] * kwargs['p'] / kwargs['n']
	benef = (kwargs['pg'] * (1 - kwargs['p']))
	consensusTime = 1 - kwargs['productionTime']
	resourcesProduced = (1 - consensusTime) * ((kwargs['n'] * (1 - consensusTime)) ** (-kwargs['alphaResources'])) * kwargs['tech'] ** kwargs['alphaResources']
	payoff = (1 - kwargs['x'][0]) * (resourcesProduced * (1 - kwargs['q'] * kwargs['d'] ) - kwargs['q'] * ( * kwargs['p'])/kwargs['n'])
	payoff = (1-q)*(1-x)*resourcesProduced+q*((1-x)*resourcesProduced-fine) + benef
	return payoff
		
def debate(res, **kwargs):
	payoff = kwargs['productivity'] * kwargs['labourForce'] ** (-kwargs['alphaResources']) * kwargs['techcapital'] ** kwargs['alphaResources']
	return payoff

def socialclass(res, **kwargs):
	return res

functions = {}
for key, value in list(locals().items()):
    if callable(value) and value.__module__ == __name__:
        functions[key] = value
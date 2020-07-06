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
	n = kwargs["n"]
	p = kwargs["p"]
	pg = kwargs['pg']
	fine = pg * p / n
	benef = ((pg * (1 - p)) ** kwargs["betaTech"]) / n
	resourcesProduced = n ** (-kwargs['alphaResources']) * kwargs['tech'] ** kwargs['alphaResources']
	payoff = (1 - kwargs['q']) * (1 - x) * resourcesProduced + kwargs['q'] * ((1 - x) * resourcesProduced - fine) + benef
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
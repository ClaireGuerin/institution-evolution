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
	resourcesProduced = kwargs["n"] ** (-kwargs['alphaResources']) * kwargs['tech'] ** kwargs['alphaResources']
	return resourcesProduced
		
def debate(res, **kwargs):
	payoff = kwargs['productivity'] * kwargs['labourForce'] ** (-kwargs['alphaResources']) * kwargs['techcapital'] ** kwargs['alphaResources']
	return payoff

def socialclass(res, **kwargs):
	return res

functions = {}
for key, value in list(locals().items()):
    if callable(value) and value.__module__ == __name__:
        functions[key] = value
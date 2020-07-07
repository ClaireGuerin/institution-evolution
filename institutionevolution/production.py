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
	assert type(kwargs["n"]) is int, "n is {0} when it should be an integer".format(type(kwargs["n"]))
	assert kwargs["n"] > 0, "n is non-positive"
	assert type(kwargs['tech']) is float, "technology is {0} when it should be a float".format(kwargs['tech'])
	assert kwargs['tech'] >= 0, "technology is negative"

	resourcesProduced = kwargs["n"] ** (-kwargs['alphaResources']) * kwargs['tech'] ** kwargs['alphaResources']
	
	assert type(resourcesProduced) is float, "resources are {0} when they should be float".format(type(resourcesProduced))
	assert resourcesProduced >= 0, "individual produced negative resources"
	return resourcesProduced
		
def debate(res, **kwargs):
	payoff = kwargs['productionTime'] * kwargs['labourForce'] ** (-kwargs['alphaResources']) * kwargs['techcapital'] ** kwargs['alphaResources']
	return payoff

def socialclass(res, **kwargs):
	return res

functions = {}
for key, value in list(locals().items()):
    if callable(value) and value.__module__ == __name__:
        functions[key] = value
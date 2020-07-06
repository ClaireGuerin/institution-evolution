from math import exp, sqrt

def pgg(res, **kwargs):
	f = float(kwargs["fb"] * (res - kwargs["c"] * kwargs["x"][0] ** 2 + kwargs["b"] * kwargs["xmean"][0]) / (1 + kwargs["gamma"] * kwargs["n"]))
	return f

def geom(res, **kwargs):
	f = float(kwargs["fb"] * exp(-sqrt(sum([x ** 2 for x in kwargs["x"]]))) / (1 + kwargs["gamma"] * kwargs["n"]))
	return f

def policing(res, **kwargs):
	ipg = kwargs["pg"] / kwargs["n"] # individual's share of the public good
	phen = kwargs["x"]
	cooperationCost = (1 - phen[0]) * res
	cooperationGain = kwargs["b"] * (1 - phen[1]) * ipg
	policing = kwargs["c"] * phen[1] * ipg * ((1 - phen[0]) ** 2)
	payoff =  cooperationCost + cooperationGain - policing
	
	f = float(kwargs["fb"] * payoff / (kwargs["gamma"] * kwargs["n"]))
	return f

def policingdemog(res, **kwargs):
	focalphen = kwargs["x"][0]
	groupphen = kwargs["xmean"][0]
	groupsize = kwargs["n"]

	gamma = ((1 - kwargs["p"]) * groupphen * groupsize) ** kwargs["gamma"]
	eta = (kwargs["p"] * groupphen * groupsize) ** kwargs["eta"]
	returnsOnInvestment = kwargs["alpha"] * gamma / (kwargs["beta1"] + kwargs["beta0"] * gamma)
	costOfInvestment = kwargs["kb"] * focalphen
	policingEffect = kwargs["epsilon"] * eta / (kwargs["zeta1"] + kwargs["zeta0"] * eta)
	relativepunishment =  0 if groupphen == 1 else (1 - focalphen) / (1 - groupphen)
	resources = (kwargs["rb"] + returnsOnInvestment - relativepunishment * policingEffect) / groupsize - costOfInvestment 
	consumption = resources / (1 + resources * kwargs["th"])

	f = float(consumption * kwargs["phi"])

	return f

def policingdemog2(res, **kwargs):
	focalphen = kwargs["x"][0]
	groupphen = kwargs["xmean"][0]
	groupsize = kwargs["n"]
	neighphen = 0 if groupsize == 1 else (groupsize * groupphen - focalphen) / (groupsize - 1)
	
	resources = (kwargs["rb"] / groupsize) * (1 - (focalphen * kwargs["c1"] + (focalphen ** 2) * kwargs["c2"]) + (kwargs["bb"] * ((focalphen + (groupsize - 1) * neighphen) * (1 - kwargs["p"])) ** kwargs["gamma"]) / groupsize - kwargs["pp"] * (1 - focalphen) * (groupphen * kwargs["p"]) ** kwargs["eta"])
	consumption = resources / (1 + resources * kwargs["th"])
	
	f = float(consumption)

	return f

def technology(res, **kwargs):
	x = kwargs['x'][0]
	n = kwargs["n"]
	q = kwargs['q']
	p = kwargs["p"]
	pg = kwargs['pg']
	fine = pg * p / n
	benef = ((pg * (1 - p)) ** kwargs["betaTech"]) / n
	
	payoff = (1 - kwargs['q']) * (1 - x) * res + kwargs['q'] * ((1 - x) * res - fine) + benef
	f = (kwargs["rb"] + payoff) / (1 + kwargs["gamma"] * kwargs["n"])
	return f

def debate(res, **kwargs):
	f = (kwargs["rb"] + res) / (1 + kwargs["gamma"] * kwargs["n"])
	return f

def socialclass(res, **kwargs):
	f = (res + 2 * kwargs['leadership']) / (1 + kwargs["gamma"] * kwargs["n"])
	return f

functions = {}
for key, value in list(locals().items()):
    if callable(value) and value.__module__ == __name__:
        functions[key] = value
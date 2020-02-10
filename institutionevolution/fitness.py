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
	phen = kwargs["x"][0]
	groupphen = kwargs["xmean"][0]
	groupsize = kwargs["n"]

	gamma = ((1 - kwargs["p"]) * groupphen * groupsize) ** kwargs["gamma"]
	eta = (kwargs["p"] * groupphen * groupsize) ** kwargs["eta"]
	returnsOnInvestment = kwargs["alpha"] * gamma / (kwargs["beta1"] + kwargs["beta0"] * gamma)
	costOfInvestment = kwargs["kb"] * phen
	policingEffect = kwargs["epsilon"] * eta / (kwargs["zeta1"] + kwargs["zeta0"] * eta)
	resources = kwargs["rb"] / groupsize + returnsOnInvestment / groupsize - costOfInvestment -(1 - phen) * policingEffect / ((1 - groupphen) * groupsize)
	consumption = resources / (1 + resources * kwargs["th"])

	f = float(consumption * kwargs["phi"])

	return f

functions = {}
for key, value in list(locals().items()):
    if callable(value) and value.__module__ == __name__:
        functions[key] = value
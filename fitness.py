def pgg(res, **kwargs):
	f = float(kwargs["fb"] * (res - kwargs["c"] * kwargs["x"] ** 2 + kwargs["b"] * kwargs["xmean"]) / (1 + kwargs["gamma"] * kwargs["n"]))
	return max(0., f)

def dummy(a):
	print(a)

functions = {"pgg": pgg}

#print(x for x in locals() if x is callable)
#func = []
#localsnapshot = locals().items()
#for key, value in localsnapshot:
#	if value is callable:
#		func.append(key)
		
#print(func)
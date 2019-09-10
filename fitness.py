def pgg(res, **kwargs):
	f = float(kwargs["fb"] * (res - kwargs["c"] * kwargs["x"][0] ** 2 + kwargs["b"] * kwargs["xmean"][0]) / (1 + kwargs["gamma"] * kwargs["n"]))
	return max(0., f)

def dummy(a):
	print('{0}! haha it works! '.format(a))

functions = {}
for key, value in list(locals().items()):
    if callable(value) and value.__module__ == __name__:
        functions[key] = value
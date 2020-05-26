def pgg(**kwargs):
	prog = {}
	prog['numberOfLeaders'] = None
	prog['civilianPublicTime'] = None
	prog['leaderPublicTime'] = None
	prog['labourForce'] = None
	return prog

def geom(**kwargs):
	prog = {}
	prog['numberOfLeaders'] = None
	prog['civilianPublicTime'] = None
	prog['leaderPublicTime'] = None
	prog['labourForce'] = None
	return prog

def policing(**kwargs):
	prog = {}
	prog['numberOfLeaders'] = None
	prog['civilianPublicTime'] = None
	prog['leaderPublicTime'] = None
	prog['labourForce'] = None
	return prog

def policingdemog(**kwargs):
	prog = {}
	prog['numberOfLeaders'] = None
	prog['civilianPublicTime'] = None
	prog['leaderPublicTime'] = None
	prog['labourForce'] = None
	return prog

def policingdemog2(**kwargs):
	prog = {}
	prog['numberOfLeaders'] = None
	prog['civilianPublicTime'] = None
	prog['leaderPublicTime'] = None
	prog['labourForce'] = None
	return prog

def technology(**kwargs):
	prog = {}
	phenos = [0 if p is None else p for p in kwargs['phen']]
	election = 0 #phenos[3]
	prog['numberOfLeaders'] = kwargs['n'] * election
	prog['civilianPublicTime'] = 0
	prog['leaderPublicTime'] = 1
	prog['labourForce'] = (kwargs['n'] - prog['numberOfLeaders']) * (1 - prog['civilianPublicTime']) + prog['numberOfLeaders'] * (1 - prog['leaderPublicTime'])
	return prog

functions = {}
for key, value in list(locals().items()):
    if callable(value) and value.__module__ == __name__:
        functions[key] = value
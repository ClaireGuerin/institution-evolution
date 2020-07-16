import sys
from launch_multiple_simulations import Launcher

try:
	metafolder = str(sys.argv[1])
	fitparfile = str(sys.argv[2])
	genparfile = str(sys.argv[3])
except IndexError as e:
	metafolder = '../simulations'
	fitparfile = 'pars/fitness_technology.txt'
	genparfile = 'pars/general_parameters.txt'
	print('no arguments provided, creating in folder "{0}"'.format(metafolder))
	with open(fitparfile, 'w', buffering=1) as f1, \
	open(genparfile, 'w', buffering=1) as f2:
		f1.writelines(['fun,pgg\n','fb,2\n','b,0.5,0.7,0.1\n','c,0.05,0.07,0.01\n','gamma,0.01\n'])
		f2.writelines('ndemes,10\n','demesize,20\n','ngen,20\n','baseres,1\n','phen,[0.0]*4\n','tech,1\n','mutrate,0.01\n','mutstep,0.02\n','migrate,0.5\n')

l = Launcher(metafolder=metafolder, parfile=fitparfile, launchfile=genparfile)
l.writeParameterFilesInFolders()
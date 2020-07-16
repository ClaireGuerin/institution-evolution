import sys
from launch_multiple_simulations import Launcher

l = Launcher(metafolder='gibberish', parfile=str(sys.argv[1]))
l.readParameterInfo()
l.createRanges()
l.createCombinations()

print(len(l.combinations))
from institutionevolution.population import Population as Pop

mypop = Pop(fit_fun='policingdemog2', inst="mysim", mutationBoundaries=True)
mypop.runSimulation()

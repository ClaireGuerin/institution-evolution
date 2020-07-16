from launch_multiple_simulations import Launcher

l = Launcher(metafolder='doesnamatter', parfile='doesnamatter', launchfile='doesnamatter')
l.launchSimulation(path=str(sys.argv[1]), mutbound=True)
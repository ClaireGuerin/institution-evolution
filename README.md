# institution-evolution

Branch|<img src="logos/travis_tessa_pride_logo.png" alt="travis ci logo" width="50"/>|<img src="logos/codecov_logo.png" alt="codecov logo" width="50"/>
---|---|---
master|[![Build Status](https://travis-ci.org/ClaireGuerin/institution-evolution.svg?branch=master)](https://travis-ci.org/ClaireGuerin/institution-evolution)|[![codecov](https://codecov.io/gh/ClaireGuerin/institution-evolution/branch/master/graph/badge.svg)](https://codecov.io/gh/ClaireGuerin/institution-evolution/branch/master)
develop|[![Build Status](https://travis-ci.org/ClaireGuerin/institution-evolution.svg?branch=develop)](https://travis-ci.org/ClaireGuerin/institution-evolution)|[![codecov](https://codecov.io/gh/ClaireGuerin/institution-evolution/branch/develop/graph/badge.svg)](https://codecov.io/gh/ClaireGuerin/institution-evolution/branch/develop)

# Installation

Download the repository *institution-evolution* on your local machine.

# Launch simulation

## Requirements

Scipy, Numpy, 
Pytest to test code 

This code is written under Python 3.7.3


## Parameters

Set parameters as desired in *pars* folder:
- fitness_parameters.txt: specific to fitness function used. For now, only Public Goods Games (PGG)
- initial_phenotypes.txt: \n for each new trait
- parameters.txt: general parameters
	- mutation rate,
	- mutation variance,
	- migration rate
- initialisation.txt: 
	- number of demes (i.e. sub-populations)
	- initial size of demes (number of individuals in each sub-population)
	- number of generations (iterations) to run.

## Command line
### Run a single simulation
python script_single_simulation.py

### Test parameter space
python script_parameter_space.py

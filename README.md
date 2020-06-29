# institution-evolution

Branch|<img src="logos/travis_tessa_pride_logo.png" alt="travis ci logo" width="50"/>|<img src="logos/codecov_logo.png" alt="codecov logo" width="50"/>
---|---|---
master|[![Build Status](https://travis-ci.org/ClaireGuerin/institution-evolution.svg?branch=master)](https://travis-ci.org/ClaireGuerin/institution-evolution)|[![codecov](https://codecov.io/gh/ClaireGuerin/institution-evolution/branch/master/graph/badge.svg)](https://codecov.io/gh/ClaireGuerin/institution-evolution/branch/master)
develop|[![Build Status](https://travis-ci.org/ClaireGuerin/institution-evolution.svg?branch=develop)](https://travis-ci.org/ClaireGuerin/institution-evolution)|[![codecov](https://codecov.io/gh/ClaireGuerin/institution-evolution/branch/develop/graph/badge.svg)](https://codecov.io/gh/ClaireGuerin/institution-evolution/branch/develop)

# Installation

Download the repository *institution-evolution* on your local machine.

# Launch simulation

> :warning: **Non-values are marked with -99 in output files**: Be mindful there when analyzing data! For instance, when technology level is not recorded in the simulation, the corresponding output file will show a mean technology level of -99 for every generation.

## Requirements

Scipy and Numpy for running simulations, Pytest to test code. To install all requirements, run: pip install -r requirements.txt

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

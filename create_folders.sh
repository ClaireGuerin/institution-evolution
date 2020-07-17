#!/bin/sh

# Load modules needed for job.
# Reminder: you can search for software with the "vit_soft" command.
source /dcsrsoft/spack/bin/setup_dcsrsoft
module load gcc python

# Move to working directory
cd /scratch/wally/FAC/FBM/DEE/llehmann/social_evolution/institution-evolution

# Create folders in metafolder with python
python prepare_simulation_folders.py ../$SLURM_JOB_NAME pars/fitness_technology.txt pars/general_parameters.txt
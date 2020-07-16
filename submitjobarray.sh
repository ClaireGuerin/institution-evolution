#!/bin/bash
#SBATCH --account llehmann_social_evolution
#SBATCH --job-name <name>
#SBATCH --partition wally
#SBATCH --array 1-x # Create a job array of x replicates with indice 1-x
#SBATCH --output %x_%A-%a.out
#SBATCH --error %x_%A-%a.err
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 2 # Number of CPUs for each replicate of the array
#SBATCH --mem 2G # Memory for each replicate of the array
#SBATCH --time 00:00:00 # time limit for each replicate of the array
#SBATCH --mail-user claire.guerin@unil.ch
#SBATCH --mail-type ALL
#SBATCH --export NONE

# Load modules needed for job.
# Reminder: you can search for software with the "vit_soft" command.
source /dcsrsoft/spack/bin/setup_dcsrsoft
module load gcc python

# Job commands.
# Create folders in metafolder with python

# Loop over all subfolders
for directory in `find /scratch/wally/FAC/FBM/DEE/llehmann/social_evolution/simulations -type d -maxdepth 1 -mindepth 1`
do
    # launch simulation on subfolder
    echo $SLURM_ARRAY_TASK_ID
    python script.py $directory
done
exit 0
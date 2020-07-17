#!/bin/bash
#SBATCH --account llehmann_social_evolution
#SBATCH --job-name techno1
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

# Job commands:
cd /scratch/wally/FAC/FBM/DEE/llehmann/social_evolution

# Read list of subfolders
IN=$(sed -n ${SLURM_ARRAY_TASK_ID}p /metafolder/folders_list.txt)
echo "Running analysis on $IN"

# Launch simulation for each folder
python institution-evolution/launch_simulation_from_folder.py $IN
exit 0
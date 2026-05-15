#!/bin/bash
##ENVIRONMENT SETTINGS; CHANGE WITH CAUTION
#SBATCH --export=NONE                #Do not propagate environment
#SBATCH --get-user-env=L             #Replicate login environment

##DEFAULT JOB SPECIFICATIONS
#SBATCH --time=6:00:00 #Set the wall clock limit
#SBATCH --ntasks-per-node=1        #Request tasks
#SBATCH --nodes=1                  #Request tasks
#SBATCH --mem=5G                   #Request Memory in MB per node
#SBATCH --output=%x-%j.out         #Send stdout/err

INPUT_FILE="${SLURM_JOB_NAME%.*}.py"

. ~/.bashrc
if [ -n "$CONDA_ENVIRONMENT" ]; then
  conda activate $CONDA_ENVIRONMENT
fi
python -u $INPUT_FILE $@
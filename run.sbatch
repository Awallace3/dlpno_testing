#!/bin/bash
#SBATCH -JDLPNO-CCSD-s22
#SBATCH -Ahive-cs207
#SBATCH -N23 
#SBATCH --mem-per-cpu=12G
#SBATCH -t4:00:00
#SBATCH -phive
#SBATCH -oreport-%j.out
#SBATCH --mail-type=START,END,FAIL
#SBATCH --mail-user=awallace43@gatech.edu

cd $HOME/data/dlnpo/dlpno_testing

module load anaconda3
conda activate orca_dlpno

srun -N23 python3 main.py

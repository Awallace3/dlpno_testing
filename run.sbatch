#!/bin/bash
#SBATCH -JDLPNO-CCSD-s22
#SBATCH -Ahive-cs207
#SBATCH -N12 --ntasks=12 --cpus-per-task=6
#SBATCH --mem-per-cpu=16G
#SBATCH -t4:00:00
#SBATCH -phive
#SBATCH -oreport-%j.out
#SBATCH --mail-type=START,END,FAIL
#SBATCH --mail-user=awallace43@gatech.edu

cd $HOME/data/dlnpo/dlpno_testing

module load anaconda3
conda activate orca_dlpno

srun -N12 -n72 python3 main.py


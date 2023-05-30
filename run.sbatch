#!/bin/bash
#SBATCH -JDLPNO-CCSD-s22
#SBATCH -Ahive-cs207
#SBATCH -N23 --ntasks=23 --cpus-per-task=1
#SBATCH --mem-per-cpu=16G
#SBATCH -t4:00:00
#SBATCH -phive
#SBATCH -oreport-%j.out
#SBATCH --mail-type=START,END,FAIL
#SBATCH --mail-user=awallace43@gatech.edu

cd $HOME/data/dlnpo/dlpno_testing
module load anaconda3/2022.05.0.1
module load openmpi/4.1.4
conda activate /storage/hive/project/chem-sherrill/sherrill-software/.conda/envs/orca_dlpno

echo "starting job..."
mpiexec -n 23 python3 main.py
echo "finished job!"


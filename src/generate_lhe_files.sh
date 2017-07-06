#!/bin/bash
#SBATCH -p general
#SBATCH -t 0-1:00
#SBATCH --mem=30
#SBATCH --mail-type=ALL
#SBATCH --mail-user=kfraser@college.harvard.edu
#SBATCH -o slurm.%N.%j.out
#SBATCH -e slurm.%N.%j.err

for particle in 'upquark' 
do
  for energy in 100 200 500 1000
  do
    ptmin=$((99 * $energy / 100))
    ptmax=$((111 * $energy / 100))
    for seed_number in {11..20}
    do 
      ./events_lh -${particle} -seed $seed_number -out "lhe_files/test${particle}-seed${seed_number}-${energy}.lhe" -qqqq -pthatmin $ptmin -pthatmax $ptmax
    done
  done
done

#!/bin/bash
#SBATCH -p general
#SBATCH -t 0-2:00
#SBATCH --mem=30
#SBATCH --mail-type=ALL
#SBATCH --mail-user=kfraser@college.harvard.edu
#SBATCH -o slurm.%N.%j.out
#SBATCH -e slurm.%N.%j.err

for energy in 1000 500 200 100
do
    ptjetmax=$((12 * $energy / 10))
    seed_number=$((${SLURM_ARRAY_TASK_ID} + 10))
    for particle in 'upquark' 
    do
        ./process_events_lh -out ../events/${energy}GEV-${particle}-event-seed${SLURM_ARRAY_TASK_ID}.txt -in "lhe_files/test${particle}-seed${seed_number}-${energy}.lhe" -ptjetmin $energy -ptjetmax $ptjetmax -seed ${SLURM_ARRAY_TASK_ID}
    done
done


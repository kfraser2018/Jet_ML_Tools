#!/bin/bash
#SBATCH -p gpu
#SBATCH --gres=gpu:1
#SBATCH -t 0-00:10 
#SBATCH --mem=2000
#SBATCH --mail-type=ALL
#SBATCH --mail-user=$USER@fas.harvard.edu
#SBATCH -o slurm.%N.%j.out
#SBATCH -e slurm.%N.%j.err

#module load gcc/4.9.3-fasrc01 cuda/7.5-fasrc02 cudnn/7.0-fasrc02
python3 jet_image_conv_example.py

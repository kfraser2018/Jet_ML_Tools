##This is for setting up the working envirionment on Harvard Odyssey Cluster
##To use it, do: source Setup_ody.sh
#load the correct version of python
source new-modules.sh
#load the correct version of python
module load python/3.6.0-fasrc01 
#load the necessary environment
source activate /n/home03/btong/.conda/envs/ml
#load modules for GPU
module load gcc/4.9.3-fasrc01 cuda/7.5-fasrc02 cudnn/7.0-fasrc02




####if you do GPU, make sure you have: ~/.theanorc
####with content
# [global]
# floatX = float32
# device = gpu0
# force_device = True

# [lib]
# cnmem = 0.90

# [dnn]
# enabled = True

# [nvcc]
# optimizer_including=cudnn
#Katie Fraser, Harvard, 2017
#
#Config File for train network

import sys
import numpy as np

do_one = np.random.uniform(.05, .3)
do_two = np.random.uniform(.2, .5)
batch_size = np.random.randint(100, 2000)
step_size = np.random.uniform(.00005,.0005)

# hyperparameters
hps = {
    'batch_size': batch_size,
    'img_size': 33,
    'epochs': 10,
    'filter_size': [8,4,4],
    'nb_filters': [64, 64, 64],
    'nb_neurons': [64, 64],
    'nb_pool': [2, 2, 2],
    'dropout': [do_one, do_two, do_two, do_two],
    'patience': 5,
    'nb_channels': 3,
    'model_name': 'Test_Parameters',
    'energy': '100GEV',
    'last_act': 'softmax',
    'n_files': 1,
    'particle1_type': 'upquark',
    'particle2_type': 'downquark',
    'kappa': 0.3,
    'data_augment': True,
    'step_size': step_size,
    'kappa_two': 0.4
}

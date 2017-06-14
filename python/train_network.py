#Katie Fraser, Harvard, 2017
#
#Trains Networks for Each Data Set

from jet_networks import train_CNN
from keras import backend as K

# hyperparameters
hps = {
    'batch_size': 128,
    'img_size': 33,
    'epochs': 3,
    'filter_size': [8,4,4],
    'nb_filters': [64, 64, 64],
    'nb_neurons': [64, 64],
    'nb_pool': [2, 2, 2],
    'dropout': [.1, .1, .1, .1],
    'patience': 5,
    'nb_channels': 2,
    'model_name': 'Img_Conv_Net',
    'energy': '1000GEV',
    'last_act': 'softmax',
    'n_files': 1,
    'particle1_type': 'gluon',
    'particle2_type': 'quark',
    'kappa': 'nocharge'
}

train_CNN(hps)

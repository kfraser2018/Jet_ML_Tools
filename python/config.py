#Katie Fraser, Harvard, 2017
#
#Trains Networks for Each Data Set

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
    'energy': '100GEV',
    'last_act': 'softmax',
    'n_files': 10,
    'particle1_type': 'upquark',
    'particle2_type': 'downquark',
    'kappa': 0.3
}

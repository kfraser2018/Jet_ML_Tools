#Katie Fraser, Harvard, 2017
#
#Config File for train network

# hyperparameters
hps = {
    'batch_size': 512,
    'img_size': 33,
    'epochs': 1,
    'filter_size': [8,4,4],
    'nb_filters': [64, 64, 64],
    'nb_neurons': [64, 64],
    'nb_pool': [2, 2, 2],
    'dropout': [.1, .3, .3, .3],
    'patience': 5,
    'nb_channels': 3,
    'model_name': 'Test_Parameters',
    'energy': '100GEV',
    'last_act': 'softmax',
    'n_files': 10,
    'particle1_type': 'upquark',
    'particle2_type': 'downquark',
    'kappa': 0.2,
    'data_augment': True,
    'step_size': .0003,
    'kappa_two': 0.3,
    'decay': 0.00002
}

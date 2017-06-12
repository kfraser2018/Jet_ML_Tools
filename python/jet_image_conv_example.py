# Patrick Komiske, Eric Metodiev, MIT, 2017
#
# A simple example showing how we can import existing jet images, train
# a Keras convolutional model, save the model, and plot and save some of 
# the ROC curves.


import heppy
from heppy import NN_models
from data_import import data_import
from keras.callbacks import EarlyStopping

# specify the number of data files to use
n_files = 2

# import existing jet images
jet_images = data_import('jetimage', range(1, n_files + 1), nb_chan = 2)

# hyperparameters
hps = { 
    'batch_size': 128,
    'img_size': 33,
    'epochs': 2,
    'filter_size': [8,4,4],
    'nb_filters': [32, 16, 16],
    'nb_neurons': [64, 64],
    'nb_pool': [2, 2, 2],
    'dropout': [.1, .1, .1, .05],
    'patience': 5,
    'nb_channels': 2,
    'model_name': 'Conv_Net_Example',
    'last_act': 'softmax'
}

# get labels for the images
Y = heppy.make_labels(n_files*10000, n_files*10000)

# split the data into train, validation, and test sets
X_train, Y_train, X_val, Y_val, X_test, Y_test = heppy.data_split(jet_images, Y)

# preprocess the data
X_train, X_val, X_test = heppy.zero_center(X_train, X_val, X_test, channels = [0])
X_train, X_val, X_test = heppy.standardize(X_train, X_val, X_test, channels = [0])

model = NN_models.conv_net_construct(hps)

history = model.fit(X_train, Y_train,
                    batch_size = hps['batch_size'],
                    epochs     = hps['epochs'],
                    callbacks  = [EarlyStopping(monitor = 'val_loss', 
                                                patience = hps['patience'], 
                                                verbose = 1, 
                                                mode = 'auto')],
                    validation_data = (X_val, Y_val))

# get a unique name to save the model as
name = heppy.get_unique_file_name('../models', hps['model_name'])
heppy.save_model(model, name + '.h5')

# construct ROC curve
qe, ge = heppy.ROC_from_model(model, X_test, Y_test)
heppy.save_ROC(model, X_test, Y_test, name, plot = True)

# plot other ROC curves
heppy.plot_inv_ROC(qe, ge)
heppy.plot_SI(qe, ge)




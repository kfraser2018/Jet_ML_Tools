# Katie Fraser, Harvard, 2017
# Based on example by Patrick Komiske, Eric Metodiev, MIT, 2017
#
# Function to Train Network for given input parameters

import numpy as np
import math
import heppy
from heppy import NN_models
from heppy import jet_RGB_images
from data_import_modified import data_import
from keras.callbacks import EarlyStopping

def train_CNN(hps):
    # import existing jet images
    jet_images = data_import('jetimage', range(1, hps['n_files'] + 1), nb_chan = hps['nb_channels'], prefix = hps['energy'], particle1_type = hps['particle1_type'], particle2_type = hps['particle2_type'], K = hps['kappa'])

    # get labels for the images
    Y = heppy.make_labels(hps['n_files']*10000, hps['n_files']*10000)

    # split the data into train, validation, and test sets
    X_train, Y_train, X_val, Y_val, X_test, Y_test = heppy.data_split(jet_images,Y)

    # Apply data augmentation; Katie will fix
    #X_train, Y_train = heppy.apply_jitter(X_train, Y_train)

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
    name = heppy.get_unique_file_name('../models', hps['model_name'],'_' + hps['energy'] + '_' + hps['last_act'])
    heppy.save_model(model, name + '.h5')

    # construct ROC curve
    heppy.save_ROC(model, X_test, Y_test, name, plot = True, show = False)



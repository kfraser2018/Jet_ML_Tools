#Katherine Fraser, Harvard, 2017
#
# Generator for Real Time Theano data augmentation

import numpy as np
from heppy import apply_jitter
from keras.preprocessing.image import ImageDataGenerator

def generator(hps, X_train, Y_train):
    if hps['nb_channels'] in {1,3}:
        datagen = ImageDataGenerator()
        for X_batch, Y_batch in datagen.flow(X_train, Y_train, batch_size=hps['batch_size']):
            X_aug, Y_aug = apply_jitter(X_batch,Y_batch)
            yield X_aug, Y_aug
    if hps['nb_channels'] == 2:
        counter = 0
        while True:
            if (counter + hps['batch_size']) < len(X_train):
                X_batch = np.stack([X_train[i,:,:,:] for i in range(counter, counter + hps['batch_size'])])
                Y_batch = np.stack([Y_train[i,:] for i in range(counter, counter + hps['batch_size'])])
            else:
                print("DEBUG")
                X_batch = np.stack(([X_train[i,:,:,:] for i in range(counter, len(X_train))],[X_train[i,:,:,:] for i in range(0, (counter + hps['batch_size'])%len(X_train))]))
                Y_batch = np.stack(([Y_train[i,:] for i in range(counter, len(X_train))],[X_train[i,:] for i in range(0, (counter + hps['batch_size'])%len(X_train))]))
            counter += hps['batch_size']
            X_aug, Y_aug = apply_jitter(X_batch,Y_batch)
            yield X_aug, Y_aug



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
        X_batch = np.zeros((hps['batch_size'],hps['nb_channels'],hps['img_size'],hps['img_size']))
        Y_batch = np.zeros((hps['batch_size'],hps['nb_channels']))
        counter = 0
        while True:
            m = 0
            for i in range(counter, counter + hps['batch_size']):
                for j in range(hps['nb_channels']):
                    for k in range(hps['img_size']):
                        for l in range(hps['img_size']):
                            X_batch[m,j,k,l] = X_train[i % len(X_train),j,k,l]
                    Y_batch[m,j] = Y_train[i % len(X_train),j]
                m += 1
                counter += hps['batch_size']
                counter = counter % len(X_train)
            X_aug, Y_aug = apply_jitter(X_batch,Y_batch)
            yield X_aug, Y_aug


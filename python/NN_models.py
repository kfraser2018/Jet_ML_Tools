from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D, SpatialDropout2D, LocallyConnected2D, ZeroPadding2D
from utils import *
from os.path import basename

def conv_net_construct(hps):

    nb_conv = hps['nb_conv']
    nb_pool = hps['nb_pool']
    img_size = hps['img_size']
    nb_filters = hps['nb_filters']
    nb_channels = hps['nb_channels']
    nb_neurons = hps['nb_neurons']
    dropout = hps['dropout']

    model = Sequential()
    model.add(Convolution2D(nb_filters[0], nb_conv[0], nb_conv[0], 
                            input_shape = (nb_channels, img_size, img_size), 
                            init = 'he_uniform', border_mode = 'valid')) 
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size = (nb_pool[0], nb_pool[0])))
    model.add(SpatialDropout2D(dropout[0]))

    model.add(Convolution2D(nb_filters[1], nb_conv[1], nb_conv[1], 
                            init='he_uniform', border_mode = 'valid'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool[1], nb_pool[1])))
    model.add(SpatialDropout2D(dropout[1]))

    model.add(Convolution2D(nb_filters[2], nb_conv[2], nb_conv[2], 
                            init='he_uniform', border_mode = 'valid')) 
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool[2], nb_pool[2])))
    model.add(SpatialDropout2D(dropout[2]))
    
    model.add(Flatten())

    model.add(Dense(nb_neurons))
    model.add(Activation('relu'))
    model.add(Dropout(dropout[3]))

    model.add(Dense(2))
    model.add(Activation('softmax'))

    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', 
                  metrics = ['accuracy'])
    model.summary()

    return model


def dense_net_construct(hps, AE = False):
    layer_dims = hps['layer_dims']
    input_dim = hps['input_dim']

    model = Sequential()
    for i,dim in enumerate(layer_dims):
        if i == 0:
            model.add(Dense(dim, input_dim = input_dim, init = 'he_uniform'))
        else:
            model.add(Dense(dim, init = 'he_uniform'))
        model.add(Activation('relu'))
    if AE == True:
        model.add(Dense(input_dim, init = 'he_uniform'))
        model.compile(loss = 'mse', optimizer = 'adam', 
                  metrics = ['accuracy'])
        
    else:
        model.add(Dense(2))
        model.add(Activation('softmax'))
        model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', 
                  metrics = ['accuracy'])

    
    model.summary()

    return model


def pileup_model(hps):

    img_size     =  hps['img_size']
    nb_channels  =  hps['nb_channels']
    
    filter_size  =  parg(hps['filter_size'])
    nb_filters   =  parg(hps['nb_filters'])
    stride       =  parg(hps['stride'])
    layers       =  parg(hps['layers'])
    zero_pad     =  hps.setdefault('zero_pad', stride[0])

    proj_layer   =  hps.setdefault('proj_layer', Convolution2D)
 
    model = Sequential()
    
    for i in range(len(layers)):
        if i == 0:
            model.add(ZeroPadding2D(padding = (zero_pad, zero_pad),
                                    input_shape = (nb_channels, img_size, img_size)))
            model.add(layers[i](nb_filters[i], filter_size[i], filter_size[i], 
                                subsample = (stride[i], stride[i]),
                                init = 'he_uniform', border_mode = 'valid')) 
        else:
            model.add(layers[i](nb_filters[i], filter_size[i], filter_size[i], 
                                subsample = (stride[i], stride[i]),
                                init = 'he_uniform', border_mode = 'valid')) 
        model.add(Activation('relu'))

    if nb_filters[len(layers)-1] > 1:
        model.add(proj_layer(1, 1, 1, init = 'he_uniform', border_mode = 'valid', activation = 'relu'))

    model.compile(loss = 'mse', optimizer = 'adam')
    model.summary()
    return model

hps_examples = {

    'hps_1layer_conv': {
        'filter_size': 5,
        'img_size': 45,
        'nb_filters': 1,
        'stride': 5,
        'nb_channels': 3,
        'layers': [Convolution2D],
    },

    'hps_2layer_conv_large': {
        'filter_size': [8, 3],
        'img_size': 45,
        'nb_filters': [1, 1],
        'stride': [2,2],
        'nb_channels': 3,
        'layers': [Convolution2D, Convolution2D],
    },

    'hps_2layer_conv_med': {
        'filter_size': [4, 5],
        'img_size': 45,
        'nb_filters': [1, 1],
        'stride': [2,2],
        'nb_channels': 3,
        'layers': [Convolution2D, Convolution2D],
    },

    'hps_1layer_conv_multichan': {
        'filter_size': 5,
        'img_size': 45,
        'nb_filters': 2,
        'stride': 5,
        'nb_channels': 3,
        'layers': [Convolution2D]
    },

    'hps_2layer_conv_multichan': {
        'filter_size': [8, 3],
        'img_size': 45,
        'nb_filters': [2, 2],
        'stride': [2,2],
        'nb_channels': 3,
        'layers': [Convolution2D, Convolution2D]
    },

}

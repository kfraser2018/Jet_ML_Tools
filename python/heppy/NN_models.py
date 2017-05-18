# Patrick Komiske, Eric Metodiev, MIT, 2017
#
# Contains two basic Keras models, a convolutional one with three convolutional
# layers and one dense layer and a dense model with an extensible number of 
# layers.

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from keras.optimizers import Adam
from keras import backend as K

from .utils import *

# ensure Theano dimension ordering
K.set_image_data_format('channels_first')

def conv_net_construct(hps):

    """ Builds a Convolutional Neural Network with an extensible number of Conv2D layers 
    followed by an extensible number of full-connected layers. Takes a dictionary of 
    hyperparameters as input.
    """

    filter_size   = hps['filter_size']
    img_size      = hps['img_size']
    nb_pool       = hps['nb_pool']
    nb_filters    = hps['nb_filters']
    nb_channels   = hps['nb_channels']
    nb_neurons    = hps['nb_neurons']
    dropout       = hps['dropout']
    act           = hps.setdefault('act', 'relu')
    dropout_layer = hps.setdefault('dropout_layer', Dropout)
    opt           = hps.setdefault('opt', Adam)
    lr            = hps.setdefault('lr', 0.001)
    comp          = hps.setdefault('compile', True)
    summary       = hps.setdefault('summary', True)
    output_dim    = hps.setdefault('output_dim', 2)

    model = Sequential()
    for i,(nbf, fs, nbp, drop) in enumerate(zip(nb_filters, filter_size, nb_pool, dropout)):
        kwargs = {} if i > 0 else {'input_shape': (nb_channels, img_size, img_size)}
        model.add(Conv2D(nbf, fs, 
                            kernel_initializer = 'he_uniform', 
                            padding = 'valid',
                            activation = act,
                            **kwargs)) 
        model.add(MaxPooling2D(pool_size = nbp))
        model.add(dropout_layer(drop))
    
    model.add(Flatten())

    for n,d in zip(parg(nb_neurons), dropout[3:]):
        model.add(Dense(n, activation = act))
        model.add(Dropout(d))

    model.add(Dense(output_dim, activation = 'softmax'))

    if comp:
        model.compile(loss = 'categorical_crossentropy', optimizer = opt(lr = lr), metrics = ['accuracy'])
        if summary:
            model.summary()

    return model

def dense_net_construct(hps):

    """ Builds a Fully-Connected (or dense) Neural Network with an extensible number of layers.
    Takes a dictionary of hyperparameters as input.
    """

    layer_dims   = hps['layer_dims']
    input_dim    = hps['input_dim']
    output_dim   = hps.setdefault('output_dim', 2)
    output_act   = hps.setdefault('output_act', 'softmax')
    comp         = hps.setdefault('compile', True)
    act          = hps.setdefault('act', 'relu')
    lr           = hps.setdefault('lr', .001)
    summary      = hps.setdefault('summary', True)
    loss         = hps.setdefault('loss', 'categorical_crossentropy')
    opt          = hps.setdefault('opt', Adam)
    metrics      = hps.setdefault('metrics', ['accuracy'])
    l2_reg       = hps.setdefault('l2_reg', 10**-8)

    model = Sequential()
    for i,dim in enumerate(layer_dims):
        kwargs = {} if i > 0 else {'input_dim': input_dim}
        model.add(Dense(dim, 
                        kernel_initializer = 'he_uniform', 
                        activation = act, 
                        kernel_regularizer = l2(l2_reg), 
                        bias_regularizer = l2(l2_reg),
                        **kwargs))
    model.add(Dense(output_dim, 
                    activation = output_act,
                    kernel_regularizer = l2(l2_reg), 
                    bias_regularizer = l2(l2_reg)))
    
    if comp:
        model.compile(loss = loss, optimizer = opt(lr = lr), metrics = metrics)
        if summary:
            model.summary()

    return model





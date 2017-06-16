# https://keras.io/layers/writing-your-own-keras-layers/
# https://github.com/bioinf-jku/SNNs/blob/master/selu.py
# https://codegists.com/snippet/python/selu_keraspy_thisismohitgupta_python

import pdb
import numpy as np
import keras
import keras.backend as K
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from keras.optimizers import Adam

from theano import tensor as T
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams

from .utils import *

# heppy/NN_models.py:
#   - Change 'act' param in hyperparameter dict from 'relu' to the
#     function object 'selu'
#   - This should work as long as the 'alpha' and 'scale' parameters
#     don't need to change. If that's required, write a new activation
#     layer to maintain this state.

_alpha = 1.6732632423543772848170429916717
_scale = 1.0507009873554804934193349852946

# Activation function (keras/activation.py)
def selu(x, alpha=_alpha, scale=_scale):
  return scale * K.elu(x, alpha)

# keras.initializers.VarianceScaling(scale=1.0, mode='fan_in', distribution='normal', seed=None)

# Dropout layer (keras/layers/core.py)
class DropoutSELU(Dropout):
  ''''''
  def __init__(self, rate, alpha=_alpha, scale=_scale, **kwargs):
    super(DropoutSELU, self).__init__(rate, **kwargs)
    self.alpha = alpha
    self.scale = scale
    self.seed = None

  def call(self, inputs, training=None):
    if 0. < self.rate < 1.:

      # (keras/backend/theano_backend.py)
      def dropout(x, level, alpha=self.alpha, scale=self.scale,
                  noise_shape=None, seed=None):
        ''''''

        if level < 0. or level >= 1:
          raise ValueError('Dropout level must be in interval[0, 1[.')
        if seed is None:
          seed = np.random.randint(1, 10e6)
        if isinstance(noise_shape, list):
          noise_shape = tuple(noise_shape)

        rng = RandomStreams(seed)
        # rng = np.random.RandomState(seed)
        keep_prob = 1. - level
        alpha_prime = -scale * alpha

        # randomly (with probability `level`) set components of x to
        # `alpha_prime`
        ## xshape = tuple([dim for dim in x._keras_shape if dim is not None])

        if noise_shape is None:
          random_tensor = rng.binomial(x.shape, p=keep_prob, dtype=x.dtype)
        else:
          random_tensor = rng.binomial(noise_shape, p=keep_prob, dtype=x.dtype)
          random_tensor = T.patternbroadcast(random_tensor, [dim==1 for dim in noise_shape])

        x = K.switch(random_tensor, x, alpha_prime)

        # affine rescale of x to ensure mean = 0 and variance = 1
        a = 1. / np.sqrt(keep_prob + keep_prob * (1 - keep_prob) * alpha_prime ** 2)
        b = -a * alpha_prime * (1 - keep_prob)

        a = np.float32(a)
        b = np.float32(b)

        return a * x + b

      def dropped_inputs():
        return dropout(inputs, self.rate,
                       noise_shape=self._get_noise_shape(inputs),
                       seed=self.seed)

      return K.in_train_phase(dropped_inputs, inputs, training=training)

    return inputs

# Two basic Keras models, modified from NN_models.py to use SELU
# activation/initialization/dropout rules. Updated lines are marked with
# '###'

K.set_image_data_format('channels_first')

def conv_net_construct(hps):
  ''''''

  filter_size   = hps['filter_size']
  img_size      = hps['img_size']
  nb_pool       = hps['nb_pool']
  nb_filters    = hps['nb_filters']
  nb_channels   = hps['nb_channels']
  nb_neurons    = hps['nb_neurons']
  dropout       = hps['dropout']
  act           = hps.setdefault('act', selu) ###
  dropout_layer = hps.setdefault('dropout_layer', DropoutSELU) ###
  opt           = hps.setdefault('opt', Adam)
  lr            = hps.setdefault('lr', 0.001)
  comp          = hps.setdefault('compile', True)
  summary       = hps.setdefault('summary', True)
  output_dim    = hps.setdefault('output_dim', 2)

  initializer = keras.initializers.VarianceScaling(scale=1.0, mode='fan_in', distribution='normal', seed=None) ###

  model = Sequential()

  for i,(nbf, fs, nbp, drop) in enumerate(zip(nb_filters, filter_size, nb_pool, dropout)):
    kwargs = {} if i > 0 else {'input_shape': (nb_channels, img_size, img_size)}
    model.add(Conv2D(nbf, fs,
                     kernel_initializer = initializer, ###
                     padding = 'valid',
                     activation = act,
                     **kwargs))
    model.add(MaxPooling2D(pool_size = nbp))

    model.add(dropout_layer(drop))

  model.add(Flatten())

  for n,d in zip(parg(nb_neurons), dropout[3:]):
    model.add(Dense(n, activation = act))
    model.add(DropoutSELU(d)) ###

  model.add(Dense(output_dim, activation = 'softmax'))

  if comp:
    model.compile(loss = 'categorical_crossentropy', optimizer = opt(lr = lr), metrics = ['accuracy'])
    if summary:
      model.summary()

  return model



























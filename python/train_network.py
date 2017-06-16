#Katie Fraser, Harvard, 2017
#
#Trains Networks for Each Data Set

from jet_networks import train_CNN
from keras import backend as K
import config

train_CNN(config.hps)
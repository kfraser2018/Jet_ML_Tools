# Katherine Fraser, Harvard University, 2017
#
# Calculates pT weighted jet charge and makes ROC curve for it

import heppy
import pickle
from data_import_modified import data_import
from sklearn import metrics
import numpy as np
import math
import matplotlib.pyplot as plt

##hps parameters is saved here
import config 

hps = config.hps

#events per file
n_files = hps['n_files']
n_ev_perf = 10000

jets, jet_tots = heppy.get_jets(hps)
jet_charges = heppy.jet_charges(hps, jets)

#Uncomment to Plot Jet Charge Histogram
heppy.plot_jet_charges(jet_charges,hps)

# Get labels for jets
labels = np.concatenate((np.zeros(n_files * n_ev_perf),np.ones(n_files * n_ev_perf)))

# Get ROC curve
fpr, tpr, thresholds = metrics.roc_curve(labels, jet_charges)

# Plot ROC curve
plt.plot(1-tpr, fpr)
plt.show()
file_name = '../plots/jet_charge_' + hps['energy'] + '_' + hps['particle1_type']            + '_' + hps['particle2_type'] + '_K=' + str(hps['kappa']) + '_ROC_data.pickle' 
with open(file_name, 'wb') as f:
    pickle.dump({'particle2_eff': 1 - tpr, 'particle1_eff': fpr}, f)

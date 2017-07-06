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

#allocate array
jet_charges = np.zeros(2 * n_files * n_ev_perf)
kappa_array = np.zeros(99)
fifty_array = np.zeros(99)

for kappa in range(1, 100): 
    index = 0
    hps['kappa'] = kappa/100
    print(hps['kappa'])            
    # Loop through quark and gluon events
    for particle_type in [hps["particle1_type"], hps["particle2_type"]]:
        # Loop through seed number
        for seed_number in range(1,1 + hps["n_files"]):
            # import the jets
            jets, jet_tots = data_import('event', range(1,1 + hps["n_files"]), seed_number, particle_type, prefix = hps["energy"])

            # fill array of jet charges
            for jet in jets:
                jet_charges[index] = heppy.compute_jet_charge(jet, hps)
                index += 1

#Plot Jet Charge Histogram
#plt.hist(jet_charges[0:n_files * n_ev_perf],100)
#plt.hist(jet_charges[n_files * n_ev_perf:2*n_files * n_ev_perf],100,facecolor='green')
#plt.show()

    # Get labels for jets
    labels = np.concatenate((np.zeros(n_files * n_ev_perf),np.ones(n_files * n_ev_perf)))

    # Get ROC curve
    fpr, tpr, thresholds = metrics.roc_curve(labels, jet_charges)

    fifty = heppy.gr_at_50_qe(1 - tpr, fpr)
    kappa_array[kappa - 1] = hps['kappa']
    print(kappa_array[kappa - 1])
    fifty_array[kappa - 1] = fifty
    print(fifty_array[kappa - 1])
# Plot 
plt.plot(kappa_array, fifty_array)
plt.show()


# Katherine Fraser, Harvard University, 2017
#
# Calculates pT weighted jet charge and makes ROC curve for it

import heppy
import pickle
from data_import_modified import data_import
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.cross_validation import train_test_split
import numpy as np
import math
import matplotlib.pyplot as plt

##hps parameters is saved here
import config 

hps = config.hps

#parameters
n_files = hps['n_files']
n_ev_perf = 10000
upper_kappa = 1
lower_kappa = .1
step_kappa = .02
depth = 3
min_samples_leaf = 100

#Fill Jet Charges
print("Filling jets...")
jets, jet_tots = heppy.get_jets(hps)
print("Computing jet charge...")
predictors = np.stack([heppy.jet_charges(hps, jets, kappa = kappa, BDT = True) for kappa in np.arange(lower_kappa, upper_kappa, step_kappa)], axis=-1)

# Get labels for jets
labels = np.concatenate((np.zeros(n_files * n_ev_perf),np.ones(n_files * n_ev_perf)))

# Split Data
X_train, X_test, label_train, label_test = train_test_split(predictors, labels, test_size = 0.2)

# Create Boosted Decision Tree
print("Creating Decision Tree...")
bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=depth, min_samples_leaf=min_samples_leaf), n_estimators=600, learning_rate = 1)

# Fit Curve and get probabilities
bdt.fit(X_train,label_train)
probs = bdt.predict_proba(X_test)

# Create ROC curve
fpr, tpr, thresholds = metrics.roc_curve(label_test, probs[:,0])

# Plot ROC curve
plt.plot(1-tpr, fpr)
file_name = '../plots/BDT_' + hps['energy'] + '_' + hps['particle1_type'] + '_' + hps['particle2_type'] + '_' + str(lower_kappa) + '_' + str(upper_kappa) + '_' + str(step_kappa)+ '_' + str(depth) + '_ROC_data.pickle' 
with open(file_name, 'wb') as f:
    pickle.dump({'particle2_eff': 1 - tpr, 'particle1_eff': fpr}, f)
plt.show()

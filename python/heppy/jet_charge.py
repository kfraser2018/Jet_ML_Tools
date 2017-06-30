# Katherine Fraser, Harvard, 2017
#
# Computes Jet Charge

import numpy as np
from data_import_modified import data_import
import matplotlib.pyplot as plt

# mapping from particle id to charge of the particle
charge_map = {11: -1, -11:  1, 13: -1, -13:  1, 22:  0, -22:  0,
              111:  0, -111:  0, 130:  0, -130:  0, 211:  1, -211: -1,
              321:  1, -321: -1, 2112:  0, -2112:  0, 2212:  1, -2212: -1}

def get_jets(hps):

    """Loops through files to create an array of jets"""
    index = 0
    # Loop through quark and gluon events
    for particle_type in [hps["particle1_type"], hps["particle2_type"]]:
        # Loop through seed number
        for seed_number in range(1,1 + hps["n_files"]):
            # import the jets
            jets, jet_tots = data_import('event', range(1,1 + hps["n_files"]), 
                             seed_number, particle_type, prefix = hps["energy"])
            if index == 0:
                all_jets = jets
                all_jet_tots = jet_tots
            else:
                all_jets = np.append(all_jets, jets)
                all_jet_tots = np.append(all_jet_tots, jet_tots)
            index += 1

    return all_jets, all_jet_tots

def jet_charges(hps, jets, n_ev_perf=10000, BDT = False, kappa = 0):

    """Returns an array of jet charges"""
    if BDT == True:
        hps['kappa'] = kappa

    #allocate array
    n_files = hps['n_files']
    jet_charges = np.zeros(2 * n_files * n_ev_perf)
    index = 0

    # fill array of jet charges
    for jet in jets:
            jet_charges[index] = compute_jet_charge(jet, hps)
            index += 1

    return jet_charges

def compute_jet_charge(jet, hps, pT_i=2, id_i = 3):

    """A functions that inputs an array of jets and returns an array of jet 
    charges
    """
    # Select Jet Momentum and particle type
    pts  = jet[:,pT_i]
    particle_id = jet[:,id_i]

    # Total jet momentum
    jet_pt = np.sum(pts)


    # Compute jet charge
    jet_charge = 0
    for pt,label in zip(pts,particle_id):
        jet_charge += (charge_map[label] * pow(pt, hps["kappa"]))/(pow(jet_pt,hps["kappa"]))
 
    # Return jet charge
    return jet_charge 

def plot_jet_charges(jet_charges, hps, n_ev_perf = 10000):

    '''Plots jet charge histogram'''
    # Set up
    n_files = hps['n_files']

    #Plot Jet Charge Histogram
    plt.hist(jet_charges[0:n_files * n_ev_perf],100)
    plt.hist(jet_charges[n_files * n_ev_perf:2*n_files * n_ev_perf],100,facecolor='green')
    plt.show()

# Katherine Fraser, Harvard, 2017
#
# Computes Jet Charge

import numpy as np

# mapping from particle id to charge of the particle
charge_map = {11: -1, -11:  1, 13: -1, -13:  1, 22:  0, -22:  0,
              111:  0, -111:  0, 130:  0, -130:  0, 211:  1, -211: -1,
              321:  1, -321: -1, 2112:  0, -2112:  0, 2212:  1, -2212: -1}

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


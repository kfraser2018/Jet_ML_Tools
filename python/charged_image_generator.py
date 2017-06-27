# Patrick Komiske, MIT, 2017
#
# An example showing how we can read in data from event/particle information, 
# create the jet images, and save them to file.

import heppy
from heppy import jet_RGB_images
from data_import_modified import data_import
import numpy as np
import math
##hps parameters is saved here
import config 

hps = config.hps
#Loop through energies
for energy in [hps["energy"]]: 
    # Loop through quark and gluon events
    for particle_type in [hps["particle1_type"], hps["particle2_type"]]:
        # Loop through seed number
        for seed_number in range(1,1 + hps["n_files"]):
            # import the jets
            jets, jet_tots = data_import('event', range(1,1 + hps["n_files"]), seed_number, particle_type, prefix = energy)

            # form the jet images
            if hps['nb_channels'] == 2:
                jet_images = np.asarray([heppy.pixelate(jet, nb_chan = hps['nb_channels'], charge_image = True, K=hps["kappa"]) for jet in jets])
            if hps['nb_channels'] == 3:
                jet_images = np.asarray([heppy.pixelate(jet, nb_chan = hps['nb_channels'], charge_image = True, K=hps["kappa"], K_two = hps["kappa_two"]) for jet in jets])
 
            # save the jet images to file
            if hps['nb_channels'] == 2:    
                filename = energy + '-' +  particle_type + '-K=' + str(hps["kappa"]) + '-K2=' + str(0) + '-jetimage-seed' + str(seed_number)
            if hps['nb_channels'] == 3:
                filename = energy + '-' +  particle_type + '-K=' + str(hps["kappa"]) + '-K2=' + str(hps["kappa_two"]) + '-jetimage-seed' + str(seed_number)
            heppy.write_images_to_file(filename, jet_images)

# Patrick Komiske, MIT, 2017
#
# An example showing how we can read in data from event/particle information, 
# create the jet images, and save them to file.

import heppy
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
            jet_images = np.asarray([heppy.pixelate(jet, nb_chan = 2, charge_image = True, K=hps["kappa"]) for jet in jets])
 
            # save the jet images to file
            filename = energy + '-' +  particle_type + '-K=' + str(hps["kappa"]) + '-jetimage-seed' + str(seed_number)
            heppy.write_images_to_file(filename, jet_images)

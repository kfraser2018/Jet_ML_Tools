# Katie Fraser, Harvard, 2017
# Adapted from code by Patrick Komiske, MIT, 2017
#
# Reads in data from event/particle information, 
# create the jet images, and save them to file.

import heppy
from data_import_modified import data_import
import numpy as np
import math

# specify number of files to use
n_files = 1

#Loop through energies
for energy in ['1000GEV']: 
    # Loop through quark and gluon events
    for particle_type in ['gluon', 'quark']:
        # Loop through seed number
        for seed_number in range(1,1 + n_files):
            # import the jets
            jets, jet_tots = data_import('event', range(1,1 + n_files), seed_number, particle_type, energy)

            # form the jet images
            jet_images = np.asarray([heppy.pixelate(jet, nb_chan = 2,img_width = 0.8) for jet in jets])
 
            # save the jet images to file
            filename = energy + '-' + particle_type + '-K=nocharge-jetimage-seed' + str(seed_number)
            heppy.write_images_to_file(filename, jet_images)

# Modified by Katie Fraser, Harvard, 2017
# From code written by Patrick Komiske, MIT, 2017
# Function for importing jet images from multiple .npz files into one numpy
# array. Tries to be efficient by allocating all necessary memory at the 
# beginning. Can also read in events assuming a csv style file format with
# an extra newline per event, particles listed one per line, comments 
# beginning with a '#', and lines denoting overal jet properties beginning
# with 'Event #, [jet_rap], [jet_phi], [jet_pt]'.


import numpy as np
import csv
import os
import heppy

def data_import(data_type, seed_range, seed_number = 1, particle_type = '', 
                prefix = '', path = '', nevents = 10000, img_size = 33, nb_chan = 1, 
                particle1_type = 'gluon', particle2_type = 'quark', K = 0):

    """ Imports data produced by the Events.cc script into python. Note that both
    gluon and quark files must be present for the desired seed range. The gluons 
    are always listed before the quarks. We assume a constant number of events
    per file.

    data_type: Either 'jetimage' or 'event'. These
               respectively return a numpy array of jet images and a list of events with their particle constituents and a separate
               list of the overall jet four-vectors.
    seed_range: a list or other iterable object containing the seeds for each file
    path: path to directory with the files. Defaults to '../events' and 
          '../images' for the type possible data_types.
    nevents: number of events per file. Note that this needs to be constant across
             the files.
    img_size: the image size of the jet images.
    channels: the channels of the jet image to return.
    """

    assert data_type in ['jetimage', 'event'], 'data_type not recognized'

    if len(path) == 0:
        path = '../events' if data_type == 'event' else '../images'

    if data_type == 'jetimage':
        particle1_string = prefix + '-' + particle1_type + '-K=' + str(K) + '-jetimage-seed{}_33x33images_' + str(nb_chan) + 'chan.npz'
        particle2_string = prefix + '-' + particle2_type + '-K=' + str(K) + '-jetimage-seed{}_33x33images_' + str(nb_chan) + 'chan.npz'
        #gluon_string = prefix + 'gluon-jetimage-seed{}_33x33images_' + str(nb_chan) + 'chan.npz'
        #quark_string = prefix + 'quark-jetimage-seed{}_33x33images_' + str(nb_chan) + 'chan.npz'
        return heppy.load_images([particle1_string.format(x) for x in seed_range],
                                 [particle2_string.format(x) for x in seed_range],
                                 nevents * len(seed_range), nevents * len(seed_range), 
                                 nb_chan = nb_chan)
    elif data_type == 'event':
        jets = []
        jet_tots = []

        filename = prefix + '-' + particle_type + '-event-seed' + str(seed_number)
        with open(os.path.join(path, filename + '.txt'), 'r') as fh:
            reader = csv.reader(fh)
            jet = []
            for row in reader:
                if len(row) > 0 and '#' in row[0]:
                    continue
                if len(row) > 0 and 'Event' in row[0]:
                     jet_tots.append(list(map(float, row[1:])))
                elif len(row) == 0:
                    jets.append(np.asarray(jet))
                    jet = []
                else:
                    jet.append(list(map(float, row)))

    
        return jets, jet_tots

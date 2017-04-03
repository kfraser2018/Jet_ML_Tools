# Patrick Komiske, Eric Metodiev, MIT, 2017

from utils import *

def sample_poisson(mean, n_samples, min_val, max_val):

    assert min_val <= mean <= max_val
    count = 0
    samples = []
    while count < n_samples:
        sample = np.random.poisson(lam = mean, size = 1)
        if sample <= max_val and sample >= min_val:
            samples.append(sample)
            count += 1
    return np.sort(samples)

def import_poisson_events(filename, mean_NPU, n_events, min_NPU, max_NPU, file_size, comment_char):

    events, jets_info = [], []
    
    # draw the NPUs to use from a Poissonian with caps at max_NPU and min_NPU
    NPUs = sample_poisson(mean_NPU, n_events, min_NPU, max_NPU)
    NPU_set = set(NPUs)
   
    for NPU in NPU_set:

        # number to draw from the file with this NPU
        num = np.count_nonzero(NPUs == NPU)
        
        # check if the number of requested events is compatible
        if num >= file_size:
            print('Warning: Trying to draw more events than file contained!')

        events_n, jets_info_n = import_single_file(filename, num = num, comment_char = comment_char)

        events.extend(events_n)
        jets_info.extend(jets_info_n)

    return np.asarray(events), np.asarray(jets_info)

def import_single_file(filename, num = -1, comment_char = '#'):

    events, jets_info = [], []

    with open(filename, 'r') as f:
        for i, row in enumerate(f):
            
            if row[0] == comment_char: 
                continue

            # read out the first num pairs of jets in the event
            if i == 2*num:
                break

            # split the event record up into parts separated by spaces
            parts = np.array(row.split()).astype(float)    

            # jet_info: ij, NPU, rho, A, JpT, Jeta, Jphi, Jm
            jet_info = parts[:8]

            # event: pt, eta, phi, is_charged, vertex, PUPPI, SoftKiller
            event = parts[8:].reshape((int(len(parts[8:])/7), 7))

            events.append(event)
            jets_info.append(jet_info)

    return np.asarray(events), np.asarray(jets_info)



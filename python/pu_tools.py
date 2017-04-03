import numpy as np
from jet_RGB_images import downsample


# ps :: returns the 4-momenta corresponding to a list of (pT, eta, phi) in an event
def ps(event, pt_i = 0, eta_i = 1, phi_i = 2):

    event = np.array(event)

    # deal with case of a single particle
    if len(event.shape) < 2:
        pT  = event[pt_i]
        eta = event[eta_i]
        phi = event[phi_i]
        return np.array([pT*np.cosh(eta), pT*np.cos(phi), pT*np.sin(phi), pT*np.sinh(eta)])

    pTs  = event[:,pt_i]
    etas = event[:,eta_i]
    phis = event[:,phi_i]
    return np.vstack([pTs*np.cosh(etas), pTs*np.cos(phis), pTs*np.sin(phis), pTs*np.sinh(etas)]).T


# ps_img :: returns the 4-momenta corresponding to a (no-channel) jet image of the event
def ps_img(image, jet_center, dists):
    ps   = []
    npix = image.shape[0]
    etas = jet_center[0] + dists
    phis = jet_center[1] + dists
    for i in range(npix):
        for j in range(npix): 
            pT = image[i][j]
            if pT == 0:
                continue
            ps.append([pT*np.cosh(etas[j]), pT*np.cos(phis[i]), pT*np.sin(phis[i]), pT*np.sinh(etas[j])])
    return np.asarray(ps)


# get a single 4-vector form an image
def p4_from_img(image, jet_center, dists):
    p4 = np.zeros(4)
    npix = image.shape[0]
    etas = jet_center[0] + dists
    phis = jet_center[1] + dists
    for i in range(npix):
        for j in range(npix): 
            pT = image[i][j]
            if pT == 0:
                continue
            p4 += [pT*np.cosh(etas[j]), pT*np.cos(phis[i]), pT*np.sin(phis[i]), pT*np.sinh(etas[j])]
    return p4


# massp :: returns the jet mass of the given 4-momentum
def massp(P):
    return np.sqrt(abs(P[0]**2 - P[1]**2 - P[2]**2 - P[3]**2))


def min(T):
    m = np.inf
    for t in T:
        nm = np.min(t)
        if nm < m:
            m = nm
    return m


def max(T):
    m = -np.inf
    for t in T:
        nm = np.max(t)
        if nm > m:
            m = nm
    return m


# calculate jet masses from jet images
def masses_from_imgs(input_imgs, neutralLV_imgs, jet_centers, num_train = 0, 
                                                              img_width = .9,
                                                              npx = 9,
                                                              cpx = 45,
                                                              model = None):

    dists_n = [(i-np.floor(npx/2))/npx*img_width for i in range(npx)]
    dists_c = [(i-np.floor(cpx/2))/cpx*img_width for i in range(cpx)]

    masses_true, masses_PU, masses_DL = [], [], []
    for image, neutral_image, jet_center in zip(input_imgs[num_train:],
                                                neutralLV_imgs[num_train:],
                                                jet_centers[num_train:]):
        
        p4_true = p4_from_img(image[0], jet_center, dists_c) + p4_from_img(neutral_image[0], jet_center, dists_n)
        
        p4_PU = p4_from_img(np.sum(image[:2], axis = 0), jet_center, dists_c) + \
                p4_from_img(downsample(np.asarray([[image[2]]]), int(cpx/npx))[0,0], jet_center, dists_n)

        if model != None:
            p4_DL = p4_from_img(image[0], jet_center, dists_c) + \
                    p4_from_img(model.predict(np.asarray([image]))[0,0], jet_center, dists_n)
            masses_DL.append(massp(p4_DL))
        
        masses_true.append(massp(p4_true))
        masses_PU.append(massp(p4_PU))

    return masses_true, masses_PU, masses_DL


# calculate dijet masses from jet images
def dimasses_from_imgs(input_imgs, neutralLV_imgs, jet_centers, num_train = 0,
                                                                img_width = .9,
                                                                npx = 9,
                                                                cpx = 45,
                                                                model = None):

    dists_n = [(i-np.floor(npx/2))/npx*img_width for i in range(npx)]
    dists_c = [(i-np.floor(cpx/2))/cpx*img_width for i in range(cpx)]

    dimasses_true_JI, dimasses_PU_JI, dimasses_DL = [], [], []
    z = zip(input_imgs[num_train::2],   neutralLV_imgs[num_train::2],   jet_centers[num_train::2],
            input_imgs[num_train+1::2], neutralLV_imgs[num_train+1::2], jet_centers[num_train+1::2])
    for imagesA, neutral_imageA, jet_centerA, imagesB, neutral_imageB, jet_centerB in z:
        p4_true = p4_from_img(imagesA[0],        jet_centerA, dists_c) + \
                  p4_from_img(neutral_imageA[0], jet_centerA, dists_n) + \
                  p4_from_img(imagesB[0],        jet_centerB, dists_c) + \
                  p4_from_img(neutral_imageB[0], jet_centerB, dists_n)

        p4_PU   = p4_from_img(np.sum(imagesA[:2], axis = 0),                             jet_centerA, dists_c) + \
                  p4_from_img(downsample(np.asarray([[imagesA[2]]]), int(cpx/npx))[0,0], jet_centerA, dists_n) + \
                  p4_from_img(np.sum(imagesB[:2], axis = 0),                             jet_centerB, dists_c) + \
                  p4_from_img(downsample(np.asarray([[imagesB[2]]]), int(cpx/npx))[0,0], jet_centerB, dists_n)

        if model != None:
            p4_DL = p4_from_img(imagesA[0], jet_centerA, dists_c) + p4_from_img(imagesB[0], jet_centerB, dists_c) + \
                    p4_from_img(model.predict(imagesA[np.newaxis])[0,0], jet_centerA, dists_n) + \
                    p4_from_img(model.predict(imagesB[np.newaxis])[0,0], jet_centerB, dists_n)
            dimasses_DL.append(massp(p4_DL))
        
        dimasses_true_JI.append(massp(p4_true))
        dimasses_PU_JI.append(massp(p4_PU))

    return dimasses_true_JI, dimasses_PU_JI, dimasses_DL
        

# calculate jet masses from 4-momenta
def masses_from_p4s(events, num_train = 0, SK = True, PUPPI = True, vert_i = 4, sk_i = 6, puppi_i = 5):

    masses_true, masses_PU, masses_SK, masses_PUPPI = [], [], [], []
    for i, event in enumerate(events[num_train:]):

        ps_all = ps(event)
        p4_true = np.sum(ps_all[event[:,vert_i] == -1], axis = 0)
        p4_PU = np.sum(ps_all, axis = 0)

        if SK:
            p4_SK = np.sum(ps_all[event[:,sk_i] == 1], axis = 0)
            masses_SK.append(massp(p4_SK))

        if PUPPI:
            p4_PUPPI = np.sum((event[:,puppi_i] * ps_all.T).T, axis = 0)
            masses_PUPPI.append(massp(p4_PUPPI))
            
        masses_true.append(massp(p4_true))
        masses_PU.append(massp(p4_PU))

    return masses_true, masses_PU, masses_SK, masses_PUPPI


# calculate dijet masses from 4-momenta
def dimasses_from_p4s(events, num_train = 0, SK = True, PUPPI = True, vert_i = 4, sk_i = 6, puppi_i = 5):

    dimasses_true, dimasses_PU, dimasses_SK, dimasses_PUPPI = [], [], [], []
    for i,(eventA, eventB) in enumerate(zip(events[num_train::2], events[num_train+1::2])):
        Aps_all, Bps_all = ps(eventA), ps(eventB)

        p4_PU   = np.sum(Aps_all, axis = 0) + np.sum(Bps_all, axis = 0)
        p4_true = np.sum(Aps_all[eventA[:,vert_i] == -1], axis = 0) + \
                  np.sum(Bps_all[eventB[:,vert_i] == -1], axis = 0)

        if SK:
            p4_SK = np.sum(Aps_all[eventA[:,sk_i] == 1], axis = 0) + np.sum(Bps_all[eventB[:,sk_i] == 1], axis = 0)
            dimasses_SK.append(massp(p4_SK))

        if PUPPI:
            p4_PUPPI = np.sum((eventA[:,puppi_i] * Aps_all.T).T, axis = 0) + \
                       np.sum((eventB[:,puppi_i] * Bps_all.T).T, axis = 0)
            dimasses_PUPPI.append(massp(p4_PUPPI))
        
        dimasses_true.append(massp(p4_true))
        dimasses_PU.append(massp(p4_PU))

    return dimasses_true, dimasses_PU, dimasses_SK, dimasses_PUPPI




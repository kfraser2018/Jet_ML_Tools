import utils 
import numpy as np

# ps :: returns the 4-momenta corresponding to a list of (pT, eta, phi) in an event
def ps(event, eta_i = 0, phi_i = 1, pt_i = 2):

    event = np.asarray(event)

    # deal with case of a single particle
    if len(event.shape) < 2:
        pT  = event[pt_i]
        eta = event[eta_i]
        phi = event[phi_i]
        return np.asarray([pT*np.cosh(eta), pT*np.cos(phi), pT*np.sin(phi), pT*np.sinh(eta)])

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


# eta_phi_pts_from_imgs :: returns a list of [eta, phi, pts] corresponding to an array of (no-channel) jet images
def eta_phi_pts_from_imgs(images, img_width):
    all_eta_phi_pts   = []
    npix = images.shape[2]
    npix2 = npix**2
    dists = [(i-np.floor(npix/2))/npix*img_width for i in range(npix)]
    eta_phi_flat = np.asarray([[[dists[j], dists[i]] for j in range(npix)] for i in range(npix)]).reshape((npix2, 2))
    for image in images:
        flat_image = image.reshape((npix2))
        mask = flat_image > 0
        if np.count_nonzero(mask) > 0:
            all_eta_phi_pts.append(np.vstack([eta_phi_flat[mask].T, flat_image[mask]]).T)
        else:
            all_eta_phi_pts.append(np.asarray([[0.0,0.0,0.0]]))
    return np.asarray(all_eta_phi_pts, order = 'c')


# get a single 4-vector from an image
def p4_from_img(image, jet_center, dists):
    return np.sum(ps_img(image, jet_center, dists), axis = 0)


def ensure_valid_phis(events, thresh = 1.5, pt_i = 0, eta_i = 1, phi_i = 2):
    for event in events:
        ref_phi = event[:,phi_i][np.argmax(event[:,pt_i])]
        event[:,phi_i][event[:,phi_i] - ref_phi >  thresh] -= 2 * np.pi
        event[:,phi_i][event[:,phi_i] - ref_phi < -thresh] += 2 * np.pi 
    return events


# massp :: returns the jet mass of the given 4-momentum
def massp(P):
    return np.sqrt(abs(P[0]**2 - P[1]**2 - P[2]**2 - P[3]**2))


# Define the N95 observable
def nf(images, f = 0.95):
    # Assuming the images are L1 normalized
    # Calculate the number of pixels required to account for a fraction of of the total pT
    cumsum = np.cumsum(np.sort(images.reshape((len(images),images.shape[2]**2)),axis=1)[:,::-1], axis=1)
    return np.argmax(np.sign(cumsum - f),axis=1)

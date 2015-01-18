"""
Feature detectors (Szeliski 4.1.1)
"""
import numpy as np
import scipy.signal as sig
import scipy.ndimage as ndi
from compvis.utils import get_patch
from compvis.imgproc.filters.kernels import KERNEL_GAUSSIAN

def sum_sq_diff(img_0, img_1, u, x, y, x_len, y_len):
    """
    Finds the summed square difference between two image patches.
    Uses even weighting across the patch.

    Parameters :
        img_0, img_1 : two images being compared
        u            : displacement vector between the patches
        x, y         : coordinates of top-left corner of first patch
        x_len, y_len : width and height of first patch
    """
    patch_0 = get_patch(img_0, x, y, x_len, y_len)
    patch_1 = get_patch(img_1, x + u[0], y + u[1], x_len, y_len)

    return np.sum((patch_1 - patch_0)**2)

def autocorr(img, u, x, y, x_len, y_len):
    """
    Computes the auto-correlation function for an image patch with a
    displacement of u. Uses even weighting across the patch.
    (Just for reference, since this is sum_sq_diff() with both images being
    the same.)

    Parameters :
        img          : image
        u            : variation in position
        x, y         : coordinates of top-left corner of patch
        x_len, y_len : width and height of patch
    """
    return sum_sq_diff(img, img, u, x, y, x_len, y_len)

def autocorr_surface(img, u_x_range, u_y_range, x, y, x_len, y_len):
    """
    Computes an auto-correlation surface for an image patch with a given range
    of displacements.

    Parameters :
        img                  : image
        u_x_range, u_y_range : range of displacements (tuples)
        x, y                 : coordinates of top-left corner of patch
        x_len, y_len         : width and height of patch

    Returns :
        X, Y : grid mesh
        Z    : auto-correlation values
    """
    X, Y = np.meshgrid(range(u_x_range[0], u_x_range[1]),
                       range(u_y_range[0], u_y_range[1]))

    z = np.array([autocorr(img, (u_x, u_y), x, y, x_len, y_len) 
                  for u_x, u_y in zip(np.ravel(X), np.ravel(Y))])
    Z = z.reshape(X.shape)

    return X, Y, Z

def harris(img, sigma_d=1, sigma_i=2, alpha=0.06):
    """
    Returns the Harris interest scores for keypoint detection.
    (Default values for sigma_d and sigma_i from Szeliski pp. 190)
    (Default value for alpha from Szeliski pp. 189)
    """
    # Gradients in x and y
    I_x = ndi.gaussian_filter(img, sigma_d, (1, 0))
    I_y = ndi.gaussian_filter(img, sigma_d, (0, 1))

    # Outer products
    I_xx = I_x**2
    I_yy = I_y**2
    I_xy = I_x * I_y

    # Convolve with Gaussian to get auto-correlation matrix
    A_xx = ndi.gaussian_filter(I_xx, sigma_i)
    A_yy = ndi.gaussian_filter(I_yy, sigma_i)
    A_xy = ndi.gaussian_filter(I_xy, sigma_i)

    # Harris scores
    A_det = A_xx * A_yy - A_xy**2
    A_tr = A_xx + A_yy
    
    #return A_det - alpha * A_tr**2
    return A_det / A_tr

def get_best_scores(scores, n_points, border=10):
    """
    Border is minimum distance from image boundary
    """
    # Mask out points too close to boundary
    print scores.shape
    mask = np.zeros(scores.shape)
    mask[border:-border, border:-border] = 1
    scores *= mask
    print scores.shape

    # Sort by response strength
    coords_sorted = np.array(np.unravel_index(np.argsort(scores, axis=None), scores.shape)).T

    # TODO: implement ANMS (prevent dense clusters)

    # Get the best scores
    best_coords = []
    best_scores = []
    for coord in coords_sorted[-n_points:]:
        best_coords.append((coord[0], coord[1]))
        best_scores.append(scores[coord[0], coord[1]])

    return best_coords, best_scores

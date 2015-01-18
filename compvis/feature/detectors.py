"""
Feature detectors (Szeliski 4.1.1)
"""
import numpy as np
from compvis.utils import get_patch

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

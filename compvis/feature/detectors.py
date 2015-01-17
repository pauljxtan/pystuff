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

def autocorr(img, delta_u, x, y, x_len, y_len):
    """
    Computes the auto-correlation function for an image patch with a
    displacement of delta_u. Uses even weighting across the patch.
    (Just for reference, since this is sum_sq_diff() with both images being
    the same.)

    Parameters :
        img          : image
        delta_u      : variation in position
        x, y         : coordinates of top-left corner of patch
        x_len, y_len : width and height of patch
    """
    return sum_sq_diff(img, img, delta_u, x, y, x_len, y_len)

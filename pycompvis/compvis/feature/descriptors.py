"""
Feature descriptors. (Szeliski 4.1.2)
"""
import numpy as np
import scipy as sp
from compvis.utils import get_patch_centered

def cross_corr(patch_0, patch_1):
    """
    Returns the cross-correlation between two same-sized image patches.

    Parameters           :
        patch_0, patch_1 : image patches
    """
    return np.sum(img_0 * img_1)

def cross_corr_norm(patch_0, patch_1):
    """
    Returns the normalized cross-correlation between two same-sized image
    patches.

    Parameters           :
        patch_0, patch_1 : image patches
    """
    n = patch_0.shape[0] * patch_0.shape[1]

    # Mean intensities
    mu_0, mu_1 = patch_0.mean(), patch_1.mean()

    # Standard deviations
    sigma_0, sigma_1 = patch_0.std(), patch_1.std()

    return (1.0 / (n - 1) * (((patch_0 - mu_0) / sigma_0) *
                             ((patch_1 - mu_1) / sigma_1)).sum())

def match_points(img_0, img_1, points_0, points_1, radius=5):
    """
    Matches two sets of points by normalized cross-correlation.

    Returns     :
        matches : the indices of the points in the second image which match to
                  each point in the first image
    """
    c = np.zeros((points_0.shape[0], points_1.shape[0]))

    # Cross-correlate each pair of points
    for i in range(points_0.shape[0]):
        for j in range(points_1.shape[0]):
            point_0 = points_0[i]
            point_1 = points_1[j]

            # Get neighbourhoods of each point
            patch_0 = get_patch_centered(img_0, point_0[0], point_0[1], radius)
            patch_1 = get_patch_centered(img_1, point_1[0], point_1[1], radius)

            # Cross-correlate
            # TODO: Make this less hacky
            if patch_0.shape != patch_1.shape:
                # This means one of the patches is extending outside the image
                c[i, j] = 0
            else:
                c[i, j] = cross_corr_norm(patch_0, patch_1)

    # Sort by cross-correlation values
    idx = np.argsort(c)

    # Return matches
    # (i.e. highest cross-correlation of each point in the first image with a
    #       point in the second image)
    return idx[:, -1]

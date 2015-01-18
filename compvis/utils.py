"""
Miscellaneous utility functions.
"""

import numpy as np

def hom_to_aug(x_hom):
    """
    Converts a homogeneous vector to an (inhomogeneous) augmented vector.
    """
    # Convert to numpy array if necessary
    if not isinstance(x_hom, np.ndarray):
        x = np.array(x)

    # Divide through by the last element to get the augmented vector
    return x_hom / x_hom[-1]

def focal_length(W, theta):
    """
    Returns the focal length of the camera.

    Parameters :
        W      : sensor width
        theta  : field of view
    """
    return W / 2 / np.tan(theta / 2)

def clip_min_max(img, val_min, val_max):
    """
    Clips the signal at the specified limits.
    """
    img[img < val_min] = val_min
    img[img > val_max] = val_max

    return img

def get_patch(img, x, y, x_len, y_len):
    """
    Extracts a patch from an image with top-left corner at (x, y) and 
    size x_len by y_len.
    """
    return img[x : x + x_len, y : y + y_len]

def get_mask(img, x, y, x_len, y_len):
    """
    Returns a binary mask with top-left corner at (x, y) and
    size x_len by y_len.
    """
    w = np.zeros(img.shape)
    w[x : x + x_len, y : y + y_len] = 1.0

    return w

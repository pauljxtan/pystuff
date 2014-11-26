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

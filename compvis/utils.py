"""
Miscellaneous utlity functions.
"""

#import numpy as np

def hom_to_aug(x_hom):
    """
    Converts a homogeneous vector to an (inhomogeneous) augmented vector.
    """
    # Divide through by the last element to get the augmented vector
    x_aug = x_hom / float(x_hom[-1])

    # Return the augmented vector
    return x_aug


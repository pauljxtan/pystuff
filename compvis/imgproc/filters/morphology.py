"""
Morphology (Szeliski 3.3.2)

DO LATER
"""

import numpy as np
import scipy.signal as sig

def threshold(f, t):
    if f >= t:
        return 1
    return 0

#def dilate(f, n):
#    """
#    Dilation with box filter (structuring element) of side n.
#    """
#    # Size of structuring element
#    S = n**2




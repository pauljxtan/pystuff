"""
Image processing (Szeliski Ch. 3)
"""

import numpy as np

RANGE_8BIT = 2**8

############################## PIXEL TRANSFORMS ##############################

def gain_bias(f, x, gain, bias):
    return gain * f(x) + bias

def linear_blend(f0, f1, x, alpha):
    return (1 - alpha) * f0(x) + alpha * f1(x)

def gamma_correction(f, x, gamma):
    """
    (gamma ~ 2.2 is good fit for most digital cameras)
    """
    return f(x)**(1.0 / gamma)

############################ COMPOSITING & MATTING ############################

def over_operator(B, F, alpha):
    return (1 - alpha) * B + alpha * F

########################### HISTOGRAM EQUALIZATION ###########################

def histogram_equalization_8bit(img):
    """
    Does not apply directly to RGB images; convert to other color space first
    """
    # Histogram
    hist, bins = np.histogram(img, bins=RANGE_8BIT)
    # Cumulative distribution function
    cdf = hist.cumsum().astype(float)
    # Normalize CDF
    cdf = cdf / cdf[-1] * (RANGE_8BIT - 1)

    # Interpolate new image
    img_eq = np.interp(img, bins[:-1], cdf)

    return img_eq

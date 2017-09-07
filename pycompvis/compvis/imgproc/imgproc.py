"""
Image processing (Szeliski Ch. 3)
"""

import numpy as np
import scipy.ndimage.filters as filt

#RANGE_8BIT = 2**8

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

def histogram_equalization(img, bits):
    """
    Don't apply directly to RGB images; convert to other color space first
    """
    # Histogram
    hist, bins = np.histogram(img, bins=2**bits)
    # Cumulative distribution function
    cdf = hist.cumsum().astype(float)
    # Normalize CDF
    cdf = cdf / cdf[-1] * (2**bits - 1)

    # Interpolate new image
    img_eq = np.interp(img, bins[:-1], cdf)

    return img_eq

############################### BORDER PADDING ###############################

# These functions are kinda redundant but I'll just leave them for reference

def pad_const(img, pad_width, value):
    img_pad = np.pad(img, pad_width, mode='constant', constant_values=value)
    return img_pad

def pad_clamp(img, pad_width):
    img_pad = np.pad(img, pad_width, mode='edge')
    return img_pad

def pad_wrap(img, pad_width):
    img_pad = np.pad(img, pad_width, mode='wrap')
    return img_pad

def pad_mirror(img, pad_width):
    img_pad = np.pad(img, pad_width, mode='reflect')
    return img_pad

#def pad_extend(img, pad_width):
#    return img

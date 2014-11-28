"""
Image processing (Szeliski Ch. 3)
"""

import numpy as np

####################################### PIXEL TRANSFORMS #######################################

def gain_bias(f, x, gain, bias):
    return gain * f(x) + bias

def linear_blend(f0, f1, x, alpha):
    return (1 - alpha) * f0(x) + alpha * f1(x)

def gamma_correction(f, x, gamma):
    """
    (gamma ~ 2.2 is good fit for most digital cameras)
    """
    return f(x)**(1.0 / gamma)

##################################### COMPOSITING & MATTING #####################################

def over_operator(B, F, alpha):
    return (1 - alpha) * B + alpha * F

#################################### HISTOGRAM EQUALIZATION ####################################

def ahe_8bit(img):
    h = np.histogram(img, bins=256, range=(0, 255))
    c = np.cumsum(h)





    

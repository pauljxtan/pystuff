"""
Pyramids (Szeliski 3.5.3)
"""
import numpy as np
import scipy.signal as sig
from compvis.imgproc.filters import kernels

def downsample(img):
    """
    Downsample an image by a factor of 2.
    """
    img_down = np.zeros((2*img.shape[0], 2*img.shape[1]))
    img_down[::2, ::2] = img[:, :]

    return sig.convolve2d(img_down, kernels.KERNEL_BILINEAR, 'same')

def gaussian_pyramid(img, levels):
    G = [img, ]

    for level in range(levels - 1):
        G.append(downsample(G[-1]))

    return G


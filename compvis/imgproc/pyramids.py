"""
Pyramids (Szeliski 3.5.3)
"""
import numpy as np
import scipy.signal as sig
from compvis.imgproc.filters import kernels

def interpolate(img):
    """
    Interpolate an image with upsampling rate r=2.
    """
    img_up = np.zeros((2*img.shape[0], 2*img.shape[1]))

    # Upsample
    img_up[::2, ::2] = img

    # Blur (need to scale by 2 since kernel has unit area)
    return sig.convolve2d(img_up, 2*kernels.KERNEL_GAUSSIAN, 'same')

def decimate(img):
    """
    Decimate an image with downsampling rate r=2.
    """
    # Blur
    img_blur = sig.convolve2d(img_down, kernels.KERNEL_GAUSSIAN, 'same')

    # Downsample
    return img_blur[::2, ::2]

def gaussian_pyramid(img, levels):
    G = [img, ]

    for level in range(levels - 1):
        G.append(decimate(G[-1]))

    return G

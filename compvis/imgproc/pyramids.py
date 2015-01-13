"""
Pyramids (Szeliski 3.5.3)
"""
import numpy as np
import scipy.signal as sig
from compvis.imgproc.filters import kernels

def interpolate(img):
    """
    Interpolates an image with upsampling rate r=2.
    """
    img_up = np.zeros((2*img.shape[0], 2*img.shape[1]))

    # Upsample
    img_up[::2, ::2] = img

    # Blur (need to scale by 2 since kernel has unit area)
    return sig.convolve2d(img_up, 2*kernels.KERNEL_GAUSSIAN, 'same')

def decimate(img):
    """
    Decimates an image with downsampling rate r=2.
    """
    # Blur
    img_blur = sig.convolve2d(img_down, kernels.KERNEL_GAUSSIAN, 'same')

    # Downsample
    return img_blur[::2, ::2]

def pyramids(img, levels):
    """
    Constructs Gaussian and Laplacian pyramids.
    """
    G = [img, ]
    L = []

    for level in range(levels - 1):
        # Blur
        img_blur = sig.convolve2d(img, kernels.KERNEL_GAUSSIAN, 'same')

        # Subtract from original and add to Laplacian pyramid
        L.append(img - img_blur)
        
        # Downsample at r=2
        img = img[::2, ::2]

        # Add to Gaussian pyramid
        G.append(img)

    return G, L

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

    # Blur (need to scale up since kernel has unit area)
    return sig.convolve2d(img_up, 4*kernels.KERNEL_GAUSSIAN, 'same')

def decimate(img):
    """
    Decimates an image with downsampling rate r=2.
    """
    # Blur
    img_blur = sig.convolve2d(img, kernels.KERNEL_GAUSSIAN, 'same')

    # Downsample
    return img_blur[::2, ::2]

def pyramids(img):
    """
    Constructs Gaussian and Laplacian pyramids.
    """
    G = [img, ]
    L = []

    # Build the Gaussian pyramid
    while img.shape[0] >= 2 and img.shape[1] >= 2:
        img = decimate(img)
        G.append(img)

    # Build the Laplacian pyramid
    for i in range(len(G) - 1):
        L.append(G[i] - interpolate(G[i + 1]))

    return G[:-1], L

def blend_pyramids(L_1, L_2, G_mask):
    return ([L_1[i] * (1.0 - G_mask[i]) + L_2[i] * G_mask[i]
             for i in range(len(G_mask))])

def reconstruct(L):
    """
    Reconstructs an image from a Laplacian pyramid.
    """
    # Interpolate all levels to the same size
    for i in range(len(L)):
        for j in range(i):
            L[i] = interpolate(L[i])

    return np.sum(L, axis=0)

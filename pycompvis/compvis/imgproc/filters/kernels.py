"""
Filter kernels (Szeliski 3.2)
"""

import numpy as np

KERNEL_BILINEAR = 1.0/16 * np.array(((1, 2, 1),
                                    (2, 4, 2),
                                    (1, 2, 1)))

KERNEL_GAUSSIAN = 1.0/256 * np.array(((1, 4,  6,  4,  1),
                                      (4, 16, 24, 16, 4),
                                      (6, 24, 36, 24, 6),
                                      (4, 16, 24, 16, 4),
                                      (1, 4,  6,  4,  1)))

KERNEL_SOBEL = 1.0/8 * np.array(((-1, 0, 1),
                                 (-2, 0, 2),
                                 (-1, 0, 1)))

KERNEL_CORNER = 1.0/4 * np.array((( 1, -2,  1),
                                  (-2,  4, -2),
                                  ( 1, -2,  1)))

def gaussian_kernel(sigma_x, sigma_y=None):
    """
    Normalized Gaussian kernel
    """
    if not sigma_y:
        sigma_y = sigma_x

    X, Y = np.meshgrid(np.arange(-sigma_x, sigma_x+1, dtype=float),
                       np.arange(-sigma_y, sigma_y+1, dtype=float))
    G = np.exp(- (X**2 / (2*sigma_x**2) + Y**2 / (2*sigma_y**2)))

    # Normalize
    return G / G.sum()

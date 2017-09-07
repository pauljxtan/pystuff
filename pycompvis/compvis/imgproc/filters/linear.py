"""
Linear filters.
"""

import numpy as np
import scipy.signal as sig
from compvis.imgproc.filters import kernels

def bilinear(img):
    # Convert to numpy array if necessary
    if not isinstance(img, np.ndarray): img = np.array(img)

    return sig.convolve2d(img, kernels.KERNEL_BILINEAR, mode='full')

def gaussian(img):
    # Convert to numpy array if necessary
    if not isinstance(img, np.ndarray): img = np.array(img)

    return sig.convolve2d(img, kernels.KERNEL_GAUSSIAN, mode='full')

def sobel(img):
    # Convert to numpy array if necessary
    if not isinstance(img, np.ndarray): img = np.array(img)

    return sig.convolve2d(img, kernels.KERNEL_SOBEL, mode='full')

def corner(img):
    # Convert to numpy array if necessary
    if not isinstance(img, np.ndarray): img = np.array(img)

    return sig.convolve2d(img, kernels.KERNEL_CORNER, mode='full')

def unsharp_mask(img, img_blur, gamma):
    # Convert to numpy arrays if necessary
    if not isinstance(img, np.ndarray): img = np.array(img)
    if not isinstance(img_blur, np.ndarray): img_blur = np.array(img_blur)

    return img * (1.0 - gamma * img_blur * img)

def summed_area_table(img):
    """
    Use summed_area_table_fast() instead. Leaving this for reference.
    """
    # Convert to numpy array if necessary
    if not isinstance(img, np.ndarray): img = np.array(img)

    table = np.zeros(img.shape)

    # Raster scan
    #---- Do top and left edges
    table[0, 0] = img[0, 0]
    for i in range(1, img.shape[0]):
        table[i, 0] = table[i-1, 0] + img[i, 0]
    for j in range(1, img.shape[1]):
        table[0, j] = table[0, j-1] + img[0, j]
    #---- Do the rest
    for i in range(1, img.shape[0]):
        for j in range(1, img.shape[1]):
            table[i, j] = (table[i-1, j] + table[i, j-1] - table[i-1, j-1]
                          + img[i, j])

    return table

def summed_area_table_fast(img):
    # Convert to numpy array if necessary
    if not isinstance(img, np.ndarray): img = np.array(img)

    return img.cumsum(axis=0).cumsum(axis=1)

def summed_area_in_rect(img, table, corners):
    # Convert to numpy arrays if necessary
    if not isinstance(img, np.ndarray): img = np.array(img)
    if not isinstance(table, np.ndarray): table = np.array(table)

    i0, i1, j0, j1 = corners

    integral = 0
    for i in range(i0, i1):
        for j in range(j0, j1):
            integral += (table[i1, j1] - table[i1, j0-1] - table[i0-1, j1]
                         + table[i0-1, j0-1])

    return integral

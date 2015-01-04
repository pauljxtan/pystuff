"""
Linear filters.
"""

import numpy as np
import scipy.signal as sig

def bilinear(img):
    # Convert to numpy array if necessary
    if not isinstance(img, np.ndarray): img = np.array(img)

    kernel = 1.0/16 * np.array(((1, 2, 1),
                                (2, 4, 2),
                                (1, 2, 1)))

    return sig.convolve2d(img, kernel, mode='full')

def gaussian(img):
    # Convert to numpy array if necessary
    if not isinstance(img, np.ndarray): img = np.array(img)

    kernel = 1.0/256 * np.array(((1, 4,  6,  4,  1),
                                 (4, 16, 24, 16, 4),
                                 (6, 24, 36, 24, 6),
                                 (4, 16, 24, 16, 4),
                                 (1, 4,  6,  4,  1)))

    return sig.convolve2d(img, kernel, mode='full')

def sobel(img):
    # Convert to numpy array if necessary
    if not isinstance(img, np.ndarray): img = np.array(img)

    kernel = 1.0/8 * np.array(((-1, 0, 1),
                               (-2, 0, 2),
                               (-1, 0, 1)))

    return sig.convolve2d(img, kernel, mode='full')

def corner(img):
    # Convert to numpy array if necessary
    if not isinstance(img, np.ndarray): img = np.array(img)

    kernel = 1.0/4 * np.array((( 1, -2,  1),
                               (-2,  4, -2),
                               ( 1, -2,  1)))

    return sig.convolve2d(img, kernel, mode='full')

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

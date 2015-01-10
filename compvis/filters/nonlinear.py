"""
Nonlinear filters.
"""

import numpy as np
import scipy.signal as sig

def neighbours(img_dims, coord):
    """
    Get all neighbours of a pixel.

    Parameters :
        img_dims : image dimensions
        coord    : coordinates of pixel
    """
    rows, cols = img_dims
    i, j = coord

    # Check if coords are within image
    if (i < 0 or j < 0 or i >= rows or j >= cols):
        return ValueError("Coordinates outside of image")

    return ([(k, l) for k in range(i-1, i+2) for l in range(j-1, j+2)
             if (k != i or l != j) and (0 <= k < rows) and (0 <= l < cols)])

def median(img, kernel_size):
    """
    Median filter.

    Parameters :
        img         : input 2D image
        kernel_size : (length, width) of kernel
    """
    # Convert to numpy array if necessary
    if not isinstance(img, np.ndarray): img = np.array(img)

    return sig.medfilt2d(img, kernel_size)

def bilateral_weight(img, pixel_coord, neigh_coord, sigma_r, sigma_d):
    """
    Bilateral weight function.

    Parameters :
        img         : image
        pixel_coord : coordinates of pixel
        neigh_coord : coordinates of neighbouring pixel
        sigma_d     : spatial parameter (larger features smoothened)
        sigma_r     : range parameter (approaches Gaussian convolution)
    """
    i, j = pixel_coord
    k, l = neigh_coord

    # Check that coordinates are within image
    # (N.B. Not necessary if calling from inside bilateral())
    #if (i < 0 or j < 0 or i >= img.shape[0] or j >= img.shape[1] or
    #    k < 0 or l < 0 or k >= img.shape[0] or l >= img.shape[1]):
    #    raise ValueError("Coordinates outside of image")

    # Get domain kernel
    d = np.exp(- ((i - k)**2 + (j - l)**2) / (2 * sigma_d**2))

    # Get range kernel 
    r = np.exp(- (img[i, j] - img[k, l])**2 / (2 * sigma_r**2))

    # If multiple colour bands, use this:
    #r = np.exp(- np.linalg.norm(img[i, j] - img[k, l]) / (2 * sigma_r**2))

    # Multiply to get weight function
    return d * r

def bilateral(img, sigma_d, sigma_r):
    """
    Bilateral filter.

    Parameters :
        img     : image
        sigma_d : spatial parameter (larger features smoothened)
        sigma_r : range parameter (approaches Gaussian convolution)
    """
    # Convert to numpy array if necessary
    if not isinstance(img, np.ndarray): img = np.array(img)

    sigma_d = float(sigma_d)
    sigma_r = float(sigma_r)

    img_filt = np.empty(img.shape)

    # Get all pixels
    pixels = [(i, j) for i in range(img.shape[0]) for j in range(img.shape[1])]

    # Loop over all pixels
    for pixel in pixels:
        # Loop over neighbours
        numer = 0.0
        denom = 0.0
        for neigh in neighbours(img.shape, pixel):
            # Compute weight function
            f = img[neigh]
            w = bilateral_weight(img, pixel, neigh, sigma_d, sigma_r)
            numer += f * w
            denom += w
        print numer, denom
        img_filt[pixel] = numer / denom
        print pixel, img[pixel], img_filt[pixel]

    return img_filt

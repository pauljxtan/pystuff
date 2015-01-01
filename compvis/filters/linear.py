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

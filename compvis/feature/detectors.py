"""
Feature detectors (Szeliski 4.1.1)
"""
def wssd(img_0, img_1, u, w):
    """
    Finds the weighted summed square difference between two image patches.

    Parameters :
        img_0, img_1 : two images being compared
        u            : displacement vector
        w            : weighting (window) function
    """
    # Check that images and window function are the same size
    if not (img_0.shape == img_1.shape == w.shape):
        return ValueError("Images and window function must all be same size")

    E = 0.0
    for x in range(img_0.shape[0]):
        for y in range(img_0.shape[1]):
            E += w[x, y] * (img_1[x+u[0], y+u[1]] - img_0[x, y])**2

    return E

def autocorr(img, delta_u, w):
    """
    Computes the auto-correlation function.

    Parameters :
        img     : image
        delta_u : variation in position
        w       : weighting (window) function
    """
    # Check that image and window function are the same size
    if not (img.shape == w.shape):
        return ValueError("Image and window function must be same size")

    E = 0.0
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            E += w[x, y] * (img[x+u[0], y+u[1]] - img[x, y])**2

    return E

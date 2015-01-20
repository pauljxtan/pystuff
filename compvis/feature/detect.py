"""
Feature detection (Szeliski 4.1.1)
"""
import numpy as np
import scipy.signal as sig
import scipy.ndimage as ndi
from compvis.utils import get_patch
from compvis.imgproc.filters.kernels import KERNEL_GAUSSIAN, gaussian_kernel

def sum_sq_diff(img_0, img_1, u, x, y, x_len, y_len):
    """
    Finds the summed square difference between two image patches.
    Uses even weighting across the patch.

    Parameters :
        img_0, img_1 : two images being compared
        u            : displacement vector between the patches
        x, y         : coordinates of top-left corner of first patch
        x_len, y_len : width and height of first patch
    """
    patch_0 = get_patch(img_0, x, y, x_len, y_len)
    patch_1 = get_patch(img_1, x + u[0], y + u[1], x_len, y_len)

    return (patch_1 - patch_0)**2).sum()

def autocorr(img, u, x, y, x_len, y_len):
    """
    Computes the auto-correlation function for an image patch with a
    displacement of u. Uses even weighting across the patch.
    (Just for reference, since this is sum_sq_diff() with both images being
    the same.)

    Parameters :
        img          : image
        u            : variation in position
        x, y         : coordinates of top-left corner of patch
        x_len, y_len : width and height of patch
    """
    return sum_sq_diff(img, img, u, x, y, x_len, y_len)

def autocorr_surface(img, u_x_range, u_y_range, x, y, x_len, y_len):
    """
    Computes an auto-correlation surface for an image patch with a given range
    of displacements.

    Parameters :
        img                  : image
        u_x_range, u_y_range : range of displacements (tuples)
        x, y                 : coordinates of top-left corner of patch
        x_len, y_len         : width and height of patch

    Returns :
        X, Y : grid mesh
        Z    : auto-correlation values
    """
    X, Y = np.meshgrid(range(u_x_range[0], u_x_range[1]),
                       range(u_y_range[0], u_y_range[1]))

    z = np.array([autocorr(img, (u_x, u_y), x, y, x_len, y_len) 
                  for u_x, u_y in zip(np.ravel(X), np.ravel(Y))])
    Z = z.reshape(X.shape)

    return X, Y, Z

def harris(img, sigma_d=1, sigma_i=2, alpha=0.06, filter_type='gaussian'):
    """
    Returns the Harris interest scores for keypoint detection.

    Parameters :
        img         : image
        sigma_d     : width of derivative Gaussian
        sigma_i     : width of integration Gaussian
        alpha       : parameter used in Harris-Stephens (1988) score
        filter_type : 'gaussian' or 'sobel'

    (Default values for sigma_d and sigma_i from Szeliski pp. 190)
    (Default value for alpha from Szeliski pp. 189)
    """
    # Gradients in x and y

    # Derivative of Gaussian
    if filter_type is 'gaussian':
        I_x = ndi.gaussian_filter(img, sigma_d, (1, 0))#, mode='nearest')
        I_y = ndi.gaussian_filter(img, sigma_d, (0, 1))#, mode='nearest')

    # Sobel
    elif filter_type is 'sobel':
        I_x = ndi.sobel(img, 0)
        I_y = ndi.sobel(img, 1)

    # Outer products
    I_xx = I_x**2
    I_yy = I_y**2
    I_xy = I_x * I_y

    # Convolve with Gaussian to get auto-correlation matrix
    A_xx = ndi.gaussian_filter(I_xx, sigma_i)
    A_yy = ndi.gaussian_filter(I_yy, sigma_i)
    A_xy = ndi.gaussian_filter(I_xy, sigma_i)

    # Harris scores
    A_det = A_xx * A_yy - A_xy**2
    A_tr = A_xx + A_yy
    
    # (Harris-Stephens 1988)
    #return A_det - alpha * A_tr**2
    
    # Harmonic mean (Brown-Szeliski-Winder 2005)
    return A_det / A_tr

def select_scores(scores, n_points, border=10):
    """
    Selects the best scores from a given map.

    Parameters :
        scores   : 2D score array
        n_points : number of points to select
        border   : minimum distance from image boundaries
    """

    # Mask out points too close to boundary
    mask = np.zeros(scores.shape)
    mask[border:-border, border:-border] = 1
    scores *= mask

    # Sort coordinates by response strength
    coords_sorted_score = np.array(np.unravel_index(np.argsort(scores, axis=None), scores.shape)).T
    #scores_sorted = scores[coords_sorted]

    # Apply ANMS selection (prevent dense clusters)
    #supp_radii = get_suppression_radii(scores)
    # Sort coordinates by supression radii
    #coords_sorted_supp = np.array(np.unravel_index(np.argsort(supp_radii, axis=None), supp_radii.shape)).T

    # Get highest scores
    best_coords = coords_sorted_score[-n_points:]

    # Get scores with highest supression radii
    #best_coords = coords_sorted_supp[-n_points:]

    best_scores = [scores[coord[0], coord[1]] for coord in best_coords]

    return np.array(best_coords), np.array(best_scores)

def get_suppression_radii(scores, c_robust=0.9):
    supp_radii = np.zeros(scores.shape)

    coords_max = np.unravel_index(scores.argmax(), scores.shape)

    for i in range(scores.shape[0]):
        for j in range(scores.shape[1]):

            # Skip the highest score (infinite suppression radius)
            if (i, j) == coords_max:
                continue

            # Find suppression radius
            r = 0
            r_found = False
            score = scores[i][j]

            while not r_found:
                r += 1

                # Keep the candidate "window" within the image
                x0 = i-r   if i-r >= 0                else 0
                x1 = i+r+1 if i+r+1 < scores.shape[0] else scores.shape[0]-1
                y0 = j-r   if j-r >= 0                else 0
                y1 = j+r+1 if j+r+1 < scores.shape[1] else scores.shape[1]-1

                candidates = scores[x0:x1, y0:y1]
                #if np.count_nonzero(score < c_robust*candidates):
                if np.count_nonzero(score < candidates):
                    r_found = True
                    break
            
            supp_radii[i][j] = r

    # Set the highest score to have the largest supression radius
    supp_radii[coords_max] = supp_radii.max() + 1

    return supp_radii

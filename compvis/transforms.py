"""
Geometric transformations described Szeliski 2011, section 2.1.2.

In general, the functions take inhomogeneous vectors as input, except for
particular transforms that act on homogeneous coordinates (e.g. homography).
"""

import numpy as np
import sys

def translate(x, t):
    """
    Translates a vector of arbitrary dimension.
    """
    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray): x = np.array(x)
    if not isinstance(t, np.ndarray): t = np.array(t)

    return x + t
    
################################ 2D TRANSFORMS ################################

def euclidean_2d(x, theta, t):
    """
    Performs a 2D Euclidean transformation (i.e. rotation and translation,
    a.k.a. rigid body motion.
    """
    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray): x = np.array(x)
    if not isinstance(t, np.ndarray): t = np.array(t)

    # Check for correct dimensions
    if x.shape != (2, ): raise ValueError("x must be 2D")
    if t.shape != (2, ): raise ValueError("t must be 2D")

    # Augmented vector
    x_aug = np.append(x, 1)

    # Rotation matrix
    R = np.array(((np.cos(theta), -np.sin(theta)),
                  (np.sin(theta),  np.cos(theta))))

    # Rotation + translation matrix
    Rt = np.concatenate((R, t.reshape(2, 1)), axis=1)

    return np.dot(Rt, x_aug)

def similarity_2d(x, s, theta, t):
    """
    Performs a 2D similarity transform (i.e. scaled rotation).
    """
    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray): x = np.array(x)
    if not isinstance(t, np.ndarray): t = np.array(t)

    # Check for correct dimensions
    if x.shape != (2, ): raise ValueError("x must be 2D")
    if t.shape != (2, ): raise ValueError("t must be 2D")

    # Augmented vector
    x_aug = np.append(x, 1)

    # Scaled rotation matrix
    sR = s * np.array(((np.cos(theta), -np.sin(theta)),
                       (np.sin(theta),  np.cos(theta))))

    # Rotation + translation matrix
    sRt = np.concatenate((sR, t.reshape(2, 1)), axis=1)

    return np.dot(sRt, x_aug)

def similarity_2d_alt(x, a, b, t):
    """
    Performs a 2D similarity transform (i.e. scaled rotation).
    """
    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray): x = np.array(x)
    if not isinstance(t, np.ndarray): t = np.array(t)
    
    # Check for correct dimensions
    if x.shape != (2, ): raise ValueError("x must be 2D")
    if t.shape != (2, ): raise ValueError("t must be 2D")

    # Augmented vector
    x_aug = np.append(x, 1)

    # Scaled rotation matrix
    sR = np.array(((a, -b),
                   (b,  a)))

    # Rotation + translation matrix
    sRt = np.concatenate((sR, t.reshape(2, 1)), axis=1)

    return np.dot(sRt, x_aug)

def affine_2d(x, A):
    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray): x = np.array(x)
    if not isinstance(A, np.ndarray): A = np.array(A)

    # Check for correct dimensions
    if x.shape != (2, ): raise ValueError("x must be 2D")
    if A.shape != (2, 3): raise ValueError("A must be 2 x 3 matrix")

    # Augmented vector
    x_aug = np.append(x, 1)

    return np.dot(A, x_aug)

def homography_2d(x_hom, H_hom):
    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    if not isinstance(H, np.ndarray):
        H = np.array(H)

    # Check for correct dimensions
    if x_hom.shape != (3, ): raise ValueError("x_hom must be 3D")
    if H_hom.shape != (3, 3): raise ValueError("H_hom must be 3 x 3 matrix")
    
    xp_hom = np.dot(H_hom, x_hom)
    # Get the augmented vector
    x_aug = utils.hom_to_aug(x_hom)

    # Normalize to inhomogeneous coordinates
    return np.array((np.dot(H[0], x_aug) / np.dot(H[2], x_aug),
                     np.dot(H[1], x_aug) / np.dot(H[2], x_aug)))

def stretch_2d(x, s, t):
    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray): x = np.array(x)
    if not isinstance(s, np.ndarray): s = np.array(s)
    if not isinstance(t, np.ndarray): t = np.array(t)

    # Check for correct dimensions
    if x.shape != (2, ): raise ValueError("x must be 2D")
    if s.shape != (2, ): raise ValueError("s must be 2D")
    if t.shape != (2, ): raise ValueError("t must be 2D")

    return s * x + t

def planar_surface_flow(x, a):
    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray): x = np.array(x)
    if not isinstance(a, np.ndarray): a = np.array(a)

    # Check for correct dimensions
    if x.shape != (2, ): raise ValueError("x must be 2D")
    if a.shape != (8, ): raise ValueError("a must be 8D")

    tmp = np.array((1, x[0], x[1], x[0]**2, x[0]*x[1]))

    return np.array((np.dot(a[[0, 1, 2, 6, 7]], tmp),
                     np.dot(a[[3, 4, 5, 7, 6]], tmp)))

def bilinear_interpolant(x, a):
    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray): x = np.array(x)
    if not isinstance(a, np.ndarray): a = np.array(a)

    # Check for correct dimensions
    if x.shape != (2, ): raise ValueError("x must be 2D")
    if a.shape != (8, ): raise ValueError("a must be 8D")

    tmp = np.array((1, x[0], x[1], x[0]*x[1]))

    return np.array((np.dot(a[[0, 1, 2, 6]], tmp),
                     np.dot(a[[3, 4, 5, 7]], tmp)))

################################ 3D TRANSFORMS ################################

def euclidean_3d(x, n, theta, t):
    """
    Performs a 3D Euclidean transformation (i.e. rotation and translation,
    a.k.a. rigid body motion.

    Parameters :
        x      : vector
        n      : (unit) rotation axis
        theta  : rotation angle
        t      : translation
    """
    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray): x = np.array(x)
    if not isinstance(n, np.ndarray): x = np.array(n)
    if not isinstance(t, np.ndarray): t = np.array(t)

    # Check for correct dimensions
    if x.shape != (3, ): raise ValueError("x must be 3D")
    if n.shape != (3, ): raise ValueError("n must be 3D")
    if t.shape != (3, ): raise ValueError("t must be 3D")

    # Augmented vector
    x_aug = np.append(x, 1)

    # Matrix form of cross product operator with n = (n_x, n_y, n_z):
    #               |  0   -n_z  n_y |
    #     n_cross = |  n_z  0   -n_x |
    #               | -n_y  n_x  0   |
    n_cross = np.array((( 0,    -n[2],  n[1]),
                        ( n[2],  0,    -n[0]),
                        (-n[1],  n[0],  0   )))
    # Rotation matrix
    R = np.identity(3) + np.sin(theta)*n_cross + (1-np.cos(theta))*n_cross**2

    # Rotation + translation matrix
    Rt = np.concatenate((R, t.reshape(3, 1)), axis=1)

    return np.dot(Rt, x_aug)

def affine_3d(x, A):
    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray): x = np.array(x)
    if not isinstance(A, np.ndarray): A = np.array(A)

    # Check for correct dimensions
    if x.shape != (3, ): raise ValueError("x must be 3D")
    if A.shape != (3, 4): raise ValueError("A must be 3 x 4 matrix")

    # Augmented vector
    x_aug = np.append(x, 1)

    return np.dot(A, x_aug)

def homography_3d(x_hom, H_hom):
    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    if not isinstance(H, np.ndarray):
        H = np.array(H)

    # Check for correct dimensions
    if x_hom.shape != (4, ): raise ValueError("x_hom must be 4D")
    if H_hom.shape != (4, 4): raise ValueError("H_hom must be 4 x 4 matrix")
    
    xp_hom = np.dot(H_hom, x_hom)
    # Get the augmented vector
    x_aug = utils.hom_to_aug(x_hom)

    # Normalize to inhomogeneous coordinates
    return np.array((np.dot(H[0], x_aug) / np.dot(H[3], x_aug),
                     np.dot(H[1], x_aug) / np.dot(H[3], x_aug),
                     np.dot(H[2], x_aug) / np.dot(H[3], x_aug)))

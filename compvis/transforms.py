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
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    if not isinstance(t, np.ndarray):
        t = np.array(t)

    return x + t
    
def euclidean_2d(x, theta, t):
    """
    Performs a 2D Euclidean transformation (i.e. rotation and translation,
    a.k.a. rigid body motion.
    """
    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    if not isinstance(t, np.ndarray):
        t = np.array(t)

    # Check if x and t have the correct dimension
    if x.shape != (2, ):
        raise ValueError("x must be 2D")
    if t.shape != (2, ):
        raise ValueError("t must be 2D")

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
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    if not isinstance(t, np.ndarray):
        t = np.array(t)

    # Check if x and t have the correct dimension
    if x.shape != (2, ):
        raise ValueError("x must be 2D")
    if t.shape != (2, ):
        raise ValueError("t must be 2D")

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
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    if not isinstance(t, np.ndarray):
        t = np.array(t)
    
    # Check if x and t have the correct dimension
    if x.shape != (2, ):
        raise ValueError("x must be 2D")
    if t.shape != (2, ):
        raise ValueError("t must be 2D")

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
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    if not isinstance(A, np.ndarray):
        A = np.array(A)

    # Check if x has correct dimension
    if x.shape[0] != 2:
        raise ValueError("x must be 2D")
    # Check if A has correct dimensions
    if A.shape != (2, 3):
        raise ValueError("A must be 2 x 3 matrix")

    # Augmented vector
    x_aug = np.append(x, 1)

    return np.dot(A, x_aug)

def homography_2d(x_hom, H_hom):
    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    if not isinstance(H, np.ndarray):
        H = np.array(H)

    # Check if x and H have the correct dimensions
    if x_hom.shape[0] != 3:
        raise ValueError("x_hom must be 3D (projective)")
    if H_hom.shape != (3, 3):
        raise ValueError("H_hom must be 3 x 3 matrix")
    
    xp_hom = np.dot(H_hom, x_hom)
    # Get the augmented vector
    x_aug = utils.hom_to_aug(x_hom)

    # Normalize to inhomogeneous coordinates
    xp = np.array((np.dot(H[0], x_aug) / np.dot(H[2], x_aug),
                   np.dot(H[1], x_aug) / np.dot(H[2], x_aug)))

    return xp

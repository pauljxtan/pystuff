"""
Geometric transformations.

See Szeliski section 2.1.2.
"""

import numpy as np
import sys

def translate(x, t):
    """
    Translates a vector of arbitrary dimension.
    """
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
    # Check if x and t have the correct dimension
    if len(x) != 2 or len(t) != 2:
        print >> sys.stderr, "x and t must be 2D"
        return

    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    if not isinstance(t, np.ndarray):
        t = np.array(t)

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
    # Check if x and t have the correct dimension
    if len(x) != 2 or len(t) != 2:
        print >> sys.stderr, "x and t must be 2D"
        return

    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    if not isinstance(t, np.ndarray):
        t = np.array(t)

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
    if x.shape[0] != 2 or t.shape[0] != 2:
        print >> sys.stderr, "x and t must be 2D"
        return

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
        print >> sys.stderr, "x must be 2D"
    # Check if A has correct dimensions
    if A.shape != (2, 3):
        print >> sys.stderr, "A must be a 2 x 3 matrix"

    # Augmented vector
    x_aug = np.append(x, 1)

    return np.dot(A, x_aug)

def homography_2d(x, H):
    return

if __name__ == '__main__':
    print translate((1, 2), (3, 4))
    print euclidean_2d((1, 2), np.pi / 4, (3, 4))
    print similarity_2d((1, 2), 5, np.pi / 4, (3, 4))
    print similarity_2d_alt((1, 2), 5, 6, (3, 4))
    A = ((3, 4, 5),
         (6, 7, 8))
    print affine_2d((1, 2), A)

"""
Geometric transformations described Szeliski 2011, section 2.1.

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

def slerp(q0, q1, alpha):
    """
    Performs spherical linear interpolation between two quaternions.

    Parameters :
        q0, q1 : quaternions
        alpha  : fraction to interpolate
    """
    # Convert to numpy arrays if necessary
    if not isinstance(q0, np.ndarray): q0 = np.array(q0)
    if not isinstance(q1, np.ndarray): q1 = np.array(q1)

    # Check for correct dimensions
    if q0.shape != (4, ): raise ValueError("q0 must be 4D")
    if q1.shape != (4, ): raise ValueError("q1 must be 4D")

    qr = q1 / q0
    vr = qr[:3]
    wr = qr[3]
    if (wr < 0): qr = -qr

    theta_r = 2 * np.arctan(np.linalg.norm(vr) / wr)
    nr = vr / np.linalgnorm(vr)
    theta_alpha = alpha * theta_r
    q_alpha = np.array((np.sin(theta_alpha/2) * nr, np.cos(theta_alpha/2)))

    return q_alpha * q0
    
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
    if not isinstance(x, np.ndarray): x = np.array(x)
    if not isinstance(H, np.ndarray): H = np.array(H)

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
    a.k.a. rigid body motion.)

    Parameters :
        x      : vector
        n      : (unit) rotation axis
        theta  : rotation angle
        t      : translation
    """
    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray): x = np.array(x)
    if not isinstance(n, np.ndarray): n = np.array(n)
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

def euclidean_3d_quaternion(x, q, t):
    """
    Performs a 3D Euclidean transformation (i.e. rotation and translation,
    a.k.a. rigid body motion.

    Parameters :
        x      : vector
        q      : (unit) quaternion
        t      : translation
    """
    # Convert to numpy arrays if necessary
    if not isinstance(x, np.ndarray): x = np.array(x)
    if not isinstance(q, np.ndarray): q = np.array(q)
    if not isinstance(t, np.ndarray): t = np.array(t)

    # Check for correct dimensions
    if x.shape != (3, ): raise ValueError("x must be 3D")
    if q.shape != (4, ): raise ValueError("q must be 4D")
    if t.shape != (3, ): raise ValueError("t must be 3D")

    # Augmented vector
    x_aug = np.append(x, 1)

    # Rotation matrix R(q)
    qx = q[0]
    qy = q[1]
    qz = q[2]
    qw = q[3]
    R = np.array((1-2*(qy*qy+qz*qz),   2*(qx*qy-qz*qw),   2*(qx*qz+qy*qw)),
                 (  2*(qx*qy+qz*qw), 1-2*(qx*qx+qz*qz),   2*(qy*qz-qx*qw)),
                 (  2*(qx*qz-qy*qw),   2*(qy*qz+qx*qw), 1-2*(qx*qx+qy*qy)))

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
    if not isinstance(x, np.ndarray): x = np.array(x)
    if not isinstance(H, np.ndarray): H = np.array(H)

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

##################################### 3D TO 2D PROJECTIONS #####################################

def orthography(p):
    # Convert to numpy array if necessary
    if not isinstance(p, np.ndarray): p = np.array(p)

    # Check for correct dimensions
    if p.shape != (3, ): raise ValueError("p must be 3D")

    A = np.concatenate((np.identity(2), np.zeros(2).reshape(2, 1)), axis=1)

    return np.dot(A, p)

def orthography_hom(p_hom):
    # Convert to numpy array if necessary
    if not isinstance(p, np.ndarray): p = np.array(p)

    # Check for correct dimensions
    if p.shape != (4, ): raise ValueError("p_hom must be 4D")

    A = np.concatenate((np.identity(3)[:,:2], np.zeros(3).reshape(3, 1), np.identity(3)[:,2]), axis=1)

    return np.dot(A, p_hom)

def orthography_scaled(p, s):
    # Convert to numpy array if necessary
    if not isinstance(p, np.ndarray): p = np.array(p)

    # Check for correct dimensions
    if p.shape != (3, ): raise ValueError("p must be 3D")

    A = s * np.concatenate((np.identity(2), np.zeros(2).reshape(2, 1)), axis=1)

    return np.dot(A, p)

def para_perspective(p_hom, A):
    # Convert to numpy arrays if necessary
    if not isinstance(p_hom, np.ndarray): p_hom = np.array(p_hom)
    if not isinstance(A, np.ndarray): A = np.array(A)

    # Check for correct dimensions
    if p_hom.shape != (4, ): raise ValueError("p_hom must be 4D")
    if A.shape != (2, 4): raise ValueError("A must be 2 x 4 matrix")
    
    B = np.concatenate((A, np.array((0, 0, 0, 1))))

    return np.dot(B, p_hom)

def perspective(p):
    # Convert to numpy array if necessary
    if not isinstance(p, np.ndarray): p = np.array(p)

    # Check for correct dimensions
    if p.shape != (3, ): raise ValueError("p must be 3D")

    return np.array((p[0]/p[2], p[1]/p[2], 1))

def perspective_hom(p_hom):
    # Convert to numpy array if necessary
    if not isinstance(p_hom, np.ndarray): p_hom = np.array(p_hom)

    # Check for correct dimensions
    if p_hom.shape != (4, ): raise ValueError("p_hom must be 4D")

    A = np.concatenate((np.identity(3), np.zeros(3).reshape(3, 1)), axis=1)

    return np.dot(A, p_hom)

def calibration_matrix(f, c, a, s):
    return np.array((f,   s, c[0]),
                    (0, a*f, c[1]),
                    (0,   0,    1))

def calibration_matrix_4x4(f, c, a, s):
    return np.array((f,   s, c[0], 0),
                    (0, a*f, c[1], 0),
                    (0,   0,    1, 0))
                    (0,   0,    0, 1))

def camera_matrix(K, R, t):
    # Convert to numpy arrays if necessary
    if not isinstance(K, np.ndarray): K = np.array(K)
    if not isinstance(R, np.ndarray): R = np.array(R)
    if not isinstance(t, np.ndarray): t = np.array(t)

    # Check for correct dimensions
    if K.shape != (3, 3): raise ValueError("K must be 3 x 3 matrix")
    if R.shape != (3, 3): raise ValueError("R must be 3 x 3 matrix")
    if t.shape != (3, ): raise ValueError("t must be 3D")

    E = np.concatenate((R, t.reshape(3, 1)), axis=1)

    return np.dot(K, E)

def camera_matrix_4x4(K_4x4, R, t):
    # Convert to numpy arrays if necessary
    if not isinstance(K_4x4, np.ndarray): K_4x4 = np.array(K_4x4)
    if not isinstance(R, np.ndarray): R = np.array(R)
    if not isinstance(t, np.ndarray): t = np.array(t)

    # Check for correct dimensions
    if K_4x4.shape != (4, 4): raise ValueError("K_4x4 must be 4 x 4 matrix")
    if R.shape != (3, 3): raise ValueError("R must be 3 x 3 matrix")
    if t.shape != (3, ): raise ValueError("t must be 3D")

    E_4x4 = np.concatenate((np.concatenate((R, t.reshape(3,1)), axis=1), np.array((0, 0, 0, 1))))

    return np.dot(K_4x4, E_4x4)

def world_to_screen_with_disparity(P_4x4, p_w):
    # Convert to numpy arrays if necessary
    if not isinstance(P_4x4, np.ndarray): P_4x4 = np.array(P_4x4)
    if not isinstance(p_w, np.ndarray): p_w = np.array(p_w)

    # Check for correct dimensions
    if P_4x4.shape != (4, 4): raise ValueError("P_4x4 must be 4 x 4 matrix")
    if p_w.shape != (3, ): raise ValueError("p_w must be 3D")

    p_w_aug = np.append(p_w, 1)

    x_s = np.dot(P_4x4, p_w_aug)

    # Normalize to (x_s, x_y, 1, d)
    return x_s / x_s[2]

"""
Color spaces. (Szeliski 2.3)
"""

import numpy as np

RBG_TO_XYZ_MATRIX  = 1 / 0.17697 * np.array(((0.49,    0.31,    0.20   ),
                                             (0.17697, 0.81240, 0.01063),
                                             (0.00,    0.01,    0.99   )))

def rgb_to_xyz(RGB):
    if not isinstance(RGB, np.ndarray): RGB = np.array(RGB)
    if RGB.shape != (3, ): raise ValueError("RGB must be 3D")

    return np.dot(RBG_TO_XYZ_MATRIX, RGB)

def xyz_to_rgb(XYZ):
    if not isinstance(XYZ, np.ndarray): XYZ = np.array(XYZ)
    if XYZ.shape != (3, ): raise ValueError("XYZ must be 3D")

    return np.dot(np.linalg.inv(RBG_TO_XYZ_MATRIX), XYZ)

def rgb_ratios(RGB):
    RGB = np.array(RGB, float)
    if RGB.shape != (3, ): raise ValueError("RGB must be 3D")

    return RGB / np.sum(RGB)

def xyz_ratios(XYZ):
    """
    i.e. chromaticity coordinates
    """
    XYZ = np.array(XYZ, float)
    if XYZ.shape != (3, ): raise ValueError("XYZ must be 3D")

    return XYZ / np.sum(XYZ)

if __name__ == '__main__':
    RGB = (12, 123, 234)
    print RGB
    XYZ = rgb_to_xyz(RGB)
    print XYZ

    print rgb_ratios(RGB)
    print xyz_ratios(XYZ)


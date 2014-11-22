import numpy as np
import random
import unittest

import transforms as tr

class TestTransforms(unittest.TestCase):

    def test_2d_transforms_random_values(self):
        # Get some random vectors and parameters
        x     = np.random.random(2)
        t     = np.random.random(2)
        theta = np.pi / np.random.random()
        s     = np.random.random()
        a     = np.random.random()
        b     = np.random.random()
        A     = np.random.random((2, 3))
        x_hom = np.random.random(3)
        H_hom = np.random.random((3, 3))
        s_sq  = np.random.random(2)
        a_psf = np.random.random(8)

        # Error tolerance
        epsilon = 1e-6
        
        # Translation
        expected = np.array((x[0] + t[0], x[1] + t[1]))
        result = tr.translate(x, t)
        self.assertTrue((np.abs(expected - result) < epsilon).all())

        # 2D Euclidean transform
        expected = np.array((np.cos(theta)*x[0] - np.sin(theta)*x[1] + t[0]*1,
                             np.sin(theta)*x[0] + np.cos(theta)*x[1] + t[1]*1))
        result = tr.euclidean_2d(x, theta, t)
        self.assertTrue((np.abs(expected - result) < epsilon).all())

        # 2D similarity transform
        expected = np.array((s*np.cos(theta)*x[0] - s*np.sin(theta)*x[1]
                             + t[0]*1,
                             s*np.sin(theta)*x[0] + s*np.cos(theta)*x[1]
                             + t[1]*1))
        result = tr.similarity_2d(x, s, theta, t)
        self.assertTrue((np.abs(expected - result) < epsilon).all())

        # 2D similarity transform (alternate)
        expected = np.array((a*x[0] - b*x[1] + t[0]*1,
                             b*x[0] + a*x[1] + t[1]*1))
        result = tr.similarity_2d_alt(x, a, b, t)
        self.assertTrue((np.abs(expected - result) < epsilon).all())

        # Affine transform
        expected = np.array((A[0,0]*x[0] + A[0,1]*x[1] + A[0,2]*1,
                             A[1,0]*x[0] + A[1,1]*x[1] + A[1,2]*1))
        result = tr.affine_2d(x, A)
        self.assertTrue((np.abs(expected - result) < epsilon).all())

        # Stretch / squash
        expected = np.array((s_sq[0]*x[0] + t[0], s_sq[1]*x[1] + t[1]))
        result = tr.stretch_2d(x, s_sq, t)
        self.assertTrue((np.abs(expected - result) < epsilon).all())

        # Planar surface flow
        expected = np.array((a_psf[0] + a_psf[1]*x[0] + a_psf[2]*x[1]
                             + a_psf[6]*x[0]**2 + a_psf[7]*x[0]*x[1],
                             a_psf[3] + a_psf[4]*x[0] + a_psf[5]*x[1]
                             + a_psf[7]*x[0]**2 + a_psf[6]*x[0]*x[1]))
        result = tr.planar_surface_flow(x, a_psf)
        self.assertTrue((np.abs(expected - result) < epsilon).all())

        # Bilinear interpolant
        expected = np.array((a_psf[0] + a_psf[1]*x[0] + a_psf[2]*x[1]
                             + a_psf[6]*x[0]*x[1],
                             a_psf[3] + a_psf[4]*x[0] + a_psf[5]*x[1]
                             + a_psf[7]*x[0]*x[1]))
        result = tr.bilinear_interpolant(x, a_psf)
        self.assertTrue((np.abs(expected - result) < epsilon).all())

if __name__ == '__main__':
    unittest.main()


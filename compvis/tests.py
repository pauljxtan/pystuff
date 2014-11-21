import numpy as np
import random
import unittest

import transforms as tr

class TestTransforms(unittest.TestCase):

    def test_2d_transforms(self):
        # Get some random vectors and parameters
        x = np.random.random(2)
        t = np.random.random(2)
        theta = np.pi / np.random.random()
        s = np.random.random()
        a = np.random.random()
        b = np.random.random()
        A = np.random.random((2, 3))
        
        # Translation
        expected = np.array((x[0] + t[0], x[1] + t[1]))
        self.assertTrue((tr.translate(x, t)
                         == np.array((x[0] + t[0], x[1] + t[1]))).all())

        # 2D Euclidean transform
        expected = np.array((np.cos(theta)*x[0] - np.sin(theta)*x[1] + t[0]*1,
                             np.sin(theta)*x[0] + np.cos(theta)*x[1] + t[1]*1))
        self.assertTrue((tr.euclidean_2d(x, theta, t) == expected).all())

        # 2D similarity transform
        expected = np.array((s*np.cos(theta)*x[0] - s*np.sin(theta)*x[1]
                             + t[0]*1,
                             s*np.sin(theta)*x[0] + s*np.cos(theta)*x[1]
                             + t[1]*1))
        self.assertTrue((tr.similarity_2d(x, s, theta, t) == expected).all())

        # 2D similarity transform (alternate)
        expected = np.array((a*x[0] - b*x[1] + t[0]*1,
                             b*x[0] + a*x[1] + t[1]*1))
        self.assertTrue((tr.similarity_2d_alt(x, a, b, t) == expected).all())

        # Affine transform
        expected = np.array((A[0,0]*x[0] + A[0,1]*x[1] + A[0,2]*1,
                             A[1,0]*x[0] + A[1,1]*x[1] + A[1,2]*1))
        self.assertTrue((tr.affine_2d(x, A) == expected).all())

if __name__ == '__main__':
    unittest.main()


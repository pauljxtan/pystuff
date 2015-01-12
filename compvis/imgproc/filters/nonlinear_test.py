import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import sys

import nonlinear as nonlin


pic = np.array(Image.open(sys.argv[1]).convert('L'))

bil = nonlin.bilateral(pic, sigma_d=3, sigma_r=50)

plt.figure()
plt.title("Original")
plt.imshow(pic, cmap=plt.cm.gray)
plt.figure()
plt.title("Bilateral")
plt.imshow(bil, cmap=plt.cm.gray)
plt.show()

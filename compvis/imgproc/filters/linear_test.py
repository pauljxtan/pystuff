import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import sys

import linear as lin


pic = np.array(Image.open(sys.argv[1]).convert('L'))

bil = lin.bilinear(pic)
gau = lin.gaussian(pic)
sob = lin.sobel(pic)
cor = lin.corner(pic)

plt.figure()
plt.title("Original")
plt.imshow(pic, cmap=plt.cm.gray)
plt.figure()
plt.title("Bilinear")
plt.imshow(bil, cmap=plt.cm.gray)
plt.figure()
plt.title("Gaussian")
plt.imshow(gau, cmap=plt.cm.gray)
plt.figure()
plt.title("Sobel")
plt.imshow(sob, cmap=plt.cm.gray)
plt.figure()
plt.title("Corner")
plt.imshow(cor, cmap=plt.cm.gray)
plt.show()

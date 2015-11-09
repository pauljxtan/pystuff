"""
An example script for performing Harris feature detection and matching.
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from compvis.feature.detectors import harris, select_scores, select_scores_anms
from compvis.feature.descriptors import match_points

print "Creating images..."
obj = np.array(Image.open("ai_160.png").convert('L'))
# Place the object at different positions in each image
img_0 = np.ones((320, 320), dtype=np.int64) * 255
img_1 = np.ones((320, 320), dtype=np.int64) * 255
# Top-left
img_0[0:160, 0:160] = obj
# Bottom-right
img_1[160:320, 160:320] = obj

print "Computing Harris scores"
scores_0 = harris(img_0)
scores_1 = harris(img_1)

print "Selecting corner detections..."
# Without ANMS
#coords_0, scores_0 = select_scores(scores_0, 64)
#coords_1, scores_1 = select_scores(scores_1, 64)

# With ANMS
coords_0, scores_0 = select_scores_anms(scores_0, 64, 1.0)
coords_1, scores_1 = select_scores_anms(scores_1, 64, 1.0)

print "Matching features..."
matches = match_points(img_0, img_1, coords_0, coords_1)

print "Plotting results..."
#plt.figure()
#plt.subplot(121)
#plt.xlim(0, 320)
#plt.ylim(320, 0)
#plt.imshow(img_0, cmap='Greys_r')
#plt.plot(coords_0[:, 1], coords_0[:, 0], 'r+')
#plt.subplot(122)
#plt.xlim(0, 320)
#plt.ylim(320, 0)
#plt.imshow(img_1, cmap='Greys_r')
#plt.plot(coords_1[:, 1], coords_1[:, 0], 'r+')

plt.figure()
plt.xlim(0, 320)
plt.ylim(320, 0)
plt.imshow(img_0, cmap='Greys_r')
plt.imshow(img_1, cmap='Greys_r', alpha=0.5)
for i, m in enumerate(matches):
    plt.plot((coords_0[i][1], coords_1[m][1]),
             (coords_0[i][0], coords_1[m][0]), 'o-', linewidth=1)

plt.show()

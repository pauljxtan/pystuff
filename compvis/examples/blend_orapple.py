import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from compvis.utils import clip_min_max
from compvis.imgproc.pyramids import pyramids, blend_pyramids, reconstruct

# Load images into numpy arrays
print "Loading images..."
apple = np.array(Image.open("apple1.jpg"))
orange = np.array(Image.open("orange1.jpg"))
mask = np.array(Image.open("mask512.jpg"))

# Normalize mask to [0, 1]
mask /= 255.0

# Build pyramids for each channel
print "Building pyramids..."
G_apple_R, L_apple_R = pyramids(apple[:,:,0])
G_apple_G, L_apple_G = pyramids(apple[:,:,1])
G_apple_B, L_apple_B = pyramids(apple[:,:,2])
G_orange_R, L_orange_R = pyramids(orange[:,:,0])
G_orange_G, L_orange_G = pyramids(orange[:,:,1])
G_orange_B, L_orange_B = pyramids(orange[:,:,2])
G_mask_R, L_mask_R = pyramids(mask[:,:,0])
G_mask_G, L_mask_G = pyramids(mask[:,:,1])
G_mask_B, L_mask_B = pyramids(mask[:,:,2])

# Blend pyramids for each channel
print "Blending pyramids..."
L_blend_R = blend_pyramids(L_apple_R, L_orange_R, G_mask_R)
L_blend_G = blend_pyramids(L_apple_G, L_orange_G, G_mask_G)
L_blend_B = blend_pyramids(L_apple_B, L_orange_B, G_mask_B)

# Reconstruct blended image for each channel
print "Reconstructing images..."
final_R = reconstruct(L_blend_R)
final_G = reconstruct(L_blend_G)
final_B = reconstruct(L_blend_B)

# Clip off values outside [0.0, 255.0]
final_R = clip_min_max(final_R, 0.0, 255.0)
final_G = clip_min_max(final_G, 0.0, 255.0)
final_B = clip_min_max(final_B, 0.0, 255.0)

# Combine each channel into the final RGB image
final = np.empty((final_R.shape[0], final_R.shape[1], 3))
final[:,:,0] = final_R
final[:,:,1] = final_G
final[:,:,2] = final_B

# Normalize to [0.0, 1.0] for plotting with imshow()
final /= 255.0

print "Plotting results..."
plt.figure()
plt.suptitle("Laplacian pyramid in each channel")
plt.subplot(331)
plt.imshow(L_apple_R[0], cmap='Greys_r')
plt.subplot(332)
plt.imshow(L_apple_G[0], cmap='Greys_r')
plt.subplot(333)
plt.imshow(L_apple_B[0], cmap='Greys_r')
plt.subplot(334)
plt.imshow(L_apple_R[2], cmap='Greys_r')
plt.subplot(335)
plt.imshow(L_apple_G[2], cmap='Greys_r')
plt.subplot(336)
plt.imshow(L_apple_B[2], cmap='Greys_r')
plt.subplot(337)
plt.imshow(L_apple_R[4], cmap='Greys_r')
plt.subplot(338)
plt.imshow(L_apple_G[4], cmap='Greys_r')
plt.subplot(339)
plt.imshow(L_apple_B[4], cmap='Greys_r')

plt.figure()
plt.suptitle("Reconstructed image in each channel")
plt.subplot(131)
plt.imshow(final_R, cmap='Greys_r')
plt.subplot(132)
plt.imshow(final_G, cmap='Greys_r')
plt.subplot(133)
plt.imshow(final_B, cmap='Greys_r')

plt.figure()
plt.title("Final reconstructed image")
plt.imshow(final)
plt.show()

plt.show()

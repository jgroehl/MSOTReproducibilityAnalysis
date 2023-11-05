import matplotlib.pyplot as plt
import numpy as np
from matplotlib_scalebar.scalebar import ScaleBar

PATH = r"D:\erlangen_data\1. Runde\1-01-L-001/"
us_data = np.load(PATH + "Scan_1_US.npy")[50:150, 5:-5]
pa_data = np.load(PATH + "Scan_1_PA.npy")[50:150, 5:-5]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 2), layout="constrained")

ax1.set_title("Ultrasound Data [a.u.]")
im1 = ax1.imshow(us_data, cmap="gray")
plt.colorbar(mappable=im1, ax=ax1, fraction=0.025, pad=0.01)
ax1.axis("off")
# Create scale bar
scalebar = ScaleBar(0.2, "mm", location="lower left")
ax1.add_artist(scalebar)

ax2.set_title("Photoacoustic Data [a.u.]")
im2 = ax2.imshow(pa_data, cmap="magma")
plt.colorbar(mappable=im2, ax=ax2, fraction=0.025, pad=0.01)
ax2.axis("off")
scalebar = ScaleBar(0.2, "mm", location="lower left")
ax2.add_artist(scalebar)

plt.savefig("example_data.png", dpi=200)
plt.close()
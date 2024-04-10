import matplotlib.pyplot as plt
import numpy as np
from matplotlib_scalebar.scalebar import ScaleBar
from path import BASE_DATA_PATH

MAXIMUM = 8
MINIMUM = 1
CMAP = "Reds"

MAXIMUM_IMAGE = 30
MINIMUM_IMAGE = -20
CMAP_IMAGE = "gray"

IDX_1 = 0
IDX_2 = 5

SUBJECT = "1-03-L"
us_datas_experienced = []
us_datas_novice = []
us_datas_trained = []
for i in range(1, 8):
    PATH = rf"{BASE_DATA_PATH}\1. Runde\{SUBJECT}-001"
    us_datas_experienced.append(np.load(PATH + f"/Scan_{str(i)}_US.npy")[50:150, 5:-5])
    PATH = rf"{BASE_DATA_PATH}\1. Runde\{SUBJECT}-003"
    us_datas_novice.append(np.load(PATH + f"/Scan_{str(i)}_US.npy")[50:150, 5:-5])
    PATH = rf"{BASE_DATA_PATH}\1. Runde\{SUBJECT}-005"
    us_datas_trained.append(np.load(PATH + f"/Scan_{str(i)}_US.npy")[50:150, 5:-5])
us_datas_experienced = np.asarray(us_datas_experienced)
us_datas_novice = np.asarray(us_datas_novice)
us_datas_trained = np.asarray(us_datas_trained)
us_data_experienced = np.std(us_datas_experienced, axis=0)
us_data_novice = np.std(us_datas_novice, axis=0)
us_data_trained = np.std(us_datas_trained, axis=0)

SUBJECT = "2-05-L"
us_datas_experienced_day2 = []
us_datas_novice_day2 = []
us_datas_trained_day2 = []
for i in range(1, 8):
    PATH = rf"{BASE_DATA_PATH}\2. Runde\{SUBJECT}-001"
    us_datas_experienced_day2.append(np.load(PATH + f"/Scan_{str(i)}_US.npy")[50:150, 5:-5])
    PATH = rf"{BASE_DATA_PATH}\2. Runde\{SUBJECT}-003"
    us_datas_novice_day2.append(np.load(PATH + f"/Scan_{str(i)}_US.npy")[50:150, 5:-5])
    PATH = rf"{BASE_DATA_PATH}\2. Runde\{SUBJECT}-005"
    us_datas_trained_day2.append(np.load(PATH + f"/Scan_{str(i)}_US.npy")[50:150, 5:-5])
us_datas_experienced_day2 = np.asarray(us_datas_experienced_day2)
us_datas_novice_day2 = np.asarray(us_datas_novice_day2)
us_datas_trained_day2 = np.asarray(us_datas_trained_day2)

us_data_experienced_day2 = np.std(us_datas_experienced_day2, axis=0)
us_data_novice_day2 = np.std(us_datas_novice_day2, axis=0)
us_data_trained_day2 = np.std(us_datas_trained_day2, axis=0)

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3, 3, figsize=(10, 5.5), layout="constrained")

im1 = ax1.imshow(us_datas_experienced[IDX_1], cmap=CMAP_IMAGE, vmin=MINIMUM_IMAGE, vmax=MAXIMUM_IMAGE)
ax1.axis("off")
scalebar = ScaleBar(0.2, "mm", location="lower left")
ax1.add_artist(scalebar)

im2 = ax2.imshow(us_datas_trained[IDX_1], cmap=CMAP_IMAGE, vmin=MINIMUM_IMAGE, vmax=MAXIMUM_IMAGE)
ax2.axis("off")
scalebar = ScaleBar(0.2, "mm", location="lower left")
ax2.add_artist(scalebar)

im3 = ax3.imshow(us_datas_novice[IDX_1], cmap=CMAP_IMAGE, vmin=MINIMUM_IMAGE, vmax=MAXIMUM_IMAGE)
cbar = plt.colorbar(mappable=im3, ax=ax3, fraction=0.025, pad=0.01)
cbar.set_label("Signal Intensity [a.u.]")
ax3.axis("off")
scalebar = ScaleBar(0.2, "mm", location="lower left")
ax3.add_artist(scalebar)

im4 = ax4.imshow(us_datas_experienced[IDX_2], cmap=CMAP_IMAGE, vmin=MINIMUM_IMAGE, vmax=MAXIMUM_IMAGE)
ax4.axis("off")
scalebar = ScaleBar(0.2, "mm", location="lower left")
ax4.add_artist(scalebar)

im5 = ax5.imshow(us_datas_trained[IDX_2], cmap=CMAP_IMAGE, vmin=MINIMUM_IMAGE, vmax=MAXIMUM_IMAGE)
ax5.axis("off")
scalebar = ScaleBar(0.2, "mm", location="lower left")
ax5.add_artist(scalebar)

im6 = ax6.imshow(us_datas_novice[IDX_2], cmap=CMAP_IMAGE, vmin=MINIMUM_IMAGE, vmax=MAXIMUM_IMAGE)
cbar = plt.colorbar(mappable=im6, ax=ax6, fraction=0.025, pad=0.01)
cbar.set_label("Signal Intensity [a.u.]")
ax6.axis("off")
scalebar = ScaleBar(0.2, "mm", location="lower left")
ax6.add_artist(scalebar)

im7 = ax7.imshow(us_data_experienced, cmap=CMAP, vmin=MINIMUM, vmax=MAXIMUM)
ax7.axis("off")
scalebar = ScaleBar(0.2, "mm", location="lower left")
ax7.add_artist(scalebar)

im8 = ax8.imshow(us_data_trained, cmap=CMAP, vmin=MINIMUM, vmax=MAXIMUM)
ax8.axis("off")
scalebar = ScaleBar(0.2, "mm", location="lower left")
ax8.add_artist(scalebar)

im9 = ax9.imshow(us_data_novice, cmap=CMAP, vmin=MINIMUM, vmax=MAXIMUM)
cbar = plt.colorbar(mappable=im9, ax=ax9, fraction=0.025, pad=0.01)
cbar.set_label("Standard Deviation [a.u.]")
ax9.axis("off")
scalebar = ScaleBar(0.2, "mm", location="lower left")
ax9.add_artist(scalebar)

plt.savefig("example_variability.svg", dpi=600)
plt.close()

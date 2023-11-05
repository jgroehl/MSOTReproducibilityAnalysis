from torchmetrics.image import StructuralSimilarityIndexMeasure
from scipy.signal import correlate2d
import numpy as np
import os.path
import torch
import json

DAYS = ["1", "2"]
PA_OR_USS = ["PA", "US"]


def normalized_cross_correlation(image1, image2):
    # Ensure both input images are of the same size
    if image1.shape != image2.shape:
        raise ValueError("Input images must have the same dimensions.")

    # Compute the mean of each image
    mean1 = np.mean(image1)
    mean2 = np.mean(image2)

    # Compute the cross-correlation using correlate2d
    cross_correlation = correlate2d(image1 - mean1, image2 - mean2, mode='valid')

    # Compute the standard deviations of both images
    std1 = np.std(image1)
    std2 = np.std(image2)

    # Compute the NCC
    ncc = cross_correlation / (std1 * std2 * image1.size)

    return np.mean(ncc)


def compute_bhattacharyya_distance(image1, image2, range_min=-3, range_max=3, num_bins=61):
    # Z-score normalization
    mean1, std1 = np.mean(image1), np.std(image1)
    mean2, std2 = np.mean(image2), np.std(image2)

    zscore_normalized_image1 = (image1 - mean1) / std1
    zscore_normalized_image2 = (image2 - mean2) / std2

    # Create histograms
    hist1, bin_edges1 = np.histogram(zscore_normalized_image1, bins=num_bins, range=(range_min, range_max))
    hist2, bin_edges2 = np.histogram(zscore_normalized_image2, bins=num_bins, range=(range_min, range_max))

    # Calculate the Bhattacharyya distance
    hist1 = hist1 / np.sum(hist1)  # Normalize histograms
    hist2 = hist2 / np.sum(hist2)

    b_distance = -np.log(np.sum(np.sqrt(hist1 * hist2)))

    return b_distance

for DAY in DAYS:
    for PA_OR_US in PA_OR_USS:
        DATA_PATH = fr"D:\erlangen_data\{DAY}. Runde/"

        OPERATORS = ["1", "2", "3", "4", "5"]
        SITE = ["L", "R"]
        SUBJECTS = ["1", "2", "3", "4", "5"]
        REPETITIONS = ["1", "2", "3", "4", "5", "6", "7"]

        data = dict()

        for operator in OPERATORS:
            print("====================================================")
            print("                  OPERATOR", operator)
            print("====================================================")
            print("")

            for site in SITE:
                for subject in SUBJECTS:

                    if operator not in data:
                        data[operator] = dict()

                    if site not in data[operator]:
                        data[operator][site] = dict()

                    if subject not in data[operator][site]:
                        data[operator][site][subject] = dict({
                            "ssim": [],
                            "MAE": [],
                            "NCC": [],
                            "BD": [],
                        })

                    for reference in REPETITIONS:
                        ref_path = (f"{DATA_PATH}/{DAY}-{str(operator).zfill(2)}"
                                    f"-{site}-{str(subject).zfill(3)}/Scan"
                                    f"_{reference}_{PA_OR_US}.npy")
                        if not os.path.exists(ref_path):
                            print(ref_path, "does not exist")
                            continue
                        reference_image = np.load(ref_path)[50:150, 5:-5]

                        for i in range(int(reference)+1, 8):
                            image_path = (f"{DATA_PATH}/{DAY}-{str(operator).zfill(2)}"
                                          f"-{site}-{str(subject).zfill(3)}/Scan"
                                          f"_{i}_{PA_OR_US}.npy")
                            if not os.path.exists(image_path):
                                continue
                            pa_data = np.load(image_path)[50:150, 5:-5]

                            # Compute SSIM
                            nr, nc = pa_data.shape
                            ssim_op = StructuralSimilarityIndexMeasure()
                            ssim = ssim_op(torch.from_numpy(reference_image.reshape((1, 1, nr, nc))),
                                           torch.from_numpy(pa_data.reshape((1, 1, nr, nc)))).item()
                            data[operator][site][subject]["ssim"].append(float(ssim))

                            # Compute MAE
                            mae = np.mean(np.abs(reference_image - pa_data))
                            data[operator][site][subject]["MAE"].append(float(mae))

                            # Compute NCC
                            ncc = normalized_cross_correlation(reference_image, pa_data)
                            data[operator][site][subject]["NCC"].append(float(ncc))

                            # Compute NCC
                            bd = compute_bhattacharyya_distance(reference_image, pa_data)
                            data[operator][site][subject]["BD"].append(float(bd))

                            print(reference, "-", i, f"= SSIM:{ssim:.2f} MAE:{mae:.2f} NCC:{ncc:.2f} BD:{bd * 100:.2f}")

        with open(f"{DATA_PATH}/ssim_scores_{PA_OR_US}.json", "w+") as json_file:
            json.dump(data, json_file)

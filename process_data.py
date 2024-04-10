# This script is essentially useless to others, but we included it for
# transparency as it shows how we processed and reconstructed the
# measurement data from the raw data. Unfortunately, the raw time series
# data measurements are > 300GB in total and thus not easily sharable.

import patato as pat
import numpy as np
import glob
import os
from path import BASE_DATA_PATH

READ_PATH = r"E:/"
WRITE_PATH = BASE_DATA_PATH

rounds = glob.glob(READ_PATH + "*Runde*/")
print(rounds)

for round in rounds:

    measurements = glob.glob(round + "/*-*")

    for measurement in measurements:
        print(measurement)
        for scan_idx, foldername in enumerate(glob.glob(measurement + f"/Scan_*/")):
            filename = foldername[:-1].split("/")[-1].split("\\")[-1]
            print(f"\t {scan_idx+1}/7")

            msot_reader = pat.iTheraMSOT(foldername, filename)
            pa_data = pat.PAData(msot_reader)

            # Reconstruct the data
            nx = 210  # number of pixels
            pre_processor = pat.MSOTPreProcessor(lp_filter=7e6,
                                                 hp_filter=5e3)  # can specify low pass/high pass/hilbert etc.

            reconstructor = pat.Backprojection(field_of_view=[0.04, 0, 0.04],
                                               n_pixels=(
                                               nx, 1, nx))  # z axis must be specified but is empty in this case.
            # Apply the pre processor
            filtered_time_series, settings, _ = pre_processor.run(pa_data.get_time_series(), pa_data)

            # `settings` is a dictionary that includes the interpolated detection geometry.
            # It is passed into the next step

            # Reconstruct the filtered time-series data.
            reconstruction, _, _ = reconstructor.run(filtered_time_series, pa_data,
                                                     1520, **settings)

            write_path = measurement.replace(READ_PATH, WRITE_PATH)
            if not os.path.exists(write_path):
                os.makedirs(write_path)

            us_data = pa_data.get_ultrasound()

            us_data = np.flipud(np.squeeze(np.mean(us_data.raw_data[:, 3], axis=0)))
            pa_data = np.flipud(np.squeeze(np.mean(reconstruction.raw_data[:, 3], axis=0)))

            np.save(write_path + f"/Scan_{scan_idx+1}_US.npy", us_data)
            np.save(write_path + f"/Scan_{scan_idx + 1}_PA.npy", pa_data)

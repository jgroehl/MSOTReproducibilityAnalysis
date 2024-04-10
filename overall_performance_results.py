import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.stats import wilcoxon
from path import BASE_DATA_PATH

DAY = ["1", "2"]
PATH = BASE_DATA_PATH
SCORES = ["BD", "MAE", "ssim", "NCC"]
BIGGER_IS_BETTER = False
OPERATOR_LABELS = ["Experienced", "Experienced", "Novice", "Novice", "Trained"]

for day in DAY:
    print(f"Experiment {day}")
    with open(rf"{PATH}\{day}. Runde/ssim_scores_US.json", "r+") as json_file:
        data = json.load(json_file)
        OPERATORS = [1, 2, 3, 4, 5]
        SITE = ["L", "R"]
        SUBJECTS = [1, 2, 3, 4, 5]

        for score in SCORES:
            print(f"\t{score}")
            task_performances = []
            for subject in SUBJECTS:
                for site in SITE:
                    for operator in OPERATORS:
                            task_performances.append(np.median(data[str(operator)][str(site)][str(subject)][score]))
            print(f"\t\t{np.mean(task_performances)}, {np.std(task_performances)}")
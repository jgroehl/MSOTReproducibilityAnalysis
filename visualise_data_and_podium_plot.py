import matplotlib.pyplot as plt
import numpy as np
import json

PA_OR_US = ["PA", "US"]
DAY = ["1", "2"]
PATH = r"D:\erlangen_data/"
SCORE = "NCC"

for day in DAY:
    for paus in PA_OR_US:
        with open(rf"{PATH}\{day}. Runde/ssim_scores_{paus}.json", "r+") as json_file:
            data = json.load(json_file)

        COLOURS = ["#648FFF", "#785EF0", "#DC267F",
                   "#FE6100", "#FFB000"]

        OPERATORS = [1, 2, 3, 4, 5]
        SITE = ["L", "R"]
        SUBJECTS = [1, 2, 3, 4, 5]
        KEY = "ssim"
        N_BOOTSTRAPS = 100
        TITLE = f"Podium Plot ({paus}, Day {day}, {SCORE})"

        task_performances = [None] * len(OPERATORS)
        for operator in OPERATORS:
            task_performances[operator-1] = []
        for subject in SUBJECTS:
            for site in SITE:
                for operator in OPERATORS:
                    for b_idx in range(N_BOOTSTRAPS):
                        _sample_data = data[str(operator)][str(site)][str(subject)][SCORE]
                        if N_BOOTSTRAPS == 1:
                            sample = _sample_data
                        else:
                            sample = np.random.choice(_sample_data, int(len(_sample_data)/2), replace=True)
                        task_performances[operator-1].append(np.mean(sample))

        print(f"Day {day}, {paus}:  {np.mean(task_performances):.2f} +/- {np.std(task_performances):.2f}")

        sort_indices = np.argsort(task_performances, axis=0)
        podium_positions = [None] * len(OPERATORS)
        for operator in OPERATORS:
            podium_positions[operator-1] = []

        for task_idx in range(sort_indices.shape[1]):
            for operator_idx in range(len(OPERATORS)):
                podium_positions[operator_idx].append(np.argwhere(sort_indices[:, task_idx] == operator_idx))
        podium_positions = len(OPERATORS) - np.squeeze(np.asarray(podium_positions))
        position_ranking = np.argsort(np.mean(podium_positions, axis=1))

        sorted_ranking = podium_positions[position_ranking, :]

        operator_labels = [f"Operator {OPERATORS[idx]}\n{np.mean(sorted_ranking[num]):.1f}" for num, idx in enumerate(position_ranking)]

        plt.title(TITLE)
        plt.hlines(OPERATORS, 0.5, len(OPERATORS)+0.5, linestyles="dashed", colors="grey", alpha=0.5)
        plt.boxplot(sorted_ranking.T, labels=operator_labels, positions=OPERATORS, showfliers=False)

        for pos, idx in zip(position_ranking, range(len(OPERATORS))):
            y = sorted_ranking[idx]
            x = np.random.random((len(y), )) * 0.4 + idx + 0.8
            plt.scatter(x, y, alpha=0.5/np.sqrt(N_BOOTSTRAPS), s=30, c=COLOURS[OPERATORS[pos]-1])

        plt.yticks(OPERATORS, OPERATORS)
        plt.ylabel("Ranking")
        plt.gca().invert_yaxis()
        plt.gca().spines[["right", "top"]].set_visible(False)
        plt.savefig(rf"{PATH}\{day}. Runde/{SCORE}_{paus}_podium.png")
        plt.close()

        plt.figure(figsize=(10, 4))
        for operator in OPERATORS:
            op_values = []
            for subject in SUBJECTS:
                for site in SITE:
                    op_values.append(data[str(operator)][str(site)][str(subject)][SCORE])
            bplot = plt.boxplot(op_values, positions=[operator + (-0.6 + 0.15*s + 0.075*s2) for s2 in range(len(SITE)) for s in SUBJECTS],
                        widths=0.06, patch_artist=True)
            for patch in bplot['boxes']:
                patch.set_facecolor(COLOURS[operator-1])

        plt.xticks(OPERATORS, [f"Operator {i}" for i in OPERATORS])
        plt.ylabel("SSIM [0, 1]")
        plt.savefig(rf"{PATH}\{day}. Runde/{SCORE}_{paus}_values.png")
        plt.close()

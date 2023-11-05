import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.stats import wilcoxon

PA_OR_US = ["PA", "US"]
DAY = ["1", "2"]
PATH = r"D:\erlangen_data/"
SCORE = "BD" # "BD", "MAE", "ssim", "NCC"
BIGGER_IS_BETTER = False
OPERATOR_LABELS = ["Experienced", "Experienced", "Novice", "Novice", "Trained"]

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
        TITLE = f"Podium Plot Experiment {day} (based on {paus})"

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
                        if BIGGER_IS_BETTER:
                            task_performances[operator-1].append(np.median(sample))
                        else:
                            task_performances[operator - 1].append(-np.median(sample))

        print(f"Day {day}, based on {paus}:  {np.mean(task_performances)*100:.2f} +/- "
              f"{np.std(task_performances)*100:.2f}")

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

        operator_labels = [f"Operator {OPERATORS[idx]}\n({OPERATOR_LABELS[idx]})" for num, idx in
                           enumerate(position_ranking)]

        plt.figure(figsize=(6, 4), layout="constrained")
        plt.title(TITLE)
        plt.hlines(OPERATORS, 0.5, len(OPERATORS)+0.5, linestyles="dashed", colors="grey", alpha=0.5)
        plt.boxplot(sorted_ranking.T, labels=operator_labels, positions=OPERATORS, showfliers=False)
        plt.xticks(fontsize=8, fontweight="bold")

        for pos, idx in zip(position_ranking, range(len(OPERATORS))):
            y = sorted_ranking[idx]
            x = np.random.random((len(y), )) * 0.4 + idx + 0.8
            y = np.random.normal(0, 0.1, (len(y), )) + y
            plt.scatter(x, y, alpha=0.5/np.sqrt(N_BOOTSTRAPS), s=30, c=COLOURS[OPERATORS[pos]-1])

        plt.yticks(OPERATORS, OPERATORS)
        plt.ylabel(f"Relative performance ranking based on {SCORE}", fontsize=8, fontweight="bold")
        plt.gca().invert_yaxis()
        plt.gca().spines[["right", "top"]].set_visible(False)
        plt.savefig(rf"{PATH}\{day}. Runde/{SCORE}_{paus}_podium.png", dpi=200)
        plt.close()

        plt.figure(figsize=(6, 4), layout="constrained")
        operators_ordered = np.asarray(OPERATORS)[np.asarray(position_ranking)]
        operator_values = [None] * 5
        for op_idx, operator in enumerate(operators_ordered):
            op_values = []
            for subject in SUBJECTS:
                for site in SITE:
                    op_values.append(data[str(operator)][str(site)][str(subject)][SCORE])
            bplot = plt.boxplot(op_values, positions=[op_idx + 1 + (-0.5 + 0.15*s + 0.075*s2) for s2 in
                                                      range(len(SITE)) for s in SUBJECTS],
                        widths=0.06, patch_artist=True, showfliers=False, showcaps=False,
                                whiskerprops=dict(color=COLOURS[operator-1], alpha=0.2),
                                medianprops=dict(color="white", alpha=0))
            for patch in bplot['boxes']:
                patch.set_facecolor(COLOURS[operator-1])
                patch.set_alpha(0.2)
            plt.boxplot(np.hstack(op_values), positions=[op_idx+1], widths=0.85, showfliers=False, showmeans=True)

            #op_values = [np.mean(op_values[i]) for i in range(len(op_values))]
            operator_values[op_idx] = [np.mean(op_values[i]) for i in range(len(op_values))]

        inc_counter = 0
        inc = (np.max(operator_values) - np.min(operator_values)) / 10
        for i in range(5):
            for j in range(i+1, 5):
                stats, pval = wilcoxon(operator_values[i], operator_values[j])
                if pval < 0.05:
                    print(f"Operator {operators_ordered[i]} vs {operators_ordered[j]}: {stats}, {pval}")
                    plt.text(1+ (i+j)/2, np.max(operator_values) + inc*(inc_counter+2.2), f"p={pval:.5f}", fontsize=8)
                    y = np.max(operator_values) + inc*(inc_counter+2)
                    plt.plot([i + 1, j + 1], [y, y], linewidth=0.5, c="black")
                    plt.plot([i + 1, i + 1], [y, y - inc / 3], linewidth=0.5, c="black")
                    plt.plot([j + 1, j + 1], [y, y - inc / 3], linewidth=0.5, c="black")
                    inc_counter += 1


        plt.xticks(OPERATORS, [f"Operator {i}" for i in operators_ordered], fontsize=8, fontweight="bold")
        plt.ylabel(f"{SCORE} ({'bigger is better' if BIGGER_IS_BETTER else 'smaller is better'})", fontsize=8,
                   fontweight="bold")
        plt.gca().spines[["right", "top"]].set_visible(False)
        plt.savefig(rf"{PATH}\{day}. Runde/{SCORE}_{paus}_values.png", dpi=200)
        plt.close()

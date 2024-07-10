import matplotlib.pyplot as plt
import json
import numpy as np
import seaborn as sns


def get_values(metric):
    return [[results[system].get(matrix, {}).get(metric, np.nan) for system in systems] for matrix in sorted_matrices]


def filter_values(values, metric):
    if metric == "Errore_Relativo":
        return [v if v is not None else np.nan for v in values]
    else:
        return [max(1e-10, v) if v is not None and v > 0 else np.nan for v in values]


def create_plot(metric, title, ylabel, filename):
    fig, ax = plt.subplots(figsize=(15, 10))
    values = get_values(metric)

    for j, (system, color) in enumerate(zip(systems, colors)):
        filtered_values = filter_values([v[j] for v in values], metric)
        ax.bar(x + j * width, filtered_values, width, label=system, color=color, alpha=0.8)

    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=16, pad=20)
    ax.set_xticks(x + width * (len(systems) - 1) / 2)
    ax.set_xticklabels([f"{matrix}\n(Size={matrix_sizes[matrix]})" for matrix in sorted_matrices],
                       rotation=45, ha='right', fontsize=10)
    ax.legend(fontsize=10, loc='upper left', bbox_to_anchor=(1, 1))

    if metric == "Errore_Relativo":
        ax.set_yscale('log')
        ax.yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:.0e}"))
    elif metric in ["Time", "Memory_Used"]:
        ax.set_yscale('log')

    ax.grid(True, which="both", ls="-", alpha=0.2)

    for bar in ax.patches:
        height = bar.get_height()
        if not np.isnan(height):
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.2e}',
                    ha='center', va='bottom', rotation=90, fontsize=8)

    ax.set_xlim(left=-0.5)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    sns.set_style("whitegrid")
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.rcParams['font.family'] = 'sans-serif'

    with open('results.json', 'r') as file:
        data = json.load(file)

    systems = list(data.keys())
    matrices = set()
    results = {system: {} for system in systems}
    matrix_sizes = {}

    for system in systems:
        for result in data[system]["Matrix_Results"]:
            file = result["File"]
            matrices.add(file)
            results[system][file] = {
                "Time": result["Time"],
                "Memory_Used": result["Memory_Used"],
                "Errore_Relativo": result["Errore_Relativo"],
                "Size": result["Size"]
            }
            matrix_sizes[file] = result["Size"]

    sorted_matrices = sorted(list(matrices), key=lambda x: matrix_sizes[x])

    x = np.arange(len(sorted_matrices))
    width = 0.15

    colors = sns.color_palette("husl", len(systems))

    metrics = ["Time", "Memory_Used", "Errore_Relativo"]
    titles = ["Tempo di esecuzione", "Memoria Utilizzata", "Errore Relativo"]
    ylabels = ["Tempo (s)", "Memoria (mB)", "Errore"]
    filenames = ["tempo_esecuzione.png", "memoria_utilizzata.png", "errore_relativo.png"]

    for metric, title, ylabel, filename in zip(metrics, titles, ylabels, filenames):
        create_plot(metric, title, ylabel, filename)

    print("I grafici sono stati salvati come file separati.")

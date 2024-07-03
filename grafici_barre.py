import matplotlib.pyplot as plt
import json
import numpy as np
import seaborn as sns

# Funzione per ottenere i valori per una metrica specifica
def get_values(metric):
    return [[results[system].get(matrix, {}).get(metric, np.nan) for system in systems] for matrix in sorted_matrices]

# Funzione per filtrare i valori None e i valori non positivi (per la scala logaritmica)
def filter_values(values):
    return [max(1e-10, v) if v is not None and v > 0 else np.nan for v in values]

if __name__ == '__main__':
    # Imposta lo stile di seaborn per un aspetto più moderno
    sns.set_style("whitegrid")
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.rcParams['font.family'] = 'sans-serif'

    # Leggi i dati dal file JSON
    with open('results.json', 'r') as file:
        data = json.load(file)

    # Estrai i dati per ogni combinazione di OS e linguaggio
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
                "N": result["N"]
            }
            matrix_sizes[file] = result["N"]

    # Ordina le matrici in base alla dimensione N
    sorted_matrices = sorted(list(matrices), key=lambda x: matrix_sizes[x])

    # Crea i grafici
    metrics = ["Time", "Memory_Used", "Errore_Relativo"]
    titles = ["Tempo di esecuzione", "Memoria Utilizzata", "Errore Relativo"]
    ylabels = ["Tempo (s)", "Memoria (unità non specificate)", "Errore"]

    fig, axes = plt.subplots(3, 1, figsize=(15, 25))
    fig.suptitle("Confronto delle prestazioni tra sistemi", fontsize=20, y=0.95)

    x = np.arange(len(sorted_matrices))
    width = 0.35

    colors = sns.color_palette("husl", len(systems))

    for i, (metric, title, ylabel) in enumerate(zip(metrics, titles, ylabels)):
        ax = axes[i]
        values = get_values(metric)

        for j, (system, color) in enumerate(zip(systems, colors)):
            filtered_values = filter_values([v[j] for v in values])
            ax.bar(x + j * width, filtered_values, width, label=system, color=color, alpha=0.8)

        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(title, fontsize=16, pad=20)
        ax.set_xticks(x + width / 2)
        ax.set_xticklabels([f"{matrix}\n(N={matrix_sizes[matrix]})" for matrix in sorted_matrices],
                           rotation=45, ha='right', fontsize=10)
        ax.legend(fontsize=10, loc='upper left', bbox_to_anchor=(1, 1))

        if metric in ["Time", "Errore_Relativo", "Memory_Used"]:
            ax.set_yscale('log')

        ax.grid(True, which="both", ls="-", alpha=0.2)

        # Aggiungi etichette dei valori sopra le barre
        for bar in ax.patches:
            height = bar.get_height()
            if not np.isnan(height):
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                        f'{height:.2e}',
                        ha='center', va='bottom', rotation=90, fontsize=8)

        # Aggiungi spazio a sinistra
        ax.set_xlim(left=-0.5)

    plt.tight_layout()
    plt.subplots_adjust(top=0.92, right=0.85, left=0.1)

    # Salva l'immagine
    plt.savefig('bar-plot.png', dpi=300, bbox_inches='tight')

    plt.show()
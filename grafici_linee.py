import matplotlib.pyplot as plt
import json
import numpy as np
import seaborn as sns
from cycler import cycler

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

for system in systems:
    for result in data[system]["Matrix_Results"]:
        file = result["File"]
        matrices.add(file)
        results[system][file] = {
            "Time": result["Time"],
            "Memory_Used": result["Memory_Used"],
            "Errore_Relativo": result["Errore_Relativo"]
        }

matrices = sorted(list(matrices))


# Funzione per ottenere i valori per una metrica specifica
def get_values(metric):
    return {system: [results[system].get(matrix, {}).get(metric, np.nan) for matrix in matrices] for system in systems}


# Funzione per filtrare i valori non validi
def filter_values(values):
    return [v if v is not None and v > 0 else np.nan for v in values]


# Crea i grafici
metrics = ["Time", "Memory_Used", "Errore_Relativo"]
titles = ["Tempo di esecuzione", "Memoria Utilizzata", "Errore Relativo"]
ylabels = ["Tempo (s)", "Memoria (unità non specificate)", "Errore"]

fig, axes = plt.subplots(3, 1, figsize=(15, 25))
fig.suptitle("Confronto delle prestazioni tra sistemi", fontsize=24, fontweight='bold', y=0.95)

# Definisci una palette di colori personalizzata
colors = sns.color_palette("husl", n_colors=len(systems))
plt.rc('axes', prop_cycle=(cycler('color', colors)))

for i, (metric, title, ylabel) in enumerate(zip(metrics, titles, ylabels)):
    ax = axes[i]
    values = get_values(metric)

    for system, color in zip(systems, colors):
        filtered_values = filter_values(values[system])
        ax.plot(matrices, filtered_values, marker='o', label=system, linewidth=2, markersize=8)

    ax.set_ylabel(ylabel, fontsize=14, fontweight='bold')
    ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
    ax.set_xticks(range(len(matrices)))
    ax.set_xticklabels(matrices, rotation=45, ha='right', fontsize=10)
    ax.legend(fontsize=12, loc='center left', bbox_to_anchor=(1, 0.5))

    # Imposta la scala logaritmica per tutti i grafici
    ax.set_yscale('log')

    # Griglia per facilitare la lettura
    ax.grid(True, which="both", ls="-", alpha=0.2)

    # Personalizza i tick
    ax.tick_params(axis='both', which='major', labelsize=10)

    # Aggiungi un bordo al grafico
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('gray')
        spine.set_linewidth(0.5)

plt.tight_layout()
plt.subplots_adjust(top=0.92, right=0.85, hspace=0.3)
plt.show()
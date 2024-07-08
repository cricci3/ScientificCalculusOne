import matplotlib.pyplot as plt
import json
import numpy as np
import seaborn as sns

LINGUAGGIO = 'MATLAB'
METRICA = 'Errore_Relativo'


# Imposta lo stile di seaborn per un aspetto più moderno
sns.set_style("whitegrid")
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['font.family'] = 'sans-serif'

# Leggi i dati dal file JSON
with open('results.json', 'r') as file:
    data = json.load(file)

# Filtra i sistemi per includere solo Windows e Linux con Python
systems = [system for system in data.keys() if LINGUAGGIO in system and ('Windows' in system or 'Linux' in system)]

matrices = set()
results = {system: {} for system in systems}
matrix_sizes = {}

for system in systems:
    for result in data[system]["Matrix_Results"]:
        file = result["File"]
        matrices.add(file)
        results[system][file] = {
            METRICA: result.get(METRICA, np.nan),
            "N": result["N"]
        }
        matrix_sizes[file] = result["N"]

# Ordina le matrici in base alla dimensione N
sorted_matrices = sorted(list(matrices), key=lambda x: matrix_sizes[x])


def get_metrics_values():
    # Funzione per ottenere i valori da stampare
    return [[results[system].get(matrix, {}).get(METRICA, np.nan) for system in systems] for matrix in sorted_matrices]


# Funzione per filtrare i valori None e i valori non positivi (per la scala logaritmica)
def filter_values(values):
    return [max(1e-10, v) if v is not None and v > 0 else np.nan for v in values]


# Crea il grafico
fig, ax = plt.subplots(figsize=(15, 10))
fig.suptitle(f"Confronto dell'utilizzo di {METRICA} tra Windows e Linux in {LINGUAGGIO}", fontsize=20, y=0.95)

x = np.arange(len(sorted_matrices))
width = 0.35

colors = sns.color_palette("husl", len(systems))

memory_values = get_metrics_values()

for j, (system, color) in enumerate(zip(systems, colors)):
    filtered_values = filter_values([v[j] for v in memory_values])
    ax.bar(x + j * width, filtered_values, width, label=system, color=color, alpha=0.8)

ax.set_ylabel("Memoria utilizzata (unità non specificate)", fontsize=12)
ax.set_xticks(x + width / 2)
ax.set_xticklabels([f"{matrix}\n(N={matrix_sizes[matrix]})" for matrix in sorted_matrices],
                   rotation=45, ha='right', fontsize=10)
ax.legend(fontsize=10, loc='upper left', bbox_to_anchor=(1, 1))

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
plt.savefig(f'{LINGUAGGIO}-{METRICA}-plot.png', dpi=300, bbox_inches='tight')

plt.show()
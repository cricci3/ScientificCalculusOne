import time
import scipy.io
import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import eigsh
from numpy.linalg import norm
import sksparse.cholmod as cholmod
import psutil
import os
import json
import platform


def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # Memoria in MB


def is_symmetric(mtrx):
    #  verifica se il numero di elementi diversi è zero.
    if (mtrx != mtrx.T).nnz == 0:
        print(f"Matrice è simmetrica")
        return True
    else:
        print(f"Matrice non è simmetrica")
        return False


def is_positive_definite(mtrx):
    try:
        eigenvalue, _ = eigsh(mtrx, k=1, which='SM')
        if eigenvalue > 0:
            print(f"Matrice definita positiva")
            return True
        else:
            print(f"Matrice non definita positiva")
            return False
    except:
        print(f"Matrice non definita positiva")
        return False


def solution(matrix):
    n = matrix.shape[0]
    xe = np.ones(n)

    start_time = time.time()

    b = matrix @ xe
    try:
        factor = cholmod.cholesky(matrix)
        x = factor(b)
        memory_after = get_memory_usage()
        computation_time = time.time() - start_time

        errore_relativo = norm(x - xe) / norm(xe)
    except cholmod.CholmodError:
        errore_relativo = None
        computation_time = None
        memory_after = None

    return errore_relativo, computation_time, memory_after


def process_matrix(matrix_name):
    json_structure = {
        'File': matrix_name,
        'Errore_Relativo': None,
        'Time': None,
        'Memory_Used': None,
        'Status': 'Failed'
    }

    try:
        data = scipy.io.loadmat(f'Matrix/{matrix_name}')
        A = csc_matrix(data['Problem'][0, 0]['A'])

        memory_after_load = get_memory_usage()
        print(memory_after_load)

        if is_symmetric(A):
            errore_relativo, mtrx_time, memory_after_solution = solution(A)
            print(memory_after_solution)

            json_structure['N'] = A.shape[0]
            json_structure['Errore_Relativo'] = float(errore_relativo)
            json_structure['Time'] = round(mtrx_time, 3)
            json_structure['Memory_Used'] = memory_after_solution - memory_after_load
            json_structure['Status'] = 'Success'
        else:
            json_structure['Status'] = 'Matrix not symmetric or not positive definite'

    except MemoryError:
        json_structure['Status'] = 'Memory Out of bound'
    except scipy.io.matlab.miobase.MatReadError:
        json_structure['Status'] = 'Error reading .mat file'
    except Exception as e:
        json_structure['Status'] = f'Error: {str(e)}'

    return json_structure


def load_existing_data():
    try:
        with open('results.json', 'r') as f:
            content = f.read()
            if content:
                return json.loads(content)
            else:
                return {}
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Warning: The JSON file is not properly formatted. Starting with an empty dictionary.")
        return {}


def save_results(data):
    with open('results.json', 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    matrixNames = ['cfd1.mat', 'cfd2.mat', 'apache2.mat', 'ex15.mat',
                   'G3_circuit.mat', 'parabolic_fem.mat', 'shallow_water1.mat']

    # Carica i dati esistenti
    existing_data = load_existing_data()

    # Identifica il sistema operativo e il linguaggio corrente
    current_os = platform.system()
    current_language = 'Python'

    # Crea una chiave unica per questa combinazione di OS e linguaggio
    key = f"{current_os}_{current_language}"

    current_results = []

    for matrix in matrixNames:
        print(f"Processing {matrix} ...")
        try:
            json_result = process_matrix(matrix)
            current_results.append(json_result)
        except Exception as e:
            print(f"Error processing {matrix}: {str(e)}")
            current_results.append({
                'File': matrix,
                'Status': f'Error: {str(e)}'
            })

    # Aggiorna o aggiungi i risultati per questa combinazione di OS e linguaggio
    if key not in existing_data:
        existing_data[key] = {}

    existing_data[key]['System_Info'] = {
        'Operating_System': current_os,
        'Language': current_language
    }
    existing_data[key]['Matrix_Results'] = current_results

    # Salva i risultati aggiornati
    save_results(existing_data)

    print("Results saved to results.json")
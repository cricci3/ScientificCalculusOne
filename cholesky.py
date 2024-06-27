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


def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # Memoria in MB


def is_symmetric(mtrx):
    return (mtrx != mtrx.T).nnz == 0


def is_positive_definite(mtrx):
    try:
        eigenvalue, _ = eigsh(mtrx, k=1, which='SM')
        return eigenvalue > 0
    except:
        return False


def solution(matrix):
    n = matrix.shape[0]
    xe = np.ones(n)

    start_time = time.time()

    b = matrix @ xe
    factor = cholmod.cholesky(matrix)
    x = factor(b)

    end_time = time.time() - start_time

    errore_relativo = norm(x - xe) / norm(xe)
    return errore_relativo, end_time


def process_matrix(matrix_name):
    result = {
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

        if is_symmetric(A) and is_positive_definite(A):
            errore_relativo, calculation_time = solution(A)
            memory_after_solution = get_memory_usage()

            result['Errore_Relativo'] = float(errore_relativo)
            result['Time'] = calculation_time
            result['Memory_Used'] = memory_after_solution - memory_after_load
            result['Status'] = 'Successful'
        else:
            result['Status'] = 'Matrix not symmetric or not positive definite'

    except MemoryError:
        result['Status'] = 'Memory Out of bound'
    except Exception as e:
        result['Status'] = f'Error: {str(e)}'

    return result


if __name__ == '__main__':
    matrixNames = ['apache2.mat', 'cfd1.mat', 'cfd2.mat', 'ex15.mat', 'Flan_1565.mat', 'G3_circuit.mat',
                   'parabolic_fem.mat', 'shallow_water1.mat', 'StocF-1465.mat']

    results = []

    for matrix in matrixNames:
        print(f"Processing {matrix}...")
        result = process_matrix(matrix)
        results.append(result)
        print(f"Result: {result['Status']}")
        print("--------------------")

    # Salva i risultati in un file JSON
    with open('results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("Results saved to results.json")

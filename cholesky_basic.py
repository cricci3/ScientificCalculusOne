import time
import scipy.io
import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import eigsh
from numpy.linalg import norm
import sksparse.cholmod as cholmod
import psutil
import os


def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # Memoria in MB


def is_symmetric(mtrx):
    #  verifica se il numero di elementi diversi è zero.
    if (mtrx != mtrx.T).nnz == 0:
        print(f"Matrice è simmetrica")
        return True
    else:
        print(f"Matrice è simmetrica")
        return False


def is_positive_definite(mtrx):
    print("start time")
    inizio_tempo = time.time()
    try:
        eigenvalue, _ = eigsh(mtrx, k=1, which='SM')
        if eigenvalue > 0:
            print(f"Matrice definita positiva")
            fine_tempo = time.time() - inizio_tempo
            print(f"Tempo dopo positive {fine_tempo} secondi")
            return True
        else:
            print(f"Matrice non definita positiva")
            fine_tempo = time.time() - inizio_tempo
            print(f"Tempo dopo positive {fine_tempo} secondi")
            return False
    except:
        print(f"Matrice non definita positiva")
        fine_tempo = time.time() - inizio_tempo
        print(f"Tempo dopo positive {fine_tempo} secondi")
        return False


def solution(matrix):
    n = matrix.shape[0]
    print(n)
    xe = np.ones(n)

    print("inizia computazione")
    start_time = time.time()

    b = matrix @ xe
    try:
        factor = cholmod.cholesky(matrix)
        x = factor(b)

        end_time = time.time()
        print("computazione finita")

        errore_relativo = norm(x - xe) / norm(xe)
        print(f"Errore relativo: {errore_relativo}")
        print(f"Time: {end_time - start_time} sec")
    except:
        print("La matrice non è definita positiva")


if __name__ == '__main__':

    data = scipy.io.loadmat(f'Matrix/ex15.mat')

    A = csc_matrix(data['Problem'][0, 0]['A'])

    memory_after_load = get_memory_usage()

    if is_symmetric(A):
        solution(A)
        memory_after_solution = get_memory_usage()
        print(f"Differenza di memoria alla fine: {memory_after_solution-memory_after_load} MB")

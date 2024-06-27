import scipy.io
import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import splu, spsolve, eigsh
from numpy.linalg import norm, cholesky
import sksparse.cholmod as cholmod



# Funzione per verificare se la matrice è simmetrica
def is_symmetric(matrix):
    return np.all(matrix.data == matrix.transpose().data)


# Funzione per verificare se la matrice è definita positiva
def is_positive_definite(matrix):
    try:
        eigenvalue, _ = eigsh(matrix, k=1, which='LM')
        return np.all(matrix.diagonal() > 0) and eigenvalue > 0
    except:
        return False


# Funzione per risolvere il sistema Ax = b usando la decomposizione LU
def solution(matrix):
    n = matrix.shape[0]
    xe = np.ones(n)

    # Calcolo del termine noto b
    b = matrix @ xe

    # Dobbiamo trovare soluzione per Ax = b ma serve x
    factor = cholmod.cholesky(matrix)
    x = factor(b)

    #y = np.transpose(R) / b

    #x = R / y

    # Verifica dell'errore
    errore_relativo = norm(x - xe, 2) / norm(xe, 2)
    print(f"Errore relativo: {errore_relativo}")


if __name__ == '__main__':
    # Carica il file .mat
    data = scipy.io.loadmat('Matrix/cfd1.mat')

    # Stampare le chiavi per esaminare la struttura del dizionario
    print(data.keys())

    A = data['Problem'][0, 0]['A']
    A = csc_matrix(A)

    # Verifica se la matrice è simmetrica
    if is_symmetric(A):
        print("La matrice è simmetrica.")
        # Verifica se la matrice è definita positiva
        if is_positive_definite(A):
            print("La matrice è definita positiva.")

            solution(A.data)
        else:
            print("La matrice non è definita positiva.")
    else:
        print("La matrice non è simmetrica.")

